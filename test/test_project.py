import click.testing import runner
import click
import os

from main.__main__ import main 


def test_cmd_from_click_works(capsys):
    """Tests engine_trial2 action (without debug mode)."""
    args = "calc_loan --start_date 20240101 --end_date 20250123 --amount 100 --currency GBP --base_ir 0.5 --margin 6"
    result = runner.invoke(main, args)
    assert True