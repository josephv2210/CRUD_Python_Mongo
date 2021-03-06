from tkinter import*
from tkinter import ttk
from tkinter import messagebox
from bson.objectid import ObjectId

import pymongo  # Se importa pymongo

MONGO_HOST = "localhost"  # direccion del host, en este caso local
MONGO_PUERTO = "27017"  # puerto
MONGO_TIEMPO_FUERA = 1000  # Tiempo que python espera para conectarse a la base de datos

MONGO_URI = "mongodb://"+MONGO_HOST+":"+MONGO_PUERTO+"/"  # Crear una URL

# Para generar una conexion a la base de datos y a la coleccion necesitamos lo siguiente
MONGO_BASEDATOS = "escuela"
MONGO_COLECCION = "alumnos"
cliente = pymongo.MongoClient(
    MONGO_URI, serverSelectionTimeoutMS=MONGO_TIEMPO_FUERA)  # Se crea el cliente
# me conecto a mi base de datos y obtenemos un objeto dentro de la variable
baseDatos = cliente[MONGO_BASEDATOS]
# desde dentro de la base de datos accedo a mi coleccion
coleccion = baseDatos[MONGO_COLECCION]
ID_ALUMNO = ""


def mostrarDatos():
    try:
        registros = tabla.get_children()
        for registro in registros:
            tabla.delete(registro)

        for documento in coleccion.find():  # Con esto vemos todos los documentos de nuestra coleccion
            # Ahora en vez de imprimir desde consola vamos a imprimir dentro de la tabla
            tabla.insert(
                '', 0, text=documento["_id"], values=documento["nombre"])

            # print(documento["nombre"]+" "+documento["sexo"]+" "+str(documento["calificacion"]))#Esto me trae todos los registros
        # cliente.server_info()  # Se hace la conexion
        # print("Conexion a mongo exitosa")
        cliente.close()  # Se cierra la conexion
    except pymongo.errors.ServerSelectionTimeoutError as errorTiempo:
        print("Tiempo exedido"+errorTiempo)  # error de tiempo
    except pymongo.errors.ConnectionFailure as errorConexion:
        print("Fallo al conectarse a mongodb " +
              errorConexion)  # error de conexion


def crearRegistro():
    # Verificamos que todos los campos esten llenos
    if len(nombre.get()) != 0 and len(calificacion.get()) != 0 and len(sexo.get()) != 0:
        try:
            documento = {"nombre": nombre.get(
            ), "calificacion": calificacion.get(), "sexo": sexo.get()}
            coleccion.insert(documento)
            nombre.delete(0, END)
            sexo.delete(0, END)
            calificacion.delete(0, END)
        except pymongo.errors.ConnectionFailure as error:
            print(error)
    else:
        messagebox.showerror(message="Los campos no pueden estar vacios")
    mostrarDatos()


def dobleCickTabla(event):
    global ID_ALUMNO  # ponemos el ID_ALUMNO como global
    # le damos a ID_Alumno el id del elemento seleccionado
    ID_ALUMNO = str(tabla.item(tabla.selection())["text"])
    # print(ID_ALUMNO)
    documento = coleccion.find({"_id": ObjectId(ID_ALUMNO)})[
                               0]  # obtenemos el _id
    # Accedemos a los datos para guardarlos
    nombre.delete(0, END)
    nombre.insert(0, documento["nombre"])
    sexo.delete(0, END)
    sexo.insert(0, documento["sexo"])
    calificacion.delete(0, END)
    calificacion.insert(0, documento["calificacion"])
    crear["state"] = "disabled"
    editar["state"] = "normal"
    borrar["state"] = "normal"


def editarRegistro():
    global ID_ALUMNO
    # Validamos que los campos no esten vacios
    if len(nombre.get()) != 0 and len(sexo.get()) != 0 and len(calificacion.get()) != 0:
        try:
            idBuscar = {"_id": ObjectId(ID_ALUMNO)}
            nuevosValores = {"nombre": nombre.get(
            ), "sexo": sexo.get(), "calificacion": calificacion.get()}
            coleccion.update(idBuscar, nuevosValores)
            nombre.delete(0, END)
            sexo.delete(0, END)
            calificacion.delete(0, END)
        except pymongo.errors.ConnectionFailure as error:
            print(error)
    else:
        messagebox.showerror("Los campos no pueden estar vacios")
    mostrarDatos()
    crear["state"] = "normal"
    editar["state"] = "disabled"
    borrar["state"] = "disabled"

def borrarRegistro():
    global ID_ALUMNO

    try:
        #Pasamos el id a buscar
        idBuscar={"_id":ObjectId(ID_ALUMNO)}
        coleccion.delete_one(idBuscar)
        nombre.delete(0, END)
        sexo.delete(0, END)
        calificacion.delete(0, END)
    except pymongo.errors.ConnectionFailure as error:
        print(error)
    mostrarDatos()
    crear["state"] = "normal"
    editar["state"] = "disabled"
    borrar["state"] = "disabled"

ventana = Tk()  # crear una ventana
tabla = ttk.Treeview(ventana, columns=2)  # Creamos una tabla en forma de arbol

tabla.grid(row=1, column=0, columnspan=2)  # definimos la posicion de la tabla
tabla.heading("#0", text="ID")  # cabezeras
tabla.heading("#1", text="NOMBRE")  # cabezeras
# Registrar el click
tabla.bind("<Double-Button-1>", dobleCickTabla)

# Entrys
# Nombre
Label(ventana, text="Nombre").grid(row=2, column=0)
nombre = Entry(ventana)
nombre.grid(row=2, column=1)
# Sexo
Label(ventana, text="Sexo").grid(row=3, column=0)
sexo = Entry(ventana)
sexo.grid(row=3, column=1)
# Calificacion
Label(ventana, text="Calificacion").grid(row=4, column=0)
calificacion = Entry(ventana)
calificacion.grid(row=4, column=1)
# Boton crear
crear = Button(ventana, text="Crear alumno",
               command=crearRegistro, bg="#8aed3a", fg="black")
crear.grid(row=5, columnspan=2)

# Boton editar
editar = Button(ventana,text="Editar alumno", command=editarRegistro, bg="yellow", fg="black")
editar.grid(row=6, columnspan=2)
editar["state"] = "disable"

# Boton borrar
borrar = Button(ventana,text="Borrar alumno", command=borrarRegistro, bg="#ff0029", fg="white")
borrar.grid(row=7, columnspan=2)
borrar["state"] = "disable"

mostrarDatos()
ventana.mainloop()  # ciclo principal, la ventana va a estar tomando el control del programa
