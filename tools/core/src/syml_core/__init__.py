import logging
from pathlib import Path
from rich.logging import RichHandler

FORMAT = "[bold]%(name)s[/] %(message)s"
logging.basicConfig(
    level=logging.INFO,
    format=FORMAT,
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True, markup=True)]
)

SYML_ROOT = (Path(__file__).parent / '..' / '..' / '..' / '..').resolve()
TOOLS_ROOT = SYML_ROOT / 'tools'
