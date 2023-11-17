from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'pragatimke'
app.config['MYSQL_DB'] = 'inventory_database'

mysql = MySQL(app)

@app.route('/')
def index():
    # Fetch data from the database
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM inventory')
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', inventory=data)

@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        item = request.form['item']
        quantity = request.form['quantity']

        # Insert data into the database
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO inventory (item, quantity) VALUES (%s, %s)', (item, quantity))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    # Delete data from the database
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM inventory WHERE id = %s', (id,))
    mysql.connection.commit()
    cur.close()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
