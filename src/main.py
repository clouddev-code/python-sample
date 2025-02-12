import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Any
import yaml
from logging.handlers import RotatingFileHandler

class BatchProcessor:
    def __init__(self) -> None:
        self.config = self.load_config()
        self.logger = self.setup_logging()

    def load_config(self) -> dict[str, Any]:
        """Load configuration from YAML file"""
        try:
            config_path = Path(__file__).parent.parent / "config" / "config.yaml"
            with open(config_path, "r") as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"Error loading config: {e}")
            sys.exit(1)

    def setup_logging(self) -> logging.Logger:
        """Setup logging configuration"""
        logger = logging.getLogger("BatchProcessor")
        logger.setLevel(logging.INFO)

        # Create logs directory if it doesn't exist
        log_dir = Path(__file__).parent.parent / "logs"
        log_dir.mkdir(exist_ok=True)

        # Console Handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(console_format)

        # File Handler
        file_handler = RotatingFileHandler(
            log_dir / "batch.log",
            maxBytes=1024*1024,  # 1MB
            backupCount=5
        )
        file_handler.setLevel(logging.INFO)
        file_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_format)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

        return logger

    def process_data(self) -> None:
        """Main data processing method"""
        try:
            self.logger.info("Starting batch process")
            # Add your batch processing logic here
            self.logger.info("Batch process completed successfully")
        except Exception as e:
            self.logger.error(f"Error during batch processing: {e}", exc_info=True)
            raise

    def cleanup(self) -> None:
        """Cleanup operations"""
        try:
            # Add cleanup logic here
            self.logger.info("Cleanup completed")
        except Exception as e:
            self.logger.error(f"Error during cleanup: {e}", exc_info=True)

def main() -> None:
    start_time = datetime.now()
    processor = BatchProcessor()

    try:
        processor.process_data()
    except Exception as e:
        processor.logger.error(f"Batch failed: {e}")
        sys.exit(1)
    finally:
        processor.cleanup()
        end_time = datetime.now()
        duration = end_time - start_time
        processor.logger.info(f"Total execution time: {duration}")

if __name__ == "__main__":
    main()
