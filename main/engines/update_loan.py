from typing import Union, Any
from datetime import datetime

import click



@click.command("update_loan")
def update_loan():
    """Update loans
    """
    click.echo(f"Hello - You're Updating a loan")


if __name__ == '__main__':
    update_loan()