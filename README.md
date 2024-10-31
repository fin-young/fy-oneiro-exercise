# fy-exercise
Interview assessment exercise - Console application for calculating a simple loan 

## Getting started & Running Tests within the file

in the terminal:
1) Create you virtual environment: python -m venv .myenv
2) Activate the virtual environment: .\.myenv\scripts\activate.ps1
3) Install dependancies: pip install -e .



#### Calculating a new loan 
You will be asked to input the required fields if they are not includded in the command line:
```sh
$ \...\fy-oneiro-exercise python main calc_loan
```

All input requirements (All rates should be a decimal when inputted in the command line): 
```sh
$ \...\fy-oneiro-exercise python main calc_loan --start_date 20240101 --end_date 20250101 --amount 100 --currency GBP --base_ir 0.05 --margin 0.05"
```
The user will:
- Will create a new loan
- Will be asked if they want to edit the terms of the loan to then recalculate
- Will be asked if they want to create another loan
- will be asked if this/these additional loans are to be edited and recalculated
- Will be asked if they want to edit & recalculate any historically calculated loans. 

#### Updating a new loan 
You will be asked to input the required fields, if they are not includded in the command
No inputs: 
```sh
$ \...\fy-oneiro-exercise python main update_loan
```
You know the loan id which you'd like to edit:
```sh
$ \...\fy-oneiro-exercise python main calc_loan --loan_id 1 
```

The user will: 
- Be shown all historically calculated loans (as stored in a csv)
- Be asked the loan ID which the used would like to edit
- Will be asked if they want to make any more changes to the loan & recalculating. 

