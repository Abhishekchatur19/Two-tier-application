import os
from flask import Flask, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', 'mysql')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'crm_user')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', 'crm_pass')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB', 'crm_db')

mysql = MySQL(app)

def init_db():
    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INT AUTO_INCREMENT PRIMARY KEY,
                message TEXT
            )
        """)
        mysql.connection.commit()
        cur.close()
    except Exception as e:
        print("DB not ready yet:", e)

@app.route("/")
def dashboard():
    init_db()
    return render_template("dashboard.html")

@app.route("/customers")
def customers():
    return render_template("customers.html")

@app.route("/leads")
def leads():
    return render_template("leads.html")

@app.route("/settings")
def settings():
    return render_template("setting.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
