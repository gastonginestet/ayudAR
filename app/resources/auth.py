from flask import redirect, render_template, request, url_for, abort, session, flash
from app.db import connection
from flask_session import Session
from app.models.user import User
from app.models.usersRoles import UsersRoles
from app.models.rol import Rol
from app.helpers.auth import authenticated


def login():
    return render_template("auth/login.html")


def authenticate():
    params = request.form
    user = User.find_by_email_and_pass(params["email"], params["password"])
    if not user:
        flash("Usuario o clave incorrecto.",'danger')
        return redirect(url_for("auth_login"))
    session["user"] = user.username
    session['id'] = user.id
    user_roles = UsersRoles.find_user_roles_by_id(user.id)
    session['roles'] = Rol.get_name_roles(user_roles)
    return redirect(url_for("home"))


def logout():
    del session["user"]
    session.clear()
    flash("La sesión se cerró correctamente.", 'info')

    return redirect(url_for("auth_login"))
