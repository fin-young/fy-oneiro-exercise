from typing import Union, Any, Optional
from datetime import datetime
import click

from  ..loan_operations.simple_loan import SimpleLoan
from ..loan_operations.loan_history import LoanHistory


@click.command("update_loan")
@click.option('--loan_id', type = int, is_flag=False, flag_value=None, help='Loan ID')
def update_loan(loan_id: Optional[int]=None):
    """Update loans
    """
    history = LoanHistory()
    history.show_history()
    history.load_loans()
    loan_id = click.prompt('Select the Loan ID you want edit', type=int) if loan_id == None else loan_id
    loan = history.all_loans[loan_id-1]

    satisfied = False
    while not satisfied:
        loan.update_loan() 
        loan.calculate_loan()
        click.echo(f"Here is the newly calculated loan:")
        loan.show_loan()   
        history.all_loans[loan_id-1] = loan
        satisfied = click.confirm("Are you satisfied & would you like to finish [Y], or make more changes to input parameter?")

    history.save_loans()

if __name__ == '__main__':
    update_loan()