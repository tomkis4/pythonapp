"""
This file is part of the CatsApp.

Authors:
- Julia Herold
- Tomasz Kiselyczka
- Grzegorz Szymanik

Licensed under the MIT License. See LICENSE file in the project root for full license information.
"""


import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)
import pytest
from app import app, mysql

@pytest.fixture
def client():
    with app.test_client() as client:
        with app.app_context():
            yield client

def test_login(client):
    # Przygotowanie danych testowych
    test_username = 'testuser'
    test_password = 'testpassword'

    # Sprawdzenie, czy użytkownik już istnieje w bazie danych
    with app.app_context():
        with mysql.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE username = %s", (test_username,))
            user = cursor.fetchone()

    # Jeśli użytkownik nie istnieje, rejestrujemy go
    if not user:
        response = client.post('/register', data=dict(
            username=test_username,
            password=test_password
        ), follow_redirects=True)
        assert response.status_code == 200  # Upewnij się, że rejestracja zakończyła się sukcesem
        assert 'Użytkownik już istnieje.' not in response.data.decode('utf-8')  # Upewnij się, że nie zwraca komunikatu o błędnej rejestracji

    # Próba logowania z poprawnymi danymi
    response = client.post('/login', data=dict(
        username=test_username,
        password=test_password
    ), follow_redirects=True)

    # Sprawdzenie, czy logowanie zakończyło się sukcesem
    assert 'Witaj ponownie, testuser!' in response.data.decode('utf-8')

    # Usunięcie użytkownika z bazy danych
    with app.app_context():
        with mysql.connection.cursor() as cursor:
            cursor.execute("DELETE FROM users WHERE username = %s", (test_username,))
        mysql.connection.commit()
