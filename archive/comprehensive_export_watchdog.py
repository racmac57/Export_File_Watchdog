import os
import shutil
import time
from datetime import datetime
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemMovedEvent
import logging
from typing import Dict

# Determine script directory and log file location
script_dir = Path(__file__).resolve().parent
log_file = script_dir / 'comprehensive_export_watchdog.log'

# Configure logging
timestamp_fmt = "%Y-%m-%d %H:%M:%S"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt=timestamp_fmt,
    handlers=[
        logging.FileHandler(str(log_file)),
        logging.StreamHandler()
    ]
)

class ComprehensiveExportHandler(FileSystemEventHandler):
    """
    Watches for specified exports in Downloads and Desktop and moves them
    using a timestamp prefix and standardized suffix.
    """

    def __init__(self):
        # === Monitored folders ===
        self.desktop_path    = Path(r"C:\Users\carucci_r\OneDrive - City of Hackensack\Desktop")
        self.down_onedrive   = Path(r"C:\Users\carucci_r\OneDrive - City of Hackensack\Downloads")
        self.down_local      = Path(r"C:\Users\carucci_r\Downloads")
        self.monitor_paths   = [
            self.desktop_path,
            self.down_onedrive,
            self.down_local
        ]

        # Ensure the folders exist
        for p in self.monitor_paths:
            p.mkdir(parents=True, exist_ok=True)

        # Base exports root
        self.base_exports = Path(r"C:\Users\carucci_r\OneDrive - City of Hackensack\05_EXPORTS")

        # === Debounce duplicate events ===
        self.recently_handled: Dict[Path, float] = {}
        self.event_debounce_seconds = 5

        # === Export configurations ===
        # Key ➔ move-rule (suffix match), dest folder, file format
        self.export_systems: Dict[str, Dict] = {
            # existing SCRPA exports on Desktop
            'SCRPA_CAD_Export': {
                'src': self.desktop_path,
                'dest': self.base_exports / '_CAD' / 'SCRPA',
                'suffix': 'SCRPA_CAD',
                'type': 'CAD',
                'format': 'xlsx'
            },
            'SCRPA_RMS_Export': {
                'src': self.desktop_path,
                'dest': self.base_exports / '_RMS' / 'SCRPA',
                'suffix': 'SCRPA_RMS',
                'type': 'RMS',
                'format': 'xlsx'
            },
            # new rules for Downloads
            'OTActivity': {
                'src': self.down_onedrive,
                'dest': self.base_exports / '_POSS_EXPORT' / 'OVERTIME_EXPORT',
                'suffix': 'OTActivity',
                'type': 'OvertimeActivity',
                'format': 'xlsx'
            },
            'TimeOffActivity': {
                'src': self.down_onedrive,
                'dest': self.base_exports / '_POSS_EXPORT' / 'TIME_OFF_EXPORT',
                'suffix': 'TimeOffActivity',
                'type': 'TimeOffActivity',
                'format': 'xlsx'
            },
            'e_ticket': {
                'src': self.down_onedrive,
                'dest': self.base_exports / '_Summons' / 'E_Ticket',
                'suffix': 'e_ticket',
                'type': 'E_Ticket',
                'format': 'xlsx'
            },
            'Backtracet_Arrests_Export': {
                'src': self.down_onedrive,
                'dest': self.base_exports / '_BACKTRACE_ARRESTS',
                'suffix': 'Backtracet_Arrests_Export',
                'type': 'Backtracet_Arrests',
                'format': 'xlsx'
            },
        }

        # Create all destination directories
        for cfg in self.export_systems.values():
            cfg['dest'].mkdir(parents=True, exist_ok=True)

        logging.info(f"Comprehensive Export Watchdog started. Log file: {log_file}")
        logging.info("Watching folders:")
        for p in self.monitor_paths:
            logging.info(f"  • {p}")

        # Immediately process any existing matching files
        self._process_existing_files()

    def _process_existing_files(self):
        logging.info("Starting initial directory scan")
        for key, cfg in self.export_systems.items():
            pattern = f"*{key}*.{cfg['format']}"
            # only scan the source folder for that rule
            for fp in cfg['src'].glob(pattern):
                if fp.is_file():
                    logging.info(f"Startup scan: found '{fp.name}' matching '{key}'")
                    self._move_file(fp, cfg)

    def on_created(self, event):
        if not event.is_directory:
            self._handle(event.src_path)

    def on_modified(self, event):
        if not event.is_directory:
            self._handle(event.src_path)

    def on_moved(self, event: FileSystemMovedEvent):
        if not event.is_directory:
            self._handle(event.dest_path)

    def _handle(self, path_str: str):
        fp = Path(path_str)
        now = time.time()

        # Ignore duplicates within debounce window
        if fp in self.recently_handled and (now - self.recently_handled[fp]) < self.event_debounce_seconds:
            return

        # Cleanup old entries
        self.recently_handled = {
            p: t for p, t in self.recently_handled.items() if (now - t) < self.event_debounce_seconds
        }

        name = fp.name.lower()
        for key, cfg in self.export_systems.items():
            if key.lower() in name and name.endswith(f".{cfg['format']}"):
                self.recently_handled[fp] = now
                time.sleep(1)  # let any write finish
                logging.info(f"Detected '{key}' in '{fp.name}', moving now.")
                self._move_file(fp, cfg)
                break

    def _move_file(self, file_path: Path, cfg: Dict):
        try:
            if not file_path.exists():
                logging.warning(f"File not found (already moved?): {file_path.name}")
                return

            ts = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            new_name = f"{ts}_{cfg['suffix']}.{cfg['format']}"
            dest_path = cfg['dest'] / new_name

            logging.info(f"Moving '{file_path.name}' -> '{dest_path.name}'")
            shutil.move(str(file_path), str(dest_path))
            logging.info(f"SUCCESS: {cfg['type']} moved: '{file_path.name}' -> '{new_name}'")

        except Exception as e:
            logging.error(f"Error moving {cfg['type']} file '{file_path.name}': {e}")

if __name__ == '__main__':
    observer = Observer()
    handler = ComprehensiveExportHandler()
    # watch each folder
    for watch_path in handler.monitor_paths:
        observer.schedule(handler, str(watch_path), recursive=False)

    observer.start()
    logging.info("Watchdog is now running. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        logging.info("Watchdog service stopped by user.")
    observer.join()
