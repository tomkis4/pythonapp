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

    # Jeśli użytkownik nie istnieje, dodaj go do bazy danych
    if not user:
        try:
            with app.app_context():
                with mysql.connection.cursor() as cursor:
                    cursor.execute("INSERT INTO users(username, password) VALUES(%s, %s)", (test_username, test_password))
                mysql.connection.commit()
        except Exception as e:
            pytest.fail(f"Błąd podczas wstawiania testowego użytkownika do bazy danych: {str(e)}")
    else:
        # Użytkownik już istnieje, nie dodawaj go ponownie
        pass

    # Próba logowania z poprawnymi danymi
    response = client.post('/login', data=dict(
        username=test_username,
        password=test_password
    ), follow_redirects=True)

    # Sprawdzenie, czy logowanie zakończyło się sukcesem
    assert b'Witaj ponownie, testuser!' in response.data

    # Usunięcie użytkownika z bazy danych
    with app.app_context():
        with mysql.connection.cursor() as cursor:
            cursor.execute("DELETE FROM users WHERE username = %s", (test_username,))
        mysql.connection.commit()
