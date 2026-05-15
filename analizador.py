import csv
from collections import Counter
import json
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

def procesar_csv(ruta_archivo):
    columnas_obligatorias = ['Folio', 'Fecha', 'Categoria', 'Monto', 'Estatus']
    
    try:
        with open(ruta_archivo, mode='r', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo)
            
            if not lector.fieldnames:
                return {"Error": "El archivo está vacío o no tiene encabezados."}
                
            faltantes = [col for col in columnas_obligatorias if col not in lector.fieldnames]
            if faltantes:
                return {"Error": f"Faltan las siguientes columnas obligatorias: {faltantes}"}

            total_registros = 0
            suma_montos = 0.0
            agrupacion_estatus = Counter()
            agrupacion_categoria = Counter()
            folios_vistos = set()
            errores = []

            for numero_fila, fila in enumerate(lector, start=2):
                folio = fila.get('Folio', '').strip()
                monto_str = fila.get('Monto', '').strip()
                estatus = fila.get('Estatus', '').strip()
                categoria = fila.get('Categoria', '').strip()

                if folio in folios_vistos:
                    errores.append(f"Fila {numero_fila}: Folio duplicado ({folio}).")
                    continue
                folios_vistos.add(folio)

                try:
                    monto = float(monto_str)
                    suma_montos += monto
                except ValueError:
                    errores.append(f"Fila {numero_fila}: Monto inválido ('{monto_str}').")
                    continue

                total_registros += 1
                agrupacion_estatus[estatus] += 1
                agrupacion_categoria[categoria] += 1

            resumen = {
                "Total de registros válidos": total_registros,
                "Suma total de montos": round(suma_montos, 2),
                "Agrupación por estatus": dict(agrupacion_estatus),
                "Agrupación por categoría": dict(agrupacion_categoria),
                "Errores detectados": errores
            }
            return resumen

    except Exception as e:
        return {"Error crítico": str(e)}


def seleccionar_archivo():
    # Abrir explorador de archivos (Filtrado solo para CSV)
    ruta_archivo = filedialog.askopenfilename(
        title="Seleccionar archivo de datos",
        filetypes=[("Archivos CSV", "*.csv")]
    )

    if ruta_archivo:
        # Procesar el archivo seleccionado
        resultados = procesar_csv(ruta_archivo)

        # Mostrar resultados en la caja de texto
        caja_resultados.delete(1.0, tk.END) # Limpiar caja
        texto_formateado = json.dumps(resultados, indent=4, ensure_ascii=False)
        caja_resultados.insert(tk.END, texto_formateado)
        
        messagebox.showinfo("Éxito", "El archivo se procesó correctamente.")

# Configuración de la ventana principal
ventana = tk.Tk()
ventana.title("Analizador de Datos")
ventana.geometry("600x500")
ventana.config(padx=20, pady=20)

etiqueta_titulo = tk.Label(ventana, text="Procesador de Archivos CSV", font=("Arial", 16, "bold"))
etiqueta_titulo.pack(pady=10)

boton_cargar = tk.Button(ventana, text="Cargar Archivo y Analizar", command=seleccionar_archivo, bg="#0078D7", fg="white", font=("Arial", 12))
boton_cargar.pack(pady=15)

caja_resultados = scrolledtext.ScrolledText(ventana, width=70, height=20, font=("Courier", 10))
caja_resultados.pack(pady=10)

ventana.mainloop()