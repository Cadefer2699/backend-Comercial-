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
        if {'email', 'clave'} - set(request.form.keys()): #validar que el usuario envie todos los parámetros requiridos
            return jsonify({'status': False, 'data':None, 'message': 'Faltan parámetros'})
        
        #Leer los parámetros email y clave
        email = request.form['email']
        clave = request.form['clave']

        #Instanciar un objeto de la clase Sesion
        obj = Sesion.iniciarSesion(email, clave)
        
        #Ejecutar el métod iniciar sesión  
        resultadoJSONString = obj.iniciarSesion() 
        
        #Convertir el JSON String a JSON Object  
        resultadoJSONObject = json.loads(resultadoJSONString) 
        
        #validar los datos del resultado enviado por el método por método iniciar sesión 
        if resultadoJSONObject['status'] == True: 
            #imprimir la respuesta del servicio web 
            return jsonify(resultadoJSONObject), 200
        else: 
            #las credenciales fueron incorrectas o el estado del usuario es inactivo 
            return jsonify(resultadoJSONObject), 401
        
        


