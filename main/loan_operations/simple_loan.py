from typing import List, Union

from datetime import date, datetime, timedelta
import calendar
import click
from prettytable import PrettyTable
import numpy as np 

from ..utilities.validations import Validations


class SimpleLoan(object):

    '''
    Target:
    1. Daily Interest Amount without margin
    2. Daily Interest Amount Accrued
    3. Accrual Date
    4. NumberofDayselapsed since the Start Date of the loan
    5. Total Interest- calculated over the given period
    
    '''  
    
    def __init__(self):
        self.loan_id: int
        
        #Input Parameters
        self.start_date: date
        self.end_date: date
        self.amount: float
        self.currency: str
        self.base_ir: float #Annual 
        self.margin: float

        #Results
        self.interest_amount_wo_margin: float   #Daily Interest Amount without margin
        self.interest_amount_accrued: float     #Daily Interest Amount Accrued
        self.accrual_date: date                 #Accrual Date
        self.days_elapsed: int                  #NumberofDayselapsed since the Start Date of the loan
        self.total_interest: float              #Total Interest- calculated over the given period


    
    
    #Main Operations
    @staticmethod
    def new_loan_process(start_date: date,
                            end_date: date,
                            amount: float,
                            currency: str,
                            base_ir: float,
                            margin: float)-> "SimpleLoan":   
        #Validate Input Params
        start_date = Validations.validate_input_date(start_date, "start_date")
        end_date = Validations.validate_input_date(end_date, "end_date")
        amount = Validations.validate_input_float(amount, "amount")
        currency = Validations.validate_input_str(currency, "currency")
        base_ir = Validations.validate_input_rate(base_ir, "base_ir")
        margin = Validations.validate_input_rate(margin, "margin")

        
        loan = SimpleLoan.create(start_date, end_date, amount, currency, base_ir, margin)
        click.echo(f"Here are the full details of the calculated loan:")
        loan.show_loan()
        
        return loan

    @staticmethod
    def create(start_date: date,
                end_date: date,
                amount: float,
                currency: str,
                base_ir: float,
                margin: float)-> "SimpleLoan":

        #setup
        loan: SimpleLoan = SimpleLoan()

        loan.start_date = start_date
        loan.end_date = end_date
        loan.amount  = amount
        loan.currency = currency
        loan.base_ir = base_ir 
        loan.margin = margin

        loan.calculate_loan()

        return loan 



    def calculate_loan(self) -> None:
        
        total_rate = self.margin + self.base_ir
        term_yrs = self._calc_loan_term(self.start_date, self.end_date)
        term_days =  (self.end_date - self.start_date).days

        self.total_interest = self._calc_total_interest(self.amount, total_rate, term_yrs) 
        self.interest_amount_wo_margin = self._calc_total_interest(self.amount, self.base_ir, term_yrs) / term_days
        self.interest_amount_accrued = self.total_interest / term_days

        time_to_accural = self._calc_term_till_accrual(self.total_interest, self.amount, term_days)        
        self.accrual_date = self.start_date + timedelta(days=time_to_accural)

        days_from_start =  (datetime.now().date() - self.start_date).days 
        
        if (days_from_start <= 0) or (days_from_start >= term_days): 
            self.days_elapsed = term_days
        else:
            self.days_elapsed = days_from_start
        


    def set_new_values(self, field: str, value: Union[float, datetime, str]) -> None:

        if field not in vars(self).keys(): 
            raise Exception(f"No such field as {field}")

        setattr(self, field, value) 




    def update_loan(self) -> None:
        
        fields_to_change = True
        while fields_to_change:
            new_input = click.prompt('What field would you like to change?', type=str)

            #Type sensitive input handling    
            if "date" in new_input:
                new_input_value = click.prompt('Input the value of (date structure should be YYYYmmdd):', type= int)
                new_input_value = datetime.strptime(str(new_input_value), "%Y%m%d").date()
            
            elif new_input in ["amount", "base_ir", "margin"]:
                new_input_value = click.prompt('Input the value of ', type= float)
            
            else: 
                new_input_value = click.prompt('Input the value of ', type= str)

            self.set_new_values(new_input, new_input_value)

            fields_to_change = click.confirm("Would you like to change more input parameter before recalculating?")


    def create_additional_loans() -> None:
        pass

    def save(self) -> None: 


        pass



    #Internal Calculations
    @staticmethod
    def _calc_term_till_accrual(total_interest: float, principle: float,  total_term: float)-> date: 
        term =  int( np.ceil(((principle/ (principle + total_interest)) * total_term)))
        return term


    
    @staticmethod
    def _calc_loan_term(start_date: date, end_date: date)-> float: 
        
        term: float = 0.0

        if end_date.year -  start_date.year == 0:
            term += (end_date - start_date).days/365 if calendar.isleap(end_date.year) else (end_date - start_date).days/365
        
        else: 
            term_days: float = (end_date - start_date).days
            
            for yr in range(start_date.year, end_date.year):
                term +=1
                term_days -= 366 if calendar.isleap(yr) else 365

            yr_frac = term_days/366 if calendar.isleap(end_date.year) else term_days/365
            term += yr_frac

        return term

    @staticmethod
    def _calc_total_interest(principle:float, rate: float, term: float)-> float:
        return  principle * rate * term







    #Printing functions

    def show_loan(self) -> None: 
        pretty = PrettyTable(list(vars(self).keys()))  
        pretty.add_row(list(vars(self).values()))
        click.echo(pretty)
