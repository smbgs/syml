from string import Template

from rich.console import Console
from rich.panel import Panel


class SymlConsole(Console):

    def print_errors(self, errors):
        if not errors:
            return

        self.print()
        for e in errors:
            lines = []

            # Printing trace if available in error
            for t in e.get('trace', []):
                for f in t.get('frames'):
                    lines.append(
                        f" ⎔ [white bold]{f.get('name')}[/] in 🗎 "
                        f"[link=file://{f.get('filename')}]{f.get('filename')}"
                        f":{f.get('lineno')}[/link]"
                    )

                self.print(Panel(
                    '\n'.join(lines),
                    title='⧳ ' + Template(e.get('message').capitalize())
                        .substitute(e),
                    title_align='left',
                    style='red'
                ))

            self.print()
