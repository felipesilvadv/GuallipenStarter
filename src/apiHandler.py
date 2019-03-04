# Modulo encargado de leer los archivos que tengan en Davis Graphics
# Para luego actualizar los datos en la api Guallipen
from requests import get, post, put, delete
import json
from os import listdir
from re import match


# Obtiene datos de la API para luego identificar y posteriormente actualizar valores
def readData(route, id=''):
    route = route.strip("/")
    if isValid(route):
        url = "https://frozen-retreat-29770.herokuapp.com/api/{}/{}".format(route, id)
        return json.loads(get(url).text)
    else:
        raise ValueError("Invalid route")

# Lee los datos internos para luego subirlos a la API
def readLocal(carpeta):
    pattern = "^OVENTAS[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]"
    datos = list(filter(lambda x: match(pattern, x) is not None, listdir(carpeta)))
    datos.sort()
    datos.reverse()
    return datos[0]


# Actuliza valores en la API
def updateData(localdata, route, id):
    if isValid(route):
        url = "https://frozen-retreat-29770.herokuapp.com/api/{}/{}".format(route, id)
        r = put(url, localdata)
        return r
    else:
        raise ValueError("Invalid route")


def createData(localdata, route):
    if isValid(route):
        url = "https://frozen-retreat-29770.herokuapp.com/api/{}/".format(route)
        r = post(url, localdata)
        return json.loads(r.text)
    else:
        raise ValueError("Invalid route")


def deleteData(route, id):
    if isValid(route):
        url = "https://frozen-retreat-29770.herokuapp.com/api/{}/{}".format(route, id)
        r = delete(url)
        return r
    else:
        raise ValueError("Invalid route")

def deletePedidos():
    url = "https://frozen-retreat-29770.herokuapp.com/api/pedidos/"
    r = get(url)
    ids = filter(lambda x: x["estado"] == -1, map(lambda x: x["_id"], json.loads(r.text)))
    for id in ids:
        deleteData("pedidos", id)



def arreglarDatos(archivo):
    with open(archivo) as file:
        texto = file.read()
    texto = texto.replace('data:', '"data":')
    texto = texto.replace('row:', '"row":')
    texto = texto.replace('SO:', '"SO":')
    texto = texto.replace('idPedido:', '"idPedido":')
    texto = texto.replace('estadoActual:', '"estadoActual":')
    texto = texto.replace('estadoSiguiente:', '"estadoSiguiente":')
    texto = texto.replace('folProducto:', '"folProducto":')
    texto = texto.replace('bodega:', '"bodega":')
    texto = texto.replace('nameCliente:', '"nameCliente":')
    texto = texto.replace('fecha:', '"fecha":')
    texto = texto.replace('cantidad:', '"cantidad":')
    texto = texto.replace('idProducto:', '"idProducto":')
    texto = texto.replace('idCliente:', '"idCliente":')
    lista = texto.split('"idProducto":')
    for i in range(1, len(lista)):
        palabra = lista[i]
        coma = palabra.find(",")
        lista[i] = '"{}"{}'.format(palabra[0:coma], palabra[coma:])
    texto = '"idProducto":'.join(lista)
    return json.loads(texto)


# Verica si la ruta entregada es válida
def isValid(route):
    validas = ["liberados", "facturados", "ingresados", "clientes",
               "pedidos", "estados", "orden", "ruta", "transportista",
               "vendedor"]
    return route in validas
