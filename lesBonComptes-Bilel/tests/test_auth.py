import sys
import os
import unittest
from flask_testing import TestCase
from mongoengine import connect, disconnect

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ..app.app import create_app
from ..app.models.user import User, db

class AuthTestCase(TestCase):

    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['MONGODB_SETTINGS'] = {
            'db': 'testdb',
            'host': 'mongodb://localhost/testdb'
        }
        app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
        return app

    def setUp(self):
        disconnect()  # Disconnect any existing connections
        connect('testdb', host='mongodb://localhost/testdb')  # Connect to test database
        self.client = self.app.test_client()

    def tearDown(self):
        db.connection.drop_database('testdb')
        disconnect()  # Disconnect from the test database

    def test_register_user(self):
        response = self.client.post('/auth/register', json={
            'username': 'testuser',
            'password': 'Testpassword1'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('Utilisateur testuser créé avec succès', response.json['message'])

    def test_register_user_short_password(self):
        response = self.client.post('/auth/register', json={
            'username': 'testuser',
            'password': 'short'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Le mot de passe doit contenir au moins 8 caractères', response.json['message'])

    def test_register_user_existing_username(self):
        User.create_user('testuser', 'Testpassword1')
        response = self.client.post('/auth/register', json={
            'username': 'testuser',
            'password': 'Testpassword2'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("Nom d'utilisateur déjà pris", response.json['message'])

    def test_login_user(self):
        User.create_user('testuser', 'Testpassword1')
        response = self.client.post('/auth/login', json={
            'username': 'testuser',
            'password': 'Testpassword1'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.json)

    def test_login_invalid_password(self):
        User.create_user('testuser', 'Testpassword1')
        response = self.client.post('/auth/login', json={
            'username': 'testuser',
            'password': 'Wrongpassword'
        })
        self.assertEqual(response.status_code, 401)
        self.assertIn('Identifiants invalides', response.json['message'])

    def test_get_user(self):
        user = User.create_user('testuser', 'Testpassword1')
        access_token = self.client.post('/auth/login', json={
            'username': 'testuser',
            'password': 'Testpassword1'
        }).json['access_token']
        response = self.client.get(f'/auth/user/{user.username}', headers={
            'Authorization': f'Bearer {access_token}'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('username', response.json)
        self.assertEqual(response.json['username'], 'testuser')

    def test_update_user(self):
        user = User.create_user('testuser', 'Testpassword1')
        access_token = self.client.post('/auth/login', json={
            'username': 'testuser',
            'password': 'Testpassword1'
        }).json['access_token']
        response = self.client.put(f'/auth/user/{user.username}', json={
            'new_username': 'updateduser',
            'new_password': 'Updatedpassword1'
        }, headers={'Authorization': f'Bearer {access_token}'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Informations de testuser mises à jour', response.json['message'])

    def test_delete_user(self):
        user = User.create_user('testuser', 'Testpassword1')
        access_token = self.client.post('/auth/login', json={
            'username': 'testuser',
            'password': 'Testpassword1'
        }).json['access_token']
        response = self.client.delete(f'/auth/user/{user.username}', headers={
            'Authorization': f'Bearer {access_token}'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Utilisateur testuser supprimé', response.json['message'])

if __name__ == '__main__':
    unittest.main()
