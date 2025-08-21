import socket
import threading
from queue import Queue
import csv
import json

# ==========================
# Entrada de usuario
# ==========================
objetivo = input("Ingrese la IP o dominio a escanear: ")
puerto_inicio = int(input("Ingrese puerto inicial: "))
puerto_fin = int(input("Ingrese puerto final: "))
archivo_txt = "resultado_scan.txt"
archivo_csv = "resultado_scan.csv"
archivo_json = "resultado_scan.json"

# Diccionario con servicios comunes
servicios_comunes = {
    21: "FTP",
    22: "SSH",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    135: "RPC",
    143: "IMAP",
    443: "HTTPS",
    445: "SMB",
    3306: "MySQL",
    3389: "RDP"
}

# Lista de puertos críticos típicos en Windows
puertos_criticos = [135, 137, 138, 139, 445, 3389]

# Cola de puertos a revisar
cola = Queue()
# Lista donde se guardan los puertos abiertos
puertos_abiertos = []

# ==========================
# Función para escanear un puerto
# ==========================
def escanear_puerto(puerto):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        resultado = s.connect_ex((objetivo, puerto))
        if resultado == 0:
            servicio = servicios_comunes.get(puerto, "Desconocido")
            alerta = "CRÍTICO" if puerto in puertos_criticos else ""
            print(f"✅ Puerto {puerto} ABIERTO ({servicio}) {alerta}")
            puertos_abiertos.append({"puerto": puerto, "servicio": servicio, "alerta": alerta})
        s.close()
    except:
        pass

# ==========================
# Función que toma puertos de la cola
# ==========================
def trabajador():
    while not cola.empty():
        puerto = cola.get()
        escanear_puerto(puerto)
        cola.task_done()

# ==========================
# Main
# ==========================
def main():
    # Llenar la cola con el rango de puertos ingresado
    for puerto in range(puerto_inicio, puerto_fin + 1):
        cola.put(puerto)

    # Crear hilos (50 en este ejemplo)
    for _ in range(50):
        hilo = threading.Thread(target=trabajador)
        hilo.start()

    # Esperar a que todos los hilos terminen
    cola.join()

    # Guardar resultados en TXT
    with open(archivo_txt, "w") as f:
        for resultado in puertos_abiertos:
            alerta = f" ⚠️ {resultado['alerta']}" if resultado['alerta'] else ""
            f.write(f"Puerto {resultado['puerto']} ABIERTO ({resultado['servicio']}){alerta}\n")

    # Guardar resultados en CSV
    with open(archivo_csv, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["puerto", "servicio", "alerta"])
        writer.writeheader()
        writer.writerows(puertos_abiertos)

    # Guardar resultados en JSON
    with open(archivo_json, "w") as f:
        json.dump(puertos_abiertos, f, indent=4)

    print(f"\n✅ Escaneo terminado. Resultados guardados en:\n- {archivo_txt}\n- {archivo_csv}\n- {archivo_json}")

# Ejecutar
if __name__ == "__main__":
    main()
