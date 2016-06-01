from reading import *
from database import *

# Below, write:
# *The cartesian_product function
# *All other functions and helper functions
# *Main code that obtains queries from the keyboard,
#  processes them, and uses the below function to output csv results
# Global Variable:
where = 'where'
special_star = ['*']
column_index = 1
table_names_index = 3
operations = ['>', '<', '=']


def print_csv(table):
    '''(Table) -> NoneType
    Print a representation of table.
    '''
    dict_rep = table.get_dict()
    columns = list(dict_rep.keys())
    print(','.join(columns))
    rows = num_rows(table)
    for i in range(rows):
        cur_column = []
        for column in columns:
            cur_column.append(dict_rep[column][i])
        print(','.join(cur_column))


def run_query(database, query):
    '''(Database, str) -> Table
    This function is to return whatever was queried.
    REQ: query must be in the right format
    >>> x = Table(None, 'f', {'a':['b'], 'b':['c']})
    >>> y = Table(None, 'g', {'d':['e'], 'e':['d']})
    >>> z = Database()
    >>> z.add_table(x)
    >>> z.add_table(y)
    >>> query = "select a,d from f,g where a='b'"
    >>> w = {'a':['b'], 'd':['e']}
    >>> v = run_query(z,query)
    >>> v = v.get_dict()
    >>> v.__eq__(w)
    True
    >>> x = Table(None, 'f', {'a':['b', 'h'], 'b':['c', 'i']})
    >>> y = Table(None, 'g', {'d':['e', 's'], 'e':['d', 't']})
    >>> z = Database()
    >>> z.add_table(x)
    >>> z.add_table(y)
    >>> query = "select a,d from f,g where a<'z'"
    >>> w = {'a':['b', 'b', 'h', 'h'], 'd':['e', 's', 'e', 's']}
    >>> v = run_query(z,query)
    >>> v = v.get_dict()
    >>> v.__eq__(w)
    True
    >>> x = Table(None, 'f', {'a':['b', 'h'], 'b':['c', 'i']})
    >>> y = Table(None, 'g', {'d':['e', 's'], 'e':['d', 't']})
    >>> z = Database()
    >>> z.add_table(x)
    >>> z.add_table(y)
    >>> query = "select a,d from f,g where a>'z'"
    >>> w = {'a':[], 'd':[]}
    >>> v = run_query(z,query)
    >>> v = v.get_dict()
    >>> v.__eq__(w)
    True
    '''
    # get all the columns needed in query.
    (column_name, table_name, how) = index_query(query)
    # run cartersian product
    # if more than one table_name, run cartesian product
    if type(table_name) == list:
        new_table = query_cartesian(database, table_name)
    else:
        # just get that table, since only one table
        new_table = database[table_name]
    # run constraint
    if type(how) != bool:
        for constraints in how:
            new_table = constraint(constraints, new_table)
    # run select
    # column_name is ['*;] is special token
    # return the whole table
    if column_name == special_star:
        new_table = new_table
    # column_name is always list
    elif type(column_name) == list:
        # get the columns from this new_table
        new_table = new_table.get_multiple_column(column_name)
    return new_table


def index_query(query):
    '''(str) -> (list of str, list of str, bool/list of str)
    This is to give back the query with the specific
    columns, table_names, and constraints were together.
    REQ: query is in the format
        select column from table_names
        or
        select column from table_names where constraint
    REQ: column, table_names cannot be empty
    REQ: if there is a where token, constraint cannot be empty
    >>> index_query('select book.author,book.title from books,movies')
    (['book.author', 'book.title'], ['books', 'movies'], True)
    >>> index_query('select b from c where d=e')
    (['b'], ['c'], ['d=e'])
    >>> index_query("select b from d where e>f, s= 'Randall Munroe'")
    (['b'], ['d'], ['e>f', "s= 'Randall Munroe'"])
    >>> index_query("select b from d where e > f, s= 'Randall Munroe'")
    (['b'], ['d'], ['e>f', "s= 'Randall Munroe'"])
    '''
    # given the query, given it to the list
    query = query.split()
    # clean the query, some also in csv format
    list_of_columns = clean(query[column_index])
    list_of_table_names = clean(query[table_names_index])
    # see if 'where' is in the query
    if where in query:
        # get the index of where
        where_index = query.index('where')
        # get the first part after where
        constraint = query[where_index+1]
        # get the rest after where
        for index in range(where_index+2, len(query)):
            # this is to clean the format
            # you can only have space btwn words
            # no spaces before or after '>', '<', '='
            condition1 = query[index-1] not in operations
            condition2 = query[index] not in operations
            if condition1 and condition2:
                space = ' '
            else:
                space = ''
            # add the other parts to the constraint
            constraint = constraint + space + query[index]
        # finally clean the constraint, since it is in csv format
        constraint = clean(constraint)
    else:
        # if no where, constraint is True
        constraint = True
    return (list_of_columns, list_of_table_names, constraint)


def cartesian_product(table1, table2):
    '''(Table, Table) -> Table
    This function is to create a whole new table where two tables
    are joined together.
    REQ: None
    >>> x = Table(None, 'a',{})
    >>> y = Table(None, 'b',{})
    >>> t = cartesian_product(x,y)
    >>> t.get_dict() == {}
    True
    >>> y = Table(None, 'b', {'Alice':['see'], 'Kumail': ['bye']})
    >>> t = cartesian_product(x,y)
    >>> z = {'Kumail': [], 'Alice': []}
    >>> t = t.get_dict()
    >>> t.__eq__(z)
    True
    >>> y = Table(None, 'b', {'Alice':['see'], 'Kumail': ['bye']})
    >>> x = Table(None, 'a', {'Ben': ['hi'], 'Ted': ['bye']})
    >>> f = cartesian_product(x,y)
    >>> f = f.get_dict()
    >>> z1 = {'Alice': ['see'], 'Kumail': ['bye'], 'Ben': ['hi'], \
    'Ted': ['bye']}
    >>> z1.__eq__(f)
    True
    >>> x = Table(None, 'f', {'a':['b', 'h'], 'b':['c', 'i']})
    >>> y = Table(None, 'g', {'d':['e', 's'], 'e':['d', 't']})
    >>> f = cartesian_product(x,y)
    >>> f = f.get_dict()
    >>> z1 = {'a':['b', 'b', 'h', 'h'], 'd':['e', 's', 'e', 's'],\
    'b':['c', 'c', 'i', 'i'], 'e':['d', 't', 'd', 't']}
    >>> z1.__eq__(f)
    True
    >>> x = Table(None, 'f', {'a':['b', 'h'], 'b':['c', 'i']})
    >>> y = Table(None, 'g', {'d':['e', 's']})
    >>> f = cartesian_product(x,y)
    >>> f = f.get_dict()
    >>> z1 = {'a':['b', 'b', 'h', 'h'], 'd':['e', 's', 'e', 's'],\
    'b':['c', 'c', 'i', 'i']}
    >>> z1.__eq__(f)
    True
    '''
    # create a new Database
    new_database = Database()
    # add tables inside Database
    new_database.add_table(table1)
    new_database.add_table(table2)
    new_table = new_database.add_table_together(table1, table2)
    return new_table


def query_cartesian(database, list_of_table_names):
    '''(Database, list) -> Table
    Given a database, it will run cartesian product through the whole list of
    table names.
    REQ: len(list_of_table_names) > 2
    REQ: table_names must be correct (it is in database)
    >>> x = Table(None, 'a',{})
    >>> y = Table(None, 'b',{})
    >>> z = Database()
    >>> z.add_table(x)
    >>> z.add_table(y)
    >>> t = query_cartesian(z, ['a','b'])
    >>> t.get_dict() == {}
    True
    >>> y = Table(None, 'b', {'Alice':['see'], 'Kumail': ['bye']})
    >>> z = Database()
    >>> z.add_table(x)
    >>> z.add_table(y)
    >>> t = query_cartesian(z, ['a','b'])
    >>> z1 = {'Kumail': [], 'Alice': []}
    >>> t = t.get_dict()
    >>> t.__eq__(z1)
    True
    >>> y = Table(None, 'b', {'Alice':['see'], 'Kumail': ['bye']})
    >>> x = Table(None, 'a', {'Ben': ['hi'], 'Ted': ['bye']})
    >>> z = Database()
    >>> z.add_table(x)
    >>> z.add_table(y)
    >>> f = query_cartesian(z, ['a','b'])
    >>> f = f.get_dict()
    >>> z1 = {'Alice': ['see'], 'Kumail': ['bye'], 'Ben': ['hi'], \
    'Ted': ['bye']}
    >>> z1.__eq__(f)
    True
    >>> x = Table(None, 'f', {'a':['b', 'h'], 'b':['c', 'i']})
    >>> y = Table(None, 'g', {'d':['e', 's'], 'e':['d', 't']})
    >>> z = Database()
    >>> z.add_table(x)
    >>> z.add_table(y)
    >>> f = query_cartesian(z, ['f','g'])
    >>> f = f.get_dict()
    >>> z1 = {'a':['b', 'b', 'h', 'h'], 'd':['e', 's', 'e', 's'],\
    'b':['c', 'c', 'i', 'i'], 'e':['d', 't', 'd', 't']}
    >>> z1.__eq__(f)
    True
    >>> x = Table(None, 'f', {'a':['b', 'h'], 'b':['c', 'i']})
    >>> y = Table(None, 'g', {'d':['e', 's']})
    >>> z = Database()
    >>> z.add_table(x)
    >>> z.add_table(y)
    >>> f = query_cartesian(z, ['f','g'])
    >>> f = f.get_dict()
    >>> z1 = {'a':['b', 'b', 'h', 'h'], 'd':['e', 's', 'e', 's'],\
    'b':['c', 'c', 'i', 'i']}
    >>> z1.__eq__(f)
    True
    '''
    # get base table
    base_table = database.get_table(list_of_table_names[0])
    # get index
    count = 1
    # loop through rest of the list
    while count < len(list_of_table_names):
        # table 2 is the next index
        t2 = database.get_table(list_of_table_names[count])
        # run cartesian product through each table
        base_table = cartesian_product(base_table, t2)
        # increase this index
        count += 1
    return base_table


def num_rows(table):
    '''(Table) -> int
    This function is to get the number of rows in a table.
    >>> x = Table(None, 'a',{})
    >>> num_rows(x)
    0
    >>> y = Table(None, 'b', {'Alice':['see'], 'Kumail': ['bye']})
    >>> num_rows(y)
    1
    '''
    # use the method num_of_rows to get the number of rows in a table
    result = table.num_of_rows()
    return result


def constraint(constraint, table):
    '''(str, Table) -> Table
    This function is to run the constraint on the table. It will delete values
    in the column that do not meet constaint.
    >>> a = {'Alice': ['hi', '29'], 'Age' : ['bye', '30']}
    >>> how = 'Alice=Age'
    >>> x = Table(None, 'a', a)
    >>> x = constraint(how, x)
    >>> x = x.get_dict()
    >>> z = {'Alice':[], 'Age': []}
    >>> z.__eq__(x)
    True
    >>> a = {'Alice': ['hi', '29'], 'Age' : ['bye', '30']}
    >>> how = 'Alice>Age'
    >>> x = Table(None, 'a', a)
    >>> x = constraint(how, x)
    >>> x = x.get_dict()
    >>> z = {'Alice':['hi'], 'Age': ['bye']}
    >>> z.__eq__(x)
    True
    >>> a = {'Alice': ['hi', '29'], 'Age' : ['bye', '30']}
    >>> how = 'Alice<Age'
    >>> x = Table(None, 'a', a)
    >>> x = constraint(how, x)
    >>> x = x.get_dict()
    >>> z = {'Alice':['29'], 'Age': ['30']}
    >>> z.__eq__(x)
    True
    >>> a = {'Alice': ['hi', '29'], 'Age' : ['bye', '30']}
    >>> how = 'Alice=29'
    >>> x = Table(None,'a', a)
    >>> x = constraint(how, x)
    >>> x = x.get_dict()
    >>> z = {'Alice':['29'], 'Age': ['30']}
    >>> z.__eq__(x)
    True
    >>> a = {'Alice': ['hi', '29'], 'Age' : ['bye', '30']}
    >>> how = 'Alice>28'
    >>> x = Table(None, 'a', a)
    >>> x = constraint(how, x)
    >>> x = x.get_dict()
    >>> z = {'Alice':['29'], 'Age': ['30']}
    >>> z.__eq__(x)
    True
    >>> a = {'Alice': ['hi', '29'], 'Age' : ['bye', '30']}
    >>> how = 'Alice<30'
    >>> x = Table(None, 'a', a)
    >>> x = constraint(how, x)
    >>> x = x.get_dict()
    >>> z = {'Alice':['29'], 'Age': ['30']}
    >>> z.__eq__(x)
    True
    >>> a = {'Alice': ['hi', '29'], 'Age' : ['bye', '30']}
    >>> how = 'Alice=hi'
    >>> x = Table(None, 'a', a)
    >>> x = constraint(how, x)
    >>> x = x.get_dict()
    >>> z = {'Alice':['hi'], 'Age': ['bye']}
    >>> z.__eq__(x)
    True
    >>> a = {'Alice': ['hi', '29'], 'Age' : ['bye', '30']}
    >>> how = 'Alice>bye'
    >>> x = Table(None, 'a', a)
    >>> x = constraint(how, x)
    >>> x = x.get_dict()
    >>> z = {'Alice':['hi'], 'Age': ['bye']}
    >>> z.__eq__(x)
    True
    >>> a = {'Alice': ['hi', '29'], 'Age' : ['bye', '30']}
    >>> how = 'Alice<g'
    >>> x = Table(None, 'a', a)
    >>> x = constraint(how, x)
    >>> x = x.get_dict()
    >>> z = {'Alice':[], 'Age': []}
    >>> z.__eq__(x)
    True
    '''
    # this is to find the how the values wil be compared
    # get the index
    if equal in constraint:
        relationship = constraint.index(equal)
    elif greater_than in constraint:
        relationship = constraint.index(greater_than)
    elif smaller_than in constraint:
        relationship = constraint.index(smaller_than)
    # get the comparison
    how = constraint[relationship]
    # get column_name1
    column_name1 = constraint[:relationship]
    # get the value/ column_name2
    comparison = constraint[relationship + 1:]
    comparison = comparison.lstrip()
    # check if the comparison is a value or a column title
    if comparison in table.keys():
        # compare the columns
        list_of_index = table.compare_columns(column_name1, comparison, how)
    else:
        # compare column1 to the comparison(val)
        list_of_index = table.compare_to_val(column_name1, comparison, how)
    # go each key in the tables
    for each_column in table.keys():
        # use method delete val
        table.del_val_in_column(each_column, list_of_index)
    return table


if(__name__ == "__main__"):
    query = input("Enter a SQuEaL query, or a blank line to exit:")
    query = "select * from books,olympics-locations,seinfeld-episodes \
    where book.author='Randall Munroe',l.country='France',e.season=0,\
    book.year=2014,l.year=1992,e.food='Salad Dressing'"
    # query = 'select * from books,olympics-locations'
    # get the database in the cu
    rrent directory
    # query = 'select * from books,olympics-locations,seinfeld-episodes \
    # where book.author=Randall Munroe,l.country=France,e.season=0,\
    # book.year>l.year,e.food=Salad Dressing'
    database = read_database()
    # use run_query to follow the command
    if query == '':
        pass
    else:
        query_table = run_query(database, query)
        # use the print_csv to print the table
        print_csv(query_table)
