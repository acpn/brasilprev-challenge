import json
import os
from flask import Flask, request
from database.client_service import ClientService
from database.product_service import ProductService
from database.order_service import OrderService
from database.models import Client, Product, Order, db, app

clientService = ClientService(db, Client)
productService = ProductService(db, Product)
orderService = OrderService(db, Order, Product, Client)

## health-check route it's a test route to terraform check if everything it's ok
## when bult the infrastructure.
@app.route('/health-check', methods=['GET'])
def index():    
    return {
        'message': 'OK',
        'version-commit': os.environ.get('HASH_COMMIT', 'invalid')
    }

@app.route('/clients', methods=['GET', 'POST'])
def index_or_create():
    client = ''   
    if request.method == 'POST':
        request_data = request.get_json()
        client = clientService.create_client(
            request_data['name'], 
            request_data['email'], 
            request_data['password'])   
             
    elif request.method == 'GET':
        client = clientService.get_all_clients()
    
    else:
        client = {
            'message': 'Wrong type of call!'
        }

    return client

@app.route('/clients/<int:_id>', methods=['PUT', 'DELETE'])
def update_or_delete(_id):
    if request.method == 'PUT':
        request_data = request.get_json()
        client = clientService.update_client(
            _id,
            request_data['name'], 
            request_data['email'], 
            request_data['password'])    
        
    elif request.method == 'DELETE':
        client = clientService.delete(_id)
            
    else:
        client = {
            'message': 'Wrong type of call!'
        }
        
    return client

@app.route('/products', methods=['GET', 'POST'])
def index_or_post_product():
    product = ''   
    if request.method == 'POST':
        request_data = request.get_json()
        product = productService.create_product(
            request_data['description'], 
            request_data['price'], 
            request_data['quantity'])        
        
    elif request.method == 'GET':
        product = productService.get_all_products()
    
    else:
        product = {
            'message': 'Wrong type of call!'
        }

    return product

@app.route('/products/<int:_id>', methods=['PUT', 'DELETE'])
def put_or_delete_product(_id):
    if request.method == 'PUT':
        request_data = request.get_json()
        product = productService.update_product(
            _id,
            request_data['description'], 
            request_data['price'], 
            request_data['quantity'])
        
    elif request.method == 'DELETE':
        product = productService.delete(_id)
    
    else:
        product = {
            'message': 'Wrong type of call!'
        }
    
    return product

@app.route('/orders', methods=['GET', 'POST'])
def index_or_post_order():
    order = ''   
    if request.method == 'POST':
        request_data = request.get_json()
        order = orderService.create_order(
            request_data['id_client'], 
            request_data['id_product'], 
            request_data['quantity'])        
        
    elif request.method == 'GET':
        order = orderService.get_all_orders()
    
    else:
        order = {
            'message': 'Wrong type of call!'
        }

    return order

@app.route('/orders/<int:_id>', methods=['PUT', 'DELETE'])
def put_or_delete_order(_id):
    if request.method == 'PUT':
        request_data = request.get_json()
        order = orderService.update_order(
            _id,
            request_data['quantity'])
        
    elif request.method == 'DELETE':
        order = orderService.delete(_id)
    
    else:
        order = {
            'message': 'Wrong type of call!'
        }
    
    return order

if __name__ == "__main__":
    app.run(host='0.0.0.0')
