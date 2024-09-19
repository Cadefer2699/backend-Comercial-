from conexionBD import Conexion as db
import json

class Sesion():
    def __init__(self, email:None, clave:None):
        self.email = email
        self.clave = clave

    def iniciarSesion(self):
        #Abrir la conexión a la BD
        con = db().open

        try:
            #Crear un cursor para almacenar los datos que devuelve la consuñta SQL, al validar las credenciales del usuario
            cursor = con.cursor()

            #Preparar una consulta SQL select para validar las credenciales del usuario
            sql = """
                    SELECT
                        u.id,
                        u.nombre,
                        u.email,
                        u.estado_usuario,
                        u.almacen_id
                    FROM
                        usuario u
                    WHERE
                        email = %s
                        and clave = %s;
                """
            
            #Ejecutar la consulta SQL
            cursor.execute(sql, [self.email, self.clave])

            #Almancenar el resultado de la consulta SQL ejecutada
            datos = cursor.fetchone()

            #Retonar el resultado
            if datos: #Validar si la consulta sql ha devuelvo registros
                if datos['estado_usuario'] == '1': #1:Activo; 0:Inactivo
                    return json.dumps({'status': True, 'data': datos, 'message': 'Inicio de sesión satisfactorio. Bienvenido a la aplicación'})
                
                else: #El usuario se encuentra inactivo
                    return json.dumps({'status': False, 'data': None, 'message': 'Cuenta inactiva. Consulte al administrador'})
            else: #No hay datos
                return json.dumps({'status': False, 'data': None, 'message': 'Credenciales incorrectas, por favor verifique'})

        except con.Error as error:
            #Retornar un mensaje de error
            return json.dumps({'status': False, 'data': None, 'message': str(error)})

        finally:
            cursor.close()
            con.close()

    def actualizarToken(self, token, UsuarioID): 
        #Abrir la conexion a la bd  
        con = db().open 
        
        #Crear un cursor para almacenar los datos de la consulta sql 
        cursor = con.cursor()
        
        #Preparar una sentecia que permita actualizar el token del usuario en la BD 
        sql = " update usuario set token = %s, estado_token='1' where id = %s"
        
        #iniciar con la actualizacíon del token 
        try: 
            #Configurar el transacción 
            con.autocommit = False #indica que la transacción se verificara y confirmara de manera manual 
            
            #ejecutar la sentencia  
            cursor.execute(sql, [token, UsuarioID]) 
            
            #confirmar la sentencia de actualización
            con.commit() 
            
        except con.Error as error: 
            #Revocar la conexión
            con.rollback()
            
            #retorna un mensaje 
            return json.dumps({'status': False, 'data': None, 'message': str(error)})
        
        finally: 
            cursor.close()
            con.close()
            
        #Si todo el método se ah ejecutado correctamente, entonces retornar un mensaje de exito
        return json.dumps({'status': True, 'data': None, 'message': 'Token actualizado satisfactoriamente'})

        