from flask import Flask
from flask import render_template, request, redirect
from flaskext.mysql import MySQL
from datetime import datetime
import os

app = Flask(__name__)
mysql = MySQL()


app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'products'

UPLOADS = os.path.join('uploads')
app.config['UPLOADS'] = UPLOADS

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

    now = datetime.now()
    tiempo = now.strftime("%Y%H%M%S")

    if(_foto.filename != ''):
        nuevoNombreFoto = tiempo + '_' + _foto.filename
        _foto.save("uploads/" + nuevoNombreFoto)

    sql = "INSERT INTO tech (name, description, stock, image) values (%s, %s, %s, %s);"
    datos = (_nombre, _description, nuevoNombreFoto)

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()

    return redirect('/')


@app.route('/delete/<int:id>')
def delete(id):
    sql = "DELETE FROM tech WHERE id=%s"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, id)
    conn.commit()

    return redirect('/')


@app.route('/modify/<int:id>')
def modify(id):
    sql = f'SELECT * FROM tech WHERE id={id}'
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    item = cursor.fetchone()
    return render_template('products/edit.html', item=item)


@app.route('/update', methods=['POST'])
def update():
    _nombre = request.form["txtNombre"]
    _description = request.form["txtDescription"]
    _stock = request.form["txtStock"]
    _foto = request.files["txtFoto"]
    id = request.form['txtId']

    datos = (_nombre, _description, _stock, id)

    conn = mysql.connect()
    cursor = conn.cursor()

    if(_foto.filename != ''):
        now = datetime.now()
        tiempo = now.strftime("%Y%H%M%S")
        nuevoNombreFoto = tiempo + '_' + _foto.filename
        _foto.save("uploads/"+nuevoNombreFoto)

    sql = f'SELECT image FROM tech WHERE id={id}'
    cursor.execute(sql)

    nombreFoto = cursor.fetchone()[0]

    os.remove(os.path.join(app.config['UPLOADS'], nombreFoto))

    conn = mysql.connect()
    cursor = conn.cursor()

    sql = f'UPDATE tech SET name={_nombre}, description={_description}, stock={_stock} WHERE id={id}'

    cursor.execute(sql)
    conn.commit()


if __name__ == '__main__':
    app.run(debug=True)
