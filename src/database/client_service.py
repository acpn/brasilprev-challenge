import json
from datetime import datetime
from flask import Response
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash

class ClientService():
    # CLientService it's a service to handle with clients CRUD.
    
    def __init__(self, db, client):
        self.db = db
        self.clientModel = client
        
    def self_json(self):
        """ Method to format responses.
            Args:
                None
            Returns:
                Dictionary: A python dictionary to show in the response.
        """
        return {'id': self.id, 'username': self.username, 'email': self.email}
    
    def check_password(self, password, db_password):
        """ Method to erify if the password it's correct.
            Args:
                password: The password informed by the client in login
                db_password: the password from database.
            Returns:
                boolean: True when the match it's perfect, False otherwise.
        """        
        return check_password_hash(db_password, password)
    
    def create_client(self, _username, _email, _password):
        """ Method to create a new client
            Args:
                _username: The client name
                _email: E-mail from the client
                _password: Password from the client
            Returns:
                Response: An flask Response object with message data and status.
        """
        try:
            client = self.clientModel(username=_username, 
                                      email=_email, 
                                      password=generate_password_hash(_password)
                                     )
            self.db.session.add(client)
            self.db.session.commit()
            
            return Response(
                response=json.dumps({
                    'Name': _username,
                    'Email': _email
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
    
    def get_all_clients(self):
        """ Method to get all clients
            Args:
                None
            Returns:
                Response: An flask Response object with message data and status.
        """
        try: 
            data = [ClientService.self_json(client) 
                    for client in  self.clientModel.query.all()]   
            
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
            
    def get_client_by_email(self, _email):
        """ Method to get client by e-mail
            Args:
                _email: e-mail from the client
            Returns:
                data: An object with Client structure.
        """
        try: 
            data = self.clientModel.query.filter_by(email=_email).first()   
            
            return data
            
        except SQLAlchemyError as err:
        
            return Response(
                response=json.dumps({"Error": str(err.args[0])}),
                status=500,
                mimetype='application/json')
            
        finally:
            self.db.session.close()
            
    
    def update_client(self, _id, _username, _email, _password):
        """ Method to update a new client
            Args:
                _username: The client name
                _email: E-mail from the client
                _password: Password from the client
            Returns:
                Response: An flask Response object with message data and status.
        """
        try:
        
            client_to_update = self.clientModel.query.filter_by(id=_id).first()
            client_to_update.username = _username if _username else client_to_update.username
            client_to_update.email = _email if _email else client_to_update.email
            client_to_update.password = _password if _password else client_to_update.password
            client_to_update.updated_at = datetime.now()
            
            self.db.session.commit()
            
            return Response(
                response=json.dumps({
                    'Name': client_to_update.username,
                    'Email': client_to_update.email
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
        """ Method to delete an client
            Args:
                _id: The client ID that should be deleted
            Returns:
                Response: An flask Response object with message data and status.
        """
        try:
        
            client_to_delete = self.clientModel.query.filter_by(id=_id).first()
            
            if client_to_delete:                        
                self.db.session.delete(client_to_delete)
                self.db.session.commit()
                
                return Response(
                    response=json.dumps({
                        'Message': 'client deleted.'
                    }),
                    status=200,
                    mimetype='application/json')
            else:
                return Response(
                    response=json.dumps({
                        'Message': 'client not found.'
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
            