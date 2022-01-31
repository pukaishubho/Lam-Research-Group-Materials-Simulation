import re

# whick key to search for in the file
search_keys = ['total pressure']
data_list = []
data_list2 = ['total pressure']

# open the file in which key is to be searched
outcar = open('/project/uml_stephen_lam/Rajni/Molten_salts/LiFNaFZr4/26-37-37/700C/Vol2x/OUTCAR','r')
for line in outcar:
    line = line.rstrip()
    # number of lines in the file
    ln = range(0, len(line), 1)
    #print(len(line))
    for key_index in range(len(search_keys)):
        # browse for 'search_keys' in every line of the file
        if re.search(search_keys[key_index], line):
	    # store the lines containing 'search_keys' in a list named data_list
            data_list.append([[]] * len(search_keys))
	    # select the value of interest, here Temperature (T)
            data_list[0][0] = line.split('kB')[key_index].split('=')[1]
            #data_list[key_index] = lines[n].split()
            data_list2.append(data_list[0][0])

textfile = open('/project/uml_stephen_lam/Rajni/Molten_salts/LiFNaFZr4/26-37-37/700C/Vol2x/totpres_9.txt','w')
for element in data_list2:
    textfile.write(element + "\n")
    print(element)
textfile.close()