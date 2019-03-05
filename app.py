# Aplicacion encargada de estar constantemente revisando (con un thread)
# los datos proporcionados por el Lab para actualizarlos en la API,
# Junto con correr el Frontend de la misma
from threading import Thread
#from src.mailer import sendMail
from src.apiHandler import readData, readLocal, updateData, deletePedidos, createData, borrarRutas, deleteRutas
#import webbrowser
import os

def updatePedidos(pedidosLocales):
    pedidos = readData('pedidos')
    clientes = readData('clientes')
    for i in range(len(pedidosLocales)):
        actualizarPedido(pedidosLocales[i], pedidos, clientes)



def actualizarPedido(pedidolocal, pedidos, clientes):
    idPedido = pedidolocal["idPedido"]
    pedido = None
    for i in range(len(pedidos)):
        if int(pedidos[i]['orden']) == idPedido:
            pedido = pedidos[i]
            break
    if pedido:
        if pedido['estado'] > 0 and pedido["estado"] < pedidolocal["estadoActual"]:
            data = {
                'estado': pedidolocal["estadoActual"]
            }
            #print("Hago put en pedidos/{}\ndata: {}".format(pedido["_id"], data))
            updateData(data, 'pedidos', pedido["_id"])
    else:
        idCliente = pedidolocal['idCliente']
        cliente = None
        for i in range(len(clientes)):
            if int(clientes[i]['id']) == idCliente:
                cliente = clientes[i]
                break
        if cliente is None:
            datos_cliente ={
                'id': idCliente,
                'nombre': pedidolocal['nameCliente']
            }

            cliente = createData(datos_cliente, 'clientes')
            clientes.append(cliente)
            #print("Se crea cliente con\ndatos = {}".format(datos_cliente))

        data = {
            'orden': idPedido,
            'estado': pedidolocal['estadoActual'],
            'cliente': cliente['_id']
        }
        pedido = createData(data, 'pedidos')
        #print("Se crea pedido\nPedido = {}".format(data))

def revisarPedidos(carpeta):
    previo = None
    while True:
        datos, nombre = readLocal(carpeta)
        if nombre != previo:
            updatePedidos(datos)
        previo = datos
        deletePedidos()

def revisarRutas():
    if borrarRutas():
        deleteRutas()

def abrirGuallipen():
    os.system('npm start --prefix C:\\Users\\dgsasac04\\AppData\\Local\\GuallipenFront-master')

carpeta = 'C:\\FTP\\'
#carpeta = 'data/'
revisarRutas()
pedidos = Thread(target=revisarPedidos, args=(carpeta,))
Guallipen = Thread(target=abrirGuallipen)
Guallipen.start()
pedidos.start()

#print(readLocal('C:\\FTP\\')['data']['row'][0])
#url = 'http://docs.python.org/'

# MacOS
#chrome_path = 'open -a /Applications/Google\ Chrome.app %s'

# Windows
#chrome_path = 'C:\\User\\dgsasac04\\AppData\\Local\\Google\\Chrome\\Application\\chrome.exe %s'

# Linux
#chrome_path = '/usr/bin/google-chrome %s'

#webbrowser.get(chrome_path).open(url)
