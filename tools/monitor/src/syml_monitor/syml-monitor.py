import logging
import os
import sys
import time
from datetime import datetime
from pathlib import Path

import coloredlogs
import yamale as yamale
from watchdog.events import PatternMatchingEventHandler, \
    FileSystemEvent
from watchdog.observers import Observer
from yamale import YamaleError
from yaml.scanner import ScannerError


class SYMLMonitor(PatternMatchingEventHandler):

    base_dir = str(
        (
            Path(os.path.realpath(__file__)).parent
            / '..' / '..' / '..' / '..'
        ).resolve()
    )

    # TODO: configurable
    schema = 'tools/syml-core/definitions/schemas/v1.yamale.yml'

    validated_timestamps = {}

    def validate(self, yaml_path):

        # TODO: this is weird, obsever should handle this instead
        validated_at = self.validated_timestamps.get(yaml_path)
        if validated_at is not None and (datetime.now() - validated_at).seconds < 3:
            return

        self.validated_timestamps[yaml_path] = datetime.now()

        schema_path = self.schema
        base_dir = self.base_dir

        if schema_path is None:
            return

        if base_dir is not None:
            schema_path = os.path.join(base_dir, schema_path)

        # Run yaml through glob and flatten list
        yamale_schema = yamale.make_schema(schema_path)
        try:
            yamale_data = yamale.make_data(yaml_path)
            for result in yamale.validate(yamale_schema, yamale_data, _raise_error=False):
                if result.isValid():
                    logging.info('[valid] %s', yaml_path)
                else:
                    logging.error(
                        '[invalid] %s',
                        str(yaml_path) + '\n\t' + '\n\t'.join(result.errors)
                    )
        except ScannerError as se:
            logging.error(
                '[exception] %s',
                str(yaml_path) + '\n\t' + str(se)
            )

    def on_modified(self, event: FileSystemEvent):
        if not event.src_path.endswith('~'):
            self.validate(event.src_path)


def monitor(path: str):

    path = Path(path).resolve()
    logging.info("starting intial validation in: %s", path)

    monitor = SYMLMonitor(ignore_directories=True)

    for p in path.glob('**/*.syml.yml'):
        monitor.validate(p)

    observer = Observer(timeout=1)
    observer.schedule(monitor, path, recursive=True)

    logging.info('starting watching path: %s', path)
    observer.start()

    try:
        while True:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()


if __name__ == '__main__':

    error_handler = logging.StreamHandler(sys.stdout)
    error_handler.addFilter(lambda r: r.levelno >= logging.ERROR)
    error_handler.setFormatter(coloredlogs.ColoredFormatter(fmt="%(asctime)s: %(message)s"))

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.addFilter(lambda r: r.levelno < logging.ERROR)
    stdout_handler.setFormatter(coloredlogs.ColoredFormatter(fmt="%(asctime)s: %(message)s"))

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[error_handler, stdout_handler]
    )

    monitor(sys.argv[1] if len(sys.argv) > 1 else '.')
