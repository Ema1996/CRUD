from flask import Flask
from flask import render_template
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

    sql = "insert into tech(image,name,description,stock) values ('vr.img','virtual headset','is like a helm that show  virtual reality','100');"
    cursor.execute(sql)

    conn.commit()

    return render_template('products/index.html')


if __name__ == '__main__':
    app.run(debug=True)
