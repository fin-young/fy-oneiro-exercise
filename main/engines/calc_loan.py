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
@click.option('--base_ir', type = float, is_flag=False, flag_value=None, help='Base Interest Rate as Decimal in command line')
@click.option('--margin', type = float, is_flag=False, flag_value=None, help='Margin as Decimal in command line')
def calc_loan(start_date: Optional[int] = None,
                end_date: Optional[int]= None,
                amount: Optional[float]= None,
                currency: Optional[str]= None,
                base_ir: Optional[float]= None,
                margin: Optional[float]= None) -> None:

    #Add new loan    
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
  
    #Store loan with previously calculated loans
    history = LoanHistory()
    history.load_loans()
    loan.loan_id = 1 if len(history.all_loans)==0 else max([int(l.loan_id) for l in history.all_loans]) +1
    history.all_loans.append(loan)

  
    #Create additional Loans
    add_more = True
    while add_more:
        add_more = click.confirm("Do you want to create another loan [y]? If not, finish [n]" )
        if add_more:
            new_loan = SimpleLoan.new_loan_process(None, None, None, None, None, None)
            new_loan.loan_id = 1 if len(history.all_loans)==0 else max([int(l.loan_id) for l in history.all_loans])+1
            history.all_loans.append(new_loan)
            click.echo(f"Here are all calculated Loans:")
            history.show_all_loans()  
        
        else:
            history.show_all_loans()  
    
    #Save all loans added
    history.save_loans()
    

    #Allow final edits to saved loans
    make_edit = True
    if make_edit:
        make_edit = click.confirm("Do you want edit any of the previously calculated loans?" )
        if make_edit:
            edit_idx = click.prompt('Select the Loan ID you want edit', type=int)
            edit_loan = history.all_loans[edit_idx]
            edit_loan.update_loan()
            edit_loan.calculate_loan()
            click.echo(f"Here is the newly calculated loan:")
            edit_loan.show_loan()                

if __name__ == '__main__':
    calc_loan()
