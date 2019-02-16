# Modulo encargado de leer los archivos que tengan en Davis Graphics
# Para luego actualizar los datos en la api Guallipen
from requests import get, post, put, delete
import json


# Obtiene datos de la API para luego identificar y posteriormente actualizar valores
def readData(route):
    route = route.strip("/")
    if isValid(route):
        url = "https://frozen-retreat-29770.herokuapp.com/api/{}/".format(route)
        return json.loads(get(url).text)
    else:
        raise ValueError("Invalid route")

# Lee los datos internos para luego subirlos la API
def readLocal():
    return

# Actuliza valores en la API
def updateData(localdata, route, id):
    if isValid(route):
        url = "https://frozen-retreat-29770.herokuapp.com/api/{}/{}".format(route, id)
        r = put(url, localdata)
        return r
    else:
        raise ValueError("Invalid route")

        
# Verica si la ruta entregada es válida
def isValid(route):
    validas = ["liberados", "facturados", "ingresados", "clientes",
               "pedidos", "estados", "orden", "ruta", "transportista",
               "vendedor"]
    return route in validas
