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
    
        #Eliminar
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

