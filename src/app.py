from flask import Flask, jsonify, url_for, request, redirect, render_template
from helper import timestamp
from data import setup
from data.database import DB_Cinema

app = Flask(__name__)

setup.create_tables()
db = DB_Cinema()

# renderizar la vista principal
@app.route("/", methods=["GET"])
def render_index():

    active_films = [
        film for film in films
        if film["estado"]
    ]

    return render_template(
        "index.html",
        title="bienvenidos",
        films=active_films
    )


@app.route("/cartelera/", methods=["GET"])
def render_cartelera():

    films_not_premier = [
        film for film in films
        if film["estado"] and
        not film["premier"]
    ]

    return render_template(
        "cartelera.html", 
        title="cartelera", 
        films=films_not_premier
    )

@app.route("/registro/", methods=["GET"])
def render_registro():

    return render_template(
        "registro.html",
        title="registro"
    )

@app.route("/todosUsuarios/", methods=["GET"])
def find_all_users():

    all_users = db.view_all_users()
    if all_users:
        return jsonify({
            "code": 200,
            "data": all_users,
            "status": "ok",
            "message": "Usuarios encontrados exitosamente",
            "timestamp": timestamp()
        })
    elif all_users == False:
        return jsonify({
            "code": 500,
            "data": {},
            "status": "error",
            "message": "Error buscando usuarios",
            "timestamp": timestamp()
        })
    else:
            return jsonify({
            "code": 200,
            "data": {},
            "status": "ok",
            "message": "No hay Usuarios",
            "timestamp": timestamp()
        })

@app.route("/buscarUsuarios/", methods=["POST"])
def find_users():

    registro = {
        "count": request.form.get("numero_usuarios")
    }

    registro = request.json['count']
    users = db.view_users(registro)
    if users:
        return jsonify({
            "code": 200,
            "data": users,
            "status": "ok",
            "message": "Usuarios encontrados exitosamente",
            "timestamp": timestamp()
        })
    return jsonify({
        "code": 500,
        "data": registro,
        "status": "error",
        "message": "Error buscando usuarios",
        "timestamp": timestamp()
        })

@app.route("/buscarUsuario/", methods=["POST"])
def find_user():

    registro = {
        "userid": request.form.get("numero_documento")
    }

    registro = request.json['userid']
    user_id = db.view_user(registro)
    if user_id:
        return jsonify({
            "code": 200,
            "data": user_id,
            "status": "ok",
            "message": "Usuario encontrado exitosamente",
            "timestamp": timestamp()
        })
    return jsonify({
        "code": 500,
        "data": registro,
        "status": "error",
        "message": "Error buscando usuario",
        "timestamp": timestamp()
        })


@app.route("/registro/", methods=["POST"])
def save_registro():

    # registro = {
    #     "userid": request.form.get("numero_documento"),
    #     "nombre": request.form.get("nombre"),
    #     "apellido": request.form.get("apellidos"),
    #     "alias": request.form.get("alias"),
    #     "tipoDoc": request.form.get("tipo_documento"),
    #     "numeroCelular": request.form.get("celular"),
    #     "email": request.form.get("correo"),
    #     "direccion": request.form.get("direccion"),
    #     "dia_nacimiento": request.form.get("dia_nacimiento"),
    #     "mes_nacimiento": request.form.get("mes_nacimiento"),
    #     "ano_nacimiento": request.form.get("ano_nacimiento"),
    #     "ciudad": request.form.get("ciudad"),
    #     "departamento": request.form.get("departamento"),
    #     "contrasena": request.form.get("contrasena"),
    #     "autorizaciones": request.form.getlist("autorizaciones")
    # }

    # insercion --> proceso sql
    insert_userid = request.json["userid"]
    insert_nombre = request.json["nombre"]
    insert_apellido = request.json["apellido"]
    insert_alias = request.json["alias"]
    insert_tipoDoc = request.json["tipoDoc"]
    insert_numeroCelular = request.json["numeroCelular"]
    insert_email = request.json["email"]
    insert_direccion = request.json["direccion"]
    insert_dia_nacimiento = request.json["dia_nacimiento"]
    insert_mes_nacimiento = request.json["mes_nacimiento"]
    insert_ano_nacimiento = request.json["ano_nacimiento"]
    insert_ciudad = request.json["ciudad"]
    insert_departamento = request.json["departamento"]
    insert_contrasena = request.json["contrasena"]
    insert_autorizaciones = request.json["autorizaciones"]

    user_id = db.insert_user(insert_nombre,insert_apellido,insert_alias,insert_tipoDoc,insert_userid,insert_numeroCelular,insert_email,insert_direccion,insert_dia_nacimiento,insert_mes_nacimiento,insert_ano_nacimiento,insert_ciudad,insert_departamento,insert_contrasena,insert_autorizaciones)
    if user_id:
        return jsonify({
            "code": 200,
            "data": user_id,
            "status": "ok",
            "message": "Usuario agregado exitosamente",
            "timestamp": timestamp()
        })
    return jsonify({
        "code": 500,
        "data": {},
        "status": "error",
        "message": "Error agregando usuario",
        "timestamp": timestamp()
        })

@app.route("/updateUser", methods=["PUT"])
def update_user():

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
    }

    update_nombre = request.json["nombre"]
    update_apellido = request.json["apellido"]
    update_alias = request.json["alias"]
    update_tipoDoc = request.json["tipoDoc"]
    update_numeroCelular = request.json["numeroCelular"]
    update_email = request.json["email"]
    update_direccion = request.json["direccion"]
    update_dia_nacimiento = request.json["dia_nacimiento"]
    update_mes_nacimiento = request.json["mes_nacimiento"]
    update_ano_nacimiento = request.json["ano_nacimiento"]
    update_ciudad = request.json["ciudad"]
    update_departamento = request.json["departamento"]
    update_contrasena = request.json["contrasena"]
    update_autorizaciones = request.json["autorizaciones"]
    
    
    id_arg = request.args.get('id')
    # insercion --> proceso sql
    
    if db.update_user(id_arg,update_nombre,update_apellido,update_alias,update_tipoDoc,update_numeroCelular,update_email,update_direccion,update_dia_nacimiento,update_mes_nacimiento,update_ano_nacimiento,update_ciudad,update_departamento,update_contrasena,update_autorizaciones):
        user_id = db.view_user(id_arg)
        return jsonify({
            "code": 200,
            "data": user_id,
            "status": "ok",
            "message": "Usuario agregado exitosamente",
            "timestamp": timestamp()
        })
    return jsonify({
        "code": 500,
        "data": {},
        "status": "error",
        "message": "Error agregando usuario",
        "timestamp": timestamp()
        })

    


@app.route("/pelicula/<int:id>/", methods=["GET"])
def render_pelicula(id):

    film_found = [
        film for film in films
        if film["id"] == id
    ]

    if film_found:
        return render_template(
            "pelicula.html", 
            film=film_found[0],
            title=film_found[0]["titulo_original"]  
        )

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

    login = {
        "usuario": request.form.get("usuario"),
        "contrasena": request.form.get("contrasena")
    }

    # inicia base de datos
    user_found = [
        user for user in users
        if login["usuario"] == user["username"]
        and login["contrasena"] == user["password"]
    ]
    # termina base de datos

    # inicia base de datos
    if user_found:
        return render_template("index.html", user=user_found[0], films=films)
    # termina base de datos

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
