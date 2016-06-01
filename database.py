# Global variables
equal = '='
greater_than = '>'
smaller_than = '<'
dot = '.'
comma = ','
next_line_symbol = '\n'
file_extensions = '.csv'
star_sign = '*'


class Table():
    '''A class to represent a SQuEaL table'''
    def __init__(self, file_name=None, title=None, my_dict=None):
        '''(Table, str, str, dict of {str: list of str}) -> NoneType
        This method will run automatically. It is used to set up the class
        Table, and its important title, and table info.
        REQ: none
        '''
        # set up the properties of a table: title and table itself
        if file_name is None:
            if (title is None) and (my_dict is None):
                self._table = {}
                self._title = ''
            else:
                self._table = my_dict
                self._title = title
        else:
            self.read_file(file_name)

    def get_title(self):
        '''(Table) -> str
        This method is used to return the title of the table.
        REQ: none
        '''
        return self._title

    def read_file(self, file_name):
        '''(Table, str) -> NoneType
        Takes in the file_name. Reads the .csv file. Put the values and
        organize it into a table. in the table, it is saved in a dictionary
        with the column names as the key, which point to the values which
        are stored in a list.
        REQ: file_name must exist, and be in the same directory
        REQ: file_name must be in .csv format
        '''
        # Open the file
        file_open = open(file_name, 'r')
        # Create a list, read the first line(the keys)
        first_line = file_open.readline()
        # clean the line, so there is only words left
        first_line = clean(first_line)
        # create a dict
        my_dict = {}
        # loop each line to get the data
        for eachline_left in file_open:
            # Check if line is empty after stripping whitespace
            if (eachline_left.lstrip() != ''):
                eachline_left = clean(eachline_left)
                # add a new count
                count = 0
                # loop, get the word at each index, and add it
                # to the correct list in the list_of_key
                while count < len(first_line):
                    word = eachline_left[count]
                    get_key = first_line[count]
                    # check if key in dict
                    if get_key in my_dict.keys():
                        # append if key in dict
                        my_dict[get_key].append(word)
                    else:
                        # create the key
                        my_dict[get_key] = [word]
                    count += 1
        # Get the correct title
        # strip the '.csv', take away last 4 char
        file_name = file_name[:len(file_name) - 4]
        self._title = file_name
        self._table = my_dict
        file_open.close()

    def set_dict(self, new_dict):
        '''(Table, dict of {str: list of str}) -> NoneType

        Populate this table with the data in new_dict.
        The input dictionary must be of the form:
            column_name: list_of_values
        REQ: none
        '''
        # already with column_name: list_of_values
        # give it a self._table
        self._table = new_dict

    def get_dict(self):
        '''(Table) -> dict of {str: list of str}
        Return the dictionary representation of this table. The dictionary keys
        will be the column names, and the list will contain the values
        for that column.
        '''
        # Use set_dict, and return the new_dict
        return self._table

    def add_column(self, title, list_of_value):
        '''(Table, str, list of str}) -> NoneType
        This method is used to add a new column with it data to the dictionary.
        REQ: title is the column_name
        REQ: list_of_value is the column's value
        '''
        self._table[title] = list_of_value

    def add_many_columns(self, my_dict):
        '''(Table, Dict {str: list of str}) -> NoneType
        This method is used to add many columns stored in a dictionary.
        REQ: dict in  format of title: column's value
        '''
        for each_title in my_dict:
            self._table[each_title] = my_dict[each_title]

    def get_column(self, column_name):
        '''(Table, str) ->  list of str
        This function is to get the list of values stored in the dictionary
        to get the list_of_values stored in the key of the dictionary.
        '''
        # Use column_name, go through the dict
        # Find the key
        # Return the list_of_values in the key
        if column_name in self._table:
            result = self._table[column_name]
        else:
            result = "NOT IN THE TABLE"
        return result

    def get_multiple_column(self, list_of_column_names):
        '''(Table, list of str/ *) -> Table
        This method is to loop through the table and get the columns
        REQ: column_name should be a key inside the table
        '''
        # Initialize a new table
        new_table = Table()
        # Loop through each column_name in list
        for column_name in list_of_column_names:
            # get the values with method get_column
            list_of_val = self.get_column(column_name)
            # add the values into the table
            new_table.add_column(column_name, list_of_val)
        return new_table

    def num_of_rows(self):
        '''(Table) -> int
        This method is to return the num of entries inside the keys.
        (This method also returns the length of the longest column)
        REQ: none
        '''
        length = 0
        for key in self._table:
            if length < len(self._table[key]):
                length = len(self._table[key])
        return length

    def repeat_values(self, num):
        '''(Table, int) -> Table
        This method repeats each value by that num.
        REQ:none
        '''
        # loop around each column in table
        for each_key in self._table:
            # get the values in that column
            entries = self._table[each_key]
            # initialize the list to get the data
            new_data = []
            # loop through each value in entry
            for each_entry in entries:
                # initialize count of # of values in num
                count = 0
                # loop through till count = # of values in num
                while count < num:
                    # append each entry
                    # this allows entry to be repeated for
                    # as many values in num
                    new_data.append(each_entry)
                    count += 1
            self._table[each_key] = new_data
        return self._table

    def repeat_all_at_once(self, num):
        '''(Table, int) -> Table
        This method is used to repeat all the values at once for a certain
        numver of times.
        REQ: none
        '''
        for each_key in self._table:
            # get the values in table
            entries = self._table[each_key]
            # initialize the list to get data
            new_data = []
            # initialize the count of # of values
            count = 0
            # loop through till count = # of values
            # this loop is in charge of repeating the
            # values in table all at once
            # by the num of values in t1
            while count < num:
                # go through each value in the column
                for each_entry in entries:
                    # append the all the values
                    new_data.append(each_entry)
                # add a count
                count += 1
            # add the new entry to new_dict
            self._table[each_key] = new_data
        return self._table

    def compare_columns(self, column_name1, column_name2, how):
        '''(Table, str, str,str) -> list of int
        This method is used to compare the values inside column_name1 and
        column_name2. Since the values are stored in a list, it will return
        a list of indexes where the values are equal.
        REQ: column_name1 and column_name2 in table
        '''
        # Get the vlaues in both columns
        column1 = self.get_column(column_name1)
        column2 = self.get_column(column_name2)
        # Initialize the list_of_indexes where columns' value
        # are compared and is True
        list_of_values = []
        # Initialize the count which represents the index
        count = 0
        # loop through the length of column 1
        # (len(column1) should be eqaul len(column2))
        while count < len(column1):
            # get the val from each column at the index(count)
            column1_val = column1[count]
            column2_val = column2[count]
            # use convert_to_float to make int/float into floats
            column1_val = convert_to_float(column1_val)
            column2_val = convert_to_float(column2_val)
            # only compare the values if both values are the same type
            # all int val are already made into float
            if type(column1_val) == type(column2_val):
                # add to the list_of_values only when
                # it passes the comparison
                if compare_value(column1_val, column2_val, how):
                        list_of_values.append(count)
            # add one to the index
            count += 1
        return list_of_values

    def compare_to_val(self, column_name1, val, how):
        '''(Table, str, obj, str) -> list of int
        This method is used to compare
        '''
        # get the list of value in the column
        column1 = self.get_column(column_name1)
        # initialize the list to keep track of indexes
        list_of_values = []
        # initialize the index count
        count = 0
        # check the type of value, if str, see if it can be converted
        if type(val) == str:
            val = convert_to_float(val)
        # check if it is a int, if it is, change to float
        elif type(val) == int:
            val = float(val)
        # go through each value in column
        for each_entry in column1:
            # convert to float if possible
            each_entry = convert_to_float(each_entry)
            # only compare if they are of the same type
            if type(each_entry) == type(val):
                # use compare values to compare
                if compare_value(each_entry, val, how):
                    list_of_values.append(count)
            # increase the index
            count += 1
        return list_of_values

    def del_val_in_column(self, column_name, list_of_int):
        '''(Table, str, list of int) -> NoneType
        This method is to delete the extra values in a column.
        This means given an list of indexes, it will only return with values
        from that index.
        '''
        # copy this list_of_index
        list_of_index = list_of_int[:]
        # get the column you want to change
        column = self.get_column(column_name)
        # initialize a new column (list)
        new_column = []
        # Go through this list_of_index
        for each_val in list_of_index:
            # take the value out of the column and save this value
            value = column.pop(each_val)
            # append this value to the new_column
            new_column.append(value)
            # get the length of the index
            list_len = len(list_of_index)
            # initialize the count(index)
            count = 0
            # go through the list_len
            while count < list_len:
                # go the index, and decrease by one
                # this is because to ensure you continue to remove the right
                # value, since popping one, the index is decreased by one
                list_of_index[count] -= 1
                count += 1
        # return the new value to the table
        self._table[column_name] = new_column
        return None

    def keys(self):
        '''(Table) -> list
        This method is used to return the keys in the Table.
        '''
        self._keys = self._table.keys()
        return self._keys


class Database():
    '''A class to represent a SQuEaL database'''

    def __init__(self, list_of_files=None):
        '''(Database) -> NoneType
        This method will run automatically. This is to set up the class
        Database. In a database, the only thing that is useful is its data.
        REQ: none
        '''
        self._database = {}
        if list_of_files is not None:
            self.read_files(list_of_files)

    def read_files(self, list_of_files):
        '''() -> Database
        This function is to first read all the .csv files in the directory.
        Second, after converting the .csv files into tables, add them to the
        Database.
        '''
        # Run each file through read_table
        for each_file in list_of_files:
            # Add them to Database
            table = Table(each_file)
            self.add_table(table)

    def set_dict(self, new_dict):
        '''(Database, dict of {str: Table}) -> NoneType
        Populate this database with the data in new_dict.
        new_dict must have the format:
            table_name: table
        '''
        # give new database table_name
        self._database = new_dict

    def get_dict(self):
        '''(Database) -> dict of {str: Table}
        Return the dictionary representation of this database.
        The database keys will be the name of the table, and the value
        with be the table itself.
        '''
        return self._database

    def add_table(self, table):
        '''(Database, Table) -> NoneType
        This method is used to add tables into the database.
        '''
        self._database[table.get_title()] = table
        return

    def get_table(self, table_name):
        '''(Database) -> Table
        Return the dictionary representation of this database.
        The database keys will be the name of the table, and the value
        with be the table itself.
        '''
        # Return a Table Object, given the Table's name
        return self._database[table_name]

    def add_table_together(self, table1, table2):
        '''(Database, Table, Table) -> Table
        Return a new table, through adding the columns is each table.
        REQ:
        '''
        # get the num of rows in the table
        rows_in_t1 = table1.num_of_rows()
        rows_in_t2 = table2.num_of_rows()
        # repeat the values for table1
        table1 = table1.repeat_values(rows_in_t2)
        # add them to new_table
        new_table = Table(None, 'cartesian product', table1)
        # repeat value all at once for table2
        my_dict = table2.repeat_all_at_once(rows_in_t1)
        # add this to the new_table
        new_table.add_many_columns(my_dict)
        return new_table


def convert_to_float(number):
    '''(str) -> float / str
    This function checks if a str can be changed to a float.
    REQ: None
    >>> convert_to_float('1')
    1.0
    >>> convert_to_float('1.0')
    1.0
    >>> convert_to_float('abc')
    'abc'
    >>> convert_to_float('ab.cd')
    'ab.cd'
    >>> convert_to_float('ab12')
    'ab12'
    >>> convert_to_float('ab.12')
    'ab.12'
    >>> convert_to_float('')
    ''
    '''
    # initial condition is false
    condition = False
    # check if it is float
    # if u can't find '.', it find will return it to -1
    if number.find(dot) != -1:
        # find where it is
        index = number.index(dot)
        # get the leftside of the str
        leftside = number[:index]
        # get the rightside of the str
        rightside = number[index + 1:]
        # check if left is all numbers
        left = leftside.isnumeric()
        # check if right is all numbers
        right = rightside.isnumeric()
        # combined condition
        # (float is where all its numbers with a decimal point)
        condition = left and right
    # check if it has "'"
    if "'" in number:
        num_index = len(number)
        result = number[1:num_index-1]
    # check if this number is only alphabets
    elif number.isalpha():
        # if only only alphabets, give str
        result = number
    # check if this number is actually a number (an int)
    elif number.isnumeric():
        # change it to float
        result = float(number)
    # check if this number can become a float
    elif condition:
        # change it to become a float
        result = float(number)
    # if it is str with other symbols
    else:
        # return it as it is
        result = number
    return result


def compare_value(val1, val2, how):
    '''(obj, obj, str) -> bool
    This function is when given how val1 or val2 is compared, it will return
    True if the comparison is true.
    REQ: type(val1) = type(val2)
    REQ: type(val1) != dict and type(val2) != dict
    REQ: type(val1) != set  and type(val2) != set
    >>> compare_value(1, 2, '=')
    False
    >>> compare_value(1, 2, '>')
    False
    >>> compare_value(1, 2, '<')
    True
    >>> compare_value('a', 'b', '=')
    False
    >>> compare_value('b', 'a', '<')
    False
    >>> compare_value('b', 'a', '>')
    True
    >>> compare_value(1.0, 2.0, '=')
    False
    >>> compare_value(1.0, 2.0, '>')
    False
    >>> compare_value(1.0, 2.0, '<')
    True
    >>> compare_value([1,2], [2,3], '=')
    False
    >>> compare_value([1,2], [2,3], '>')
    False
    >>> compare_value([1,2], [2,3], '<')
    True
    >>> compare_value([1,2], [2,1], '=')
    False
    >>> compare_value([1,2], [2,1], '>')
    False
    >>> compare_value([1,2], [2,1], '<')
    True
    '''
    # set it as false first, the comparison given is not found
    result = False
    # find the comparison
    if how == equal:
        # check if val1 is equal to val2
        if val1 == val2:
            result = True
    elif how == greater_than:
        # check if val1 is greater than val2
        if val1 > val2:
            result = True
    elif how == smaller_than:
        # check if val1 is less than val2
        if val1 < val2:
            result = True
    return result


def clean(message):
    '''(str) -> list
    This function is supposed to take a message
    clean it by splitting each word by its comma, then strip the \n.
    REQ:
    >>> clean('happy, sad, row')
    ['happy', 'sad', 'row']
    >>> clean('happy,')
    ['happy', '']
    >>> clean('happy, sad, row\n')
    ['happy', 'sad', 'row']
    >>> clean('happy,sad,row\n')
    ['happy', 'sad', row']
    >>> clean('')
    ['']
    >>> clean(',,')
    ['','', '']
    '''
    # first take away the '\n'
    message = message.rstrip(next_line_symbol)
    # Find how many ',' there are
    num_of_comma = message.count(comma)
    # create list
    new_list = []
    # loop through each time there is a comma
    for each_comma in range(num_of_comma):
        # find the index of the coma
        index_comma = message.index(comma)
        # slice the message to get the word
        word = message[:index_comma]
        # erase that word from the message
        message = message[index_comma + 1:]
        # add that word to the new_list
        new_list.append(word)
        # clean any spaces in the front
        message = message.lstrip()
    # Add the final word to the list
    new_list.append(message)
    return new_list
