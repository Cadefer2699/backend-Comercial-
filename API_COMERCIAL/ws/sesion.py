from flask import Blueprint, request, jsonify
from models.Sesion import Sesion
import json
import jwt #pyjwt
import datetime
from config import SecretKey

#Crear un módulo para gestionar los endpoints relacionados a la sesión del usuario
ws_sesion = Blueprint('ws_sesion', __name__)

#Crear un endpoint para el inicio de sesión
@ws_sesion.route('/usuario/login', methods=['POST'])
def login():
    if request.method == 'POST':
        #validar que el usuario envie todos los parámetros requiridos
        if {'email', 'clave'} - set(request.form.keys()): 
            return jsonify({'status': False, 'data':None, 'message': 'Faltan parámetros'}), 400 
        
        #Leer los parámetros email y clave
        email = request.form['email']
        clave = request.form['clave']

        #Instanciar un objeto de la clase Sesion con los parámetros de email y clave
        obj_sesion = Sesion(email, clave)
        
        #Ejecutar el métod iniciar sesión  
        resultadoJSONString = obj_sesion.iniciarSesion() 
        
        #Convertir el JSON String a JSON Object  
        resultadoJSONObject = json.loads(resultadoJSONString) 
        
        #validar los datos del resultado enviado por el método por método iniciar sesión 
        if resultadoJSONObject['status'] == True: 
            
            #almacenar los datos del usuario en una variable de sesión
            usuarioID = resultadoJSONObject['data']['id']
            
            #Generar y otorgar el token al usuario que ah iniciado sesión satisfactoriamente 
            token = jwt.encode({'usuarioID': usuarioID, 'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60*60)}, SecretKey.JWT_SECRET_KEY) #tiempo de vida de una hora
            
            #incorporar el token en los datos de la sesión del usuario  
            resultadoJSONObject['data']['token'] = token #almacenar el token en los datos de la sesión del usuario 
            
            #actualizar el token del usuario en la base de datos 
            resultadoActualizarTokenJSONObject = json.loads(obj_sesion.actualizarToken(token, usuarioID)) #en un solo método  
            
            #ocurrio un error al actualizar el token
            if resultadoActualizarTokenJSONObject['status'] == False:
                return jsonify(resultadoJSONObject), 500
            
            
            #imprimir la respuesta del servicio web 
            return jsonify(resultadoJSONObject), 200
        
        else: 
            #las credenciales fueron incorrectas o el estado del usuario es inactivo 
            return jsonify(resultadoJSONObject), 401
        
        


