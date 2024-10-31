from typing import Callable, Optional, List
import click

from main.engines.calc_loan import calc_loan
from main.engines.update_loan import update_loan


CONTEXT_SETTINGS = dict(auto_envvar_prefix="TODO")

class MainCli(click.MultiCommand):
    def list_commands(self, ctx) -> List[str]:
        return [
            "functional_test",
            "update_loan",
            "calc_loan"
        ]

    def get_command(self, ctx, name) -> Optional[click.Command]:
        if name == "functional_test":
            return click.echo("Testing from the cmd - Success!")    
        if name == "update_loan":
            return update_loan
        if name == "calc_loan":
            return calc_loan
    

        raise AssertionError("CLI command not found: " + name)

@click.command(cls=MainCli, context_settings=CONTEXT_SETTINGS)
def main() -> None:
    pass

if __name__ == "__main__":
    main()