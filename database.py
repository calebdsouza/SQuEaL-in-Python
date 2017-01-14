class Table():
    '''A class to represent a SQuEaL table'''

    def __init__(self):
        """
        (Table) -> NoneType

        Initializes this Table to have a to have an empty dictionary
        """
        # Creates an empty table dictionary
        self._table_dict = {}

    def set_dict(self, new_dict):
        '''(Table, dict of {str: list of str}) -> NoneType

        Clears the old table values in this Table and populate this Table with
        the data from the given dicitoanry, new_dict.
        REQ: The input dictionary must be of the form:
            column_name: list_of_values
        REQ: Must be called upon a valid Table object
        '''
        # Set dictioary to empty
        self._table_dict.clear()
        # Populates this table with the data in new_dict
        self._table_dict.update(new_dict)

    def add_column_names(self, column_names):
        """
        (Table, list of str) -> NoneType

        Called upon an empty Table(contains no data), uses the given list of
        strings to add the given column names to the Table creating new empty
        columns in the process, by setting the table dictionary keys
        to the column with values which are empty lists
        REQ: Must be called upon a vaild Table object, which shuold not have
            data, can contaion comlumn names
        """
        # Loop through the list of column names
        for name in column_names:
            # Create a new empty column in this Table (dictionary)
            self._table_dict[name] = []

    def add_element_to_column(self, column_name, element):
        """
        (Table, str, str) -> NoneType

        Given an element to add under a given column name in this valid Table,
        which this method is called adds the given element to the given
        idetified column
        REQ: Must be called upon a vaild Table object
        """
        # Locate the list value using the column_name for the key and append
        # the element to the list value of the given column_name
        self._table_dict[column_name].append(element)

    def add_row(self, column_name_list, row_data):
        """
        (Table, list of str, list of str) -> NoneType

        Given a row, which is a list of strings containing elements for each
        of the existing columns in the Table, adds each element in the row
        to the respective coloumn.
        REQ: The elements in the row (list) must be ordered in accordance with
        the coresponding given column names to be positioned it from letf(as 0)
        to rigth(number of columns in the table)
        REQ: len(column_name_list) == len(row_data)
        """
        # Get the length of the column names list
        names_len = len(column_name_list)
        # Loop through the comlumn name list and row list at the same time
        for index in range(names_len):
            # Get the element needed to be added in a column of the Table
            element = row_data[index]
            # Get the name of the column to inset the element
            column_name = column_name_list[index]
            # Add the element in the column to the comlmun in this Table
            self.add_element_to_column(column_name, element)

    def add_rows(self, column_name_list, rows_list):
        """
        (Table, list of str, list of lists of str) -> NoneType

        Given rows, which is a list of list containing strings, which are
        elements for each of the existing columns in the Table, adds each
        element in the row from the list of rows to the respective coloumn.
        REQ: The elements in the row (list) must be ordered in accordance with
        the coresponding given column names to be positioned it from letf(as 0)
        to rigth(number of columns in the table)
        REQ: len(column_name_list) == len(rows_list)
        """
        # Get the length of the column names list
        number_of_rows = len(rows_list)
        # Loop through the comlumn name list and row list at the same time
        for index in range(number_of_rows):
            # Get the row need to be added the Table under the respective
            # columns
            row = rows_list[index]
            # Add the element in the column to the comlmun in this Table
            self.add_row(column_name_list, row)

    def add_column_elements(self, column_name, column_elements):
        """
        (Table, str, list of str) -> NoneType

        Given a name for a column and it's elements for that column, will
        create a column of the given column name in this Table, with the new
        created column containing the given column elements.
        REQ: must be called upon a valid Table object
        REQ: len(column_name) > 0
        REQ: len(columen_elements) > 0
        """
        self._table_dict[column_name] = (self._table_dict[column_name][0:] +
                                         column_elements)

    def get_dict(self):
        '''(Table) -> dict of {str: list of str}

        Return the dictionary representation of this table. The dictionary keys
        will be the column names, and the list will contain the values
        for that column.
        REQ: Must be called upon a valid Table object
        '''
        # Get the dictionary representation of this Table object
        dict_rep = self._table_dict

        # Returnt he dictionary represetnation of this Table object
        return dict_rep

    def get_column_names(self):
        """
        (Table) -> list of str

        Returns a list of all the column names of this Table, which this method
        is called upon.
        REQ: Must be called upon a valid Table object
        """
        # Get a list of column names from this Table (table dictionary)
        column_names = list(self._table_dict.keys())

        # Return the list of column names
        return column_names

    def is_empty(self):
        """
        Table -> bool

        Called upon a vaild Talble object, will return True if thsi table is
        empty, and False if this Table is not empty
        REQ: Must be called upon a valid Table object
        """
        # Check is the lenght of this table dictionary is zero
        is_empty_table = len(self._table_dict) == 0
        # Return the result of the check
        return is_empty_table

    def num_rows(self):
        """
        (Table) -> int

        Returns the largest number of rows among each column in this Table, if
        this table is empty, has no columns to get the num of rows, will
        return -1
        REQ: Must be called upon a valid Table object
        """
        # Check if the Table is empty(containes any columns)
        if(len(self._table_dict) == 0):
            # Store column length as zero
            column_length = 0
        else:
            # Get the column name(key) which the has the longest list(rows) in
            # length
            largest_column = max(self._table_dict)

            # Get the numerical value of the number of rows in the largest
            # column
            column_length = len(self._table_dict[largest_column])

        # Return the number of rows
        return column_length

    def get_row(self, column_names, row_num):
        """
        (Table, list of str) -> list of str

        Given a list of vaild column names, all of which exist in this Table,
        and a valid row number in this Table, returns a list of each element
        in the given columns, identifies by the column names of the given row.
        REQ: must be called upon a vaild Table Object
        REQ: all the names in the list of column names, must vaild and exist
        in this Table object
        REQ: slef.num_rows() > row_num > -1
        """
        # Create a list to store the current row data
        row_data = []
        # Loop through the list of column names
        for name in column_names:
            # Append row data to respective row data list
            row_data.append(self._table_dict[name][row_num])

        # Return the row data list
        return row_data

    def get_rows(self, column_names, row_index_list):
        """
        (Table, list of str, list of int) -> list of lists of str

        Given a list of vaild column names, all of which exist in this Table,
        and a list of valid row numbers in this Table, returns a list where
        each element is a list the value in the row from the identified columns
        of the given row.
        REQ: must be called upon a vaild Table Object
        REQ: all the names in the list of column names, must vaild and exist
        in this Table object
        REQ: each integer element inf the row index list must be a vaild row
        number, which is greater than -1 and less than slef.num_rows()
        """
        # Create a list ot store the required rows
        required_rows = []
        # Loop thorugh all the list of row indexes wanted
        for index in range(len(row_index_list)):
            # Get the row of the current given row index
            current_row = self.get_row(column_names, row_index_list[index])
            # Append the current row to the list of required rows
            required_rows.append(current_row)
        # Return the list of required rows
        return required_rows

    def get_selected_column_rows(self, column_names):
        """
        (Table, list of str) -> list of str

        Given a list of vaild column names which exist in this Table object,
        returns a list of rows, which contains element only from the
        specified columns identifies by the given list of column names.
        REQ: must be called upon a valid Table object
        REQ: len(column_names) > 0
        REQ: each name in the given list of column names must exist in this
        Table object
        """
        # Create a place to sotre the list of rows
        rows_list = []
        # Get the number of rows in this table
        num_rows = self.num_rows()
        # Get the column names in this Table
        column_names = self.get_column_names()
        # Loop trough each row in this table
        for row_index in range(num_rows):
            # Append row data to respective row data list
            current_row_data = self.get_row(column_names, row_index)
            # Append current row to table data list
            rows_list.append(current_row_data)
        # Returnt the created table data list
        return rows_list

    def get_column(self, column_name):
        """
        (Table, str) -> list of str

        Given a string, which is a single vaild column name that exist in this
        Table object, returns all the elements in that spesific column
        REQ: must be called upon a vaild Table object
        REQ: column_name must be a vaild name which exist in this Table object
        REQ: len(column_name) > 0
        """
        # Get column elements of given column name
        column = self._table_dict.get(column_name)

        # Return column elements
        return column

    def combine_tables(self, other_table):
        """
        (Table, Table) -> NoneType

        Given a vaild Table object, will combine all the columns in the given
        Table object with this Table object.
        REQ: must be called upon a valid Table object
        REQ: other_table should not be empty
        """
        # Get other table dictionary
        other_dict = other_table._table_dict
        # Combined tables
        self._table_dict.update(other_dict)

    def compare_tables(self, other_table):
        """
        (Table, Table) -> bool

        Given a vaild Table object, will compare all the columns in the given
        Table object with this Table object, returns True if all the columns
        are the same, else returns false if one or more columns are not the
        same.
        REQ: must be called upon a valid Table object
        REQ: other_table should not be empty
        """
        # Set compare result to True
        is_same = True
        # Get other table dictionary
        other_dict = other_table._table_dict
        # Get the column names in the other Table
        other_column_names = other_table.get_column_names()
        # Loop thorugh the list of column names in the other Table
        for name in other_column_names:
            # Check if the columns are not the same in both Tables
            if(not(self.get_column(name) == other_table.get_column(name))):
                # Set compare result to False
                is_same = False
        # Return the resultant compare value
        return is_same

    def __str__(self):
        """
        (Table) -> str

        Returns a string representation of this Table.
        REQ: must be called upon a vaild Table object
        """
        # Get string representation of the tble dicationary
        dict_rep = str(self._table_dict)
        # return the string representation of this Table
        return dict_rep

    def print_csv(self):
        '''(Table) -> NoneType
        Print a representation of table in csv format.
        '''
        # no need to edit this one, but you may find it useful (you're welcome)
        dict_rep = self.get_dict()
        columns = list(dict_rep.keys())
        print(','.join(columns))
        rows = self.num_rows()
        for i in range(rows):
            cur_column = []
            for column in columns:
                cur_column.append(dict_rep[column][i])
            print(','.join(cur_column))


class Database():
    '''A class to represent a SQuEaL database'''

    def __init__(self):
        """
        (Database) -> NoneType

        Initializes this Database to have a to have an empty dictionary
        """
        # Creates a empty database dictionary
        self._database_dict = dict()

    def set_dict(self, new_dict):
        '''(Database, dict of {str: Table}) -> NoneType

        Populate this database with the data in new_dict.
        REQ: new_dict must have the format:
            table_name: table
        REQ: Must be called upon a valid Database object
        '''
        # Populates this database with the data in new_dict
        self._database_dict.update(new_dict)

    def get_dict(self):
        '''(Database) -> dict of {str: Table}

        Return the dictionary representation of this database.
        The database keys will be the name of the table, and the value
        with be the table itself.
        REQ: Must be called upon a valid Database object
        '''
        # Get the dictionary representation of this Database object
        dict_rep = self._database_dict

        # Returnt he dictionary represetnation of this Database object
        return dict_rep

    def add_table_name(self, table_name):
        """
        (Database, str) -> NoneType

        Called upon an empty database(contains no data), uses the given list of
        table names to add the given table names to the Database by creating
        new empty Tables in the process, by setting the database dictionary
        keys to the Tables s which are empty
        REQ: Must be called upon a vaild database object, which shuold not have
               data, can contaion Table names (keys)
        """
        # Updates the database dictionary atrabuite with the given table
        # names as keys
        self._database_dict[table_name] = None

    def add_table_names(self, table_names):
        """
        (Database, list of str) -> NoneType

        Called upon an empty database(contains no data), uses the given list of
        table names to add the given table names to the Database by creating
        new empty Tables in the process, by setting the database dictionary
        keys to the Tables s which are empty
        REQ: Must be called upon a vaild database object, which shuold not have
            data, can contaion Table names (keys)
        """
        # Updates the database dictionary atrabuite with the given table
        # names as keys
        self._database_dict.update(dict.fromkeys(table_names))

    def add_table_to_database(self, table_name, table):
        """
        (Database, str, Table) -> NoneType

        Given a Table value to assign for a given table name(key) of this
        valide Database object, which this method is called upon, adds the
        the given Table to Database under the given table name(key).
        REQ: Must be called upon a vaild Database object
        """
        # Add table to database dictionary
        self._database_dict[table_name] = table

    def get_table(self, table_name):
        """
        (Database, str) -> Table

        Given a vaild Table name(str) that exist in this Database, which this
        method is called upon, returns the Table with that name(key) in this
        Database.
        REQ: Must be called upon a vaild Database object
        REQ: Given table_name must exist in this Database of which this method
        is called upon
        """
        # Get the Table from this Database dictioanry
        resultant_table = self._database_dict[table_name]
        # Return the Table found
        return resultant_table

    def get_tables(self, table_names):
        """
        (Database, list of str) ->  list of Table

        Given a list of valid table names, which exist in this Database object,
        returns a list of Table, which are specified by the given list of
        table names.
        REQ: must be called upon a valid Database object
        REQ: len(table_names) > 0
        REQ: the names in the list of table naems must valid and exist in this
        Database object
        """
        # Create a list to store the required Tables from the Database
        table_list = []
        # Loop thorugh the given list of Table names
        for name in table_names:
            # Get the Table of the current name form this Database
            current_table = self.get_table(name)
            # Append the current Table to the list of Tables
            table_list.append(current_table)
        # Return the list of tables
        return table_list
