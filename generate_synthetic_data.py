import psycopg2
from faker import Faker

fake = Faker()

# Connect to the database
conn = psycopg2.connect(
    dbname="book_recommendation",
    user="postgres",
    password="Olivier11",
    host="localhost"
)
cur = conn.cursor()

# Generate synthetic users
for _ in range(10):
    username = fake.user_name()
    email = fake.email()
    cur.execute("INSERT INTO users (username, email) VALUES (%s, %s)", (username, email))

# Generate synthetic books
for _ in range(50):
    title = fake.sentence(nb_words=4)
    author = fake.name()
    genre = fake.word()
    description = fake.paragraph(nb_sentences=5)
    cover_image_url = fake.image_url()
    cur.execute(
        "INSERT INTO books (title, author, genre, description, cover_image_url) VALUES (%s, %s, %s, %s, %s)",
        (title, author, genre, description, cover_image_url)
    )

conn.commit()
cur.close()
conn.close()
