import json
from datetime import datetime
from flask import Response
from sqlalchemy.exc import SQLAlchemyError

class OrderService():
    # OrderService it's a service to handle with ORDERS CRUD.
    
    def __init__(self, db, order, product, client):
        self.db = db
        self.orderModel = order
        self.productModel = product
        self.clientModel = client
        
    def self_json(self):
        """ Method to format responses.
            Args:
                None
            Returns:
                Dictionary: A python dictionary to show in the response.
        """
        return {
            'id': self.id,
            'client_id': self.client_id,
            'product_id': self.product_id,
            'order_quantity': self.order_quantity,
            'order_value': str(self.order_value),
            'created_at': str(self.created_at)
        }
    
    def create_order(self, _id_client, _id_product, _quantity):
        """ Method to create an order for a given client.
            Args:
                _id_client: Client id from 
                _id_product: Product id 
                _quantity: Quantity purchased by the client
            Returns:
                Response: An flask Response object with message data and status.
        """
        try:
            product = self.productModel.query.filter_by(id=_id_product).first()
            client = self.clientModel.query.filter_by(id=_id_client).first()
            
            if product and client:
                total = product.price * _quantity
            
                order = self.orderModel(client_id=_id_client, 
                                          product_id=_id_product, 
                                          order_quantity=_quantity,
                                          order_value=total)
                
                self.db.session.add(order)
                self.db.session.commit()
            
                return Response(
                    response=json.dumps({
                        'Client': client.username,
                        'Product': product.description,
                        'Quantity': _quantity,
                        'Value': str(product.price),
                        'Total value': str(total)                        
                    }),
                    status=201,
                    mimetype='application/json')
            
            else:
                return Response(
                    response=json.dumps({
                        'Message': 'Product or client found, \
                            check the informations.'
                    }),
                    status=200,
                    mimetype='application/json')
            
        except SQLAlchemyError as err:
            self.db.session.rollback()
            
            return Response(
                response=json.dumps({"Error": str(err.args[0])}),
                status=500,
                mimetype='application/json')
            
        finally:
            self.db.session.close()
    
    def get_all_orders(self):
        """ Method to get all orders
            Args:
                None
            Returns:
                Response: An flask Response object with message data and status.
        """
        try:
            data = [OrderService.self_json(order) 
                    for order in  self.orderModel.query.all()]             
            
            return Response(
                response=json.dumps(data),
                status=200, 
                mimetype='application/json')
            
        except SQLAlchemyError as err:
        
            return Response(
                response=json.dumps({"Error": str(err.args[0])}),
                status=500,
                mimetype='application/json')
            
        finally:
            self.db.session.close()            
    
    def update_order(self, _id, _quantity):
        """ Method to update an order
            Args:
                _id: The order ID that should be updated
                _quantity: Quantity that will be updated in the order
            Returns:
                Response: An flask Response object with message data and status.
        """
        try:
        
            order_to_update = self.orderModel.query.filter_by(id=_id).first()
            
            if order_to_update:
                product = self.productModel.query.filter_by(
                    id=order_to_update.product_id).first()
                
                order_to_update.order_value = _quantity * product.price
                order_to_update.order_quantity = _quantity               
                order_to_update.updated_at = datetime.now()
            
                self.db.session.commit()
            
                return Response(
                    response=json.dumps({'message': 'Order updated.'}),
                    status=200, 
                    mimetype='application/json')
            else:
                return Response(
                    response=json.dumps({'message': 'Order not found.'}),
                    status=200, 
                    mimetype='application/json')
            
        except SQLAlchemyError as err:
            self.db.session.rollback()
            
            return Response(
                response=json.dumps({"Error": str(err.args[0])}),
                status=500,
                mimetype='application/json')
            
        finally:
            self.db.session.close()
            
    def delete(self, _id):
        """ Method to delete an order
            Args:
                _id: The order ID that should be deleted
            Returns:
                Response: An flask Response object with message data and status.
        """
        try:
        
            order_to_delete = self.orderModel.query.filter_by(id=_id).first()
            
            if order_to_delete:                        
                self.db.session.delete(order_to_delete)
                self.db.session.commit()
                
                return Response(
                    response=json.dumps({
                        'Message': 'Order deleted.'
                    }),
                    status=200,
                    mimetype='application/json')
            else:
                return Response(
                    response=json.dumps({
                        'Message': 'Order not found.'
                    }),
                    status=200,
                    mimetype='application/json')
            
        except SQLAlchemyError as err:
            self.db.session.rollback()
            
            return Response(
                response=json.dumps({"Error": str(err.args[0])}),
                status=500,
                mimetype='application/json')
            
        finally:
            self.db.session.close()
            