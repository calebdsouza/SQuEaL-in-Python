from reading import *
from database import *

# Below, write:
# *The cartesian_product function
# *All other functions and helper functions
# *Main code that obtains queries from the keyboard,
#  processes them, and uses the below function to output csv results


def map_keys_arguments(key_words, query):
    """
    (list of str, str) -> dict
    Given a list of a key words in a query and a query statment, returns a
    dictionary where the keys are the query key words and the values are
    the arguments for the query key words.
    REQ: len(key_words) > 0
    REQ: vaild query statment containing 'select', 'form', with 'where' as
    optional eg 'select one,two form table, where one=two'
    >>> key_words = ['select', 'from', 'where']
    >>> query = 'select m.title,m.studio,m.gross,o.category \
    from movies,oscars where m.title=o.title'
    >>> map_keys_arguments(key_words, query)
    {'select':'['m.title', 'm.studio', 'm.gross', 'o.category'],\
    'from': ['movies', 'oscars'], 'where':'m.title=o.title'}
    """
    OPTIONAL_KEY = 'where'
    # Create a dicitonary to store a mapped query key word to argument
    query_dict = {}
    # Store the split query statment at the spaces in the string in a list
    query_parts = query.split(' ')

    # Loop thorugh each token
    for key in key_words:
        # Check if the key word 'where' exist in the query
        if(query.find(key) > -1):
            # Find the index of the argument ofr the current qery key word
            # in the list
            key_word_arg_index = query_parts.index(key) + 1
            # Find the index of the query key words values in the list
            argument = query_parts[key_word_arg_index]
            # Split the argument for the query key word at the commas if they
            # exist
            argument = argument.split(',')
            # Map the query key word token to the argument in the dictionary
            query_dict[key] = argument
    # Return the query dictionary
    return query_dict


def process_select(table, column_names):
    """
    (Table, list of str) -> Table

    Given a list of vaild column names, which exist in the given Table obejct
    that is valid, returns a table containing only columns from the
    indicated given Table selected by the given list of column names
    REQ: len(column_name) > 0
    REQ: table must be a vaild Table object
    REQ: The given column names in column_names must exist in the given Table
    object
    >>> t1 = Table()
    >>> d1 = {'F': ['a', '1'], 'S': ['b', '2'], 'T': ['ff', 'ee']}
    >>> t1.set_dict(d1)
    >>> column_names = ['*']
    >>> r = process_select(t1, column_names)
    >>> check1 = Table()
    >>> check_dict = {'F': ['a', '1'], 'S': ['b', '2'], 'T': ['ff', 'ee']}
    >>> check1.set_dict(check_dict)
    >>> r.compare_tables(check1)
    True
    >>> t1 = Table()
    >>> d1 = {'F': ['a', '1'], 'S': ['b', '2'], 'T': ['ff', 'ee']}
    >>> t1.set_dict(d1)
    >>> column_names = ['F']
    >>> r = process_select(t1, column_names)
    >>> check2 = Table()
    >>> check_dict = {'F': ['a', '1']}
    >>> check2.set_dict(check_dict)
    >>> r.compare_tables(check2)
    True
    """
    # Store the constant key character to select all column_names
    SELECT_ALL = str('*')
    # Create a table to store the selected columns
    selected_table = Table()
    # Check if the given column names is the select all key character
    if(column_names[0] == SELECT_ALL):
        # Get all the column names from the given Table
        column_names = table.get_column_names()
        # Add columns to the resultant table containing the selected columns
        selected_table.add_column_names(column_names)
    else:
        # Add columns to the resultant table containing the selected columns
        selected_table.add_column_names(column_names)
    # Loop through the column name list
    for name in column_names:
        # Get the column from the given table, which is a list of it's elements
        column = table.get_column(name)
        # Add the selected columns to the resultant selected table
        selected_table.add_column_elements(name, column)
    # Return the resultant table containing the selected columns
    return selected_table


def proecss_from(database, table_names):
    """
    (Database, list of str) -> Table
    Given a argument for the query key word 'from', which is a list of csv
    table files, returns a table containing all the table data from each Table
    indeicated by the given table names.
    REQ: database must be a vaild Database objet
    REQ: len(table_names) > 0
    REQ: given table names must exist in the given database
    >>> t1 = Table()
    >>> d1 = {'F': ['a', '1'], 'S': ['b', '2']}
    >>> t1.set_dict(d1)
    >>> t2 = Table()
    >>> d2 = {'T': ['ff', 'ee']}
    >>> t2.set_dict(d2)
    >>> db = Database()
    >>> d3 = {'a': t1, 'b': t2}
    >>> db.set_dict(d3)
    >>> table_names = ['b']
    >>> r = proecss_from(db, table_names)
    >>> check1 = Table()
    >>> check_dict = {'T': ['ff', 'ee']}
    >>> check1.set_dict(check_dict)
    >>> r.compare_tables(check1)
    True
    """
    # Get list of required Tables from the Database
    table_list = database.get_tables(table_names)
    # Check if there is more than one Table in the list of table names
    if(len(table_names) == 2):
        # Get the processed cartesian product Table of the two Tables
        tables_from_database = cartesian_product(table_list[0], table_list[1])
    elif(len(table_names) > 2):
        # GEt the processed cartesian product Table of the first two Tables
        product = cartesian_product(table_list[0], table_list[1])
        # Loop through the list of tables starting from the third element
        for index in range(2, len(table_list)):
            # Get the processed cartesian product Table of the first privouse
            # Table and the next table from the list of Tables
            product = cartesian_product(product, table_list[index])
        # Store the finally processed cartesian product Table
        tables_from_database = product
    else:
        # Store the only given table
        tables_from_database = table_list[0]

    # Return the required Tables from the Database
    return tables_from_database


def process_where(table, where_argument_list):
    """
    (Table, list of str) -> Table
    Given of list of conditions regarding the given table, will return a table
    containing only the selected rows which sattifies the given conditions
    REQ: table must be a vaild Table object
    REQ: len(wher_argument_list) > 0
    REQ: each condition fomr the list should contain vaild table names found
    in the given table and must have either '>' or '=" only
    i.e. 'name1=name2'
    >>> t = Table()
    >>> d = {'a': ['1', '1'], 'b': ['1', '2']}
    >>> t.set_dict(d)
    >>> c = ['a=b']
    >>> rr = process_where(t, c)
    >>> check1 = Table()
    >>> check_dict = {'a': ['1'], 'b': ['1']}
    >>> check1.set_dict(check_dict)
    >>> rr.compare_tables(check1)
    True
    >>> t = Table()
    >>> d = {'a': ['1', '2'], 'b': ['3', '2']}
    >>> t.set_dict(d)
    >>> c = ['a=1','b>1']
    >>> r = process_where(t, c)
    >>> check2 = Table()
    >>> check_dict = {'a': ['1', '2'], 'b': ['3', '2']}
    >>> check2.set_dict(check_dict)
    >>> r.compare_tables(check2)
    True
    """
    # Create a Table to store the vaild rows whichs satisfies the list of
    # constraints
    processed_table = Table()
    # Get a list of all column names in the given Table object
    column_names = table.get_column_names()
    # Create columns in the processed Table
    processed_table.add_column_names(column_names)
    # Create a list to store the vaild rows after each contraint is processed
    vaild_rows = []
    # Loop through each where argument in the list of where arguments
    for constraint in where_argument_list:
        # Get the resultant vaild rows that  after the current constraint is
        # processed
        resultant_rows = process_constraint(table, constraint)
        # Get rid of dupicates from the resultant rows list that are in the
        # vaild rows list
        remove_duplicate_elements(vaild_rows, resultant_rows)
        # Add the resultant row to the valid rows list
        merge_lists(vaild_rows, resultant_rows)

    # Add the valid rows to the talbe
    processed_table.add_rows(column_names, vaild_rows)

    # Return the final processed table
    return processed_table


def process_constraint(table, where_argument):
    """
    (Table, str) -> list of lists of  str
    Given a vaild constraint containning a column name that exist in given
    table followed by a '=' or '>' operator and anpthe vaild table name or
    value element, returns a list if a list of str, which are vaild rows,
    which satifies the given where argument constraint.
    REQ: table msut be a vaild Table object
    REQ: len(where_argument) > 0
    REQ: where_argument must contain a single operator, which is '=' or '>'
    only, and vaild table names that must exist in the Table or a value element
    >>> t = Table()
    >>> d = {'a': ['1', '1'], 'b': ['1', '2']}
    >>> t.set_dict(d)
    >>> c = 'a=b'
    >>> process_constraint(t, c)
    [['1', '1']]
    >>> t = Table()
    >>> d = {'a': ['1', '2'], 'b': ['3', '2']}
    >>> t.set_dict(d)
    >>> c = 'b>1'
    >>> process_constraint(t, c)
    [['3', '1'], ['2', '2']]
    """
    # Find the operator position in where constraint argument
    operator_index = operator_position(where_argument)
    # Get a list of constraint values in th where argument
    constraint_values = get_constraint_values(where_argument, operator_index)
    # Determine if the constraint values contains only column names of the
    # given table
    if(has_only_column_names(table, constraint_values)):
        # Handle the contraint containing column names only, by getting a list
        # vaild row indexes in the given table
        vaild_row_indexes = handle_column_names_only(table, where_argument,
                                                     operator_index)
    else:
        # Handle the contraint containing a column names and an element value,
        # by getting a list vaild row indexes in the given table
        vaild_row_indexes = handle_value_and_column_name(table, where_argument,
                                                         operator_index)
    # Get a list of all column names in the given Table object
    column_names = table.get_column_names()
    # Get the vaild rows, which satisfies the where argument, from the given
    # Table
    vaild_rows_list = table.get_rows(column_names, vaild_row_indexes)
    # Return list of vaild rows form the given Table
    return vaild_rows_list


def operator_position(where_argument):
    """
    (str)-> int
    Given a single vaild string where argument constraint, which is a vaild
    column name, followed by an operator, followed by another vaild column
    name or value element constant, returns the integer index postion of the
    operator, whihch is either '=' or '>'
    REQ: len(where_argument) > 0
    REQ: must contain ONE of a '=' or '>'
    REQ: where_argument must be in the format: column name, operator, column
    name/value, with no spaces
    >>> arg = 'name>2'
    >>> operator_position(arg)
    4
    >>> arg = 'columnname=columnname'
    >>> operator_position(arg)
    10
    """
    # Create a list of all possible operators
    EQUAL_OPERATOR = str('=')
    GREATER_THAN_OPERATOR = str('>')
    # Check if the equal opertor is in the where argument
    if(where_argument.find(EQUAL_OPERATOR) > -1):
        # Get positon of equal operator
        position = where_argument.find(EQUAL_OPERATOR)
    # Check if the greater than opertor is in the where argument
    elif(where_argument.find(GREATER_THAN_OPERATOR) > -1):
        # Get positon of greater than operator
        position = where_argument.find(GREATER_THAN_OPERATOR)
    else:
        position = -1
    # Return the poisiton of the operator
    return position


def get_constraint_values(where_argument, operator_index):
    """
    (str, int) -> list of str
    Given a vaild string argument constraint for the key word where, which
    follows the format; a vaild column name, followed by an operator, followed
    by another vaild column name or value element constant and the index
    position of the operator in the where argument constraint string, returns
    a list constain strings, where each string is the constraint values(column
    name or value element).
    REQ: len(where_argument) > 0
    REQ: len(where_argument) > operator_index > 0
    REQ: where_argument must contain ONE of a '=' or '>'
    REQ: where_argument must be in the format: column name, operator, column
    name/value, with no spaces
    REQ: operator index must represent the index position of the operator
    in the given where_argument string
    >>> arg1 = 'name1=name2'
    >>> opt_index1 = 5
    >>> get_constraint_values(arg1, opt_index1)
    ['name1', 'name2']
    >>> arg2 = 'name1>33'
    >>> opt_index2 = 5
    >>> get_constraint_values(arg2, opt_index2)
    ['name1', '33']
    """
    # Create a list to store the values in the constraint
    value_list = []
    # Add the first value in the constriant in the values list
    value_list.append(where_argument[:operator_index])
    # Add the second value in the constraint in the values list
    value_list.append(where_argument[operator_index+1:])
    # Return the list of values
    return value_list


def has_only_column_names(table, constraint_values):
    """
    (Table, list of str) -> bool
    Given a list of constraint values, which are either vaild column names
    which exit in the given Table or vaild value element, and a vaild Table
    obeject, returns True if the all the constraint values in the given list
    of string are only column names, which exist in the the given Table
    object.
    REQ: table must be a vaild Table object
    REQ: len(constraint_values) > 0
    >>> table1 = Table()
    >>> dict1 = {'a': ['1', '1'], 'b': ['1', '2']}
    >>> table1.set_dict(dict1)
    >>> values1 = ['a', '100']
    >>> has_only_column_names(table1, values1)
    False
    >>> table2 = Table()
    >>> dict2 = {'a': ['1', '1'], 'b': ['1', '2']}
    >>> table2.set_dict(dict2)
    >>> values2 = ['a', 'b']
    >>> has_only_column_names(table2, values2)
    True
    >>> table3 = Table()
    >>> dict3 = {'a': ['1', '1'], 'b': ['1', '2']}
    >>> table3.set_dict(dict3)
    >>> values3 = ['1', '2']
    >>> has_only_column_names(table3, values3)
    False
    """
    # Create a place to store the boolean check if the given list of contraint
    # values contains only column names in the given table
    has_only_col_names = False
    # Get column name in this table
    column_names = table.get_column_names()
    # Loop through the list of column names
    for name in column_names:
        if(name == constraint_values[1]):
            has_only_col_names = True
    # Return if the given constraint values are all column names
    return has_only_col_names


def handle_value_and_column_name(table, where_argument, operator_index):
    """
    (Table, str, int) -> list of int
    Given a vaild Table object, a vaild string argument constraint for the
    key word 'where'of the format; column name followed by an operator followed
    by a value, and an index operator position of the operator in the
    given 'where' arguement constraint string, returns a list of vaild row
    number(indexes), which satisfies, the given 'where' arguement constraint
    string.
    REQ: table must be a vaild Table object
    REQ: len(where_argument) > 0
    REQ: where_argument must contain ONE of a '=' or '>'
    REQ: where_argument must be in the format: column name, operator, value
    element, with no spaces
    REQ: operator index must represent the index position of the operator
    in the given where_argument string
    REQ: len(where_argument) > operator_index > 0
    >>> table1 = Table()
    >>> dict1 = {'a': ['33', '1'], 'b': ['1', '2']}
    >>> table1.set_dict(dict1)
    >>> arg1 = 'a>2'
    >>> opt_index1 = 1
    >>> handle_value_and_column_name(table1, arg1, opt_index1)
    [0]
    >>> table2 = Table()
    >>> dict2 = {'a': ['1', '3', '1'], 'b': ['1', '2', '4'], \
    'c':['1', '2', '5']}
    >>> table2.set_dict(dict2)
    >>> arg2 = 'a=1'
    >>> opt_index2 = 1
    >>> handle_value_and_column_name(table2, arg2, opt_index2)
    [0, 2]
    >>> table3 = Table()
    >>> dict3 = {'a': ['cc', 'a', 'aab'], 'b': ['a', 'bb', 'baa']}
    >>> table3.set_dict(dict3)
    >>> arg3 = 'a=cc'
    >>> opt_index3 = 1
    >>> handle_value_and_column_name(table3, arg3, opt_index3)
    [0]
    """
    # Get the constraint values in teh where argument
    constraint_values = get_constraint_values(where_argument, operator_index)
    # Get the column name of for the column indicated in the constraint
    column_name = constraint_values[0]
    # Get the element value indicated in the constraint, which is not a column
    # name
    value_element = constraint_values[1]

    # Create a place to store the valid row indexes, which satisfies the where
    # argument constraint
    vaild_row_indexes = []
    # Get required column of the given column name from table
    column = table.get_column(column_name)

    # Determine the operation in the where argument
    if(where_argument[operator_index] == '='):
        # Loop through the column elements of the given column name for the
        # where argument
        for column_element_index in range(len(column)):
            # Check if the column element is a number
            if(column[column_element_index].isdecimal() and
               value_element.isdecimal()):
                # Check if the column element satisfies the where arugment
                # constraint (equals the other contraint value)
                if(float(column[column_element_index]) ==
                   float(value_element)):
                    # Append the row index to the list of valid row indexes
                    vaild_row_indexes.append(column_element_index)
            else:
                # Check if the column element satisfies the where arugment
                # constraint (equals the other contraint value)
                if(column[column_element_index] == value_element):
                    # Append the row index to the list of valid row indexes
                    vaild_row_indexes.append(column_element_index)
    else:
        # Loop through the column elements of the given column name for the
        # where argument
        for column_element_index in range(len(column)):
            # Check if the column element is a number
            if(column[column_element_index].isdecimal() and
               value_element.isdecimal()):
                # Check if the column element satisfies the where arugment
                # constraint (greater than the other contraint value)
                if(float(column[column_element_index]) > float(value_element)):
                    # Append the row index to the list of valid row indexes
                    vaild_row_indexes.append(column_element_index)
            else:
                # Check if the column element satisfies the where arugment
                # constraint (greater than the other contraint value)
                if(column[column_element_index] > value_element):
                    # Append the row index to the list of valid row indexes
                    vaild_row_indexes.append(column_element_index)
    # Return the list of valid row indexes
    return vaild_row_indexes


def handle_column_names_only(table, where_argument, operator_index):
    """
    (Table, str, int) -> list of int
    Given a vaild Table object, a vaild string argument constraint for the
    key word 'where'of the format; column name followed by an operator followed
    by another column name, and an index operator position of the operator
    in the given 'where' arguement constraint string, returns a list of
    vaild row number(indexes), which satisfies, the given 'where' arguement
    constraint string.
    REQ: table must be a vaild Table object
    REQ: len(where_argument) > 0
    REQ: where_argument must contain ONE of a '=' or '>'
    REQ: where_argument must be in the format: column name, operator, column
    name, with no spaces
    REQ: operator index must represent the index position of the operator
    in the given where_argument string
    REQ: len(where_argument) > operator_index > 0
    >>> table1 = Table()
    >>> dict1 = {'a': ['33', '1'], 'b': ['1', '2']}
    >>> table1.set_dict(dict1)
    >>> arg1 = 'a>b'
    >>> opt_index1 = 1
    >>> handle_column_names_only(table1, arg1, opt_index1)
    [0]
    >>> table2 = Table()
    >>> dict2 = {'a': ['1', '3', '5'], 'b': ['1', '2', '4'], \
    'c':['1', '2', '5']}
    >>> table2.set_dict(dict2)
    >>> arg2 = 'a=c'
    >>> opt_index2 = 1
    >>> handle_column_names_only(table2, arg2, opt_index2)
    [0, 2]
    >>> table3 = Table()
    >>> dict3 = {'a': ['a', 'a', 'aab'], 'b': ['a', 'bb', 'baa']}
    >>> table3.set_dict(dict3)
    >>> arg3 = 'a=b'
    >>> opt_index3 = 1
    >>> handle_column_names_only(table3, arg3, opt_index3)
    [0]
    """
    # Get the constraint values in teh where argument
    constraint_values = get_constraint_values(where_argument, operator_index)
    # Get the first column name of for the column indicated in the constraint
    column_name_one = constraint_values[0]
    # Get the second column name of for the column indicated in the constrain
    column_name_two = constraint_values[1]
    # Create a place to store the valid row indexes, which satisfies the where
    # argument constraint
    vaild_row_indexes = []
    # Get required column elements of the first given column name from table
    column_one = table.get_column(column_name_one)
    # Get required column elements of the second given column name from table
    column_two = table.get_column(column_name_two)
    # Determine the operation in the where argument
    if(where_argument[operator_index] == '='):
        # Loop through the column elements of the given column name for the
        # where argument
        for column_element_index in range(len(column_two)):
            # Check if the column elements are a numbers
            if(column_one[column_element_index].isdecimal() and
               column_two[column_element_index].isdecimal()):
                # Check if the column element satisfies the where arugment
                # constraint (equals the other contraint value)
                if(float(column_one[column_element_index]) ==
                   float(column_two[column_element_index])):
                    # Append the row index to the list of valid row indexes
                    vaild_row_indexes.append(column_element_index)
            else:
                # Check if the column element satisfies the where arugment
                # constraint (equals the other contraint value)
                if(column_one[column_element_index] ==
                   column_two[column_element_index]):
                    # Append the row index to the list of valid row indexes
                    vaild_row_indexes.append(column_element_index)
    else:
        # Loop through the column elements of the given column names from the
        # where argument
        for column_element_index in range(len(column_two)):
            # Check if the column elements are a numbers
            if(column_one[column_element_index].isdecimal() and
               column_two[column_element_index].isdecimal()):
                # Check if the column element satisfies the where arugment
                # constraint (equals the other contraint value)
                if(float(column_one[column_element_index]) >
                   float(column_two[column_element_index])):
                    # Append the row index to the list of valid row indexes
                    vaild_row_indexes.append(column_element_index)
            else:
                # Check if the column element satisfies the where arugment
                # constraint (greater than the other contraint value)
                if(column_one[column_element_index] >
                   column_two[column_element_index]):
                    # Append the row index to the list of valid row indexes
                        vaild_row_indexes.append(column_element_index)
    # Return the list of valid row indexes
    return vaild_row_indexes


def remove_duplicate_elements(list_one, list_two):
    """
    (list of str, int, list of str, int) -> NoneType
    Given two list containg either integers or stringgs removes duplicates
    elements of the second given list, which already exist in the
    first given list.
    REQ: len(list_one) > 0
    REQ: len(list_two) > 0
    REQ: len(list_one) == len(list_two)
    >>> list_one = ['1', 1, 'a', 'ba', 'ac2', 'c2a']
    >>> list_two = ['1', 'aaa', 'ab', 'a2c', 'ac2', 1]
    >>> remove_duplicate_elements(list_one, list_two)
    >>> list_two == ['aaa', 'ab', 'a2c']
    True
    >>> list_one = ['1', 1, 'a', 'ba', 'ac2', 'c2a']
    >>> list_two = ['2', '2aaa', 'ab', 'a2c', '2ac2', 2]
    >>> remove_duplicate_elements(list_one, list_two)
    >>> list_two == ['2', '2aaa', 'ab', 'a2c', '2ac2', 2]
    True
    """

    # Create a place to store the length of list two
    list_two_length = len(list_two)
    # Loop thorugh the second given list (list_two)
    for one_index in range(len(list_one)):
        # Create a counter
        two_index = 0
        # Loop through the first given list (list_one)
        while(two_index < list_two_length):
            # Check if the current element in list two is in list one
            if(list_one[one_index] == list_two[two_index]):
                # Remove the dublicate element from list two
                list_two.remove(list_one[one_index])
            # Get the current length of list two
            list_two_length = len(list_two)
            # increase the counter
            two_index += 1


def merge_lists(list_one, list_two):
    """
    ((list of str, int), (list of str, int)) -> NoneType
    Given two list, which can contain integers or stirng, takes the second
    given lis tand merges it in the first given list.
    REQ: len(list_one) > 0
    REQ: len(list_two) > 0
    REQ: len(list_one) == len(list_two)
    >>> list_one = ['1', 1, 'a']
    >>> list_two = ['22', 2, 'b']
    >>> merge_lists(list_one, list_two)
    >>> list_one == ['1', 1, 'a', '22', 2, 'b']
    True
    """
    # Loop through the second given list (list_two)
    for index_two in range(len(list_two)):
        # Append element from list_two to list_one
        list_one.append(list_two[index_two])


def cartesian_product(table_one, table_two):
    """
    (Table, Table) -> Table
    Given two vaild Table objects, returns the cartesian product of table_one
    and table_two, which is where each row in table_one is paried with every
    row in the table_two.
    REQ: table_one must be a vaild Table object
    REQ: table_two must be a vaild Table object
    >>> table1 = Table()
    >>> table2 = Table()
    >>> product = cartesian_product(table1, table2)
    >>> dict = product.get_dict()
    >>> dict == {}
    True
    >>> table1 = Table()
    >>> dict1 = {'a': ['1', '3'], 'b': ['2', '4']}
    >>> table1.set_dict(dict1)
    >>> table2 = Table()
    >>> dict2 = {'c': ['a', 'c'], 'd': ['b', 'd']}
    >>> table2.set_dict(dict2)
    >>> product = cartesian_product(table1, table2)
    >>> check2 = Table()
    >>> check_dict = {'a': ['1', '1', '3', '3'], 'b': ['2', '2', '4', '4'],\
    'c': ['a', 'c', 'a', 'c'], 'd': ['b', 'd', 'b', 'd']}
    >>> check2.set_dict(check_dict)
    >>> product.compare_tables(check2)
    True
    >>> table1 = Table()
    >>> dict1 = {'a': ['1', '3']}
    >>> table1.set_dict(dict1)
    >>> table2 = Table()
    >>> dict2 = {'c': ['a', 'c', 'f'], 'd': ['b', 'd', 'e']}
    >>> table2.set_dict(dict2)
    >>> product = cartesian_product(table1, table2)
    >>> check3 = Table()
    >>> check_dict = {'a': ['1', '1', '1', '3', '3', '3'],\
    'd': ['b', 'd', 'e', 'b', 'd', 'e'], 'c': ['a', 'c', 'f', 'a', 'c', 'f']}
    >>> check3.set_dict(check_dict)
    >>> product.compare_tables(check3)
    True
    """
    # Create a table to store the cartesian product
    cartesian_table = Table()
    # Check which of the given tables are empty
    if(not (table_one.is_empty() and table_two.is_empty())):
        # Get the number of rows in table one
        num_row_table_one = table_one.num_rows()
        # Get the number of rows in table two
        num_row_tabel_two = table_two.num_rows()
        # Get the repeated row processed Table (each row in table_one is
        # paried, with every row in table_two)
        repeat_rows_in_table_one = repeat_rows(table_one, num_row_tabel_two)
        # Get the repeated table processed Table (each row in table_two is
        # paried with each row in table_one sequentially
        repeat_table_in_table_two = repeat_table(table_two, num_row_table_one)
        # Combime the repeated row processed Table to the result cartiesian
        # product Table
        cartesian_table.combine_tables(repeat_rows_in_table_one)
        # Combime the repeated table processed Table to the result cartiesian
        # product Table
        cartesian_table.combine_tables(repeat_table_in_table_two)
    elif(table_one.is_empty()):
        # Store the cartestain product as table_two
        cartesian_table = table_two
    elif(table_two.is_empty()):
        # Store teh cartestain product as table_one
        cartesian_table = table_one
    # Return the cartesian product table
    return cartesian_table


def repeat_rows(table, repeat_num):
    """
    (Table, int) -> Table
    Given a vaild Table, and a integer greater than or equal to 0 representing
    the number of time each two in the given table should be repeated, reutrns
    a Table of with each row of the given Table repeat the number of time
    equal to the given integer
    REQ: table must be a vaild table
    REQ: repeat_num > -1
    REQ: if each of the given tables are not empty each of the given tables
    must have columns, where the length of all colcumnns are equal
    REQ: table must not be empty, mean there should be at least one column
    with at leat one column element
    >>> tabe1 = Table()
    >>> dict1 = {'a': ['1', '2'], 'b': ['1', '2']}
    >>> table1.set_dict(dict1)
    >>> repeat_num1 = 2
    >>> result = repeat_rows(table1, repeat_num1)
    >>> check = Table()
    >>> check_dict = {'a': ['1', '1', '2', '2'],\
    'b': ['1', '1', '2', '2']}
    >>> check.set_dict(check_dict)
    >>> result.compare_tables(check)
    True
    """
    # Create a place to store the resultant reapeated rows Table
    repeated_rows_table = Table()
    # Get the column names of the given Table object
    column_names = table.get_column_names()
    # Add columns to the resultant table
    repeated_rows_table.add_column_names(column_names)
    # Get the number of rows in the given table
    number_of_rows = table.num_rows()
    # Loop through the number of rows in the given Table
    for row_index in range(number_of_rows):
        # Get the current row from Table
        current_row = table.get_row(column_names, row_index)
        # Loop through the number of repeats
        for index in range(repeat_num):
            # Add the current row to the given table
            repeated_rows_table.add_row(column_names, current_row)
    # Return the resultant repeated rows Table
    return repeated_rows_table


def repeat_table(table, repeat_num):
    """
    (Table, int) -> Table
    Given a vaild Table, and an integer greater or equal to 0, representing
    the number of time all the rows in the given Table as a group is repeated,
    returns a Table of the all rows in the given Table, as a group, repeated
    the same number of times as the given integer(repeat number).
    REQ: table must be a vaild table
    REQ: repeat_num > -1
    REQ: if each of the given tables are not empty each of the given tables
    must have columns, where the length of all colcumnns are equal
    REQ: table must not be empty, mean there should be at least one column
    with at leat one column element
    >>> tabe1 = Table()
    >>> dict1 = {'a': ['1', '2'], 'b': ['a', 'b']}
    >>> table1.set_dict(dict1)
    >>> repeat_num1 = 2
    >>> result = repeat_rows(table1, repeat_num1)
    >>> check = Table()
    >>> check_dict = {'a': ['1', '1', '2', '2'], 'b': ['a', 'a', 'b', 'b']}
    >>> check.set_dict(check_dict)
    >>> result.compare_tables(check)
    True
    """
    # Create a place to store the resultant reapeated table Table
    repeated_table = Table()
    # Get the column names of the given Table object
    column_names = table.get_column_names()
    # Add columns to the resultant table
    repeated_table.add_column_names(column_names)
    # Get the all rows from cureent given Table
    all_rows = table.get_selected_column_rows(column_names)
    # Loop through the number of repeats
    for index in range(repeat_num):
        # Add the current row to the given table
        repeated_table.add_rows(column_names, all_rows)
    # Return the resultant repeated rows Table
    return repeated_table


def run_query(database, query):
    """
    (Database, str) -> Table
    Given a vaild Database object and a string which is a query statment, runs
    the given query on the given database, and returns a table represting the
    resulting table.
    REQ: database must be a vaild Database objects containing vaild Table
    objects
    REQ: len(query) > 0
    REQ: query string must be containing the key qords 'select', 'form', with
    'where' as optional eg 'select one,two form table where nameone=nametwo,
    name>value  or 'select one,two form table'
    REQ: The given argumetn in the query string for the key word 'from' must
    contain valid names of Table objects in the given Database object
    seperated by commas
    REQ: THe givne argument in the query string for the key word 'select' must
    contain valid coumns names in the Table obects identified in the argument
    given for the key word 'form'
    REQ: the given argument in the query for the key word 'where' must contain
    a single operator, which is '=' or '>'only, and vaild table names that must
    exist in the Tables from the argument given for the key word 'from' or a
    value element, in  the formart; table_name operator table_name2/value
    (with no spaces), where all constraints are sperated by commas
    >>> table1 = Table()
    >>> dict1 = {'a': ['1', '2'], 'b': ['a', 'b']}
    >>> table1.set_dict(dict1)
    >>> table2 = Table()
    >>> dict2 = {'c': ['1', '3'], 'd': ['2', '4']}
    >>> table2.set_dict(dict2)
    >>> db = Database()
    >>> db.set_dict({'t1': table1, 't2': table2})
    >>> query = 'select * from t1,t2'
    >>> result = run_query(db, query)
    >>> check1 = Table()
    >>> check_dict = ({'b': ['a', 'a', 'b', 'b'], 'a': ['1', '1', '2', '2'],\
    'd': ['2', '4', '2', '4'], 'c': ['1', '3', '1', '3']})
    >>> check1.set_dict(check_dict)
    >>> result.compare_tables(check1)
    True
    >>> table1 = Table()
    >>> dict1 = {'a': ['1', '2'], 'b': ['a', 'b']}
    >>> table1.set_dict(dict1)
    >>> table2 = Table()
    >>> dict2 = {'c': ['1', '3'], 'd': ['2', '4']}
    >>> table2.set_dict(dict2)
    >>> db = Database()
    >>> db.set_dict({'t1': table1, 't2': table2})
    >>> query = 'select * from t1,t2 where a=c'
    >>> result = run_query(db, query)
    >>> check2 = Table()
    >>> check_dict = {'c': ['1'], 'b': ['a'], 'a': ['1'], 'd': ['2']}
    >>> check2.set_dict(check_dict)
    >>> result.compare_tables(check2)
    True
    >>> table1 = Table()
    >>> dict1 = {'a': ['1', '2'], 'b': ['a', 'b']}
    >>> table1.set_dict(dict1)
    >>> table2 = Table()
    >>> dict2 = {'c': ['1', '3', '5'], 'd': ['2', '4', '6']}
    >>> table2.set_dict(dict2)
    >>> db = Database()
    >>> db.set_dict({'t1': table1, 't2': table2})
    >>> query = 'select * from t1,t2 where a=c,d>3 '
    >>> result = run_query(db, query)
    >>> check3 = Table()
    >>> check_dict = {'d': ['2', '4', '6', '4', '6'], 'b': ['a', 'a', 'a',\
    'b', 'b'], 'a': ['1', '1', '1', '2', '2'], 'c': ['1', '3', '5', '3', '5']}
    >>> check3.set_dict(check_dict)
    >>> result.compare_tables(check3)
    True
    >>> table1 = Table()
    >>> dict1 = {'a': ['1', '2'], 'b': ['a', 'b']}
    >>> table1.set_dict(dict1)
    >>> table2 = Table()
    >>> dict2 = {'c': ['1', '3', '5'], 'd': ['2', '4', '6']}
    >>> table2.set_dict(dict2)
    >>> db = Database()
    >>> db.set_dict({'t1': table1, 't2': table2})
    >>> query = 'select d,c,a from t1,t2 where a=c,d>3 '
    >>> result = run_query(db, query)
    >>> check3 = Table()
    >>> check_dict = {'d': ['2', '4', '6', '4', '6'],\
    'c': ['1', '3', '5', '3', '5'], 'a': ['1', '1', '1', '2', '2']}
    >>> check3.set_dict(check_dict)
    >>> result.compare_tables(check3)
    True
    >>> table1 = Table()
    >>> dict1 = {'a': ['1', '2'], 'b': ['a', 'b']}
    >>> table1.set_dict(dict1)
    >>> table2 = Table()
    >>> dict2 = {'c': ['1', '3', '5'], 'd': ['2', '4', '6']}
    >>> table2.set_dict(dict2)
    >>> db = Database()
    >>> db.set_dict({'t1': table1, 't2': table2})
    >>> query = 'select d,c,a,b from t1,t2 where a=c,d>3,a>b,a=2'
    >>> result = run_query(db, query)
    >>> check4 = Table()
    >>> check_dict = {'c': ['1', '3', '5', '3', '5', '1'],\
    'd': ['2', '4', '6', '4', '6', '2'],\
    'a': ['1', '1', '1', '2', '2', '2'], 'b': ['a', 'a', 'a', 'b', 'b', 'b']}
    >>> check4.set_dict(check_dict)
    >>> result.compare_tables(check4)
    True
    """
    # Create a list of key words in a query statment
    QUERY_KEY_WORDS = ['from', 'where', 'select']

    # Break up query into a dictioanry where the keys are the key words and
    # values are the respective arguments
    query_dict = map_keys_arguments(QUERY_KEY_WORDS, query)
    # Get from argument, which is a list of column names
    from_argument = query_dict.get(QUERY_KEY_WORDS[0])
    # Process argument for the key word 'from'
    processed_from_table = proecss_from(database, from_argument)

    # Check if the key word 'where' exist in the query
    if(query.find(QUERY_KEY_WORDS[1]) > -1):
        # Process argument constraint for the key word 'where'
        processed_where_table = process_where(processed_from_table,
                                              query_dict.get(
                                                            QUERY_KEY_WORDS[1]
                                                            ))
    else:
        # procesed where_table should be passed the from table if the key word
        # 'where' is not in the given query statment
        processed_where_table = processed_from_table

    # Process argument for the key word 'Select'
    processed_select_table = process_select(processed_where_table,
                                            query_dict.get(QUERY_KEY_WORDS[2]))
    # Return the resultant query table
    return processed_select_table

# Main
if(__name__ == "__main__"):
    # Read the database of this file's dicrectory
    database = read_database()
    # Get the uers query statment
    query = input("Enter a SQuEaL query, or a blank line to exit:")
    # Loop user query stament input until the user inputs and empty statment
    while(not (query == '')):
        # Get the resultant Table object of the given query statment
        query_table = run_query(database, query)
        # Print the Table object in the csv format
        query_table.print_csv()
        # Get a new query statment from the user
        query = input("Enter a SQuEaL query, or a blank line to exit:")
