# Code for working with word search puzzles
#
# Do not modify the existing code
#
# Complete the tasks below marked by *task*
#
# Before submission, you must complete the following header:
#
# I hear-by decree that all work contained in this file is solely my own
# and that I received no help in the creation of this code.
# I have read and understood the University of Toronto academic code of
# behaviour with regards to plagiarism, and the seriousness of the
# penalties that could be levied as a result of committing plagiarism
# on an assignment.
#
# Name: Yang Chin Chen
# MarkUs Login: yangch66
#

PUZZLE1 = '''
glkutqyu
onnkjoaq
uaacdcne
gidiaayu
urznnpaf
ebnnairb
xkybnick
ujvaynak
'''

PUZZLE2 = '''
fgbkizpyjohwsunxqafy
hvanyacknssdlmziwjom
xcvfhsrriasdvexlgrng
lcimqnyichwkmizfujqm
ctsersavkaynxvumoaoe
ciuridromuzojjefsnzw
bmjtuuwgxsdfrrdaiaan
fwrtqtuzoxykwekbtdyb
wmyzglfolqmvafehktdz
shyotiutuvpictelmyvb
vrhvysciipnqbznvxyvy
zsmolxwxnvankucofmph
txqwkcinaedahkyilpct
zlqikfoiijmibhsceohd
enkpqldarperngfavqxd
jqbbcgtnbgqbirifkcin
kfqroocutrhucajtasam
ploibcvsropzkoduuznx
kkkalaubpyikbinxtsyb
vjenqpjwccaupjqhdoaw
'''


def rotate_puzzle(puzzle):
    '''(str) -> str
    Return the puzzle rotated 90 degrees to the left.
    '''

    raw_rows = puzzle.split('\n')
    rows = []
    # if blank lines or trailing spaces are present, remove them
    for row in raw_rows:
        row = row.strip()
        if row:
            rows.append(row)

    # calculate number of rows and columns in original puzzle
    num_rows = len(rows)
    num_cols = len(rows[0])

    # an empty row in the rotated puzzle
    empty_row = [''] * num_rows

    # create blank puzzle to store the rotation
    rotated = []
    for row in range(num_cols):
        rotated.append(empty_row[:])
    for x in range(num_rows):
        for y in range(num_cols):
            rotated[y][x] = rows[x][num_cols - y - 1]

    # construct new rows from the lists of rotated
    new_rows = []
    for rotated_row in rotated:
        new_rows.append(''.join(rotated_row))

    rotated_puzzle = '\n'.join(new_rows)

    return rotated_puzzle


def lr_occurrences(puzzle, word):
    '''(str, str) -> int
    Return the number of times word is found in puzzle in the
    left-to-right direction only.

    >>> lr_occurrences('xaxy\nyaaa', 'xy')
    1
    '''
    return puzzle.count(word)

# ---------- Your code to be added below ----------

# *task* 3: write the code for the following function.
# We have given you the header, type contract, example, and description.


def total_occurrences(puzzle, word):
    '''(str, str) -> int
    Return total occurrences of word in puzzle.
    All four directions are counted as occurrences:
    left-to-right, top-to-bottom, right-to-left, and bottom-to-top.

    >>> total_occurrences('xaxy\nyaaa', 'xy')
    2
    '''
    # your code here
    puzzle_count = 0
    # count left-to-right occurrences
    puzzle_count += lr_occurrences(puzzle, word)
    puzzle = rotate_puzzle(puzzle)
    # count top-to-bottom occurrences
    puzzle_count += lr_occurrences(puzzle, word)
    puzzle = rotate_puzzle(puzzle)
    # count right-to-left occurrences
    puzzle_count += lr_occurrences(puzzle, word)
    puzzle = rotate_puzzle(puzzle)
    # count bottom-to-top occurrences
    puzzle_count += lr_occurrences(puzzle, word)
    return puzzle_count

# *task* 5: write the code for the following function.
# We have given you the function name only.
# You must follow the design recipe and complete all parts of it.
# Check the handout for what the function should do.


def in_puzzle_horizontal(puzzle, word):
    '''(str,str) -> bool
    Return True if you can find word in the puzzle either left-to-right or
    right-to-left.
    REQ: none
    >>> in_puzzle_horizontal(PUZZLE1, 'brian')
    True
    >>> in_puzzle_horizontal(PUZZLE1, 'nick')
    True
    >>> in_puzzle_horizontal(PUZZLE1, 'apple')
    False
    '''
    # count= 0 at first
    puzzle_count = 0
    # count from left-to-right
    puzzle_count += lr_occurrences(puzzle, word)
    # count from right-to-left
    puzzle = rotate_puzzle(puzzle)
    puzzle = rotate_puzzle(puzzle)
    puzzle_count += lr_occurrences(puzzle, word)
    # True iff puzzle_count>0
    return (puzzle_count > 0)

# *task* 8: write the code for the following function.
# We have given you the function name only.
# You must follow the design recipe and complete all parts of it.
# Check the handout for what the function should do.


def in_puzzle_vertical(puzzle, word):
    '''(str,str) -> bool
    Return True if you can find word in the puzzle either top-to-bottom or
    bottom-to-top.
    REQ: none
    >>> in_puzzle_vertical(PUZZLE1, 'brian')
    True
    >>> in_puzzle_vertical(PUZZLE1, 'nick')
    True
    >>> in_puzzle_vertical(PUZZLE1, 'apple')
    False
    '''
    # give variable for count, count = 0
    puzzle_count = 0
    # count how many for top-to-bottom
    puzzle = rotate_puzzle(puzzle)
    puzzle_count += lr_occurrences(puzzle, word)
    # count how many for bottom-to-top
    puzzle = rotate_puzzle(puzzle)
    puzzle = rotate_puzzle(puzzle)
    puzzle_count += lr_occurrences(puzzle, word)
    # Return True iff count > 0
    return (puzzle_count > 0)

# *task* 9: write the code for the following function.
# We have given you the function name only.
# You must follow the design recipe and complete all parts of it.
# Check the handout for what the function should do.


def in_puzzle(puzzle, word):
    '''(str,str) -> bool
    Return True if word can be found anywhere in puzzle. This can also means
    return true when word can be found horizontally or vertically.
    REQ: none
    >>> in_puzzle(PUZZLE1, 'brian')
    True
    >>> in_puzzle(PUZZLE1, 'nick')
    True
    >>> in_puzzle(PUZZLE1, 'apple')
    False
    >>> in_puzzle(PUZZLE1, 'go')
    True
    '''
    # Call function in_puzzle_horizontal and in_puzzle_vertical
    # Only one has to be true to return true
    Case_1 = in_puzzle_horizontal(puzzle, word)
    Case_2 = in_puzzle_vertical(puzzle, word)
    return (Case_1 or Case_2)


# *task* 10: write the code for the following function.
# We have given you only the function name and parameters.
# You must follow the design recipe and complete all parts of it.
# Check the handout for what the function should do.


def in_exactly_one_dimension(puzzle, word):
    ''' (str,str) -> bool
    Return True iff word can be found horzontally and not vertically or
    vertically and not horizontally
    REQ: none
    >>> in_exactly_one_dimension(PUZZLE1, 'brian')
    False
    >>> in_exactly_one_dimension(PUZZLE1, 'nick')
    False
    >>> in_exactly_one_dimension(PUZZLE1, 'go')
    True
    >>> in_exactly_one_dimension(PUZZLE1, 'apple')
    True
    >>> in_exactly_one_dimension(PUZZLE1, 'kanyavju')
    True
    '''
    # Check case1: where it is true if word is found only horizontally
    Case1 = in_puzzle_horizontal(puzzle, word)
    Case2 = not (in_puzzle_vertical(puzzle, word))
    # Check case3: where it is true if word is found only vertically
    Case3 = in_puzzle_vertical(puzzle, word)
    Case4 = not (in_puzzle_horizontal(puzzle, word))
    # Check case5 where it is true if word is not found at all
    Case5 = not(in_puzzle(puzzle, word))
    return ((Case1 and Case2) or (Case3 and Case4) or Case5)

# *task* 11: write the code for the following function.
# We have given you only the function name and parameters.
# You must follow the design recipe and complete all parts of it.
# Check the handout for what the function should do.


def all_horizontal(puzzle, word):
    ''' (str,str) -> bool
    Return True iff word can only found horizontal in the puzzle
    REQ: none
    >>> all_horizontal(PUZZLE1, 'brian')
    False
    >>> all_horizontal(PUZZLE1, 'nick')
    False
    >>> all_horizontal(PUZZLE1, 'go')
    False
    >>> all_horizontal(PUZZLE1, 'apple')
    True
    >>> all_horizontal(PUZZLE1, 'kanyavhy')
    True
    '''
    # Return True iff only horizontal or doesn't exist
    # Case 1: only horizontal
    Case_1 = (in_exactly_one_dimension(puzzle, word))
    # Case 2: in one dimension
    Case_2 = (in_puzzle_horizontal(puzzle, word))
    # Case 3: doesn't exist
    Case_3 = (not(in_puzzle(puzzle, word)))
    return (Case_1 and Case_2) or (Case_3)

# *task* 12: write the code for the following function.
# We have given you only the function name and parameters.
# You must follow the design recipe and complete all parts of it.
# Check the handout for what the function should do.


def at_most_one_vertical(puzzle, word):
    '''(str,str) -> bool
    Return True when word occurs once and when it occurs vertical.
    REQ: none
    >>> at_most_one_vertical(PUZZLE1, 'brian')
    False
    >>> at_most_one_vertical(PUZZLE1, 'nick')
    False
    >>> at_most_one_vertical(PUZZLE1, 'goug')
    True
    >>> at_most_one_vertical(PUZZLE1, 'apple')
    False
    >>> at_most_one_vertical(PUZZLE1, 'kanyahy')
    False
    '''
    # Case1: True only when word occurs at most once
    Case_1 = (total_occurrences(puzzle, word) <= 1)
    # Case2: True when it is only vertical
    Case_2 = not(all_horizontal(puzzle, word))
    return (Case_1 and Case_2)


def do_tasks(puzzle, name):
    '''(str, str) -> NoneType
    puzzle is a word search puzzle and name is a word.
    Carry out the tasks specified here and in the handout.
    '''

    # *task* 1a: add a print call below the existing one to print
    # the number of times that name occurs in the puzzle left-to-right.
    # Hint: one of the two starter functions defined above will be useful.

    # the end='' just means "Don't start a newline, the next thing
    # that's printed should be on the same line as this text
    print('Number of times', name, 'occurs left-to-right: ', end='')
    # your print call here
    print(lr_occurrences(puzzle, name))

    # *task* 1b: add code that prints the number of times
    # that name occurs in the puzzle top-to-bottom.
    # (your format for all printing should be similar to
    # the print statements above)
    # Hint: both starter functions are going to be useful this time!
    puzzle = rotate_puzzle(puzzle)
    print('Number of times', name, 'occurs top-to-bottom: ', end='')
    print(lr_occurrences(puzzle, name))

    # *task* 1c: add code that prints the number of times
    # that name occurs in the puzzle right-to-left.
    puzzle = rotate_puzzle(puzzle)
    print('Number of times', name, 'occurs right-to-left: ', end='')
    print(lr_occurrences(puzzle, name))

    # *task* 1d: add code that prints the number of times
    # that name occurs in the puzzle bottom-to-top.
    puzzle = rotate_puzzle(puzzle)
    print('Number of times', name, 'occurs bottom-to-down: ', end='')
    print(lr_occurrences(puzzle, name))

    # *task* 4: print the results of calling total_occurrences on
    # puzzle and name.
    # Add only one line below.
    # Your code should print a single number, nothing else.
    print(total_occurrences(puzzle, name))

    # *task* 6: print the results of calling in_puzzle_horizontal on
    # puzzle and name.
    # Add only one line below. The code should print only True or False.
    print(in_puzzle_horizontal(puzzle, name))

do_tasks(PUZZLE1, 'brian')

# *task* 2: call do_tasks on PUZZLE1 and 'nick'.
# Your code should work on 'nick' with no other changes made.
# If it doesn't work, check your code in do_tasks.
# Hint: you shouldn't be using 'brian' anywhere in do_tasks.
do_tasks(PUZZLE1, 'nick')

# *task* 7: call do_tasks on PUZZLE2 (that's a 2!) and 'nick'.
# Your code should work on the bigger puzzle with no changes made to do_tasks.
# If it doesn't work properly, go over your code carefully and fix it.
do_tasks(PUZZLE2, 'nick')

# *task* 9b: print the results of calling in_puzzle on PUZZLE1 and 'nick'.
# Add only one line below. Your code should print only True or False.
print(in_puzzle(PUZZLE1, 'nick'))

# *task* 9c: print the results of calling in_puzzle on PUZZLE2 and 'anya'.
# Add only one line below. Your code should print only True or False.
print(in_puzzle(PUZZLE2, 'anya'))
