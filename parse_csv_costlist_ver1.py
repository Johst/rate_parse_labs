## This script opens and MS Excel or CSV file and moves grouped MNC's into one row each.
#  C:/Users/johastje/AppData/Local/Programs/Python/Python36/python.exe C:\Users\johastje\Desktop\PythonPlay\Costlists\parse_costlist_ver1.py

import csv
# filename = 'vanilla_costlist.csv'
filename = 'C:\\Users\\johastje\\Desktop\\PythonPlay\\Costlists\\csv_files\\vanilla_costlist_short.csv'

try:
    with open(filename) as f:
        reader = csv.reader(f)
        my_list = list(reader)  
        # header_row = next(reader) #process first line and store in a list

    # or more advanced where enumerate will get index of each item as well as the value
    # for index, column_header in enumerate(header_row):
    # print(index, column_header)

    # print the compelete list
    print('Print compelete list:\n', my_list, '\n')

    # how many rows in file
    a=len(my_list)
    print('Rows in file:', a, '\n')

    # how many elements in a row
    b=len(my_list[1])
    print('Elements in row:', b, '\n')

    # print first two rows
    print('First two rows:')
    print(my_list[0]) # header row
    print(my_list[1], '\n') # second row, forst data row


    # print each item in a row
    print('Print each item in row:')
    for item in my_list[1]:
        print(item)
    #print(my_list[1][0]) # first field in first data row (second row)
    #print(my_list[1][1]) # second field in first data row (second row)
    #print(my_list[1][2])
    #print(my_list[1][3])
except Exception as e: print('An error occured: ', e)
