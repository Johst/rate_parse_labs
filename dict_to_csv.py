
# to file
import json, csv

# advanced dict
mydict = {'Apples':5, 'Pears':6, 'Blueberries':8}
dictCars = {'Audi':
            {
            'speed':70,
            'color':2
            },
        'BMW':
            {
            'speed':60,
            'color':3
            }
        }

     
# print style 1
for x in dictCars:
    print (x)
    for y in dictCars[x]:
        print (y,':',dictCars[x][y])

# print for csv output (manual file creation)
for x in dictCars:
    string = str(x) + ","
    for y in dictCars[x]:
        string = string + str(dictCars[x][y]) + ","
    string = string[:-1] # remove the last comma of row
    print(string)       


# write something to file
path = 'dict_to_csv.csv'
header="Model,Speed,Color" + "\n"
writer = open(path,'a')   
writer.write(header) 
for x in dictCars:
    string = str(x) + ","
    for y in dictCars[x]:
        string = string + str(dictCars[x][y]) + ","
    string = string[:-1] # remove the last comma of row
    writer.write(string + "\n")               
        