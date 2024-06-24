import requests
import json
import sys
from time import sleep
from user_token import get_api_token

#Llama a la funcion get_api_token del programa user_token para conseguir el token utilizado en las autorizaciones

token = get_api_token()
autorizacion = f'"Bearer {token}"'

#URL base de donde solicitar la informacion
url = "https://api.fu.do/v1alpha1/products?sort=id%2C-id%2Cname%2C-name&include=productCategory"

#Solicita el valor de inflacion dado por el indec del mes, de no ingresar un numero se maneja el ValueError
while True:
    try:
        indec = float(input("Ingrese el ultimo dato de inflacion del indec:\n"))
        break
    except ValueError as errn:
        print(f"Error, {errn}, Ingrese un numero real, separando digitos con puntos y sin simbolos")

# Define los headers para el request inicial de informacion
headers = {
    "Accept": "application/json",
    "authorization": autorizacion

}

#Manejo de excepciones a la hora de realizar el request de informacion
try:
    response = requests.get(url, headers=headers)
    items = response.json()
    items_json_str = json.dumps(items)
    items_json = json.loads(items_json_str)
except requests.exceptions.HTTPError as errh:
    print(f"Error http {errh}")
    sleep(1)
    sys.exit(1)
except requests.exceptions.ConnectionError as errc:
    print(f"Error al conectarse a la API, {errc} ")
    sleep(1)
    sys.exit(1)
except requests.exceptions.Timeout as errt:
    print(f"Error de timeout {errt}")
    sleep(1)
    sys.exit(1)
except requests.exceptions.InvalidHeader as errhe:
    print(f"Error con el envio de credenciales, puede tener que actualizar su API secret o token, {errhe}")
    sleep(1)
    sys.exit(1)
except requests.exceptions.RequestException as err:
    print(f"Error desconocido, contactese con soporte, {err}")
    sleep(1)
    sys.exit(1)
else:

    # URL base del endpoint
    base_url = "https://api.fu.do/v1alpha1/products/"

    # Itera sobre la lista de objetos del menu
    for objeto in items_json["data"]:

        # Construye la URL del producto especifico
        product_url = base_url + objeto["id"]

        # Construye el payload para el PATCH request
        data = {
            "data": {
                "id": objeto["id"],
                "type": "Product",
                "attributes": {
                    "price": objeto["attributes"]["price"] + (objeto["attributes"]["price"] * ((indec + 5)) / 100)

                }
            }
        }

        #Header para el patch
        h = {
            "accept": "application/json",
            "authorization": autorizacion,
            "content-type": "application/json",
        }

        # Envia el PATCH request
        response = requests.patch(product_url, headers=h, json=data)

        # Checkea el response status
        if response.status_code == 200:
            print(f"Product with ID {objeto['id']} updated successfully")
        else:
            print(f"Failed to update product with ID {objeto['id']}. Status code: {response.status_code}")
