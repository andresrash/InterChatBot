import time

import openpyxl
import pywhatkit as kit

# Datos necesarios

contact_no = "+573137048612"
name = "Cristian Cardona"
image_path = "images/greetings.jpg"
message = "Hola " + name
wait_time = 10 # tiempo que espera antes de enviar el mensaje en minutos
close_tab = True # Cerrar la pestaña del navegador 
close_time = 20 # tiempo para cerrar la pestaña en minutos


# conectarse al excel 
wb = openpyxl.load_workbook('EnvioMensajes.xlsx')
ws = wb.active
ws = wb['Hoja1']
print('Total numero de filas : '+str(ws.max_row)+'. y total de columnas: '+str(ws.max_column))

# obtener los datos de la 1 fila
values = [ws.cell(row=1,column=i).value for i in range(1,ws.max_column+1)]
print(values)

# obtener la matriz
values = [
    [ws.cell(row=r, column=c).value for c in range(1, ws.max_column + 1)]
    for r in range(1,ws.max_row+1)  # filas 1 al maximo de filas 
]
print(values)


# libreria que envia automaticamente los mensajes
# sendwhatmsg_instantly(phone_no: str, message: str, wait_time: int = 15, tab_close: bool = False, close_time: int = 3) -> None

#kit.sendwhatmsg_instantly(contact_no, message, wait_time, close_tab)
time.sleep(5)


