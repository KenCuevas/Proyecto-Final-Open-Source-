import os.path
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from jinja2 import FileSystemLoader, Environment
import webbrowser
import os
from tkinter.ttk import * 
import functools 

#Ventana principal
app = Tk()
app.title("Sistema de calificaciones estudiantil")
MyLeftPos = (app.winfo_screenwidth() - 500) / 2
myTopPos = (app.winfo_screenheight() - 300) / 2
app.geometry( "%dx%d+%d+%d" % (500, 300, MyLeftPos, myTopPos))

vVentana = str()
vCampos = {}
query=str()

#Nombre de la base de datos
db_name = 'Practica4.db'
#Tamaño de ventana
w, h = app.winfo_screenwidth(), app.winfo_screenheight()

#Toplevel
def toplevel(vVentana, vCampos):
    top = Toplevel()
    
    if vVentana == "Calificacion":
          MyLeftPos = (top.winfo_screenwidth() - 1170) / 2
          myTopPos = (top.winfo_screenheight() - 500) / 2
          top.geometry( "%dx%d+%d+%d" % (1170, 500, MyLeftPos, myTopPos))
    elif vVentana == "Materia":
          MyLeftPos = (top.winfo_screenwidth() - 550) / 2
          myTopPos = (top.winfo_screenheight() - 420) / 2
          top.geometry( "%dx%d+%d+%d" % (550, 420, MyLeftPos, myTopPos))            
    else:
          MyLeftPos = (top.winfo_screenwidth() - 760) / 2
          myTopPos = (top.winfo_screenheight() - 420) / 2
          top.geometry( "%dx%d+%d+%d" % (760, 420, MyLeftPos, myTopPos))  

    #                                                                    Frame de formulario                                                                         #
    ##################################################################################################################################################################
    frame = LabelFrame(top, text = 'Registrar '+ vVentana)
    frame.grid(row = 1, column = 1, columnspan = 2, pady = 20)
    frame.place()

    #Renderizar formulario
    render_form(vCampos, top, frame)

    #Boton para guardar
    ttk.Button(frame, text = 'Guardar ' + vVentana, command = lambda: agregar(vVentana, vCampos, top)).grid(row = len(vCampos)+1, columnspan = 4, sticky = W + E)
    ##################################################################################################################################################################


    #                                                                          Tabla                                                                                #
    ##################################################################################################################################################################
    tabla(vCampos, top, vVentana)
    #Datos de tabla
    llenartabla(vVentana, top)

    #Botones eliminar, editar y generar
    ttk.Button(top, text = '', command = lambda: eliminar(vVentana, vCampos, top)).grid(row = len(vCampos)+1, columnspan = 1, column = 0, sticky = W + E)
    ttk.Button(top, text = 'ELIMINAR', command = lambda: eliminar(vVentana, vCampos, top)).grid(row = len(vCampos)+1, columnspan = 1, column = 1, sticky = W + E)
    ttk.Button(top, text = 'EDITAR', command = lambda: editar(vVentana, vCampos, top, frame)).grid(row = len(vCampos)+1, columnspan = 1, column = 2, sticky = W + E)
    ###################################################################################################################################################################

#Render de fomrularios
def render_form(vCampos, top, frame):
    for (i, (id_campo, campo)) in enumerate(vCampos.items()):
        if i>4 :
              Label(frame, text = campo["label"]).grid(row = (i-5), column = 2)
        else:
              Label(frame, text = campo["label"]).grid(row = i, column = 0)

        vCampos[id_campo]["entry"] = Entry(frame)
        vCampos[id_campo]["entry"].focus()

        if i>4 :
              vCampos[id_campo]["entry"].grid(row = (i-5), column = 3) 
        else:
              vCampos[id_campo]["entry"].grid(row = (i), column = 1) 
        

#Render de tabla
def tabla(vCampos, top, vVentana):
    top.tree = ttk.Treeview(top, height = 10, columns = [ campo["label"] for campo in vCampos.values()])
    top.tree.column("#0", width=3, minwidth=1)
    top.tree.grid(row = len(vCampos.items()), column = 1, columnspan = 2)
    print(vVentana)
    for (id_campo, campo) in vCampos.items():
          if vVentana == "Calificacion":
                top.tree.column(campo["label"], width=100, minwidth=20) 
                
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
    print(parameters)
    run_query(query, parameters)
    llenartabla(vVentana, top)
    warning("Agregado", "Registro agregado correctamente", top)

########################################## EDITAR ############################################
def nuevovalor(vCampos,vVentana, top, edit_wind):
      parameters = []
      for key in range(len(dict.keys(vCampos))):
            parametro = (list( dict.keys( vCampos ) )[ key ])
            entry = vCampos[parametro]["entry"]
            parameters.append(entry.get())
      edit_records(parameters,vVentana, top, edit_wind, vCampos)

def editar(vVentana, vCampos, top, frame):
    parameters = []
    try:
      top.tree.item(top.tree.selection())['values'][0]
    except IndexError as e:
      warning("Error", "Por favor seleccionar un registro", top)
      return

    edit_wind = Toplevel()
    
    edit_wind.title(f'Editar {vVentana}')
    MyLeftPos = (top.winfo_screenwidth() - 300) / 2
    myTopPos = (top.winfo_screenheight() - 300) / 2
    edit_wind.geometry( "%dx%d+%d+%d" % (300, 300, MyLeftPos, myTopPos))  

    for (i, (id_campo, campo)) in enumerate(vCampos.items()):
          
          Label(edit_wind, text = campo["label"]).grid(row = i, column = 1)
          vCampos[id_campo]["entry"] = Entry(edit_wind)
          vCampos[id_campo]["entry"].grid(row = i, column = 2)
          vCampos[id_campo]["entry"].insert(0, top.tree.item(top.tree.selection())['values'][i])
          if(i == 0):
                vCampos[id_campo]["entry"].configure(state='readonly')
       
    ttk.Button(edit_wind, text = 'EDITAR', command = lambda: nuevovalor(vCampos, vVentana, top, edit_wind)).grid(row = len(vCampos)+1, column = 2)

def edit_records(parameters,vVentana, top, edit_wind, vCampos):
        query = f'UPDATE {vVentana} SET '
         
        for key in range(len(dict.keys(vCampos))):
            parametro = (list( dict.keys( vCampos ) )[ key ])            
            query += f'{list( dict.keys( vCampos ) )[ key ]} = ? '

            if key != len(dict.keys(vCampos)) - 1:
                  query += ','
        query += f'where {(list( dict.keys( vCampos ) )[ 0 ])} = {parameters[0]}'       

        #Ejecutar comando
        run_query(query, parameters)

        #Cerrar popup
        edit_wind.destroy()

        #Llenar tabla
        llenartabla(vVentana, top)
        warning("Modificador", "Registro modificado correctamente", top)


def promedio(calificaciones):
      promedios = []
      literales = []
      for id, valor in enumerate(calificaciones):
            vPromedio=(functools.reduce(lambda a,b : a+b, calificaciones[id]) /len(calificaciones[id]))
            promedios.append(vPromedio)
            if vPromedio>=90:
                  literales.append('<h1 style="color:blue">A</h1>')
            elif vPromedio>=80:
                  literales.append('<h1 style="color:green">B</h1>')
            elif vPromedio>=70:
                  literales.append('<h1 style="color:orange">C</h1>')
            elif vPromedio>=60:
                  literales.append('<h1 style="color:pink">D</h1>')
            else:
                  literales.append('<h1 style="color:red">F </h1>')

      return (promedios,literales)

def reportehtml(estudiante, Materias, Calificaciones, promedio):
      print(estudiante, Materias, Calificaciones,promedio)
      row = ""
      counter = 0

      for i, materia in enumerate(Materias):
            counter = 0
            print(counter)  
            if i == 0:
                  
                  row = str(row) + "<tr><th scope = 'row' > " + \
                  str(estudiante[1]
                      ) + " </th> <td> "+str(estudiante[i])+" </td> " + \
                      "<td> "+str(materia)+" </td> "
                      
                  row = str(row) + "<td> <p>Practica 1: "+str(Calificaciones[i][0])+"</p> " + \
                        "<p>Practica 2: "+str(Calificaciones[i][1])+"</p> "+ \
                        "<p>Foro 1: "+str(Calificaciones[i][2])+"</p>"+ \
                        "<p>Foro 2: "+str(Calificaciones[i][3])+"</p>" + \
                        "<p>Primer parcial: "+str(Calificaciones[i][4])+"</p>" + \
                        "<p>Segundo parcial: "+str(Calificaciones[i][5])+"</p>" + \
                        "<p>Examen final: "+str(Calificaciones[i][6])+"</p>" + \
                        "<p>Promedio: "+str(promedio[0][i])+"</p>" + \
                        "</td> <td>" + \
                        str(promedio[1][i])+" </td > </tr>"
            else:
                  
                  row += "<tr><th scope = 'row' > " + \
                          " </th> <td> --- </td> " + \
                          "<td> "+str(materia)+" </td> "

                  row = str(row) + "<td> <p>Practica 1: "+str(Calificaciones[i][0])+"</p> " + \
                        "<p>Practica 2: "+str(Calificaciones[i][1])+"</p> "+ \
                        "<p>Foro 1: "+str(Calificaciones[i][2])+"</p>"+ \
                        "<p>Foro 2: "+str(Calificaciones[i][3])+"</p>" + \
                        "<p>Primer parcial: "+str(Calificaciones[i][4])+"</p>" + \
                        "<p>Segundo parcial: "+str(Calificaciones[i][5])+"</p>" + \
                        "<p>Examen final: "+str(Calificaciones[i][6])+"</p>" + \
                        "<p>Promedio: "+str(promedio[0][i])+"</p>" + \
                        "</td> <td>" + \
                        str(promedio[1][i])+" </td > </tr>"                
            

                                                                
                    




      # Content to be published
      content = row

      # Configure Jinja and ready the template
      env = Environment(
      loader=FileSystemLoader(searchpath="templates")
      )
      template = env.get_template("Front_end.html")

      with open("Report.html", "w") as f:
        f.write(template.render(content=content))

      new = 2

      BASE_DIR = os.path.dirname(os.path.abspath(__file__))

      # open an HTML file on my own(Windows) computer

      url = "file://" + os.path.join(BASE_DIR, 'Report.html')
      webbrowser.open(url, new=new)

def informacion(estudiante):
      Registros = []
      Materia = []
      Calificaciones = []
      query = f'SELECT * FROM Calificacion where Matricula = {estudiante[1]}'
      db_rows = run_query(query)
      for row in db_rows:
            Registros.append(row)

      for mat in Registros:
            Materia.append(mat[8])

      for cal in Registros:
            Calificaciones.append(cal[1:8])

      reportehtml(estudiante, Materia, Calificaciones, promedio(Calificaciones))
 
def eliminar(vVentana, vCampos, top):
    vTitulo = vVentana
    vCondicion = list( dict.keys( vCampos ) )[ 0 ]
    try:
      curItem = top.tree.item(top.tree.focus())
      valor = curItem['values'][0]
    except IndexError as e:
      warning("Error", "Por favor seleccionar un registro", top)
      return
               
    query = f'DELETE FROM {vTitulo} WHERE {vCondicion} = ?'
    run_query(query, (valor, ))
    llenartabla(vTitulo, top)
    warning("Eliminado", "Registro eliminado correctamente", top)

def run_query(query, parameters = ()):
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        result = cursor.execute(query, parameters)
        conn.commit()
    return result

def warning(title, information, top):
    messagebox.showinfo(title, information, parent=top)

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

# Combo box de estudiantes #
Estudiantes_combobox = ttk.Combobox(app, width=40)
Estudiantes_combobox.place(x=110, y=150)

BuscarButton = Button(app, text="GENERAR HTML", command=lambda: informacion(estudiante[Estudiantes_combobox.current()]))
BuscarButton.place(x=195, y=180)

query = "SELECT Nombre, Matricula FROM Estudiante"
estudiante = []
mat = []
db_rows = run_query(query)
for row in db_rows:
      estudiante.append(row)


Estudiantes_combobox['values']=estudiante


################################################################ GENERAR HTML ############################################################################

# Mostrar la ventana
app.mainloop()


