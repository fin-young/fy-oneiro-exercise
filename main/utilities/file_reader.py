from typing import List, Dict, Optional, Any, Generator

import os
import csv 
from csv import DictWriter


class FileReader(object):

    

    @staticmethod
    def read_csv(filepath: str, encoding: Optional[str] = "utf-8")-> List[List[Any]]:
        # Reads a CSV file iteratively, yielding each row as a list.
        #     filename: The path to the CSV file.
        #     encoding: optional
        # Yields: A list representing a row of the CSV file.

        content: List[List[Any]] = []
        with open(file=filepath, mode='r', encoding= encoding) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                content.append(row)

        return content



    @staticmethod
    def write_csv(content: List[List[str]], filepath: str)-> None:
        # Writes a CSV file iteratively
        #     filename: The path to the CSV file.
        with open(file=filepath, mode='w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(content)

    @staticmethod
    def append_csv(content: List[List[str]], filepath: str, encoding: Optional[str] = "utf-8")-> None:
        store = FileReader.read_csv(filepath, encoding)
        for i in range(len(content)): store.append(content[i])
        FileReader.write_csv(store, filepath)



    @staticmethod
    def get_loans():
        pth = os.getcwd()

    
    @staticmethod
    def write_dict_to_csv(content: List[Dict[str, str]], filepath: str)-> None:
        keys = content[0].keys()

        with open(filepath, 'w', newline='') as csv:
            writer = DictWriter(csv, keys)
            writer.writeheader()
            writer.writerows(content)
