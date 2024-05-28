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
import pytest
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL

# ścieżka do katalogu głównego aplikacji
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from website.app import app, mysql

@pytest.fixture
def client():
    with app.test_client() as client:
        with app.app_context():
            yield client

def get_unique_post_title(base_title):
    with app.app_context():
        with mysql.connection.cursor() as cursor:
            cursor.execute("SELECT title FROM posts WHERE title LIKE %s", (base_title + '%',))
            existing_titles = cursor.fetchall()
            titles_set = {title[0] for title in existing_titles}

            counter = 1
            new_title = base_title
            while new_title in titles_set:
                new_title = f"{base_title} {counter}"
                counter += 1
            
            return new_title

def test_add_post(client):
    # Przygotowanie danych testowych
    test_username = 'testuser'
    test_password = 'testpassword'
    base_post_title = 'Testowy Tytuł'
    post_content = 'To jest treść testowego postu.'

    # Rejestracja testowego użytkownika
    with app.app_context():
        with mysql.connection.cursor() as cursor:
            cursor.execute("DELETE FROM posts WHERE user_id IN (SELECT user_id FROM users WHERE username = %s)", (test_username,))
            cursor.execute("DELETE FROM users WHERE username = %s", (test_username,))
            cursor.execute("INSERT INTO users(username, password) VALUES(%s, %s)", (test_username, test_password))
        mysql.connection.commit()

    # Logowanie testowego użytkownika
    response = client.post('/login', data=dict(
        username=test_username,
        password=test_password
    ), follow_redirects=True)
    assert response.status_code == 200
    assert 'Forum' in response.data.decode('utf-8')

    # Dodanie nowego postu z unikalnym tytułem
    post_title = get_unique_post_title(base_post_title)
    print(f"Generated unique post title: {post_title}") 
    response = client.post('/add_post', data=dict(
        post_title=post_title,
        post_content=post_content
    ), follow_redirects=True)
    assert response.status_code == 200
    assert 'Forum' in response.data.decode('utf-8')

    # Sprawdzenie, czy post został dodany
    with app.app_context():
        with mysql.connection.cursor() as cursor:
            cursor.execute("SELECT post_id, title, content, user_id FROM posts WHERE title = %s AND content = %s", (post_title, post_content))
            post = cursor.fetchone()
            assert post is not None
            print(f"Database entry: {post}")  
            assert post[1] == post_title
            assert post[2] == post_content

    # Usunięcie testowego postu i użytkownika
    with app.app_context():
        with mysql.connection.cursor() as cursor:
            cursor.execute("DELETE FROM posts WHERE title = %s AND content = %s", (post_title, post_content))
            cursor.execute("DELETE FROM users WHERE username = %s", (test_username,))
        mysql.connection.commit()
