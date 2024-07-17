from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Esea.123'
app.config['MYSQL_DB'] = 'biblioteca_db'
mysql = MySQL(app)

app.secret_key = "mysecretkey"

@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM autores')
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', autores = data)


@app.route('/add_autor', methods=['POST'])
def add_autor():
    if request.method == 'POST':
       nombre = request.form['nombre']
       nacionalidad = request.form['nacionalidad']
       print(nombre)
       print(nacionalidad)
       cur = mysql.connection.cursor()
       cur.execute('INSERT INTO autores (nombre, nacionalidad) VALUES (%s, %s)',
        (nombre, nacionalidad)) 
       mysql.connection.commit()
       flash('Autor agregado satisfactoriamente')
       return redirect(url_for('Index'))
    
  

@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit_autor(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        nacionalidad = request.form['nacionalidad']
        try:
            cur = mysql.connection.cursor()
            cur.execute('UPDATE Autores SET Nombre = %s, Nacionalidad = %s WHERE idAutor = %s', (nombre, nacionalidad, id))
            mysql.connection.commit()
            flash('Autor actualizado satisfactoriamente')
        except Exception as e:
            print(f"Error: {e}")
            flash('Ocurrió un error al actualizar el autor')
        return redirect(url_for('Index'))
    else:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM Autores WHERE idAutor = %s', (id,))
        data = cur.fetchone()
        cur.close()
        return render_template('modcautor.html', autor=data)

@app.route('/delete/<string:id>')
def delete_autor(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM Autores WHERE idAutor = %s', [id])
        mysql.connection.commit()
        flash('Contacto eliminado satisfactoriamente')
    except Exception as e:
        print(f"Error: {e}")
        flash('Ocurrió un error al eliminar el autor')
    return redirect(url_for('Index'))

if __name__=='__main__':
    app.run(port = 5000, debug=True)
    
