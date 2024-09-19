
from flask import Blueprint, request, jsonify
from models.Producto import Producto
import json
import jwt #pyjwt
import datetime
from config import SecretKey

#crear un módulo para gestionar los endpoints 
ws_producto = Blueprint('ws_producto', __name__) 

#Crear un endpoint para el catalogo de productos 
@ws_producto.route('/producto/catalogo/<int:almacen_id>/<int:producto_id>', methods=['GET']) 
def catalogo(almacen_id, producto_id):  
    if request.method == 'GET':  
        #validar que el usuario haya ingresado el almacen id 
        if not almacen_id: 
            return jsonify({'status': False, 'data': None, 'message': 'Faltan parámetros'}), 400
        
        if not producto_id: 
            return jsonify({'status': False, 'data': None, 'message': 'Faltan parámetros'}), 400
        
    #Instanciamos a la clase Producto 
    obj = Producto() 
    
    #ejecutar el método catalogo para traer los datos 
    resultadoCatalogoJSONObject = json.loads(obj.catalogo(almacen_id, producto_id))
    
    #imprimir el resultado del servicio web 
    if resultadoCatalogoJSONObject['status'] == True:
        return jsonify(resultadoCatalogoJSONObject), 200
    else:
        return jsonify(resultadoCatalogoJSONObject), 500
    