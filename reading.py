# Functions for reading tables and databases

import glob
from database import *


# YOU DON'T NEED TO KEEP THE FOLLOWING CODE IN YOUR OWN SUBMISSION
# IT IS JUST HERE TO DEMONSTRATE HOW THE glob CLASS WORKS. IN FACT
# YOU SHOULD DELETE THE PRINT STATEMENT BEFORE SUBMITTING
# file_list = glob.glob('*.csv')
# print(file_list)

# Write the read_table and read_database functions below

def read_table(table_file_name):
    """
    (str) -> Table

    Given a string, which is a name of a table file with the extention '.csv'
    reads the table file, and returns a Table object representing the table
    file containing all the data in the given table file.
    REQ: table_file_name must contain the extention .csv
    REQ: data in the table file must be seperated by commas, no spaces
    REQ: len(table_file_name) > 4
    """
    # Get the file handle based off the given table file name
    file_handle = open(table_file_name, 'r')
    # Create a Table to store the data form the .csv table file
    file_data_table = Table()
    # Get the string of column names (first line) from the file table
    column_names_str = file_handle.readline()
    # Get the list of column names from the string of column names
    column_name_list = ((column_names_str.strip('\n')).split(','))
    # Add the column names to the Table object
    file_data_table.add_column_names(column_name_list)

    # Get Data For Each Column
    # Loop the rest of the unread lines in the file containning the column data
    for next_line in file_handle:
        # Strip the current line being read of tralling space and newline
        next_line = next_line.strip('\n')
        # Split the current line at the commonas in the string
        row_data = next_line.split(',')
        # Check if the next line is empty
        if(not(next_line == '')):
            # Add the list of each element in a row to the table
            file_data_table.add_row(column_name_list, row_data)
    # Close the file
    file_handle.close()

    # Return the create Table containing the table file data
    return file_data_table


def read_database():
    """
    () -> Database

    Reads all the table files with the extention .csv in the same directory
    as this file and returns a Database object containing Table objects,
    which represent the table files in this directory.
    REQ: table files in this directory must contain vaild file names with the
    extention .csv with a len(table file name) > 4
    REQ: data in the table file must be seperated by commas, no spaces
    """
    # Store the length of the string '.csv' extention
    CSV_LENGTH = 4
    # Create a list of all the table file names in the current directory
    table_file_names = glob.glob('*.csv')
    # Create a Database to store the Tables
    database_of_tables = Database()
    # Loop through the list of table file names
    for table_name in table_file_names:
        # For each table file name create a table
        table = read_table(table_name)
        # Strip .csv from the current table name
        table_name = table_name[0:(len(table_name) - CSV_LENGTH)]
        # Add the Table name to the Database object
        database_of_tables.add_table_name(table_name)
        # Add created Table to the repective key(table name) in the Database
        database_of_tables.add_table_to_database(table_name, table)
    # Return the resultant database
    return database_of_tables
