"""
Modernized Export Watchdog Service

Monitors designated folders for export files and automatically organizes them
into structured directories with year-based subfolders for time-series exports.
"""

import os
import shutil
import time
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Tuple
from logging.handlers import RotatingFileHandler
import logging

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemMovedEvent


class FileMover:
    """
    Handles robust file moving with lock detection and retry logic.
    """

    def __init__(self, max_retries: int = 5, retry_delay: float = 2.0):
        """
        Initialize the FileMover.

        Args:
            max_retries: Maximum number of retry attempts
            retry_delay: Delay in seconds between retries
        """
        self.max_retries = max_retries
        self.retry_delay = retry_delay

    def is_file_locked(self, file_path: Path) -> bool:
        """
        Check if a file is locked (e.g., open in Excel).

        Args:
            file_path: Path to the file to check

        Returns:
            True if file is locked, False otherwise
        """
        if not file_path.exists():
            return False

        try:
            # Try to open the file in exclusive mode
            with open(file_path, 'r+b') as f:
                pass
            return False
        except (IOError, OSError, PermissionError):
            return True

    def move_file(
        self,
        source: Path,
        destination: Path,
        logger: logging.Logger
    ) -> bool:
        """
        Move a file with retry logic and lock detection.

        Args:
            source: Source file path
            destination: Destination file path
            logger: Logger instance for logging

        Returns:
            True if move was successful, False otherwise
        """
        if not source.exists():
            logger.warning(f"Source file does not exist: {source.name}")
            return False

        # Ensure destination directory exists
        destination.parent.mkdir(parents=True, exist_ok=True)

        for attempt in range(1, self.max_retries + 1):
            if self.is_file_locked(source):
                if attempt < self.max_retries:
                    logger.info(
                        f"File '{source.name}' is locked (attempt {attempt}/{self.max_retries}). "
                        f"Retrying in {self.retry_delay} seconds..."
                    )
                    time.sleep(self.retry_delay)
                    continue
                else:
                    logger.error(
                        f"File '{source.name}' is locked after {self.max_retries} attempts. "
                        f"Skipping move."
                    )
                    return False

            try:
                shutil.move(str(source), str(destination))
                logger.info(f"Successfully moved '{source.name}' -> '{destination.name}'")
                return True
            except (IOError, OSError, PermissionError) as e:
                if attempt < self.max_retries:
                    logger.warning(
                        f"Error moving '{source.name}' (attempt {attempt}/{self.max_retries}): {e}. "
                        f"Retrying in {self.retry_delay} seconds..."
                    )
                    time.sleep(self.retry_delay)
                else:
                    logger.error(f"Failed to move '{source.name}' after {self.max_retries} attempts: {e}")
                    return False
            except Exception as e:
                logger.error(f"Unexpected error moving '{source.name}': {e}")
                return False

        return False


class YearExtractor:
    """
    Extracts year information from filenames based on different strategies.
    """

    @staticmethod
    def extract_year_start(filename: str) -> Optional[str]:
        """
        Extract year from the start of filename (first 4 digits).

        Pattern: YYYY_MM_Monthly_*.xlsx
        Example: 2025_11_Monthly_CAD.xlsx -> "2025"

        Args:
            filename: Filename to extract year from

        Returns:
            Year string (4 digits) or None if not found
        """
        match = re.match(r'^(\d{4})_', filename)
        return match.group(1) if match else None

    @staticmethod
    def extract_year_end_range(filename: str) -> Optional[str]:
        """
        Extract year from the end of a date range (after "to_").

        Pattern: YYYY_MM_to_YYYY_MM_*.xlsx
        Example: 2024_09_to_2025_09_Rolling13_RMS.xlsx -> "2025"

        Args:
            filename: Filename to extract year from

        Returns:
            Year string (4 digits) or None if not found
        """
        match = re.search(r'to_(\d{4})_', filename)
        return match.group(1) if match else None

    @staticmethod
    def extract_year(filename: str, strategy: str) -> Optional[str]:
        """
        Extract year based on the specified strategy.

        Args:
            filename: Filename to extract year from
            strategy: Strategy to use ("start" or "end_range")

        Returns:
            Year string (4 digits) or None if not found
        """
        if strategy == "start":
            return YearExtractor.extract_year_start(filename)
        elif strategy == "end_range":
            return YearExtractor.extract_year_end_range(filename)
        else:
            return None


class ExportWatchdogHandler(FileSystemEventHandler):
    """
    File system event handler that monitors and organizes export files.
    """

    def __init__(self, base_exports: Path, logger: logging.Logger):
        """
        Initialize the watchdog handler.

        Args:
            base_exports: Base directory for all exports
            logger: Logger instance for logging
        """
        self.base_exports = base_exports
        self.logger = logger
        self.file_mover = FileMover()
        self.year_extractor = YearExtractor()

        # Get user home directory dynamically
        home = Path.home()
        onedrive_base = home / "OneDrive - City of Hackensack"

        # === Monitored folders ===
        self.desktop_path = onedrive_base / "Desktop"
        self.down_onedrive = onedrive_base / "Downloads"
        self.down_local = home / "Downloads"
        self.monitor_paths = [
            self.desktop_path,
            self.down_onedrive,
            self.down_local
        ]

        # Ensure monitored folders exist
        for p in self.monitor_paths:
            p.mkdir(parents=True, exist_ok=True)

        # === Debounce duplicate events ===
        self.recently_handled: Dict[Path, float] = {}
        self.event_debounce_seconds = 5

        # === Export configurations ===
        # Legacy rules (preserved from original)
        self.legacy_rules: Dict[str, Dict] = {
            'SCRPA_CAD_Export': {
                'src': self.desktop_path,
                'dest': self.base_exports / '_CAD' / 'SCRPA',
                'suffix': 'SCRPA_CAD',
                'type': 'CAD',
                'format': 'xlsx',
                'year_based': False
            },
            'SCRPA_RMS_Export': {
                'src': self.desktop_path,
                'dest': self.base_exports / '_RMS' / 'SCRPA',
                'suffix': 'SCRPA_RMS',
                'type': 'RMS',
                'format': 'xlsx',
                'year_based': False
            },
            'OTActivity': {
                'src': self.down_onedrive,
                'dest': self.base_exports / '_POSS_EXPORT' / 'OVERTIME_EXPORT',
                'suffix': 'OTActivity',
                'type': 'OvertimeActivity',
                'format': 'xlsx',
                'year_based': False
            },
            'TimeOffActivity': {
                'src': self.down_onedrive,
                'dest': self.base_exports / '_POSS_EXPORT' / 'TIME_OFF_EXPORT',
                'suffix': 'TimeOffActivity',
                'type': 'TimeOffActivity',
                'format': 'xlsx',
                'year_based': False
            },
            'e_ticket': {
                'src': self.down_onedrive,
                'dest': self.base_exports / '_Summons' / 'E_Ticket',
                'suffix': 'e_ticket',
                'type': 'E_Ticket',
                'format': 'xlsx',
                'year_based': False
            },
            'Backtracet_Arrests_Export': {
                'src': self.down_onedrive,
                'dest': self.base_exports / '_BACKTRACE_ARRESTS',
                'suffix': 'Backtracet_Arrests_Export',
                'type': 'Backtracet_Arrests',
                'format': 'xlsx',
                'year_based': False
            },
        }

        # New rules with year-based organization
        self.new_rules: Dict[str, Dict] = {
            'Monthly_CAD': {
                'keywords': ['Monthly_CAD'],
                'target_dir': '_CAD/monthly_export',
                'year_strategy': 'start',
                'format': 'xlsx',
                'year_based': True
            },
            'Monthly_RMS': {
                'keywords': ['Monthly_RMS'],
                'target_dir': '_RMS/monthly_export',
                'year_strategy': 'start',
                'format': 'xlsx',
                'year_based': True
            },
            'Rolling13_CAD': {
                'keywords': ['Rolling13_CAD'],
                'target_dir': '_CAD/rolling_13',
                'year_strategy': 'end_range',
                'format': 'xlsx',
                'year_based': True
            },
            'Rolling13_RMS': {
                'keywords': ['Rolling13_RMS'],
                'target_dir': '_RMS/rolling_13',
                'year_strategy': 'end_range',
                'format': 'xlsx',
                'year_based': True
            },
            'ResponseTime_CAD': {
                'keywords': ['ResponseTime_CAD'],
                'target_dir': '_CAD/response_time',
                'year_strategy': 'end_range',
                'format': 'xlsx',
                'year_based': True
            },
            'ResponseTime_RMS': {
                'keywords': ['ResponseTime_RMS'],
                'target_dir': '_RMS/response_time',
                'year_strategy': 'end_range',
                'format': 'xlsx',
                'year_based': True
            },
        }

        # Create all destination directories (without year subfolders)
        for cfg in self.legacy_rules.values():
            cfg['dest'].mkdir(parents=True, exist_ok=True)

        self.logger.info(f"Export Watchdog initialized. Base exports: {self.base_exports}")
        self.logger.info("Watching folders:")
        for p in self.monitor_paths:
            self.logger.info(f"  • {p}")

        # Process any existing matching files
        self._process_existing_files()

    def _process_existing_files(self) -> None:
        """Scan monitored folders for existing files matching our rules."""
        self.logger.info("Starting initial directory scan")

        # Process legacy rules
        for key, cfg in self.legacy_rules.items():
            pattern = f"*{key}*.{cfg['format']}"
            for fp in cfg['src'].glob(pattern):
                if fp.is_file():
                    self.logger.info(f"Startup scan: found '{fp.name}' matching '{key}'")
                    self._move_legacy_file(fp, cfg)

        # Process new rules
        for key, cfg in self.new_rules.items():
            for keyword in cfg['keywords']:
                pattern = f"*{keyword}*.{cfg['format']}"
                for monitor_path in self.monitor_paths:
                    for fp in monitor_path.glob(pattern):
                        if fp.is_file():
                            self.logger.info(f"Startup scan: found '{fp.name}' matching '{key}'")
                            self._move_new_rule_file(fp, cfg)

    def on_created(self, event) -> None:
        """Handle file creation events."""
        if not event.is_directory:
            self._handle(event.src_path)

    def on_modified(self, event) -> None:
        """Handle file modification events."""
        if not event.is_directory:
            self._handle(event.src_path)

    def on_moved(self, event: FileSystemMovedEvent) -> None:
        """Handle file move events."""
        if not event.is_directory:
            self._handle(event.dest_path)

    def _handle(self, path_str: str) -> None:
        """
        Process a file system event.

        Args:
            path_str: Path to the file that triggered the event
        """
        fp = Path(path_str)
        now = time.time()

        # Ignore duplicates within debounce window
        if fp in self.recently_handled:
            if (now - self.recently_handled[fp]) < self.event_debounce_seconds:
                return

        # Cleanup old entries
        self.recently_handled = {
            p: t for p, t in self.recently_handled.items()
            if (now - t) < self.event_debounce_seconds
        }

        name_lower = fp.name.lower()

        # Check legacy rules first
        for key, cfg in self.legacy_rules.items():
            if key.lower() in name_lower and name_lower.endswith(f".{cfg['format']}"):
                self.recently_handled[fp] = now
                time.sleep(1)  # Let any write finish
                self.logger.info(f"Detected '{key}' in '{fp.name}', moving now.")
                self._move_legacy_file(fp, cfg)
                return

        # Check new rules
        for key, cfg in self.new_rules.items():
            for keyword in cfg['keywords']:
                if keyword.lower() in name_lower and name_lower.endswith(f".{cfg['format']}"):
                    self.recently_handled[fp] = now
                    time.sleep(1)  # Let any write finish
                    self.logger.info(f"Detected '{key}' in '{fp.name}', moving now.")
                    self._move_new_rule_file(fp, cfg)
                    return

    def _move_legacy_file(self, file_path: Path, cfg: Dict) -> None:
        """
        Move a file using legacy naming convention (timestamp prefix).

        Args:
            file_path: Path to the file to move
            cfg: Configuration dictionary for this rule
        """
        try:
            if not file_path.exists():
                self.logger.warning(f"File not found (already moved?): {file_path.name}")
                return

            ts = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            new_name = f"{ts}_{cfg['suffix']}.{cfg['format']}"
            dest_path = cfg['dest'] / new_name

            self.logger.info(f"Moving '{file_path.name}' -> '{dest_path.name}'")
            success = self.file_mover.move_file(file_path, dest_path, self.logger)

            if success:
                self.logger.info(f"SUCCESS: {cfg['type']} moved: '{file_path.name}' -> '{new_name}'")
            else:
                self.logger.error(f"FAILED: Could not move {cfg['type']} file '{file_path.name}'")

        except Exception as e:
            self.logger.error(f"Error moving {cfg['type']} file '{file_path.name}': {e}")

    def _move_new_rule_file(self, file_path: Path, cfg: Dict) -> None:
        """
        Move a file using new naming convention with year-based subfolders.

        Args:
            file_path: Path to the file to move
            cfg: Configuration dictionary for this rule
        """
        try:
            if not file_path.exists():
                self.logger.warning(f"File not found (already moved?): {file_path.name}")
                return

            # Extract year from filename
            year = self.year_extractor.extract_year(file_path.name, cfg['year_strategy'])

            if not year:
                self.logger.warning(
                    f"Could not extract year from '{file_path.name}' using strategy '{cfg['year_strategy']}'. "
                    f"Moving to base directory without year subfolder."
                )
                dest_dir = self.base_exports / cfg['target_dir']
            else:
                dest_dir = self.base_exports / cfg['target_dir'] / year

            # Keep original filename
            dest_path = dest_dir / file_path.name

            self.logger.info(f"Moving '{file_path.name}' -> '{dest_path}'")
            success = self.file_mover.move_file(file_path, dest_path, self.logger)

            if success:
                self.logger.info(
                    f"SUCCESS: {cfg['target_dir']} file moved: '{file_path.name}' -> '{dest_path}'"
                )
            else:
                self.logger.error(f"FAILED: Could not move file '{file_path.name}'")

        except Exception as e:
            self.logger.error(f"Error moving file '{file_path.name}': {e}")


def setup_logging(script_dir: Path) -> logging.Logger:
    """
    Configure logging with rotating file handler.

    Args:
        script_dir: Directory where the script is located

    Returns:
        Configured logger instance
    """
    # Create logs directory
    logs_dir = script_dir / 'logs'
    logs_dir.mkdir(exist_ok=True)

    # Log file path
    log_file = logs_dir / 'watchdog_service.log'

    # Create logger
    logger = logging.getLogger('ExportWatchdog')
    logger.setLevel(logging.INFO)

    # Remove existing handlers
    logger.handlers.clear()

    # Rotating file handler (5MB max, keep 5 backup files)
    file_handler = RotatingFileHandler(
        str(log_file),
        maxBytes=5 * 1024 * 1024,  # 5MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.INFO)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Formatter
    timestamp_fmt = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt=timestamp_fmt
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


def main() -> None:
    """Main entry point for the watchdog service."""
    # Determine script directory
    script_dir = Path(__file__).resolve().parent

    # Setup logging
    logger = setup_logging(script_dir)

    # Get base exports directory dynamically
    home = Path.home()
    base_exports = home / "OneDrive - City of Hackensack" / "05_EXPORTS"

    # Create base exports directory if it doesn't exist
    base_exports.mkdir(parents=True, exist_ok=True)

    # Initialize handler
    handler = ExportWatchdogHandler(base_exports, logger)

    # Setup observer
    observer = Observer()
    for watch_path in handler.monitor_paths:
        observer.schedule(handler, str(watch_path), recursive=False)

    observer.start()
    logger.info("Watchdog service is now running. Press Ctrl+C to stop.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        logger.info("Watchdog service stopped by user.")
    finally:
        observer.join()


if __name__ == '__main__':
    main()

