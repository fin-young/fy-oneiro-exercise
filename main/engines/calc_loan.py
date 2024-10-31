from typing import Optional
import click
from datetime import datetime

from ..utilities.validations import Validations
from ..loan_operations.simple_loan import SimpleLoan
from ..loan_operations.loan_history import LoanHistory



@click.command("calc_loan")
@click.option('--start_date', type = int, is_flag=False, flag_value=None, help='Start Date (date) as YYYYmmdd:')
@click.option('--end_date', type = int, is_flag=False, flag_value=None, help='End Date (date) as YYYYmmdd:')
@click.option('--amount', type = float, is_flag=False, flag_value=None,help='Loan Amount (amount field)')
@click.option('--currency', type = str, is_flag=False, flag_value=None,help='Currency code - 3 letter ISO.')
@click.option('--base_ir', type = float, is_flag=False, flag_value=None, help='Base Interest Rate (percentage)')
@click.option('--margin', type = float, is_flag=False, flag_value=None, help='Margin (percentage)')
def calc_loan(start_date: Optional[int] = None,
                end_date: Optional[int]= None,
                amount: Optional[float]= None,
                currency: Optional[str]= None,
                base_ir: Optional[float]= None,
                margin: Optional[float]= None) -> None:
    
    click.echo(f"Hello - You're calculating a new Loan. If you've missed any input parameters you'll be asked to fill them in on the cmd")

    loan = SimpleLoan.new_loan_process(start_date, end_date, amount, currency, base_ir, margin)
    not_finished = True

    while not_finished:
        not_finished = click.confirm("Do you want to recalculate the loan with new parameters [y]? If not [n] can finish" )
        if not_finished:
            loan.update_loan()
            loan.calculate_loan()
            click.echo(f"Here is the newly calculated loan:")
            loan.show_loan()        
  

    history = LoanHistory()
    history.load_loans()
    loan.loan_id = 1 if len(history.all_loans)==0 else max([int(l.loan_id) for l in history.all_loans]) +1
    history.all_loans.append(loan)

  
    #Create additional Loans
    add_more = True
    while add_more:
        add_more = click.confirm("Do you want to create another loan [y]? If not [n] can finish" )
        if add_more:
            new_loan = SimpleLoan.new_loan_process(None, None, None, None, None, None)
            new_loan.loan_id = 1 if len(history.all_loans)==0 else max([int(l.loan_id) for l in history.all_loans])+1
            history.all_loans.append(new_loan)
            click.echo(f"Here are all calculated Loans:")
            history.show_all_loans()  


    history.save_loans()

if __name__ == '__main__':
    calc_loan()
