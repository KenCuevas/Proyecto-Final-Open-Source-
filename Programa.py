from tkinter import *
from tkinter import ttk

import sqlite3
from datetime import datetime


raiz = Tk()
raiz.geometry("400x200")
raiz.title("Home")

db_name = 'Practica4.db'
w, h = raiz.winfo_screenwidth(), raiz.winfo_screenheight()


#TopLevel
def toplevel(titulo, campos):
    top = Toplevel() 
    top.geometry("%dx%d+0+0" % (w, h))
    top.title(titulo) 
    frame = LabelFrame(top, text = 'Registrar '+ titulo)
    frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)


    def run_query(query, parameters = ()):
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    #Llenar tabla
    def llenartabla(titulo, top):
        #Limpiando tabla
        records = top.tree.get_children()
        for element in records:
            top.tree.delete(element)
        #Llamando información
        query = "SELECT * FROM " + titulo + ";"
        db_rows = run_query(query)
        #Llenando información
        for row in db_rows:
            top.tree.insert('', 'end', values = row)
    
        #Eliminarimport os.path
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import webbrowser
import os

app = Tk()
app.title("Sistema de calificaciones estudiantiles")
app.geometry("800x350")

vVentana = str()
vCampos = {}
query=str()

#Nombre de la base de datos
db_name = 'Practica4.db'


w, h = app.winfo_screenwidth(), app.winfo_screenheight()

#Toplevel
def toplevel(vVentana, vCampos):
    top = Toplevel() 
    top.geometry("%dx%d+0+0" % (w, h))
    top.title(vVentana) 
    frame = LabelFrame(top, text = 'Registrar '+ vVentana)
    frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)

    render_form(vCampos, top, frame)
    ttk.Button(frame, text = 'Guardar ' + vVentana, command = lambda: agregar(vVentana, vCampos, top)).grid(row = len(vCampos)+1, columnspan = 2, sticky = W + E)
    tabla(vCampos, top)
    llenartabla(vVentana, top)
    #Botones eliminar, editar y generar
    ttk.Button(top, text = 'ELIMINAR', command = lambda: eliminar(vVentana, vCampos, top)).grid(row = len(vCampos)+1, column = 0, sticky = W + E)
    ttk.Button(top, text = 'EDITAR', command = editar).grid(row = len(vCampos)+1, column = 1, sticky = W + E)
    #ttk.Button(top, text = 'GENERAR HTML', command = generarhtml).grid(row = len(vCampos)+2, column = 0, sticky = W + E)

#Formularios renderizados
def render_form(vCampos, top, frame):
    for (i, (id_campo, campo)) in enumerate(vCampos.items()):
        Label(frame, text = campo["label"]).grid(row = i, column = 0)
        vCampos[id_campo]["entry"] = Entry(frame)
        vCampos[id_campo]["entry"].focus()
        vCampos[id_campo]["entry"].grid(row = i, column = 1) 

#Tabla
def tabla(vCampos, top):
    top.tree = ttk.Treeview(top, height = 10, columns = [ campo["label"] for campo in vCampos.values()])
    top.tree.column("#0", width=0)
    top.tree.grid(row = len(vCampos.items()), column = 0, columnspan = 2)

    for (id_campo, campo) in vCampos.items():
        top.tree.heading(campo["label"], text = campo["label"], anchor = CENTER)

#Leer
def llenartabla(vVentana, top):
    #Limpiando tabla
    records = top.tree.get_children()
    for element in records:
        top.tree.delete(element)
    #Llamando información
    query = "SELECT * FROM " + vVentana + ";"
    db_rows = run_query(query)
    #Llenando información
    for row in db_rows:
        top.tree.insert('', 'end', values = row)

#Agregar
def agregar(vVentana, vCampos, top):
    parameters = []
    query = f'INSERT INTO {vVentana} VALUES('
      
    for key in range(len(dict.keys(vCampos))):
        query += '?'
        parametro = (list( dict.keys( vCampos ) )[ key ])
        entry = vCampos[parametro]["entry"]
        parameters.append(entry.get())
        entry.delete(0, END)   
        if key != len(dict.keys(vCampos)) - 1:
            query += ','

    query += ')'
    print(query)
    run_query(query, parameters)
    llenartabla(vVentana, top)
    Message(top, text="agregado correctamente")


def editar():
    print('editado')

def eliminar(vVentana, vCampos, top):
    vTitulo = vVentana
    vCondicion = list( dict.keys( vCampos ) )[ 0 ]
    try:
      curItem = top.tree.item(top.tree.focus())
      valor = curItem['values'][0]
    except IndexError as e:
      print("Selecciona una registro")
      return
               
    query = f'DELETE FROM {vTitulo} WHERE {vCondicion} = ?'
    run_query(query, (valor, ))
    llenartabla(vTitulo, top)

def generarhtml():
    print("generado")

def run_query(query, parameters = ()):
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        result = cursor.execute(query, parameters)
        conn.commit()
    return result


#Informacion
def estudiantes():
    vVentana="Estudiante"
    vCampos = {      
      "Matricula": {
        "label": "Matricula",
      },
      "Nombre": {
        "label": "Nombre", 
      },
      "Sexo": {
        "label": "Sexo"
      },
    }
    toplevel(vVentana, vCampos)

def materias():
    vVentana="Materia"
    vCampos={
      "Nombre": {
        "label": "Nombre",
      },
      "Creditos": {
        "label": "Creditos",
      }
    }
    toplevel(vVentana, vCampos)

def calificaciones():
    vVentana="Calificacion"
    vCampos= {
      "Id": {
        "label":"Id"
      },
      "practica 1": {
        "label": "practica 1",
      },
      "practica 2": {
        "label": "practica 2",
      },
      "foro 1": {
        "label": "foro 1",
      },
      "foro 2":  {
        "label":"foro 2",
      },
      "primer parcial": {
        "label": "primer parcial",
      },
      "segundo parcial":  {
        "label":"segundo parcial",
      },
      "examen final": {
        "label": "examen final",
      },
      "Materia": {
        "label": "Materia",
      },
      "Matricula": {
        "label": "Matricula"
      }
    }
    toplevel(vVentana, vCampos)

# Crear el menu principal
menubarra = Menu(app)
menubarra.add_command(label="Estudiantes", command=estudiantes)
menubarra.add_command(label="Materias", command=materias)
menubarra.add_command(label="Calificaciones", command=calificaciones)


# Mostrar el menu
app.config(menu=menubarra)

# Mostrar la ventana
app.mainloop()

    def eliminar():
        if titulo == "Estudiante":
            vCondicion = "Matricula"
        elif titulo == "Materia":
            vCondicion = "Nombre"
        elif titulo == "Calificacion":
            vCondicion = "Id"
        
        try:
            curItem = top.tree.item(top.tree.focus())
            valor = curItem['values'][0]
        except IndexError as e:
            print("Selecciona una registro")
            return
               
        query = f'DELETE FROM {titulo} WHERE {vCondicion} = ?'
        run_query(query, (valor, ))
        llenartabla(titulo, top)

    #Editar
    def editar():
        print("Editar")

    #Agregar
    def agregar():
        
        if titulo == "Estudiante":
            query = 'INSERT INTO Estudiante VALUES(?, ?, ?)'
            parameters =  (top.matricula.get(), top.nombre.get(), top.sexo.get())
            top.matricula.delete(0, END)
            top.nombre.delete(0, END)
            top.sexo.delete(0, END)
        elif titulo == "Materia":
            query = 'INSERT INTO Materia VALUES(?, ?)'
            parameters = (top.materia.get(), top.credito.get())
            top.materia.delete(0, END)
            top.credito.delete(0, END)
        elif titulo == "Calificacion":
            query = 'INSERT INTO Calificacion VALUES(NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
            parameters = (top.practica1.get(), top.practica2.get(), top.foro1.get(), top.foro2.get(), top.parcial1.get(), top.parcial2.get(), top.examenfinal.get(), top.materia.get(), top.matricula.get())
            top.practica1.delete(0, END)
            top.practica2.delete(0, END)
            top.foro1.delete(0, END)
            top.foro2.delete(0, END)
            top.parcial1.delete(0, END)
            top.parcial2.delete(0, END)            
            top.examenfinal.delete(0, END)
            top.materia.delete(0, END)
            top.matricula.delete(0, END)            

        run_query(query, parameters)
        llenartabla(titulo, top)
        Message(top, text="agregado correctamente")

        
    def html_create(result):
        now = datetime.now()
        template = open("template.html","r")
        output = open("us.html","w")
        text = template.read().format(get_result = result, date = now)
        html = output.write(text)
        template.close()
        output.close()

    def datoshtml():
        html_create("hola mundo")


    if titulo == "Estudiante":
        #Matricula Input
        Label(frame, text = 'Matricula: ').grid(row = 1, column = 0)
        top.matricula = Entry(frame)
        top.matricula.focus()
        top.matricula.grid(row = 1, column = 1)

        #Nombre Input
        Label(frame, text = 'Nombre: ').grid(row = 2, column = 0)
        top.nombre = Entry(frame)
        top.nombre.grid(row = 2, column = 1)

        #Sexo Input
        Label(frame, text = 'Sexo: ').grid(row = 3, column = 0)
        top.sexo = Entry(frame)
        top.sexo.grid(row = 3, column = 1)

        #Boton para generar reporte
        ttk.Button(top, text = 'GENERAR REPORTE HTML ', command = datoshtml).grid(row = len(campos)+5, columnspan = 2)    
        

    elif titulo == "Materia":
        print("Materias")
        #Materia Input
        Label(frame, text = 'Materia: ').grid(row = 1, column = 0)
        top.materia = Entry(frame)
        top.materia.focus()
        top.materia.grid(row = 1, column = 1)

        #Credito Input
        Label(frame, text = 'Creditos: ').grid(row = 2, column = 0)
        top.credito = Entry(frame)
        top.credito.grid(row = 2, column = 1) 

    elif titulo == "Calificacion":
        print("Calificaciones")
        #Practica 1
        Label(frame, text = 'Practica 1: ').grid(row = 1, column = 0)
        top.practica1 = Entry(frame)
        top.practica1.focus()
        top.practica1.grid(row = 1, column = 1)

        #Practica 2 
        Label(frame, text = 'Practica 2: ').grid(row = 2, column = 0)
        top.practica2 = Entry(frame)
        top.practica2.grid(row = 2, column = 1) 

        #Foro 1
        Label(frame, text = 'Foro 1: ').grid(row = 3, column = 0)
        top.foro1 = Entry(frame)
        top.foro1.grid(row = 3, column = 1) 

        #Foro 2
        Label(frame, text = 'Foro 2: ').grid(row = 4, column = 0)
        top.foro2 = Entry(frame)
        top.foro2.grid(row = 4, column = 1) 

        #Primer parcial
        Label(frame, text = 'Primer parcial: ').grid(row = 5, column = 0)
        top.parcial1 = Entry(frame)
        top.parcial1.grid(row = 5, column = 1) 

        #Segundo parcial
        Label(frame, text = 'Segundo parcial ').grid(row = 6, column = 0)
        top.parcial2 = Entry(frame)
        top.parcial2.grid(row = 6, column = 1) 

        #Examen final
        Label(frame, text = 'Examen final: ').grid(row = 7, column = 0)
        top.examenfinal = Entry(frame)
        top.examenfinal.grid(row = 7, column = 1) 

        #Materia final
        Label(frame, text = 'Materia: ').grid(row = 8, column = 0)
        top.materia = Entry(frame)
        top.materia.grid(row = 8, column = 1) 

        #Matricula final
        Label(frame, text = 'Matricula: ').grid(row = 9, column = 0)
        top.matricula = Entry(frame)
        top.matricula.grid(row = 9, column = 1) 

    #Boton para añadir
    ttk.Button(frame, text = 'Guardar ' + titulo, command = agregar).grid(row = len(campos)+1, columnspan = 2, sticky = W + E)    

    #Tabla
    top.tree = ttk.Treeview(top, height = 10, columns = campos)
    top.tree.column("#0", width=0)
    top.tree.grid(row = len(campos), column = 0, columnspan = 2)

    for i in range(0, len(campos)):
        top.tree.heading(campos[i], text = campos[i], anchor = CENTER)


    #Botones eliminar y editar
    ttk.Button(top, text = 'ELIMINAR', command = eliminar).grid(row = len(campos)+1, column = 0, sticky = W + E)
    ttk.Button(top, text = 'EDITAR', command = editar).grid(row = len(campos)+1, column = 1, sticky = W + E)



    # Filling the Rows
    llenartabla(titulo, top)

global title

#Estudiantes
def estudiantes():
    title="Estudiante"
    campos=["Matricula","Nombre", "Sexo"]
    toplevel(title, campos)

#Materias
def materias():
    title="Materia"
    campos=["Materia", "Creditos"]
    toplevel(title, campos)

#Calificaciones
def calificaciones():
    title="Calificacion"
    campos=["Id","practica 1", "practica 2", "foro 1", "foro 2", "primer parcial", "segundo parcial", "examen final", "Materia", "Matricula"]
    toplevel(title, campos)




# Crear el menu principal
menubarra = Menu(raiz)
menubarra.add_command(label="Estudiantes", command=estudiantes)
menubarra.add_command(label="Materias", command=materias)
menubarra.add_command(label="Calificaciones", command=calificaciones)

# Mostrar el menu
raiz.config(menu=menubarra)

# Mostrar la ventana
raiz.mainloop()

