# Functions for reading tables and databases

import glob
from database import *

# a table is a dict of {str:list of str}.
# The keys are column names and the values are the values
# in the column, from top row to bottom row.

# A database is a dict of {str:table},
# where the keys are table names and values are the tables.

# YOU DON'T NEED TO KEEP THE FOLLOWING CODE IN YOUR OWN SUBMISSION
# IT IS JUST HERE TO DEMONSTRATE HOW THE glob CLASS WORKS. IN FACT
# YOU SHOULD DELETE THE PRINT STATEMENT BEFORE SUBMITTING


# Write the read_table and read_database functions below
# Global variable
files = glob.glob('*.csv')


def read_table(file_name):
    '''(str) -> Table
    Takes in the file_name. Reads the .csv file. Put the values and organize
    it into a table. in the table, it is saved in a dictionary with the
    column names as the key, which point to the values which are stored
    in a list.
    REQ: file_name must exist, and be in the same directory
    (to have a meaningful table)
    REQ: file_name must be in .csv format
    (to have a meaningful table)
    '''
    result = Table(file_name)
    return result


def read_database():
    '''() -> Database
    This function is to first read all the .csv files in the directory.
    Second, after converting the .csv files into tables, add them to the
    Database.
    REQ: file_name must exist, and be in the same directory
    REQ: file_name must be in .csv format or else it won't be a meaningful
    Table (it will not crash if file is not found, or if file is found)
    '''
    result = Database(files)
    return result
