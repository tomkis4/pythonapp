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

# Forum
@app.route('/forum')
def forum():
    if 'loggedin' in session:
        # Pobierz posty z bazy danych
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM posts")
        posts = cur.fetchall()
        cur.close()
        return render_template('forum.html', posts=posts)
    else:
        return redirect(url_for('login'))

# Dodawanie nowego posta
@app.route('/add_post', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST' and 'loggedin' in session:
        userDetails = request.form
        post_content = userDetails['post_content']
        # Dodaj nowy post do bazy danych
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO posts(content, author) VALUES(%s, %s)", (post_content, session['username']))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('forum'))
    elif 'loggedin' in session:
        return render_template('add_post.html')
    else:
        return redirect(url_for('login'))

# Dodawanie komentarza
@app.route('/add_comment/<int:post_id>', methods=['POST'])
def add_comment(post_id):
    if request.method == 'POST' and 'loggedin' in session:
        userDetails = request.form
        comment_content = userDetails['comment_content']
        # Dodaj nowy komentarz do bazy danych
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO comments(content, post_id, author) VALUES(%s, %s, %s)", (comment_content, post_id, session['username']))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('forum'))
    else:
        return redirect(url_for('login'))

# Wylogowanie
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)





