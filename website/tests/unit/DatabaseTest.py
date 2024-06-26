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
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(project_root)
import pytest
from app import app, mysql  

@pytest.fixture(scope='module')
def client():
    with app.test_client() as client:
        with app.app_context():
            yield client

def test_database_connection(client):
    # Próba wykonania operacji select na bazie danych
    try:
        with mysql.connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            print(f"Result from database query: {result}")

        # Sprawdzenie, czy operacja została wykonana poprawnie
        assert result == (1,)  # Jeśli operacja została wykonana poprawnie, wynikiem powinien być krotka zawierająca wartość 1    

    except Exception as e:
        # Jeśli wystąpił błąd podczas operacji na bazie danych, test zostanie zakończony niepowodzeniem
        pytest.fail(f"Błąd podczas operacji na bazie danych: {str(e)}")

