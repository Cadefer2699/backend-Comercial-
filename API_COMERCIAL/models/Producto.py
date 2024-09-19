from conexionBD import Conexion as db 
import json 
from util import CustomJsonEncoder

class Producto(): 
    #definición del constructor
    def __init__(self, id=None, nombre=None, precio=None, categoriaId=None):  
        self.id = id
        self.nombre = nombre
        self.precio = precio
        self.categoriaId = categoriaId
        
    def catalogo(self, almacenID, productoID):  
        #Abrir la conexion a la bd 
        con = db().open
        
        #crear un cursor para almacenar los datos de la consulta sql 
        cursor = con.cursor()
        
        #preparar la sentencia 
        sql = """ 
            SELECT
                p.id,
                p.nombre, 
                p.precio, 
                p.nombre AS categoria, 
                CONCAT('static/imgs-catalogo/productos/', p.id, '.jpg') AS foto, 
                s.stock
            FROM 
				producto p 
                INNER JOIN categoria c ON (p.categoria_id = c.id)
                LEFT JOIN stock_almacen s ON (p.id = s.producto_id)
            WHERE 
                s.almacen_id = %s
				AND (case when %s=0 then TRUE ELSE p.id=%s end)
			ORDER BY
				2
        """
        
        try: 
            #Ejecutar la sentencia 
            cursor.execute(sql, [almacenID, productoID, productoID])
        
            #Recuperar los datos de la consulta, almacenarlos en la variable datos
            datos = cursor.fetchall() 
            
            #Retornar un mensaje con los datos recuperados 
            if datos: 
                return json.dumps({'status': True, 'data': datos, 'message': 'catalogo de productos'})
            else: 
                return json.dumps({'status': True, 'data': None, 'message': 'Sin registros'})
            
            
        except con.Error as error: 
            #Retornar un mensaje de error
            return json.dumps({'status': False, 'data': None, 'message': str(error)})

        finally:
            cursor.close()
            con.close()
            
        
        
        
        
        