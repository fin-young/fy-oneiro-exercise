from typing import List, Any, Dict
import os
from prettytable import PrettyTable
import click
from datetime import datetime


from .simple_loan import SimpleLoan
from ..utilities.file_reader import FileReader


class LoanHistory(object):
    '''
    Handles the loading, saving, printing and sorting of multiple SimpleLoan classes
    '''
    
    def __init__(self):
        self.history_fname: str = "loans.csv"
        self.all_loans: List[SimpleLoan] = []
    
    @property
    def history_fpath(self):
        return os.path.join(os.getcwd(), self.history_fname)


    def show_history(self) -> None:
        self.history_exists()
        memory = FileReader.read_csv(filepath=self.history_fpath)
        first = True
        
        if len(memory) <= 1:
             click.echo("There are no loans calculated previously")
        
        else:
            for row in memory:
                if first:
                    first = False
                    pretty = PrettyTable(row)    
                    continue
            
                pretty.add_row(row)
            
            click.echo(pretty)


    def show_all_loans(self):
        click.echo("Below are all historically calculated Loans:") 
        loans_as_dict = self.loans_to_dict()
        
        first = True
        for loan in loans_as_dict:
            if first:
                first = False
                headers = list(loan.keys())
                id_idx = headers.index("loan_id")
                headers = [headers[id_idx] ]+ [h for h in headers if h!=headers[id_idx] ]

                pretty = PrettyTable(headers)    
                
            vals = list(loan.values())  
            vals = [vals[id_idx]] + [vals[i] for i in range(len(vals)) if i!=id_idx]
            pretty.add_row(vals)
        
        click.echo(pretty)        



    def load_loans(self) -> List[SimpleLoan]:
        self.history_exists()
        memory = FileReader.read_csv(filepath=self.history_fpath)
        loans: List[SimpleLoan] = []
        first = True
        
        if len(memory) <= 1:
            return []

        for idx, row in enumerate(memory):
            
            if first:
                first = False
                headers = row
                continue
            
            loan = self._valid_setter(dict(zip(headers, row)))
            loans.append(loan)
        
        self.all_loans = loans

    def save_loans(self) -> None:
        
        self.all_loans.sort(key=lambda x:int(x.loan_id))
        loan_dicts = self.loans_to_dict()
        FileReader.write_dict_to_csv(loan_dicts, self.history_fpath)
        

    def loans_to_dict(self) -> List[Dict[str, Any]]:
        #Turn all to dictionaries to ensure all can be displayed correctly

        all_headers = set()
        for loan in self.all_loans:
            for key in vars(loan).keys(): all_headers.add(key)
        
        all_headers = list(all_headers)
        template = {h: None for h in all_headers}
        result: List[Dict[str, Any]] = []

        for loan in self.all_loans:
            new = template.copy()
            for key, val in vars(loan).items():
                new[key] = val
            result.append(new)
        
        return result

    @staticmethod
    def _valid_setter(input_dictionary: Dict[str, Any], ) -> "SimpleLoan":
        loan = SimpleLoan()
        
        for key, val in input_dictionary.items(): 
            
            if "date" in key:
                setattr(loan, key, datetime.strptime(val, "%Y-%m-%d").date()) 

            elif key == "loan_id":
                setattr(loan, key, int(val))

            elif key == "currency":
                setattr(loan, key, str(val)) 
            
            else:
                setattr(loan, key, float(val))     
        
        return loan 


    def history_exists(self) -> None:

        if not os.path.isfile(self.history_fpath):
            FileReader.write_csv([], self.history_fpath)
        