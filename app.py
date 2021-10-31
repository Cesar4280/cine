from flask import jsonify, url_for, request, redirect, render_template, flash, session
from helper import timestamp
from data import setup
from data.database import DB_Cinema

from src import create_app

from data.film import films
from data.user import users

app = create_app()
app.config.update(
    ENV='development'
)
#Establece conecion a la base datos
setup.create_tables()
db = DB_Cinema()

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)

@app.errorhandler(500)
def server_error(error):
    return render_template('500.html', error=error)

# renderizar la vista principal
@app.route("/", methods=["GET"])
def render_index(user = None, tipoUsuario = None):

    if user:
        flash("Bienvenido")
        return render_template('index.html', user=user)

    return render_template("index.html")


@app.route("/cartelera/", methods=["GET"])
def render_cartelera():

    films_not_premier = [
        film for film in films
        if film["estado"] and
        not film["premier"]
    ]

    return render_template("cartelera.html", films=films_not_premier)


@app.route("/registro/", methods=["GET"])
def render_registro():

    return render_template("registro.html")

@app.route("/pelicula/", methods=["GET"])
def render_peli():

    return render_template("pelicula.html")

@app.route("/pelispedia/", methods=["GET"])
def render_pelispedia():

    return render_template("pelis.html")

@app.route("/admin/", methods=["GET"])
def render_admin():
    user_id = request.args.get("doc", False)
    data_none = {
            "nombre": "",
            "apellido": "",
            "correo": "",
            "direccion": "",
            "fecha_nacimiento": ""
        }

    if not user_id:
        return render_template("admin.html", user=data_none)
    else: # consulta a la base de datos
        data = db.view_user(user_id)
        if data:
            data["correo"] = data["email"]
            data["fecha_nacimiento"] = data["fechaNacimiento"]
            return render_template("admin.html", user=data)
        else:
            return render_template("admin.html", user=data_none)

@app.route("/compras/", methods=["GET"])
def render_compras():

    return render_template("compras.html")


@app.route("/pagos/", methods=["GET"])
def render_pagos():

    return render_template("pagos.html")

@app.route("/registro/", methods=["POST"])
def save_registro():

    registro = {
        "userid": request.form.get("numero_documento"),
        "nombre": request.form.get("nombre"),
        "apellido": request.form.get("apellidos"),
        "alias": request.form.get("alias"),
        "tipoDoc": request.form.get("tipo_documento"),
        "numeroCelular": request.form.get("celular"),
        "email": request.form.get("correo"),
        "direccion": request.form.get("direccion"),
        "dia_nacimiento": request.form.get("dia_nacimiento"),
        "mes_nacimiento": request.form.get("mes_nacimiento"),
        "ano_nacimiento": request.form.get("ano_nacimiento"),
        "ciudad": request.form.get("ciudad"),
        "departamento": request.form.get("departamento"),
        "contrasena": request.form.get("contrasena"),
        "autorizaciones": request.form.getlist("autorizaciones")
        }

    if db.insert_user(**registro):
        flash('Nombre de usuario registrado con exito.')
        return redirect(url_for("render_registro"))
    return redirect(url_for("server_error"))

@app.route("/buscar_usuario/", methods=["POST"])
def get_user():
    
    cedula = request.form.get("doc")

    data = db.view_user(cedula)
    print(data)
    return render_template("admin.html", user=data)

@app.route("/editar_usuario/", methods=["PUT"])
def update_user():

    registro = {
        "nombre":request.form.get("nombre"),
        "apellido": request.form.get("apellidos"),
        "email": request.form.get("correo"),
        "direccion": request.form.get("direccion"),
        "fechaNacimiento": request.form.get("fecha_nacimiento")
    }

    id_arg = request.args.get('id')
    # insercion --> proceso sql
    if db.update_user(id_arg,**registro):
        db.view_user(id_arg)
        flash('Usuario actualizado con exito.')
        return render_template("admin.html")
    return render_template("admin.html")


@app.route("/pelicula/<int:id>/", methods=["GET"])
def render_pelicula(id):

    film_found = [
        film for film in films
        if film["id"] == id
    ]

    if film_found:
        return render_template("pelicula.html", film=film_found[0])

    return jsonify({
        "code": 404,
        "status": "not found",
        "message": "Pelicula no encontrada"
    })

    # SELECT --> proceso sql
    # cur = sqlite.connection.cursor()
    # cur.execute("SELECT * FROM cat WHERE CAT_ID=%s", (id,))
    # film = cur.fetchone()
    # cur.close()
    # res = {"film": film, "timestamp": timestamp()}
    # res.update(
    #     {"code": 200, "status": "ok", "message": "Pelicula encontrado"}
    #     if film else
    #     {"code": 404, "status": "not found", "message": "Pelicula no encontrado"}
    # )
    # return jsonify(res)

@app.route("/login/", methods=["GET"])
def render_login():
    return render_template("login.html", title="login")


@app.route("/login/", methods=["POST"])
def login():
    
    log = {
        "correo": request.form.get("correo"),
        "contrasena": request.form.get("contrasena")
    }
    user_found = db.login(**log)
    if user_found:
        if user_found["tipoUsuario"] == "cliente":
            return redirect(url_for('render_index',**user_found))
        elif user_found["tipoUsuario"] == "adm":
            return render_template("admin.html", user=user_found, films=films)
        else:
            return render_template("admin.html", user=user_found, films=films)
    
    flash('Correo y/o contraseña incorrectas.')
    return render_template("login.html", title="login")


@app.route("/agregarpelicula/", methods=["POST"])
def add_film():

    add_film = {
        "nombre_imagen": request.form.get("nombre_imagen"),
        "nombre_video": request.form.get("nombre_video"),
        "titulo_espanol": request.form.get("titulo_espanol"),
        "titulo_original": request.form.get("titulo_original"),
        "fecha_estreno": request.form.get("fecha_estreno"),
        "idiomas": request.form.get("idiomas"),
        "tiempo": request.form.get("tiempo"),
        "genero": request.form.get("genero"),
        "clasificacion": request.form.get("clasificacion"),
        "sinopsis": request.form.get("sinopsis"),
        "pais_origen": request.form.get("pais_origen"),
        "director": request.form.get("director"),
        "actores": request.form.get("actores"),
        "premier": request.form.get("premier"),
        "estado": request.form.get("estado")
    }

    film_found = [
        film for film in films
        if film["titulo_original"] == add_film["titulo_original"]
    ]

    if film_found:
        return jsonify({
            "code": 409,
            "status": "conflict",
            "message": "No se puede agregar dos o mas peliculas con el mismo titulo"
        })

    films.append(add_film)

    return jsonify({
        "code": 400,
        "status": "ok",
        "message": "pelicula agregada al sistema"
    })


@app.route("/editarpelicula/<int:id>/", methods=["POST"])
def update_film(id):

    update_film = {
        "nombre_imagen": request.form.get("nombre_imagen"),
        "nombre_video": request.form.get("nombre_video"),
        "titulo_espanol": request.form.get("titulo_espanol"),
        "titulo_original": request.form.get("titulo_original"),
        "fecha_estreno": request.form.get("fecha_estreno"),
        "idiomas": request.form.getlist("idiomas"),
        "tiempo": request.form.get("tiempo"),
        "genero": request.form.get("genero"),
        "clasificacion": request.form.get("clasificacion"),
        "sinopsis": request.form.get("sinopsis"),
        "pais_origen": request.form.get("pais_origen"),
        "director": request.form.get("director"),
        "actores": request.form.getlist("actores"),
        "premier": request.form.get("premier"),
        "estado": request.form.get("estado")
    }

    film_found = [
        film for film in films
        if film["id"] == id
    ]

    if film_found:

        film_found[0].update(update_film)

        return jsonify({
            "code": 400,
            "status": "ok",
            "message": "pelicula actualizada correctamente"
        })

    return jsonify({
        "code": 404,
        "status": "not found",
        "message": "Pelicula no encontrada"
    })


@app.route("/eliminarpelicula/<int:id>/", methods=["GET"])
def delete_film(id):

    film_found = [
        film for film in films
        if film["id"] == id
    ]

    if film_found:

        if film_found[0]["estado"]:

            film_found[0]["estado"] = False

            return jsonify({
            "code": 400,
            "status": "ok",
            "message": "pelicula eliminada correctamente"
        })

        return jsonify({
            "code": 409,
            "status": "conflict",
            "message": "la pelicula indicada se encuentra inactiva"
        })


    return jsonify({
        "code": 404,
        "status": "not found",
        "message": "Pelicula no encontrada"
    })


# llamado de la ejecucion del servidor en el navegador
if __name__ == "__main__":
    app.run(port=5000, debug=True)
