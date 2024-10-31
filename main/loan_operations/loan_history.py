from typing import List, Any, Dict
import os
from prettytable import PrettyTable
import click

from .simple_loan import SimpleLoan
from ..utilities.file_reader import FileReader


class LoanHistory(object):
    def __init__(self):
        self.history_fname: str = "loans.csv"
        self.all_loans: List[SimpleLoan] = []
    
    @property
    def history_fpath(self):
        return os.path.join(os.getcwd(), self.history_fname)


    
    def show_history(self) -> None:
        memory = FileReader.read_csv(filepath=self.history_fpath)
        first = True
        for row in memory:
            if first:
                first = False
                pretty = PrettyTable(row)    
                continue
        
            pretty.add_row(row)
        
        click.echo(pretty)


    def show_all_loans(self):
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

    
    def select_stored_loan(self, loan_id: int) -> "SimpleLoan":
        
        memory = FileReader.read_csv(filepath=self.history_fpath)
        first = True
        found = False
        index = 0

        while not found:
            row = memory[index]
            if first:
                first = False
                headers = row
                index +=1
                continue
            
            if index == loan_id:
                loan_data = dict(zip(headers, row))
                found = True
            
            index +=1

        #set data to class 
        loan = SimpleLoan()
        for key, val in loan_data.items(): 
            setattr(loan, key, val) 
               
        return loan
    

    def load_loans(self) -> List[SimpleLoan]:
        memory = FileReader.read_csv(filepath=self.history_fpath)
        loans: List[SimpleLoan] = []
        first = True

        for idx, row in enumerate(memory):
            
            if first:
                first = False
                headers = row
                continue
            
            loan = SimpleLoan()
            for key, val in dict(zip(headers, row)).items(): 
                setattr(loan, key, val) 
            
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
        


