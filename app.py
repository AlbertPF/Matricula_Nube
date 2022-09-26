##===========================
#==========================
# AQUI CREO LAS RUTAS PARA MI CRUD
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/escuela_edit')
def edit_escuela():
    return render_template('edit_user.html')

@app.route('/curso_edit')
def edit_curso():
    return render_template('edit_curso.html')    

@app.route('/estudiante_edit')
def edit_estudiante():
    return render_template('edit_estudiante.html')        

@app.route('/matricula_edit')
def edit_matricula():
    return render_template('edit_matricula.html') 