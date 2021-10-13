from flask import Flask, jsonify, url_for, request, redirect, render_template
from helper import timestamp
from data.film import films
from data.user import users

app = Flask(__name__)

# renderizar la vista principal


@app.route("/", methods=["GET"])
def render_index():

    active_films = [
        film for film in films
        if film["estado"]
    ]

    return render_template("index.html", films=active_films)

@app.route("/menu/", methods=["GET"])
def render_menu():
    return render_template("menu.html")


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


@app.route("/registro/", methods=["POST"])
def save_registro():

    registro = {
        "correo": request.form.get("correo"),
        "contrsena": request.form.get("contrasena"),
        "nombre": request.form.get("nombre"),
        "apellidos": request.form.get("apellidos"),
        "tipo_documento": request.form.get("tipo_documento"),
        "numero_documento": request.form.get("numero_documento"),
        "dia_nacimiento": request.form.get("dia_nacimiento"),
        "mes_nacimiento": request.form.get("mes_nacimiento"),
        "ano_nacimiento": request.form.get("ano_nacimiento"),
        "departamento": request.form.get("departamento"),
        "ciudad": request.form.get("ciudad"),
        "direccion": request.form.get("direccion"),
        "celular": request.form.get("celular"),
        "alias": request.form.get("alias"),
        "autorizaciones": request.form.getlist("autorizaciones")
    }

    # insercion --> proceso sql

    # return redirect(url_for("render_registro"))

    return jsonify({
        "code": 200,
        "data": registro,
        "status": "ok",
        "message": "usuario agregado exitosamente",
        "timestamp": timestamp()
    })


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


@app.route("/login/", methods=["POST"])
def login():

    login = {
        "username": request.form.get("username"),
        "password": request.form.get("password")
    }

    user_found = [
        user for user in users
        if user["username"] == login["username"]
        and user["password"] == login["password"]
    ]

    if user_found:
        return render_template("index.html", user=user_found[0], films=films)

    return jsonify({
        "code": 404,
        "status": "not found",
        "message": "Usuario o credenciales incorrectas"
    })


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
