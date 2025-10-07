import base64

import requests

# Credenciales
username = ''
password = ''
credentials = f'{username}:{password}'


# Codificar en Base64
encoded_credentials = base64.b64encode(credentials.encode()).decode()

print(username, ":", password, " Credent:", credentials)
print ("base 64 encode", encoded_credentials)

# Conexion
url = 'https://www3.interrapidisimo.com/apilogin/api/Autenticacion/Login'

#Parametros Headers
params = {'get_full_session': 'true'}
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Basic {encoded_credentials}'
}

# Respuesta de la Api
response = requests.get(url, headers=headers, params=params)

if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print(f'Error: {response.status_code} - {response.text}')


    
# Desconeccion 
url = 'https://wwwrapsprod.interrapidisimo.com/glpi/apirest.php/killSession'

# Parametros Header
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Basic {encoded_credentials}',   # <-- Autenticación básica
    'Session-Token': '83af7e620c83a50a18d3eac2f6ed05a3ca0bea62'
}

# Respuesta de la Api
response = requests.get(url, headers=headers)

print(f'Error: {response.status_code} - {response.text}')

