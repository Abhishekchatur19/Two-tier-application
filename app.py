import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configure MySQL from environment variables
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'default_user')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', 'default_password')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB', 'default_db')

# Initialize MySQL
mysql = MySQL(app)

def init_db():
    with app.app_context():
        cur = mysql.connection.cursor()
        cur.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INT AUTO_INCREMENT PRIMARY KEY,
            message TEXT
        );
        ''')
        mysql.connection.commit()  
        cur.close()

@app.route('/')
def hello():
    cur = mysql.connection.cursor()
    cur.execute('SELECT message FROM messages')
    messages = cur.fetchall()
    cur.close()
    return render_template('index.html', messages=messages)

@app.route('/submit', methods=['POST'])
def submit():
    new_message = request.form.get('new_message')
    cur = mysql.connection.cursor()
    cur.execute('INSERT INTO messages (message) VALUES (%s)', [new_message])
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': new_message})
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/customers")
def customers():
    return render_template("customers.html")

@app.route("/leads")
def leads():
    return render_template("leads.html")

@app.route("/tickets")
def tickets():
    return render_template("tickets.html")

@app.route("/add-customer")
def add_customer():
    return render_template("add-customer.html")

@app.route("/reports")
def reports():
    return render_template("reports.html")

@app.route("/settings")
def settings():
    return render_template("settings.html")


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)