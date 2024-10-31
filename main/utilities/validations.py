from datetime import date, datetime
import click
import os


class Validations(object):


    @staticmethod
    def validate_input_date(value: int, desc: str) -> date:
        if value == None:
            value = click.prompt(f'Input Parameter: {desc} (YYYYmmdd)', type=int)
        
        if type(value) == int:
            value = datetime.strptime(str(value), "%Y%m%d").date()
        
        return value
    
    @staticmethod
    def validate_input_rate(value: float, desc: str) -> date:
        if value == None:
            value = click.prompt(f'Input Parameter: {desc} (as percentage)', type=float)

        if type(value) == int: 
            value = float(value)
        return value*0.01


    @staticmethod
    def validate_input_float(value: float, desc: str) -> date:
        if value == None:
            value = click.prompt(f'Input Parameter: {desc}', type=float)

        if type(value) == int: 
            value = float(value)
        return value

    
    @staticmethod
    def validate_input_str(value: str, desc: str) -> str:
        if value == None or len(value) > 3 or type(value)!= str:
            value = click.prompt(f'Input Parameter: {desc} (string value - Currency as ISO3)', type=str)
        
        return value

    @staticmethod
    def validate_input_int(value: int, desc: str) -> int:
        if value == None or type(value)!= int:
            value = click.prompt(f'Input Parameter: {desc} (Integer)', type=int)
        
        return value    

    @staticmethod
    def validate_loans_history() -> None:
        filepath = os.path.join(os.getcwd(), "loans.csv") 
        if not os.path.isfile(filepath):
            pass
        else:
            pass