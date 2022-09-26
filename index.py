#from crypt import methods
import email
from email.policy import default
from flask import Flask, render_template, flash, request, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime




#importo mis configuraciones
from app import app


app=Flask(__name__)

#


#add datebase
#app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///users.db'
#app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost/user'

#=======conexión a base de datos de biblioteca ===================

#app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost/bd_matricula'
app.config['SQLALCHEMY_DATABASE_URI']='mysql://admin:albert191229@bd-libros.ci6nf51jc7go.us-east-1.rds.amazonaws.com/bd_matricula'

app.config['SQLALCHEMY_TRACK_MODEFICATIONS']=False
# secret key
app.config['SECRET_KEY']='My super secret that no one is supposed to knaw'

#initialize the database
db=SQLAlchemy(app)

#=========================================================================================================

#=====Tabla Escuela ====
class Escuela(db.Model):
    __tablename__ = 'escuela'
    #id=db.Column(db.Integer, primary_key=True)
    codigo=db.Column(db.String(10),primary_key=True)
    nombre=db.Column(db.String(200),nullable=False)
    duracion=db.Column(db.Integer, nullable=False)
    

    #create a String
#=====Tabla Estudiante ====    
class Estudiante(db.Model):
    __tablename__ = 'estudiante'
    id=db.Column(db.Integer, primary_key=True)
    DNI=db.Column(db.Integer,nullable=False)
    apellidos=db.Column(db.String(200),nullable=False)
    nombres=db.Column(db.String(200),nullable=False)
    feNacimiento=db.Column(db.String(30),nullable=False)
    sexo=db.Column(db.String(1),nullable=False)
    codEscuela = db.Column(db.String(10), db.ForeignKey('escuela.codigo'))#agregando esto al architeck
    category = db.relationship("Escuela")

#=====Tabla Curso====== 
class Curso(db.Model):
    __tablename__ = 'curso'
    #id=db.Column(db.Integer, primary_key=True)
    codigo=db.Column(db.String(10),primary_key=True)
    nombre=db.Column(db.String(200),nullable=False)
    credito=db.Column(db.Integer, nullable=False)
    
   
    
#=====Tabla Matricula====== 
class Matricula(db.Model):
    __tablename__ = 'matricula'

    #id=db.Column(db.Integer, primary_key=True)
    codigo=db.Column(db.Integer,primary_key=True)
    codEstudiante = db.Column(db.Integer, db.ForeignKey('estudiante.id'))
    category = db.relationship("Estudiante")

    codCurso = db.Column(db.String(10), db.ForeignKey('curso.codigo'))
    category = db.relationship("Curso")


# ==========Ingresando Datos ======


#====ingresando datos a Tabla Escuela====
#escuela1 = Escuela(codigo='EAPIIS', nombre='Ingeniería Informatica y Sistemas', duracion=10)
#db.session.add(escuela1)
#db.session.commit()

#====ingresando datos a Tabla Estudiante====
#estudiante1 = Estudiante(DNI='73658684', apellidos="Pfuño Alccahuamani", nombres="Luis Albert", feNacimiento ="24/10/2001", sexo= "M", codEscuela ="EAPIIS")
#db.session.add(estudiante1)
#db.session.commit()


#====ingresando datos a Tabla Curso====
#curso1 = Curso(codigo='ISA803', nombre="Computación en la nube",credito=2)
#db.session.add(curso1)
#db.session.commit()

#====ingresando datos a Tabla Matricula====
#matricula1= Matricula(codigo='001', codEstudiante='1',codCurso="ISA803")
#db.session.add(matricula1)
# db.session.commit()



#====================================================
with app.app_context():#cada vez que inicio el server me crea las tablas
    db.create_all()



#===========================================


#create a form class


@app.route('/')
def index():
    first_nombre = 'Yo veo doramas'
    stuff='this is bold text'
    flash("welcome to our website")
    favorite_pizza=['Peperony','Calzonee','Hawaiana', 41]

    return render_template('index.html',
    first_nombre=first_nombre,
    stuff=stuff,
    favorite_pizza=favorite_pizza)

@app.route('/user/<nombre>')
def user(nombre):
    return render_template('user.html',
    nombre=nombre)


# ====== Agragar Nombre ============
class NamerForm(FlaskForm):
    nombre=StringField("Nombre", validators=[DataRequired()])
    submit=SubmitField('Submit')



@app.route('/nombre',methods=['GET','POST'])
def nombre():
    nombre=None
    form=NamerForm()
    #validate form
    if form.validate_on_submit():
        nombre=form.nombre.data
        form.nombre.data=''
        flash("From Submitted Successfully")
    return render_template('name.html',
    nombre=nombre,
    form=form)



#======= Agregar  Escuela ============
class EscuelaForm(FlaskForm):
    codigo = StringField("Código", validators=[DataRequired()])
    nombre = StringField("Nombre de la Escuela Profesional", validators=[DataRequired()])
    duracion = StringField("Duración", validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/escuela/add', methods=['GET','POST'])
def add_escuela():
    nombre=None
    form=EscuelaForm()
    #validate form
    if form.validate_on_submit():
        escuela = Escuela(codigo=form.codigo.data, nombre = form.nombre.data, duracion = form.duracion.data)
        db.session.add(escuela)
        db.session.commit()
        nombre=form.nombre.data
        form.codigo.data=''
        form.nombre.data=''
        form.duracion.data=''
        flash("From Submitted Successfully")
    our_escuela = Escuela.query.order_by(Escuela.nombre)

    return render_template('add_escuela.html',
    nombre=nombre,
    form=form,
    our_escuela = our_escuela)

#=============Upadate Escuela===========

@app.route('/Escuela_edit/<codigo>',methods=['GET','POST'])
def update_escuela(codigo):
    esc=Escuela.query.get(codigo)
    form=EscuelaForm()
    if form.validate_on_submit():
        esc.codigo=form.codigo.data
        esc.nombre=form.nombre.data
        esc.duracion=form.duracion.data

        db.session.commit()

    nombre=form.nombre.data
    form.codigo.data=''
    form.nombre.data=''
    form.duracion.data=''
    flash("From Submitted Successfully")
    our_escuela=Escuela.query.order_by(Escuela.nombre)

    return render_template('edit_escuela.html',esc=esc,form=form,nombre=nombre,our_escuela=our_escuela)

@app.route('/delete_Escuela/<codigo>')
def delete_escuela(codigo):
    deleteEscuelta = Escuela.query.get(codigo)
    db.session.delete(deleteEscuelta)
    db.session.commit()
    return redirect('/escuela/add')



#=======Agregar  Curso============

class CursoForm(FlaskForm):
    codigo = StringField("Código", validators=[DataRequired()])
    nombre = StringField("Nombre", validators=[DataRequired()])
    credito = StringField("Creditos", validators=[DataRequired()])
    submit = SubmitField('Submit')




@app.route('/curso/add', methods=['GET','POST'])
def add_curso():
    nombre=None
    form=CursoForm()
    #validate form
    if form.validate_on_submit():
        curso = Curso(codigo=form.codigo.data, nombre = form.nombre.data, credito = form.credito.data)
        db.session.add(curso)
        db.session.commit()
        nombre=form.nombre.data
        form.codigo.data=''
        form.nombre.data=''
        form.credito.data=''
        flash("From Submitted Successfully")
    our_curso = Curso.query.order_by(Curso.nombre)

    return render_template('add_curso.html',
    nombre=nombre,
    form=form,
    our_curso = our_curso)

#==========Upadate Curso ===========

@app.route('/curso_edit/<codigo>',methods=['GET','POST'])
def update_curso(codigo):
    cur=Curso.query.get(codigo)
    form=CursoForm()
    if form.validate_on_submit():
        cur.codigo=form.codigo.data
        cur.nombre=form.nombre.data
        cur.credito=form.credito.data

        db.session.commit()

    nombre=form.nombre.data
    form.codigo.data=''
    form.nombre.data=''
    form.credito.data=''
    flash("From Submitted Successfully")
    our_curso=Curso.query.order_by(Curso.nombre)
    return render_template('edit_curso.html',cur=cur,form=form,nombre=nombre,our_curso=our_curso)



@app.route('/delete_curso/<codigo>')
def delete_curso(codigo):
    deleteCurso = Curso.query.get(codigo)
    db.session.delete(deleteCurso)
    db.session.commit()
    return redirect('/curso/add')



#======= Agregar  Estudiante============
class EstudianteForm(FlaskForm):
    DNI = StringField("DNI", validators=[DataRequired()])
    apellidos = StringField("Apellidos", validators=[DataRequired()])
    nombres = StringField("Nombres", validators=[DataRequired()])
    feNacimiento = StringField("Fecha de Nacimiento", validators=[DataRequired()])
    sexo = StringField("Sexo", validators=[DataRequired()])
    codEscuela = StringField("Código de Escuela", validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/estudiante/add', methods=['GET','POST'])
def add_estudiante():
    nombres=None
    form=EstudianteForm()
    #validate form
    if form.validate_on_submit():
        escuela = Estudiante(DNI=form.DNI.data, apellidos = form.apellidos.data, nombres = form.nombres.data, feNacimiento = form.feNacimiento.data, sexo = form.sexo.data, codEscuela = form.codEscuela.data )
        db.session.add(escuela)
        db.session.commit()
        nombres=form.nombres.data
        form.DNI.data=''
        form.apellidos.data=''
        form.nombres.data=''
        form.feNacimiento.data=''
        form.sexo.data=''
        form.codEscuela.data=''
        flash("From Submitted Successfully")
    our_estudiante = Estudiante.query.order_by(Estudiante.nombres)
    escu=Escuela.query.order_by(Escuela.codigo)

    return render_template('add_estudiante.html',
    nombres=nombres,
    form=form,
    our_estudiante = our_estudiante, escu=escu)


@app.route('/estudiante_edit/<id>',methods=['GET','POST'])
def update_estudiante(id):
    est=Estudiante.query.get(id)
    form=EstudianteForm()
    if form.validate_on_submit():
        est.DNI=form.DNI.data
        est.apellidos=form.apellidos.data
        est.nombres=form.nombres.data
        est.feNacimiento=form.feNacimiento.data
        est.sexo=form.sexo.data
        est.codEscuela=form.codEscuela.data
    
        db.session.commit()

    nombres=form.nombres.data
    form.DNI.data=''
    form.apellidos.data=''
    form.nombres.data=''
    form.feNacimiento.data=''
    form.sexo.data=''
    form.codEscuela.data=''
    flash("From Submitted Successfully")
    our_estudiante=Estudiante.query.order_by(Estudiante.nombres)
    escu=Escuela.query.order_by(Escuela.codigo)
    escuel=Escuela.query.get(est.codEscuela)

    return render_template('edit_estudiante.html',est=est,form=form,nombres=nombres,our_estudiante=our_estudiante,escu=escu,escuel=escuel)


# @app.route('/estudiante/add', methods=['GET','POST'])
# def add_estudiante():
#     nombres=None
#     form=EstudianteForm()
#     #validate form
#     if form.validate_on_submit():
#         escuela = Estudiante(DNI=form.DNI.data, apellidos = form.apellidos.data, nombres = form.nombres.data, feNacimiento = form.feNacimiento.data, sexo = form.sexo.data, codEscuela = form.codEscuela.data )
#         db.session.add(escuela)
#         db.session.commit()
#         nombres=form.nombres.data
#         form.DNI.data=''
#         form.apellidos.data=''
#         form.nombres.data=''
#         form.feNacimiento.data=''
#         form.sexo.data=''
#         form.codEscuela.data=''
#         flash("From Submitted Successfully")
#     our_estudiante = Estudiante.query.order_by(Estudiante.nombres)

#     return render_template('add_estudiante.html',
#     nombres=nombres,
#     form=form,
#     our_estudiante = our_estudiante)




#jakc
#===========Upadate Escuela===============
# @app.route('/estudiante_edit/<id>',methods=['GET','POST'])
# def update_estudiante(id):
#     est=Estudiante.query.get(id)
#     form=EstudianteForm()
#     if form.validate_on_submit():
#         est.DNI=form.DNI.data
#         est.apellidos=form.apellidos.data
#         est.nombres=form.nombres.data
#         est.feNacimiento=form.feNacimiento.data
#         est.sexo=form.sexo.data
#         est.codEscuela=form.codEscuela.data
    
#         db.session.commit()

#     nombres=form.nombres.data
#     form.DNI.data=''
#     form.apellidos.data=''
#     form.nombres.data=''
#     form.feNacimiento.data=''
#     form.sexo.data=''
#     form.codEscuela.data=''
#     flash("From Submitted Successfully")
#     our_estudiante=Estudiante.query.order_by(Estudiante.nombres)

#     return render_template('edit_estudiante.html',est=est,form=form,nombres=nombres,our_estudiante=our_estudiante)

@app.route('/delete_estudiante/<id>')
def delete_estudiante(id):
    deleteEstudiante = Estudiante.query.get(id)
    db.session.delete(deleteEstudiante)
    db.session.commit()
    return redirect('/estudiante/add')


#==========Agregar Matricula===============

class MatriculaForm(FlaskForm):
    codigo = StringField("Código", validators=[DataRequired()])
    codEstudiante = StringField("Código del Estudiante", validators=[DataRequired()])
    codCurso = StringField("Código del Curso", validators=[DataRequired()])
    submit = SubmitField('Submit')

#matricula1= Matricula(codigo='001', codEstudiante='1',codCurso="ISA803")


@app.route('/matricula/add', methods=['GET','POST'])
def add_matricula():
    codEstudiante=None
    form=MatriculaForm()
    #validate form
    if form.validate_on_submit():
        matricula = Matricula(codigo=form.codigo.data, codEstudiante = form.codEstudiante.data, codCurso = form.codCurso.data)
        db.session.add(matricula)
        db.session.commit()
        codEstudiante=form.codEstudiante.data
        form.codigo.data=''
        form.codEstudiante.data=''
        form.codCurso.data=''
        flash("From Submitted Successfully")
    our_matricula = Matricula.query.order_by(Matricula.codEstudiante)
    cur=Curso.query.order_by(Curso.codigo)

    return render_template('add_matricula.html',
    codEstudiante=codEstudiante,
    form=form,
    our_matricula= our_matricula,cur=cur)

@app.route('/matricula_edit/<codigo>',methods=['GET','POST'])
def update_matricula(codigo):
    mat=Matricula.query.get(codigo)
    form=MatriculaForm()
    if form.validate_on_submit():
        mat.codigo=form.codigo.data
        mat.codEstudiante=form.codEstudiante.data
        mat.codCurso=form.codCurso.data

        db.session.commit()

    codEstudiante=form.codEstudiante.data
    form.codigo.data=''
    form.codEstudiante.data=''
    form.codCurso.data=''
    flash("From Submitted Successfully")
    our_matricula=Matricula.query.order_by(Matricula.codEstudiante)
    cur=Curso.query.order_by(Curso.codigo)
    curs=Curso.query.get(mat.codCurso)
    return render_template('edit_matricula.html',mat=mat,form=form,codEstudiante=codEstudiante,our_matricula=our_matricula,cur=cur,curs=curs)


# @app.route('/matricula/add', methods=['GET','POST'])
# def add_matricula():
#     codEstudiante=None
#     form=MatriculaForm()
#     #validate form
#     if form.validate_on_submit():
#         matricula = Matricula(codigo=form.codigo.data, codEstudiante = form.codEstudiante.data, codCurso = form.codCurso.data)
#         db.session.add(matricula)
#         db.session.commit()
#         codEstudiante=form.codEstudiante.data
#         form.codigo.data=''
#         form.codEstudiante.data=''
#         form.codCurso.data=''
#         flash("From Submitted Successfully")
#     our_matricula = Matricula.query.order_by(Matricula.codEstudiante)

#     return render_template('add_matricula.html',
#     codEstudiante=codEstudiante,
#     form=form,
#     our_matricula= our_matricula)


#jakc
#Upadate User
# @app.route('/matricula_edit/<codigo>',methods=['GET','POST'])
# def update_matricula(codigo):
#     mat=Matricula.query.get(codigo)
#     form=MatriculaForm()
#     if form.validate_on_submit():
#         mat.codigo=form.codigo.data
#         mat.codEstudiante=form.codEstudiante.data
#         mat.codCurso=form.codCurso.data

#         db.session.commit()

#     codEstudiante=form.codEstudiante.data
#     form.codigo.data=''
#     form.codEstudiante.data=''
#     form.codCurso.data=''
#     flash("From Submitted Successfully")
#     our_matricula=Matricula.query.order_by(Matricula.codEstudiante)

#     return render_template('edit_matricula.html',mat=mat,form=form,codEstudiante=codEstudiante,our_matricula=our_matricula)

@app.route('/delete_matricula/<codigo>')
def delete_matricula(codigo):
    deleteMatricula = Matricula.query.get(codigo)
    db.session.delete(deleteMatricula)
    db.session.commit()
    return redirect('/matricula/add')



if __name__=='__main__':
    app.run(debug=True,port=5000,host="0.0.0.0")