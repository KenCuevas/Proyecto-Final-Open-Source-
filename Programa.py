import os.path
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
