# Aplicacion encargada de estar constantemente revisando (con un thread)
# los datos proporcionados por el Lab para actualizarlos en la API,
# Junto con correr el Frontend de la misma
from threading import Thread
from src.mailer import sendMail
from src.apiHandler import readData, readLocal, updateData
from random import choice
