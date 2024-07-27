import pandas as pd
import psycopg2

def get_db_connection():
    conn = psycopg2.connect(
        dbname="book_recommendation",
        user="postgres",
        password="Olivier11",
        host="localhost"
    )
    return conn

def fetch_ratings():
    conn = get_db_connection()
    query = """
    SELECT u.username, b.title, r.rating
    FROM ratings r
    JOIN users u ON r.user_id = u.user_id
    JOIN books b ON r.book_id = b.book_id;
    """
    ratings_df = pd.read_sql_query(query, conn)
    conn.close()
    return ratings_df

def recommend_books(user, ratings_df):
    user_ratings = ratings_df.pivot_table(index='username', columns='title', values='rating')
    user_ratings = user_ratings.fillna(0)
    user_similarity = user_ratings.corrwith(user_ratings.loc[user])
    similar_users = user_similarity.sort_values(ascending=False).index[1:]
    recommended_books = []

    for similar_user in similar_users:
        similar_user_ratings = user_ratings.loc[similar_user]
        similar_user_unread_books = similar_user_ratings[similar_user_ratings == 0].index
        user_read_books = user_ratings.loc[user][user_ratings.loc[user] > 0].index
        recommendations = [book for book in similar_user_unread_books if book not in user_read_books]
        recommended_books.extend(recommendations)
        
        if len(recommended_books) >= 5:
            break

    return recommended_books[:5]

