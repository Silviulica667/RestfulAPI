import tkinter as tk
import requests
from tkinter import messagebox
import random
import datetime
import json

API_URL = "http://127.0.0.1:5000/senzori"


def refresh_list():
    response = requests.get(API_URL)
    if response.status_code == 200:
        sensors_list.delete(0, tk.END)
        for sensor in response.json():
            sensors_list.insert(tk.END, f"{sensor['id']}, {sensor['nume']}, {sensor['tip']}, {sensor['valoare']}, {sensor['unitate']}, {sensor['locatie']}, {sensor['time']}")

def add_to_json(sensor_data):
    try:
        with open("senzori_data.json", "r") as f:
            senzori = json.load(f)
            if not isinstance(senzori, list):  
                senzori = []  
    except (FileNotFoundError, json.JSONDecodeError):
        senzori = []  

    senzori.append(sensor_data) 

    with open("senzori_data.json", "w") as f:
        json.dump(senzori, f, indent=4)  

def add_sensor():

    sensor_data = {
        "id": int(entry_id.get()),
        "nume": entry_nume.get(),
        "tip": entry_tip.get(),
        "valoare": int(random.randint(0,50)),
        "unitate": entry_unitate.get(),
        "locatie": entry_locatie.get(),
        "time": entry_data.get()
    }

    requests.post(API_URL, json=sensor_data)
    refresh_list()

def update_sensor():
    sensor_id = int(entry_id.get())

    sensor_data = {
        "id": sensor_id,
        "nume": entry_nume.get(),
        "tip": entry_tip.get(),
        "valoare": random.randint(0, 50),
        "unitate": entry_unitate.get(),
        "locatie": entry_locatie.get(),
        "time": entry_data.get()
    }

    requests.put(f"{API_URL}/{sensor_id}", json=sensor_data)
    refresh_list()

def delete_sensor():
    selected = sensors_list.curselection()
    sensor_text = sensors_list.get(selected[0])
    
    sensor_id = int(sensor_text.split(",")[0].strip()) 

    requests.delete(f"{API_URL}/{sensor_id}")
    refresh_list()


def update_time():

    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry_data.delete(0, tk.END) 
    entry_data.insert(0, current_time)  
    root.after(1000, update_time)  

root = tk.Tk()
root.title("Client Senzori")

frame = tk.Frame(root)
frame.pack(pady=10)

# Lista senzori
tk.Label(frame, text="Senzori disponibili:").pack()
sensors_list = tk.Listbox(frame, width=50)
sensors_list.pack()

tk.Label(frame, text="ID").pack()
entry_id = tk.Entry(frame)
entry_id.pack()

tk.Label(frame, text="Nume").pack()
entry_nume = tk.Entry(frame)
entry_nume.pack()

tk.Label(frame, text="Tip").pack()
entry_tip = tk.Entry(frame)
entry_tip.pack()

tk.Label(frame, text="Unitate").pack()
entry_unitate = tk.Entry(frame)
entry_unitate.pack()

tk.Label(frame, text="Locatie").pack()
entry_locatie = tk.Entry(frame)
entry_locatie.pack()

tk.Label(frame, text="Time").pack()
entry_data = tk.Entry(frame)
entry_data.pack()

update_time()

#butoane
tk.Button(frame, text="Adaugă senzor", command=add_sensor).pack(pady=5)
tk.Button(frame, text="Update senzor", command=update_sensor).pack(pady=5)
tk.Button(frame, text="Sterge senzor", command=delete_sensor).pack(pady=5)

refresh_list()
root.mainloop()
