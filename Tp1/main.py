def secuenciaEscape(datos: str):
    '''Verifica si es una secuencia de Escape'''
    tamano = len(datos) - 2
    esc = '7D'
    for i in range(tamano-1,0,-1):
        j = i - 1
        if datos[j] + datos[i] == esc:
            return True
        else:
            return False

def busqueda_tramas(contenido):
    '''Retorna una lsita con las tramas de contenido, estas tramas retornadas no tiene los primeros dos bits que indican la cabezera 7E y la cantidad de secuencias de Escape'''
    lista_tramas = []
    trama = '7E'
    flag = '7E'
    count_esc = 0

    for i in range(0,len(contenido)-1,2):
        j = i+1
        trama += (contenido[i]+contenido[j])
        if (contenido[i]+contenido[j]) == flag:
            if not secuenciaEscape(trama):
                lista_tramas.append(trama[0:-2])
                trama = '7E'
            else:
                trama = trama[:-4] + '7E'
                count_esc += 1
        #Guarda la ultima trama
        if j == len(contenido)-2:
            lista_tramas.append(trama)

    return lista_tramas[1:],count_esc


def verificador_long_correcta(lista_tramas):
    '''a partir de una lista de tramas, retorna las tramas con longitud correcta sin los primeros 2 bytes que indican la longitud
      y los ultimo byte que indica el check sum de la trama'''
    tramas_correctas = []
    tramas_incorrectas = []
    for trama in lista_tramas:
        longitud = trama[2:6]
        longitud = int(longitud,16) * 2
        datos_trama = trama[6:-2]
        longitud_trama = len(datos_trama)
        if longitud == longitud_trama:
            tramas_correctas.append(trama)
        else:
            tramas_incorrectas.append(trama)

    return tramas_correctas, tramas_incorrectas

def check_sum(lista_tramas):
    '''a partir de una lista de tramas, retorna las tramas con la suma correcta'''
    aux = int('FF',16)
    contador_checksum = 0
    tramas_correctas = []
    tramas_incorrectas = []

    for t in lista_tramas:
        checksum = t[-2:]
        checksum = int(checksum,16)
        trama = t[6:-2]
        total = 0
        for i in range(0,len(trama),2):
            j = i + 1
            num = trama[i] + trama[j]
            num = int(num,16)
            total += num

        total = 255 - (total % 256)
                
        if total == checksum:
            contador_checksum += 1
            tramas_correctas.append(t)
        else:
            tramas_incorrectas.append(t)
    return tramas_correctas,tramas_incorrectas




#Inicio programa
archivo = open("Tramas_802-15-4.log") #Ruta del Archivo
contenido = archivo.read()#Leemos el Archivo y lo convierte a String

lista_tramas, secuencia_escape= busqueda_tramas(contenido)
lista_tramas_long_correctas, lista_tramas_long_incorrectas = verificador_long_correcta(lista_tramas)
lista_tramas_checksum_correcto, lista_tramas_checksum_incorrecto = check_sum(lista_tramas_long_correctas)

print('tramas totales: ', len(lista_tramas))
print('tramas longitud correcta: ', len(lista_tramas_long_correctas))
print('tramas longitud incorrecta: ', len(lista_tramas_long_incorrectas))
print('tramas longitud correcta y checksum corrrecto: ', len(lista_tramas_checksum_correcto))
print('tramas longitud correcta y checksum incorrecto: ', len(lista_tramas_checksum_incorrecto))
print('tramas con secuencia de escape: ',secuencia_escape)


print("------------Tramas Longitud Incorrecta----------")
print(lista_tramas_long_incorrectas)