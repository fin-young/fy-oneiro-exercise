from typing import Optional
import click
from datetime import datetime


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

  
if __name__ == '__main__':
    calc_loan()
