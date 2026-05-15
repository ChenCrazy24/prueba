import csv
from collections import Counter
import json
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from datetime import datetime
import sqlite3 

def procesar_csv(ruta_archivo, filtro_estatus="", filtro_categoria=""):
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

                if filtro_estatus and filtro_estatus.lower() not in estatus.lower():
                    continue
                if filtro_categoria and filtro_categoria.lower() not in categoria.lower():
                    continue

                if folio in folios_vistos:
                    errores.append(f"Fila {numero_fila}: Folio duplicado ({folio}).")
                    continue
                folios_vistos.add(folio)

                try:
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

def guardar_en_bd(resultados):
    try:
        conexion = sqlite3.connect('historial_analisis.db')
        cursor = conexion.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analisis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha_ejecucion TEXT,
                total_registros INTEGER,
                suma_montos REAL,
                resumen_json TEXT
            )
        ''')

        fecha_ahora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        total = resultados.get("Total de registros válidos", 0)
        suma = resultados.get("Suma total de montos", 0.0)
        json_completo = json.dumps(resultados, ensure_ascii=False)

        cursor.execute('''
            INSERT INTO analisis (fecha_ejecucion, total_registros, suma_montos, resumen_json)
            VALUES (?, ?, ?, ?)
        ''', (fecha_ahora, total, suma, json_completo))

        conexion.commit()
        conexion.close()
    except Exception as e:
        messagebox.showwarning("Advertencia BD", f"El resumen se generó pero no se guardó en BD: {e}")

def seleccionar_archivo():
    ruta_archivo = filedialog.askopenfilename(
        title="Seleccionar archivo de datos",
        filetypes=[("Archivos CSV", "*.csv")]
    )

    if ruta_archivo:
       
        f_estatus = entrada_estatus.get().strip()
        f_categoria = entrada_categoria.get().strip()
        
        resultados = procesar_csv(ruta_archivo, f_estatus, f_categoria)
        
        caja_resultados.delete(1.0, tk.END)
        texto_formateado = json.dumps(resultados, indent=4, ensure_ascii=False)
        caja_resultados.insert(tk.END, texto_formateado)
        
        if "Error" not in resultados and "Error crítico" not in resultados:
            guardar_en_bd(resultados)
            mensaje = "El archivo se procesó y se guardó en la Base de Datos local."
        else:
            mensaje = "El archivo se procesó, pero se encontraron errores de estructura."
            
        messagebox.showinfo("Proceso Terminado", mensaje)
        boton_exportar.config(state=tk.NORMAL)

def exportar_resultados():
    contenido = caja_resultados.get(1.0, tk.END).strip()
    
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

if __name__ == "__main__":
    ventana = tk.Tk()
    ventana.title("Analizador de Datos")

    ventana.geometry("650x650")
    ventana.config(padx=20, pady=20)

    etiqueta_titulo = tk.Label(ventana, text="Procesador de Archivos CSV", font=("Arial", 16, "bold"))
    etiqueta_titulo.pack(pady=10)

    frame_filtros = tk.Frame(ventana)
    frame_filtros.pack(pady=10)

    tk.Label(frame_filtros, text="Filtrar por Estatus:", font=("Arial", 10)).grid(row=0, column=0, padx=5)
    entrada_estatus = tk.Entry(frame_filtros, width=15)
    entrada_estatus.grid(row=0, column=1, padx=5)

    tk.Label(frame_filtros, text="Filtrar por Categoría:", font=("Arial", 10)).grid(row=0, column=2, padx=10)
    entrada_categoria = tk.Entry(frame_filtros, width=15)
    entrada_categoria.grid(row=0, column=3, padx=5)

    frame_botones = tk.Frame(ventana)
    frame_botones.pack(pady=15)

    boton_cargar = tk.Button(frame_botones, text="Cargar CSV y Analizar", command=seleccionar_archivo, bg="#0078D7", fg="white", font=("Arial", 11))
    boton_cargar.grid(row=0, column=0, padx=10)

    boton_exportar = tk.Button(frame_botones, text="Exportar JSON", command=exportar_resultados, bg="#28A745", fg="white", font=("Arial", 11), state=tk.DISABLED)
    boton_exportar.grid(row=0, column=1, padx=10)

    caja_resultados = scrolledtext.ScrolledText(ventana, width=75, height=20, font=("Courier", 10))
    caja_resultados.pack(pady=10)

    ventana.mainloop()