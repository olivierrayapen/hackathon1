from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        dbname="book_recommendation",
        user="postgres",
        password="Olivier11",
        host="localhost"
    )
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM books')
    books = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', books=books)

@app.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (username, email) VALUES (%s, %s)", (username, email))
        conn.commit()
        cur.close()
        conn.close()
        return redirect('/')
    return render_template('register.html')

@app.route('/rate', methods=('GET', 'POST'))
def rate():
    if request.method == 'POST':
        user_id = request.form['user_id']
        book_id = request.form['book_id']
        rating = request.form['rating']
        review = request.form['review']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO ratings (user_id, book_id, rating, review) VALUES (%s, %s, %s, %s)",
            (user_id, book_id, rating, review)
        )
        conn.commit()
        cur.close()
        conn.close()
        return redirect('/')
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM users')
    users = cur.fetchall()
    cur.execute('SELECT * FROM books')
    books = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('rate.html', users=users, books=books)

if __name__ == '__main__':
    app.run(debug=True)
