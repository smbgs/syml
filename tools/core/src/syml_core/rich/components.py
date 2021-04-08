from string import Template

from rich.console import Console
from rich.panel import Panel


class SymlConsole(Console):

    def print_errors(self, errors):
        if not errors:
            return

        self.print()
        for e in errors:

            # Printing error
            self.print(Panel(
                Template(e.get('message').capitalize()).substitute(e),
                title_align='left',
                style='red'
            ))

            # Printing trace if available in error
            for t in e.get('trace', []):
                lines = [f"   {t.get('exc_value')}"]
                for f in t.get('frames'):
                    lines.append(
                        f" ⎔ [white bold]{f.get('name')}[/] in 🗎 "
                        f"[white][link=file://{f.get('filename')}]{f.get('filename')}"
                        f":{f.get('lineno')}[/link][/]"
                    )

                self.print(Panel(
                    '\n'.join(lines),
                    title=f"⧳ {t.get('exc_type')}",
                    title_align='left',
                    style='#ffaa00'
                ))

            self.print()

    def print_info(self, info):
        if not info:
            return

        for i in info:
            self.print(
                '   • ' + Template(i.get('message')).substitute(i)
            )
