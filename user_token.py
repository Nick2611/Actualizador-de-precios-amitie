from time import sleep
import requests
import json
import sys
from tkinter import Tk, Canvas, Entry, Button

def retrieve_input(e_1, e_2, w):
    global api_key
    global api_secret

    api_key = e_1.get()
    api_secret = e_2.get()
    w.destroy()

def mainscreen():
    window = Tk()

    window.geometry("585x713")
    window.configure(bg="#FFFFFF")

    canvas = Canvas(
        window,
        bg="#FFFFFF",
        height=713,
        width=585,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    canvas.place(x=0, y=0)

    canvas.create_rectangle(
        0.0,
        0.0,
        585.0,
        90.0,
        fill="#9DFF6F",
        outline=""
    )

    canvas.create_text(
        55.0,
        25.0,
        anchor="nw",
        text="ACTUALIZADOR DE MENU",
        fill="#000000",
        font=("Inter Black", 30, "bold")
    )

    canvas.create_rectangle(
        97.0,
        262.0,
        488.0,
        308.0,
        fill="#D9D9D9",
        outline=""
    )

    canvas.create_text(
        135.0,
        275.0,
        anchor="nw",
        text="INGRESE SU API SECRET",
        fill="#000000",
        font=("Inter Black", 20)
    )

    canvas.create_rectangle(
        97.0,
        118.0,
        488.0,
        164.0,
        fill="#D9D9D9",
        outline=""
    )

    canvas.create_text(
        147.0,
        136.0,
        anchor="nw",
        text="INGRESE SU API KEY",
        fill="#000000",
        font=("Inter Black", 20)
    )

    entry_1 = Entry(
        window,
        bd=2,  # Border width
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=1,  # Highlight thickness
        highlightbackground="#BFBFBF",  # Highlight background color
        highlightcolor="#BFBFBF",  # Highlight color (same as background for no change on focus)
        font=("Arial", 14)  # Font settings
    )
    entry_1.place(
        x=93.0,
        y=188.0,
        width=400.0,
        height=45.0
    )

    entry_2 = Entry(
        window,
        bd=2,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=1,
        highlightbackground="#BFBFBF",
        highlightcolor="#BFBFBF",
        font=("Arial", 14)
    )
    entry_2.place(
        x=93.0,
        y=336.0,
        width=400.0,
        height=45.0
    )

    button_1 = Button(
        window,
        text="Enviar",
        borderwidth=0,
        highlightthickness=0,
        command=lambda: retrieve_input(entry_1, entry_2, window),
        relief="flat"
    )
    button_1.place(
        x=174.0,
        y=460.0,
        width=252.0,
        height=39.0
    )

    window.resizable(False, False)
    window.mainloop()

def get_api_token():
    mainscreen()

    url = "https://auth.fu.do/api"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    data = {
        "apiKey": api_key,
        "apiSecret": api_secret,
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # Raise HTTPError for bad responses
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
        sleep(1)
        sys.exit(1)  # Exit program with status 1 (or any non-zero code)
    except requests.exceptions.ConnectionError as errc:
        print(f"Connection Error: {errc}")
        sleep(1)
        sys.exit(1)  # Exit program
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
        sleep(1)
        sys.exit(1)  # Exit program
    except requests.exceptions.RequestException as err:
        print(f"Request Exception: {err}")
        sleep(1)
        sys.exit(1)  # Exit program

    try:
        token = response.json().get('token')
        if token:
            print(f"Token obtenido: {token}")
            print()
            return token
        else:
            print("No se pudo obtener el token.")
            sys.exit(1)  # Exit program if token is not obtained
    except json.JSONDecodeError as json_err:
        print(f"Error al decodificar la respuesta JSON: {json_err}")
        sys.exit(1)  # Exit program




