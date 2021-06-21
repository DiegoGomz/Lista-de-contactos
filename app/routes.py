from flask import render_template, flash, redirect, url_for
from app import app
from app import Bootstrap
from app import db
from app.forms import LoginForm, ContactForm, SignUpForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Contact

@app.route("/")
@app.route("/index")
def index():
    
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    o=""
    Lista=Contact.query.filter_by(users_id=current_user.id).all()
    return render_template("index.html", lista=Lista)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        #POST
        #Iniciar sesión con base de datos
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("No se encontro el usuario o la contraseña esta incorrecta")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        flash("Iniciaste Sesión correctamente, Hola {}".format(form.username.data))
        return redirect("/index")
    return render_template("login.html", title="Login",form=form)


@app.route("/secreto")
@login_required #Falto importar
def secreto():
    return "Pagina secreta"

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/contact/delete/<int:id>", methods=["POST"])
@login_required
def delete_contact(id):
    contact= Contact.query.filter_by(id=id).first()
    if contact:
        if current_user.id==contact.users_id:
            db.session.delete(contact)
            db.session.commit()
            return redirect(url_for("index"))
        else:
            return redirect(url_for("404"))
    else:
        flash("El contacto no existe")
    return redirect(url_for("index"))

@app.route("/contact/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_contact(id):
    contact= Contact.query.filter_by(id=id).first()
    if contact:
        if current_user.id==contact.users_id:
            pass
            form=ContactForm()
            if form.validate_on_submit():
                contact.name=form.name.data
                contact.email=form.email.data
                contact.number=form.number.data
                contact.users_id=current_user.id
                db.session.add(contact)
                db.session.commit()
                return redirect(url_for("index"))
            form.name.data=contact.name
            form.email.data=contact.email
            form.number.data=contact.number
            edit=True
            return render_template("contact.html", edit=edit,form=form)
        else:
            return redirect(url_for("404"))
    return redirect(url_for("index"))

@app.route("/contact", methods=["GET", "POST"])
@login_required
def contact():
    form=ContactForm()  
    if form.validate_on_submit():
        p=Contact()
       
        p.name=form.name.data
        p.email=form.email.data
        p.number=form.number.data
        p.users_id=current_user.id
        db.session.add(p)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("contact.html", form=form, edit=False)

@app.route("/signup", methods=["GET", "POST"])
def singup():
    if current_user.is_authenticated:
         return redirect(url_for("index")) 
    form=SignUpForm()
    if form.validate_on_submit():
        user= User.query.filter_by(username=form.username.data).first()
        if user:
            return redirect(url_for("signup"))
        user= User.query.filter_by(email=form.email.data).first()
        if user:
            return redirect(url_for("signup"))
        u=User()
        u.username=form.username.data
        u.email=form.email.data
        u.set_password(form.password.data)
        db.session.add(u)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("signup.html", form=form)