import unittest
import os
from analizador import procesar_csv

class TestAnalizador(unittest.TestCase):
    
    def setUp(self):
        # 1. Preparamos un archivo temporal para que la prueba lo lea
        self.archivo_prueba = 'datos_test_temp.csv'
        with open(self.archivo_prueba, 'w', encoding='utf-8') as f:
            f.write("Folio,Fecha,Categoria,Monto,Estatus\n")
            f.write("X001,2024-05-14,Software,100.00,Pagado\n")
            f.write("X002,2024-05-15,Hardware,50.00,Pendiente\n")

    def tearDown(self):
        # 3. Limpiamos borrando el archivo temporal al terminar
        if os.path.exists(self.archivo_prueba):
            os.remove(self.archivo_prueba)

    def test_calculos_correctos(self):
        # 2. Ejecutamos tu función y le hacemos un "examen"
        resultado = procesar_csv(self.archivo_prueba)
        
        # Verificamos que detectó 2 registros y que sumó 150.0
        self.assertEqual(resultado["Total de registros válidos"], 2)
        self.assertEqual(resultado["Suma total de montos"], 150.0)

if __name__ == '__main__':
    unittest.main()