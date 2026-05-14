import csv
from collections import Counter

def procesar_csv(ruta_archivo):
    columnas_obligatorias = ['Folio', 'Fecha', 'Categoria', 'Monto', 'Estatus']
    
    try:
        with open(ruta_archivo, mode='r', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo)
            
            if not lector.fieldnames:
                return "Error: El archivo está vacío o no tiene encabezados."
                
            faltantes = [col for col in columnas_obligatorias if col not in lector.fieldnames]
            if faltantes:
                return f"Error: Faltan las siguientes columnas obligatorias: {faltantes}"

            #Variables para el resumen
            total_registros = 0
            suma_montos = 0.0
            agrupacion_estatus = Counter()
            agrupacion_categoria = Counter()
            folios_vistos = set()
            errores = []

            #Leer registros y procesar información
            for numero_fila, fila in enumerate(lector, start=2): # start=2 porque la 1 es el encabezado
                folio = fila.get('Folio', '').strip()
                monto_str = fila.get('Monto', '').strip()
                estatus = fila.get('Estatus', '').strip()
                categoria = fila.get('Categoria', '').strip()

                
                if folio in folios_vistos:
                    errores.append(f"Fila {numero_fila}: Folio duplicado encontrado ({folio}).")
                    continue
                folios_vistos.add(folio)

                try:
                    monto = float(monto_str)
                    suma_montos += monto
                except ValueError:
                    errores.append(f"Fila {numero_fila}: Monto inválido ('{monto_str}'). Se omitirá de la suma.")
                    continue

                #Recolectar datos para agrupación
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

    except FileNotFoundError:
        return "Error: No se encontró el archivo."
    except Exception as e:
        return f"Ocurrió un error inesperado: {str(e)}"

if __name__ == "__main__":
    print("--- Iniciando Análisis de Archivo ---")
    resultados = procesar_csv('datos.csv')
    
    import json
    print(json.dumps(resultados, indent=4, ensure_ascii=False))