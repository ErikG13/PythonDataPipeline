import codecs
path = 'XXXXXX/starts_data.csv'
pathPSV = 'XXXXXX/starts_PSV.csv'
#Función para abrir el archivo a limpiar
#Function to open the file to clean
def open_file(path):
    try:
        f = open(path, 'r')
        list_f = list(f)
        return list_f
    except FileExistsError:
        print('Corrupted File')
    except FileNotFoundError:
        print('File Not Found')

#Borrando la primera y ultima fila del archivo - Los mensajes del hacker
#Deleted first and last rows of file - Those are messages by the hacker
def deletedMessagesData(list_f):
    list_file = list(list_f)
    del list_file[0]
    del list_file[len(list_file)-1]
    return list_file

#Función que obtendrá los cabeceros de las columnas
#Function that get the headers of the columns
def getHeaders(list_file):
    columns = []
    list_file = str(list_file[0]).replace('~','|').split('|')
    for column in list_file:
        column = column.replace('\n','')
        column = "\"" + column + "\""
        columns.append(column)
    return columns

#Funcion que reemplazara las comas, tabuladores por pipes (","," " => "|")
#Function that replacing commas, tabs by pipes
def replacedCharacters_CSV(list_file, csv_separator = ","):
    del list_file[0]
    list_rows = []
    for line in list_file:
        line = line.rstrip('\n')
        line = str(line).replace(',','|').replace('\t', '|').split('|') #
        list_rows.append(line)
    return list_rows

#Funcion que añadira los valores de las columnas entre comillas
#Function that adding quotes in each value
def addQuotes(list_rows, headers):
    for raw in range(len(list_rows)):
        for column in range(headers):
            list_rows[raw][column] = "\"" + list_rows[raw][column] + "\"" 
    return list_rows

#Funcion que transformará el CSV a PSV
#Function that transform CSV to PSV
def changeCSV_to_PSV(row_converted, headers):
    dataset = []
    register = ''
    row_converted.insert(0, headers)
    for row in row_converted:
        register = str(row).replace('\'','').replace('[','').replace(']','').replace(' ','').replace(',','|')
        dataset.append(register)
    register = ''
    return dataset

#Funcion que escribe el archivo PSV final
#Function that write final PSV file
def writeFilePSV(list_file, pathPSV):
    try:
        f = codecs.open(pathPSV,'w+', 'utf-8')
        print('Exitoso')
        for row in list_file:
            f.writelines('{}\n'.format(row))
    except Exception as e:
        print(e)
    finally:
        f.close()

file_opened = open_file(path) #Var for open file
clean_listMessages = deletedMessagesData(file_opened) #Var for clean dataset
headers = getHeaders(clean_listMessages) #var for get headers of dataset
convertCSV_to_PSV = replacedCharacters_CSV(clean_listMessages)
addingQuotes = addQuotes(convertCSV_to_PSV, len(headers))
convertCSV_PSV = changeCSV_to_PSV(addingQuotes, headers)
writeFilePSV(convertCSV_PSV, pathPSV)

