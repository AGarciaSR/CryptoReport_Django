import csv

def handle_transaction_csv(f):
    lines = []
    # Número de transacciones encontradas en el CSV
    number_t = 0
    for line in f:
        # Por cada línea del archivo csv la pasamos a String, dividimos por ";" y eliminamos el carácter de salto de línea
        new_line = str(line).split(";")[:-1]
        # Eliminamos los 2 primeros caracteres del primer elemento, que corresponden a un identificador de bytes que no hace falta
        new_line[0] = new_line[0][2:]
        lines.append(new_line)
        number_t += 1
    f.close()
    # Pasamos la primera línea del CSV a una lista aparte, para manejarlo después
    # lines = data[0].split('\n')
    # Eliminamos la primera línea,que contiene los nombres de campo, para dejar sólo los datos de usuario
    #data.pop(0)
    # for dato in data:
    #    prob = dato.strip().split(';')
        
    return lines