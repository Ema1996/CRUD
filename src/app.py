from flask import Flask
from flask import render_template, request, redirect
from flaskext.mysql import MySQL

app = Flask(__name__)
mysql = MySQL()


app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'products'

mysql.init_app(app)


@app.route('/')
def index():
    conn = mysql.connect()
    cursor = conn.cursor()

    sql = "SELECT * FROM tech;"
    cursor.execute(sql)

    tech = cursor.fetchall()

    conn.commit()

    return render_template('products/index.html', tech=tech)


@app.route('/create')
def create():
    return render_template('products/create.html')


@app.route('/store', methods=["POST"])
def store():
    _nombre = request.form["txtNombre"]
    _description = request.form["txtDescription"]
    _stock = request.form["txtStock"]
    _foto = request.files["txtFoto"]

    sql = "INSERT INTO tech (name, description, stock, image) values (%s, %s, %s, %s);"
    datos = (_nombre, _description, _stock, _foto.filename)

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()

    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
