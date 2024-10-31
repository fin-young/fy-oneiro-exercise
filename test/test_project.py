import  click.testing
import click
import os
from datetime import datetime, date


from main.__main__ import main 

from main.loan_operations.simple_loan import SimpleLoan
from main.loan_operations.loan_history import LoanHistory

# cmd Tests
def test_main_cmd_from_click_works(capsys):
    """Tests click is accessing cli."""
    args = "functional_test"
    runner = click.testing.CliRunner()
    result = runner.invoke(main, args)
    assert "No such command 'functional_test'" in result.exception 

def test_main_calc_loan(capsys):
    """Tests calc_loan action"""
    args = "calc_loan"
    runner = click.testing.CliRunner()
    args = "calc_loan --start_date 20240101 --end_date 20250123 --amount 100 --currency GBP --base_ir 0.5 --margin 6"
    result = runner.invoke(main, args)
    assert result.exception == None



def test_main_update_loan(capsys):
    """Tests update_loan action."""
    args = "update_loan --loan_id 2"
    runner = click.testing.CliRunner()
    result = runner.invoke(main, args)
    assert result.exception == None

#Unit Tests

def test_calculating_simple_loan(capsys):
    #input_params: 
    start_date = 20230101
    end_date = 20250101
    amount  = 100
    currency = "GBP"
    base_ir = 5
    margin = 5
    loan = SimpleLoan.new_loan_process(start_date, end_date, amount, currency, base_ir, margin)
    assert type(loan) == SimpleLoan

    