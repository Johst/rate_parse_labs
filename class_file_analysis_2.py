# Analysis of Cost files
# C:/Users/johastje/AppData/Local/Programs/Python/Python36/python.exe C:\Users\johastje\Desktop\PythonPlay\Costlists\class_file_analysis_2.py



class File_analysis():
    """Methods to analyze A2P supplier's rate decks"""
    
    def __init__(self):
        """Initialize name and age attributes."""
        
    def count_rows(self, filename):
        """Count number of rows in file"""

        num_rows_infile = num
        print("Number of rows in file: ", num_rows_infile)

    def header_rownum(self, filename):
        """Find which row number that is the header row."""
        header_rownum = 1
        print("The header row is at row number: ", str(header_rownum) + " " + mymsg)

    def header_show(self, filename):
        """Find header row and print it"""
        with open (filename) as f:
            reader = csv.reader(f)
            header_row = next(reader)
            print("This is the header row: ", header_row)          

    def header_index(self, filename):
        """Print headers and their positions in file"""
        with open (filename) as f:
            reader = csv.reader(f)
            header_row = next(reader)
           
            for index, column_header in enumerate(header_row):
                print(index, column_header)

    def get_column_data(self, filename, index):
        """Extract and read data from a index/column"""
        with open (filename) as f:
            reader = csv.reader(f)
            header_row = next(reader) # moves cursoer to first data row

            data = [] # list to add the data of the column index in
           
            # Loop through remaining rows after header
            for row in reader:
                data.append(row[index])  

            print(data)            
    
    def get_column_data_float(self, filename, index):
        """Extract and read data from a index/column with floats"""
        # Use this method when yo need to calaculate or plot data
        with open (filename) as f:
            reader = csv.reader(f)
            header_row = next(reader)

            data = []
           
            # Loop through remaining rows after header
            for row in reader:
                data_int = float(row[index])
                data.append(data_int)  

            print(data)  

    def find_in_file(self, filename, word):
        """Check if a word or value exist in file"""
        
        with open (filename) as f:
            reader = csv.reader(f)

            word_exist = False
            row_num = 0
           
            # Loop through remaining rows after header
            for row in reader:
                if word_exist: break
                row_num = row_num + 1
                for element in row:
                    if element.lower() == word.lower():
                        word_exist = True

            if word_exist:
                print("The word", word, "was found in file on row", row_num) 

            else:
                print("The word" , word,  "was not found in file.")          

    def find_header_row(self, filename):
        """Find the header row number"""
        
        with open (filename) as f:
            reader = csv.reader(f)

            word1 = 'mcc'
            word2 = 'price'
            word3 = 'rate'
            word_exist = False
            row_num = 0
           
            # Loop through remaining rows after header
            for row in reader:
                if word_exist: break
                row_num = row_num + 1
                for element in row:
                    if element.lower() == word1.lower() or \
                       element.lower() == word2.lower() or \
                       element.lower() == word3.lower() :
                        word_exist = True
        
            print(str(row_num))                

    def find_indexs(self, filename):
        """Find index for mcc, mnc, cost"""
        
        with open (filename) as f:
            reader = csv.reader(f)
            header_row = next(reader)
        
        # convert all to lower case
        header_row = [item.lower() for item in header_row]  
        mccmnc = False
        try:
            str1 = 'MCC'
            str2 = 'mnc'
            str3 = 'rate'
       
            print ("Index for mcc : ", header_row.index(str1.lower()))
            print ("Index for mnc : ", header_row.index(str2.lower()))
            print ("Index for cost : ", header_row.index(str3.lower()))
        except ValueError:
            for item in header_row:
                if item.lower() == 'mccmnc':
                   mccmnc = True
                
            if mccmnc:
                print("MCCMNC concat was found!")
            else:
                print("One or more of the keys not found in file!")
    
    def multipleMNC(self, filename):
        """Moves multiple MNC to one row each. Takes the filename as argument and a new file as output"""
        
        # open source file
        with open (filename) as f:
            reader = csv.reader(f)
            header_row = next(reader)
            # convert all to lower case
            header_row = [item.lower() for item in header_row]  
        
            try:
                strMNC = 'mnc'
                # call def to find mnc column index
                strMNC_column = header_row.index(strMNC.lower())
                print ("Columun index for MNC in input file is: ", strMNC_column)

            except ValueError:
                for item in header_row:
                    if item.lower() != 'strMNC':
                       print('No MNC column was found')
                       break    

            # open a destination file for writing

            # loop through each row in source file

            # separator = ';'
            separator = input('Enter MNC separator type, for example a semicolon or space: ')
            outfile = 'C:\\Users\\johastje\\Desktop\\PythonPlay\\Costlists\\csv_files\\cleanMNC.csv'
            
            # Open destination file
            fo = open(outfile, 'a', newline='')
            writer = csv.writer(fo)
            writer.writerow(header_row)

            for row in reader:
                if separator in row[strMNC_column]:
                    arrMNCs =[]
                    arrMNCs.append(row[strMNC_column].split(separator))
                    # loop through all the mnc's
                    for arrMNC in arrMNCs:
                         #print(arrMNC) # ['07', '05']
                         #print(row) # ['240', '07;05', '0.06', 'Alpha']
                         #print(row[1]) # 07;05
                         #print(arrMNC[0]) # 07
                         #print(arrMNC[1]) # 05
                         for element in arrMNC:
                             row[1] = element
                             print(row)
                             writer.writerow(row)
            
                else:
                    print(row) 
                    writer.writerow(row)            
                         

# Main program
import csv

# filename = 'costlist_test_semic.csv'
# filename = 'costlist_test_short.csv'
filename = 'C:\\Users\\johastje\\Desktop\\PythonPlay\\Costlists\\csv_files\\vanilla_costlist_short.csv'
# filename = 'costlist_mccmnc.csv'

# Instance the class
my_analysis = File_analysis()

# my_analysis.count_rows(15)   
# my_analysis.header_rownum("hello")
# my_analysis.header_show(filename)
# my_analysis.header_index(filename)
# my_analysis.get_column_data(filename, 2)
# my_analysis.get_column_data_float(filename, 2)
# my_analysis.find_in_file(filename, 'Mnc')
# my_analysis.find_header_row(filename)
# my_analysis.find_indexs(filename)
my_analysis.multipleMNC(filename)

# 1. Find header row
# 2. Go to header row (next * head row num) Enumerate to find column indexes
# 3. Find the col index for mcc, mnc, cost, if mccmnc split if first, and write to lists
# 4. Write lists to a CSV file (potentially a json with effective date and account name) 


    
