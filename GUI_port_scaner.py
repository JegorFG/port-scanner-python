import tkinter as tk
from tkinter import ttk, messagebox
import socket
import threading
import queue
import csv
import json
import datetime

# --- Diccionario de servicios comunes ---
SERVICIOS_COMUNES = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    135: "RPC",
    137: "NetBIOS",
    138: "NetBIOS",
    139: "SMB",
    143: "IMAP",
    443: "HTTPS",
    445: "SMB",
    3306: "MySQL",
    3389: "RDP",
    5432: "PostgreSQL",
    8080: "HTTP-alt"
}

# --- Función de escaneo ---
def scan_port(ip, port, results_queue):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((ip, port))
        if result == 0:
            service = SERVICIOS_COMUNES.get(port, "Desconocido")
            results_queue.put((port, service))
        sock.close()
    except:
        pass

def start_scan():
    ip = entry_ip.get()
    port_range = entry_ports.get()

    try:
        start, end = map(int, port_range.split("-"))
    except:
        messagebox.showerror("Error", "Formato de puertos incorrecto. Ejemplo: 20-100")
        return

    results.delete(1.0, tk.END)
    results_queue = queue.Queue()
    threads = []

    for port in range(start, end + 1):
        thread = threading.Thread(target=scan_port, args=(ip, port, results_queue))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    # Mostrar resultados
    open_ports = []
    while not results_queue.empty():
        port, service = results_queue.get()
        results.insert(tk.END, f"[✔] Puerto {port} abierto ({service})\n")
        open_ports.append({"puerto": port, "servicio": service})

    if open_ports:
        save_results(ip, open_ports)
    else:
        results.insert(tk.END, "⚠ No se encontraron puertos abiertos.\n")

# --- Guardar resultados en TXT, CSV y JSON ---
def save_results(ip, open_ports):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    # TXT
    with open(f"resultados_{timestamp}.txt", "w") as f:
        f.write(f"Resultados del escaneo en {ip}\n")
        for p in open_ports:
            f.write(f"Puerto {p['puerto']} abierto ({p['servicio']})\n")

    # CSV
    with open(f"resultados_{timestamp}.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Puerto", "Servicio"])
        for p in open_ports:
            writer.writerow([p['puerto'], p['servicio']])

    # JSON
    with open(f"resultados_{timestamp}.json", "w") as f:
        json.dump({"ip": ip, "puertos_abiertos": open_ports}, f, indent=4)

    messagebox.showinfo("Guardado", f"Resultados guardados como resultados_{timestamp}.[txt|csv|json]")

# --- GUI ---
root = tk.Tk()
root.title("Escáner de Puertos - Python")
root.geometry("600x450")

frame = ttk.Frame(root, padding=10)
frame.pack(fill="both", expand=True)

ttk.Label(frame, text="IP o dominio:").grid(row=0, column=0, sticky="w")
entry_ip = ttk.Entry(frame, width=30)
entry_ip.grid(row=0, column=1)

ttk.Label(frame, text="Rango de puertos (ej: 20-100):").grid(row=1, column=0, sticky="w")
entry_ports = ttk.Entry(frame, width=15)
entry_ports.grid(row=1, column=1)

btn_scan = ttk.Button(frame, text="Iniciar Escaneo", command=start_scan)
btn_scan.grid(row=2, column=0, columnspan=2, pady=10)

results = tk.Text(frame, height=15, width=70)
results.grid(row=3, column=0, columnspan=2)

root.mainloop()
