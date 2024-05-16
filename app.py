from flask import Flask
from flask import render_template 
from flask import url_for
from flask import request                       #recepciona la informacion
from flask import redirect                      #redirecciona 

import pymysql
from datetime import datetime



       
app = Flask(__name__)


#Inicio conexion a la base de datos
conexion = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='biblioteca'
)

cursor = conexion.cursor()

# Realiza consultas y operaciones de base de datos utilizando el cursor
#cursor.execute("SELECT * FROM tabla")

# Confirma y ejecuta la sentencia SQL
#conn.commit()

#cursor.close()
#conn.close()

#Fin conexion a la base de datos



@app.route('/')
def inicio():
    """ se crean las rutas de navegacion """
    print(url_for('inicio'))
    print(url_for('libros'))
    return render_template('sitio/index.html')


@app.route('/libros')
def libros():
    return render_template('sitio/libros.html')

@app.route('/admin')
def admin_index():
    return render_template('admin/index.html')

@app.route('/admin/login')
def admin_login():
    return render_template('admin/login.html')

@app.route('/admin/libros')
def admin_libros():

    cursor.execute("SELECT * FROM libros")
    libros = cursor.fetchall() # recibe todos los datos de la consulta
    conexion.commit() # Ejecuta 
    print(libros)        

  
    return render_template('admin/libros.html',listaLibros = libros)

@app.route('/admin/libros/guardar', methods=['POST']) # Recibe los datos enviados por POST
def admin_libros_guardar():

    nombre = request.form['nombreLibro']
    imagen = request.files['imagenLibro']
    url = request.form['urlDescarga']

    #variable tiempo para cambiar el nombre de la imagen
    tiempo = datetime.now()
    horaActual = tiempo.strftime('%Y%H%M%S')

    #cambio de nombre de la imagen y guardado
    if imagen.filename!="":
        nuevoNombreImagen = f"{horaActual}_{imagen.filename}"
        imagen.save("templates/sitio/img/libros"+nuevoNombreImagen)


    #insert a base de datos
    sql = "INSERT INTO `libros` (`nombre_libro`, `imagen_libro`, `url_libro`) VALUES (%s,%s,%s);"
    datos = (nombre,nuevoNombreImagen,url)  #Agregamos los datos a la consulta
    cursor = conexion.cursor()  #creamos un objeto
    cursor.execute(sql,datos) #ejecutamos el objeto con la consulta y los datos recibidos
    conexion.commit() #confirmamos la ejecucion 

    return redirect('/admin/libros')

@app.route('/admin/libros/borrar',methods=['POST'])
def admin_libros_borrar():  

    id_libro = request.form['id_libro']

    #solo hace la consulta
    cursor.execute("SELECT * FROM libros WHERE id_libro = %s",(id_libro))
    libro = cursor.fetchall()
    conexion.commit()
    print(libro)
    #fin de la consulta

    #Eliminacion de registro
    cursor.execute("DELETE FROM libros WHERE id_libro = %s",(id_libro) )  
    conexion.commit() #confirmamos ejecucion
    #Fin de eliminacion registro
   



    return redirect('/admin/libros')

if __name__ == '__main__':
    app.run(debug=True)



