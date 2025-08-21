# port-scanner-python

# 🔍 Escáner de Puertos Avanzado en Python

Este proyecto implementa un **escáner de puertos TCP** escrito en Python, diseñado para **fines educativos y prácticas de ciberseguridad ética**.  
Permite identificar qué puertos están abiertos en un host dentro de un rango definido, utilizando **multithreading** para mayor velocidad y eficiencia.

---

## 🚀 Características

- Permite al usuario **ingresar la IP o dominio** y el **rango de puertos** por consola.  
- Escaneo de un **rango de puertos configurable** (por defecto 1–1000).  
- Uso de **50 hilos en paralelo** para acelerar el escaneo.  
- Detección de **servicios comunes** (HTTP, SSH, SMB, etc.).  
- Identificación de **puertos críticos típicos de Windows** (135, 137–139, 445, 3389).  
- Resultados mostrados en pantalla y guardados en **TXT, CSV y JSON** para fácil análisis.  
- Código comentado para fácil aprendizaje y modificación.  

---

## 🛠️ Requisitos

- Python 3.8 o superior  
- Librerías estándar (ya incluidas con Python):  
  - `socket`  
  - `threading`  
  - `queue`  
  - `csv`  
  - `json`  

---

## 📌 Uso

1. Clona este repositorio o descarga el archivo:  

   ```bash
   git clone https://github.com/JegorFG/port-scanner-python.git
   cd port-scanner-python
