# pip install bcrypt
# pip install sqlite3

# Import necessary modules
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from passlib.hash import bcrypt_sha256 # For password hashing
import sqlite3 # For SQLite database interaction
from flask_cors import CORS  # For handling cross-origin request
from flask_limiter import Limiter # For rate limiting (avoid "click spamming") 

# Create a Flask app instance
app = Flask(__name__)

# Apply CORST to our Flask app
CORS(app)  # Enable the frontend, hosted on a different server, to communicate with backend
           # We can change "/login" for "http://backend.com/login" in the frontend

# Initialize Flask-Limiter
# limiter = Limiter(app, key_func=lambda: session.get("username", ""))
# limiter = Limiter(app, key_func=lambda: request.remote_addr)  # Use IP address as the rate limiting

# Configure secret key for session management (needed for a certain Flask features)
app.secret_key = "your_secret_key"

# Set the session cookie domain
# app.config['SESSION_COOKIE_DOMAIN'] = '.example.com'

# Function to estabilish a connctior to the SQLite database
def get_db_connection():
    conn = sqlite3.connect('database.sqlite')  # Connect to the SQLite database
    conn.row_factory = sqlite3.Row  # Access query results as rows
    return conn  # Return the connection object

# Create the 'users' table if it does not exist
def create_users_table():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
                 id INTERGER PRIMARY KEY,
                 username TEXT NOT NULL UNIQUE,
                 password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


# Route for the homepage
@app.route('/')
def home():
    return render_template('index.html')  # Render the index.html template


# Route for handing the login POST request
@app.route('/login', methods=['POST'])
# @limiter.limit("5 per minute")  # Allow only 5 requests per minute
def login():
    #  Get username and password from the JSON request body
    username = request.json.get('username')
    password = request.json.get('password')

    # Estabilish a connection to the SQLite database
    conn = get_db_connection()

    # Fetch user details from the database based on the provided username
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()

    # Close the database connection
    conn.close()

    # Check if the user exists and the provideed password matches the hashed password
    if user and bcrypt_sha256.verify(password, user['password']):

        session["username"] = username  # Store username in session 

        return jsonify({'success': True, 'message': 'Login is successful!'}), 200  # Return sucess response if login is successful
    else:
        return jsonify({'success': False, 'message': 'Username or password is incorrect.'}), 400  # Return failure response if login fails


@app.route('/register', methods=['POST'])
# @limiter.limit("5 per minute")  # Allow only 5 requests per minute
def register():
    # Get username, password and e-mail from the JSON request body
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        return jsonify({'success': False, 'message': 'Both username and password are required.'}), 400
    if len(password) < 6:
        return jsonify({'success': False, 'message': 'Password must be greater than 6 characters.'}), 400
    
    # Check if user already exists
    conn = get_db_connection()  # Estabilish a connection to the SQLite database
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()  # Fetch user details from the database
    conn.close()  # Close the database connection
    if user: return jsonify({'success': False, 'message': 'The user already exists.'}), 400

    # Hash the password
    hashed_password = bcrypt_sha256.hash(password)

    # Estabilish a connection to the SQLite database
    conn = get_db_connection()

    try:
        # Insert the new user into the database
        conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Account created!'}), 200  # Return success response if registration is successful
    except Exception as e: 
        print(e)
        conn.rollback()
        conn.close()
        return jsonify({'success': False, 'message': 'An error ocurred during the registration.'}), 500
    finally:
        conn.close()


# Route for the dashboard
@app.route("/dashboard")
def dashboard():
    if "username" in session:   # Check if user is logged in
        return render_template("dashboard.html", username=session["username"])
    else:
        return redirect(url_for("index"))  # Redirect to index if not logged in
    

@app.route("/logout", methods=['GET'])
# @limiter.limit("5 per minute")  # Allow only 5 requests per minute
def logout():
    session.pop("username", None)  # Remove username from session
    return jsonify({'success': True, 'message': 'Logout is successful!'}), 200


@app.route("/criandoUmModeloDeInvestimento", methods=['PUT'])
def criandoUmModeloDeInvestimento():
    if "username" in session or True:   # Check if user is logged in
        params = request.get_json()
        print('params', params)
        # We will run our investing model
        try:
            from CriandoUmModeloDeInvestimento import criandoUmModeloDeInvestimento
            resultado = criandoUmModeloDeInvestimento(params)
            print(resultado)
            print('json', jsonify({'success': True, 'message': 'Successful!', 'resultado': resultado}))
            return jsonify({'success': True, 'message': 'Successful!', 'resultado': resultado}), 200
        except Exception as e:
            return jsonify({'success': False, 'message': 'Error.'}), 400
    else:
        return jsonify({'success': False, 'message': 'Not Logged!'}), 400  # Redirect to index if not logged in


@app.route("/pegadoDadosEmSitesAutomatizarCriacaoCarteira", methods=['PUT'])
def pegarDadosEmSitesAutomatizarCriacaoCarteira():
    if "username" in session or True:   # Check if user is logged in
        params = request.get_json()
        print('params', params)
        # We will run our investing model
        try:
            from PegarDadosEmSitesAutomatizarCriacaoCarteira import pegarDadosEmSitesAutomatizarCriacaoCarteira
            resultado = pegarDadosEmSitesAutomatizarCriacaoCarteira()
            print(resultado)
            print('json', jsonify({'success': True, 'message': 'Successful!', 'resultado': resultado}))
            return jsonify({'success': True, 'message': 'Successful!', 'resultado': resultado}), 200
        except Exception as e:
            return jsonify({'success': False, 'message': 'Error.'}), 400
    else:
        return jsonify({'success': False, 'message': 'Not Logged!'}), 400  # Redirect to index if not logged in


# Run the Flask app if the script is executed directly
if __name__ == '__main__':
    create_users_table()
    app.run(debug=True)