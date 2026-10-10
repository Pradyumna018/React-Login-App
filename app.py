from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # allows requests from React (port 3000)

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",              # or your dedicated user (e.g., reactuser)
    password="Subha@1992",    # your MySQL password
    database="react"          # your database name
)
cursor = conn.cursor(dictionary=True)

# Root route for testing
@app.route('/')
def home():
    return "✅ Flask backend is running successfully!"

# Signup route
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"status": "fail", "message": "Username and password required"}), 400

    cursor.execute("SELECT * FROM react_table WHERE username=%s", (username,))
    if cursor.fetchone():
        return jsonify({"status": "fail", "message": "User already exists"}), 409

    cursor.execute("INSERT INTO react_table (username, password) VALUES (%s, %s)", (username, password))
    conn.commit()
    return jsonify({"status": "success", "message": "User registered successfully"}), 201

# Login route
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    cursor.execute("SELECT * FROM react_table WHERE username=%s AND password=%s", (username, password))
    user = cursor.fetchone()

    if user:
        return jsonify({"status": "success", "message": f"Welcome to PKM Live Family, {username}"}), 200
    return jsonify({"status": "fail", "message": "Invalid credentials"}), 401

# View all users
@app.route('/users', methods=['GET'])
def get_users():
    cursor.execute("SELECT username FROM react_table")
    users = cursor.fetchall()
    return jsonify(users), 200

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
