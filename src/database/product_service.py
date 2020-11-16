import json
from datetime import datetime
from flask import Response
from sqlalchemy.exc import SQLAlchemyError

class ProductService():
    # ProductService it's a service to handle with Product CRUD.
    
    def __init__(self, db, product):
        self.db = db
        self.productModel = product
        
    def self_json(self):
        """ Method to format responses.
            Args:
                None
            Returns:
                Dictionary: A python dictionary to show in the response.
        """
        return {
            'id': self.id, 
            'description': self.description, 
            'price': str(self.price),
            'quantity': self.quantity
        }
    
    def create_product(self, _description, _price, _quantity):
        """ Method to create a new product
            Args:
                _description: Product description
                _price: Product price
                _quantity: Product quantity
            Returns:
                Response: An flask Response object with message data and status.
        """
        try:
            product = self.productModel(description=_description, 
                                        price=_price, 
                                        quantity=_quantity)
            self.db.session.add(product)
            self.db.session.commit()
            
            return Response(
                response=json.dumps({
                    'Description': _description,
                    'Price': _price,
                    'Quantity': _quantity,
                    }),
                status=201, 
                mimetype='application/json')
            
        except SQLAlchemyError as err:
            self.db.session.rollback()
            
            return Response(
                response=json.dumps({"Error": str(err.args[0])}),
                status=500,
                mimetype='application/json')
            
        finally:
            self.db.session.close()
    
    def get_all_products(self):
        """ Method to get all products
            Args:
                None
            Returns:
                Response: An flask Response object with message data and status.
        """
        try: 
            data = [ProductService.self_json(product) 
                    for product in  self.productModel.query.all()]   
            
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
            
    
    def update_product(self, _id, _description, _price, _quantity):
        """ Method to update a product
            Args:
                _id: The product ID that should be updated
                _description: The product description
                _price: Value from the product
                _quantity: Quantity from the product
            Returns:
                Response: An flask Response object with message data and status.
        """
        try:
        
            product_to_update = self.productModel.query.filter_by(id=_id).first()
            product_to_update.description =  \
                _description if _description else product_to_update.description
            product_to_update.price = _price if _price else product_to_update.price
            product_to_update.quantity = \
                _quantity if _quantity else product_to_update.quantity
            product_to_update.updated_at = datetime.now()
            
            self.db.session.commit()
            
            return Response(
                response=json.dumps({
                    'Description': product_to_update.description,
                    'Price': str(product_to_update.price),
                    'Quantity': product_to_update.quantity,
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
            
    def delete(self, _id):
        """ Method to delete an product
            Args:
                _id: The product ID that should be deleted
            Returns:
                Response: An flask Response object with message data and status.
        """
        try:
        
            product_to_delete = self.productModel.query.filter_by(id=_id).first()
            
            if product_to_delete:                        
                self.db.session.delete(product_to_delete)
                self.db.session.commit()
                
                return Response(
                    response=json.dumps({
                        'Message': 'Product deleted.'
                    }),
                    status=200,
                    mimetype='application/json')
            else:
                return Response(
                    response=json.dumps({
                        'Message': 'Product not found.'
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
            