import os
from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', 'mysql')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'crm_user')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', 'crm_pass')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB', 'crm_db')

mysql = MySQL(app)

def init_db():
    cur = mysql.connection.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INT AUTO_INCREMENT PRIMARY KEY,
            message TEXT
        )
    """)
    mysql.connection.commit()
    cur.close()

# ---------- CRM UI ROUTES ----------

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

# ---------- API ROUTES ----------

@app.route('/submit', methods=['POST'])
def submit():
    new_message = request.form.get('new_message')
    cur = mysql.connection.cursor()
    cur.execute('INSERT INTO messages (message) VALUES (%s)', (new_message,))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': new_message})

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
