import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)

SYML_ROOT = (Path(__file__).parent / '..' / '..' / '..' / '..').resolve()
TOOLS_ROOT = SYML_ROOT / 'tools'
