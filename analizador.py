import csv
from collections import Counter
import json
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from datetime import datetime

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
                fecha_str = fila.get('Fecha', '').strip()
                monto_str = fila.get('Monto', '').strip()
                estatus = fila.get('Estatus', '').strip()
                categoria = fila.get('Categoria', '').strip()

                
                if folio in folios_vistos:
                    errores.append(f"Fila {numero_fila}: Folio duplicado ({folio}).")
                    continue
                folios_vistos.add(folio)

                try:
                    # Verifica que la fecha tenga el formato Año-Mes-Día
                    datetime.strptime(fecha_str, '%Y-%m-%d')
                except ValueError:
                    errores.append(f"Fila {numero_fila}: Fecha mal formateada ('{fecha_str}'). Use formato AAAA-MM-DD.")
                    continue

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
    ruta_archivo = filedialog.askopenfilename(
        title="Seleccionar archivo de datos",
        filetypes=[("Archivos CSV", "*.csv")]
    )

    if ruta_archivo:
        resultados = procesar_csv(ruta_archivo)
        
        caja_resultados.delete(1.0, tk.END)
        texto_formateado = json.dumps(resultados, indent=4, ensure_ascii=False)
        caja_resultados.insert(tk.END, texto_formateado)
        
        messagebox.showinfo("Éxito", "El archivo se procesó correctamente.")
        boton_exportar.config(state=tk.NORMAL)

# Exportar resultados 
def exportar_resultados():

    contenido = caja_resultados.get(1.0, tk.END).strip()
    
    # Abrimos explorador para que el usuario elija dónde guardar
    ruta_guardado = filedialog.asksaveasfilename(
        title="Exportar resultados",
        defaultextension=".json",
        filetypes=[("Archivo JSON", "*.json")],
        initialfile="resumen_datos.json"
    )

    if ruta_guardado:
        try:
            with open(ruta_guardado, 'w', encoding='utf-8') as archivo:
                archivo.write(contenido)
            messagebox.showinfo("Éxito", f"Resultados exportados correctamente a:\n{ruta_guardado}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo: {str(e)}")

# Configuración de la ventana principal
ventana = tk.Tk()
ventana.title("Analizador de Datos")
ventana.geometry("650x600")
ventana.config(padx=20, pady=20)

etiqueta_titulo = tk.Label(ventana, text="Procesador de Archivos CSV", font=("Arial", 16, "bold"))
etiqueta_titulo.pack(pady=10)

frame_botones = tk.Frame(ventana)
frame_botones.pack(pady=15)

boton_cargar = tk.Button(frame_botones, text="Cargar CSV y Analizar", command=seleccionar_archivo, bg="#0078D7", fg="white", font=("Arial", 11))
boton_cargar.grid(row=0, column=0, padx=10)

boton_exportar = tk.Button(frame_botones, text="Exportar JSON", command=exportar_resultados, bg="#28A745", fg="white", font=("Arial", 11), state=tk.DISABLED)
boton_exportar.grid(row=0, column=1, padx=10)

caja_resultados = scrolledtext.ScrolledText(ventana, width=75, height=20, font=("Courier", 10))
caja_resultados.pack(pady=10)

ventana.mainloop()