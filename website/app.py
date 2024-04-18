from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL

app = Flask(__name__)

# Ustawienie klucza tajnego
app.secret_key = 'super_secret_key'

# Konfiguracja bazy danych
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # Twój użytkownik MySQL
app.config['MYSQL_PASSWORD'] = ''  # Twoje hasło MySQL
app.config['MYSQL_DB'] = 'python'  # Nazwa bazy danych

mysql = MySQL(app)

# Strona główna
@app.route('/')
def index():
    return render_template('index.html')

# Rejestracja
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Pobierz dane z formularza
        userDetails = request.form
        username = userDetails['username']
        password = userDetails['password']

        try:
            # Sprawdź czy użytkownik już istnieje
            cur = mysql.connection.cursor()
            result = cur.execute("SELECT * FROM users WHERE username = %s", (username,))
            if result > 0:
                return 'Użytkownik już istnieje.'
            else:
                # Zapisz dane do bazy danych
                cur.execute("INSERT INTO users(username, password) VALUES(%s, %s)", (username, password))
                mysql.connection.commit()
                cur.close()
                return redirect(url_for('login'))
        except Exception as e:
            return f'Wystąpił błąd podczas rejestracji: {str(e)}'

    return render_template('register.html')

# Logowanie
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Pobierz dane z formularza
        userDetails = request.form
        username = userDetails['username']
        password = userDetails['password']

        try:
            # Sprawdź czy użytkownik istnieje w bazie danych
            cur = mysql.connection.cursor()
            result = cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
            if result > 0:
                session['loggedin'] = True
                session['username'] = username
                return redirect(url_for('forum'))
            else:
                return 'Niepoprawne dane logowania. Spróbuj ponownie.'
        except Exception as e:
            return f'Wystąpił błąd podczas logowania: {str(e)}'

    return render_template('login.html')

# Strona dodawania postu
@app.route('/add_post', methods=['GET', 'POST'])
def add_post():
    if 'loggedin' in session:
        if request.method == 'POST':
            userDetails = request.form
            post_title = userDetails['post_title']
            post_content = userDetails['post_content']
            # Dodaj nowy post do bazy danych
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO posts(title, content, user_id) VALUES(%s, %s, (SELECT user_id FROM users WHERE username = %s))", (post_title, post_content, session['username']))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('forum'))
        else:
            return render_template('add_post.html')
    else:
        return redirect(url_for('login'))

# Endpoint forum
@app.route('/forum')
def forum():
    print("Funkcja widoku forum została wywołana.")  # Dodatkowe drukowanie w celu debugowania

    if 'loggedin' in session:
        try:
            # Pobierz wszystkie posty z bazy danych
            cur = mysql.connection.cursor()
            cur.execute("SELECT posts.title, posts.content, users.username AS author, posts.created_at FROM posts JOIN users ON posts.user_id = users.user_id ORDER BY posts.created_at DESC")
            posts = cur.fetchall()
            cur.close()

            # Dodatkowe drukowanie w celu debugowania
            print(posts)

            # Przekazanie listy postów do szablonu forum.html
            return render_template('forum.html', posts=posts)
        except Exception as e:
            return f'Wystąpił błąd podczas pobierania postów: {str(e)}'
    else:
        return redirect(url_for('login'))



# Wylogowanie
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)






