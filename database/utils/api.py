from datetime import datetime

from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from database.utils.database import DataBase

db = DataBase("db/smart_shop.db")
app = Flask(__name__)
CORS(app)

app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True

@app.route("/estados", methods=["GET"])
def get_all_estados_route():
    try:
        success, estados = db.get_all_estados()

        return jsonify({"success": success, "data": estados}), 200
    except Exception as e:
        print(f"Hubo un problema al obtener los estados. Motivo: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/estados_pedidos", methods=["GET"])
def get_all_estados_pedidos_route():
    try:
        success, estados = db.get_all_estados_pedidos()

        return jsonify({"success": success, "data": estados}), 200
    except Exception as e:
        print(f"Hubo un problema al obtener los estados. Motivo: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/pedidos", methods=["GET"])
def get_all_pedidos_route():
    try:
        success, estados = db.get_all_pedidos()

        return jsonify({"success": success, "data": estados}), 200
    except Exception as e:
        print(f"Hubo un problema al obtener los estados. Motivo: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/usuarios", methods=["GET"])
def get_all_usuarios_route():
    try:
        success, estados = db.get_all_usuarios()

        return jsonify({"success": success, "data": estados}), 200
    except Exception as e:
        print(f"Hubo un problema al obtener los estados. Motivo: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/modelos", methods=["GET"])
def get_all_modelos_route():
    try:
        success, modelos = db.get_all_modelos()
        return jsonify({"success": success, "data": modelos}), 200
    except Exception as e:
        print(f"Hubo un problema al obtener los modelos. Motivo: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/productos", methods=["GET"])
def get_productos_route():
    try:
        success, productos = db.get_all_productos()
        return jsonify({"success": success, "data": productos}), 200
    except Exception as e:
        print(f"Hubo un problema al obtener los productos. Motivo: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/add/modelo", methods=["GET"])
def add_modelo_route():
    args = request.args

    if not args:
        return jsonify({"success": False, "error": "Indica los datos del producto."}), 400

    try:
        id_modelo = args["id_modelo"]
        nombre_modelo = args["nombre_modelo"]
        precio = float(args["precio"])
        descripcion = args.get("descripcion", None)  # Optional, default to None
        categoria = args.get("categoria", None)  # Optional, default to None
        url_imagen = args.get("url_imagen", None) # Optional, default to None
        estante = args.get("estante", None)  # Optional, default to None
        pasillo = args.get("pasillo", None)  # Optional, default to None
        imagen2 = args.get("imagen2", None)  # Optional, default to None
        imagen3 = args.get("imagen3", None)  # Optional, default to None
        destacado = args.get("destacado", None)  # Optional, default to None

        success, modelo = db.add_modelo(id_modelo,
                                        nombre_modelo,
                                        precio,
                                        descripcion,
                                        categoria,
                                        url_imagen if url_imagen else "NULL",
                                        int(estante) if estante else "NULL",
                                        int(pasillo) if pasillo else "NULL",
                                        imagen2 if imagen2 else "NULL",
                                        imagen3 if imagen3 else "NULL",
                                        destacado if destacado else 0)
        return jsonify({"success": success, "data": modelo}), 200
    except Exception as e:
        print(f"Hubo un problema al insertar el modelo. Motivo: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/remove/modelo", methods=["GET"])
def remove_modelo_route():
    args = request.args

    if not args:
        return jsonify({"success": False, "error": "Indica el ID del modelo."}), 400

    try:
        id_modelo = args["id_modelo"]
        delete_productos = int(args.get("delete_productos", 1))

        success = db.remove_modelo(id_modelo, delete_productos != 0)
        return jsonify({"success": success}), 200
    except Exception as e:
        print(f"Hubo un problema al borrar el modelo. Motivo: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/edit/modelo", methods=["GET"])
def edit_modelo_route():
    args = request.args

    if not args:
        return jsonify({"success": False, "error": "Indica los datos del producto."}), 400

    try:
        id_modelo = args["id_modelo"]
        nombre_modelo = args.get("nombre_modelo", None)
        precio = args.get("precio", None)
        descripcion = args.get("descripcion", None)  # Optional, default to None
        categoria = args.get("categoria", None)  # Optional, default to None
        url_imagen = args.get("url_imagen", None) # Optional, default to None
        estante = args.get("estante", None)  # Optional, default to None
        pasillo = args.get("pasillo", None)  # Optional, default to None
        imagen2 = args.get("imagen2", None)  # Optional, default to None
        imagen3 = args.get("imagen3", None)  # Optional, default to None
        destacado = args.get("destacado", None)  # Optional, default to None
        print(f"Recibidos los datos del modelo: {id_modelo}, {nombre_modelo}, {precio}, {descripcion}, {categoria}, {url_imagen}, {estante}, {pasillo}, {imagen2}, {imagen3}, {destacado}")

        success, modelo = db.edit_modelo(id_modelo,
                                        nombre_modelo,
                                        float(precio) if precio else None,
                                        descripcion if descripcion else None,
                                        categoria if categoria else None,
                                        url_imagen if url_imagen else None,
                                        int(estante) if estante else None,
                                        int(pasillo) if pasillo else None,
                                        imagen2 if imagen2 else None,
                                        imagen3 if imagen3 else None,
                                         destacado if destacado else None)
        return jsonify({"success": success, "data": modelo}), 200
    except Exception as e:
        print(f"Hubo un problema al editar el modelo. Motivo: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/find/modelo", methods=["GET"])
def find_modelo_route():
    args = request.args

    try:
        id_modelo = args.get("id_modelo", None)
        nombre_modelo = args.get("nombre_modelo", None)
        precio = args.get("precio", None)
        url_imagen = args.get("url_imagen", None)
        estante = args.get("estante", None)
        pasillo = args.get("pasillo", None)

        success, modelo = db.find_modelo(id_modelo, nombre_modelo, precio, url_imagen, estante, pasillo)
        return jsonify({"success": success, "data": modelo}), 200
    except Exception as e:
        print(f"Hubo un problema al obtener el modelo. Motivo: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/add/producto", methods=["GET"])
def add_producto_route():
    args = request.args

    if not args:
        return jsonify({"success": False, "error": "Indica los datos del producto."}), 400

    try:
        id_etiqueta = args["id_etiqueta"]
        id_modelo = args["id_modelo"]
        id_estado = args["id_estado"]
        fecha_venta = args.get("fecha_venta", "NULL")  # Optional, default to NULL

        success, producto = db.add_producto(id_etiqueta, id_modelo, id_estado, fecha_venta)
        return jsonify({"success": success, "data": producto}), 200
    except Exception as e:
        print(f"Hubo un problema al insertar el producto. Motivo: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/remove/producto", methods=["GET"])
def remove_producto_route():
    args = request.args

    if not args:
        return jsonify({"success": False, "error": "Indica la etiqueta del producto."}), 400

    try:
        id_etiqueta = args["id_etiqueta"]

        success = db.remove_producto(id_etiqueta)
        return jsonify({"success": success}), 200
    except Exception as e:
        print(f"Hubo un problema al borrar el producto. Motivo: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/edit/producto", methods=["GET"])
def edit_producto_route():
    args = request.args

    if not args:
        return jsonify({"success": False, "error": "Indica los datos del producto."}), 400

    try:
        id_etiqueta = args["id_etiqueta"]
        id_modelo = args.get("id_modelo", None)
        id_estado = args.get("id_estado", None)
        fecha_venta = args.get("fecha_venta", None)  # Optional, default to NULL

        _, estados = db.get_all_estados()
        estados_validos = [estado['id_estado'] for estado in estados]
        if id_estado not in estados_validos: raise Exception(f"Intento de cambiar la etiqueta a una no válida ({id_estado}).")

        success, modelo = db.edit_producto(id_etiqueta, id_modelo, id_estado, fecha_venta)
        return jsonify({"success": success, "data": modelo}), 200
    except Exception as e:
        print(f"Hubo un problema al editar el modelo. Motivo: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/find/producto", methods=["GET"])
def find_producto_route():
    args = request.args

    try:
        id_etiqueta = args.get("id_etiqueta", None)
        id_modelo = args.get("id_modelo", None)
        id_estado = args.get("id_estado", None)
        fecha_venta = args.get("fecha_venta", None)

        success, producto = db.find_producto(id_etiqueta, id_modelo, id_estado, fecha_venta)
        return jsonify({"success": success, "data": producto}), 200
    except Exception as e:
        print(f"Hubo un problema al obtener el producto. Motivo: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/get/stock", methods=["GET"])
def get_stock_route():
    args = request.args

    if not args:
        return jsonify({"success": False, "error": "Indica el ID del producto."}), 400

    try:
        id_modelo = args.get("id_modelo")

        success, stock = db.get_stock(id_modelo)
        return jsonify({"success": success, "data": stock}), 200
    except Exception as e:
        print(f"Hubo un problema al obtener el stock. Motivo: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/img404')
def obtener_imagen():
    try:
        return send_file('../cdn/localhost-file-not-found.png', mimetype='image/jpeg')  # Ajusta el tipo MIME según la imagen
    except FileNotFoundError:
        return "Imagen not encontrada", 404

@app.route("/add/usuario", methods=["GET"])
def add_usuario_route():
    args = request.args

    if not args:
        return jsonify({"success": False, "error": "Indica los datos del producto."}), 400

    try:
        email = args["email"]
        nombre = args["nombre"]
        apellidos = args["apellidos"]
        direccion = args["direccion"]
        contrasena = args["contrasena"]
        telefono = args.get("telefono", "NULL")  # Optional, default to NULL

        success, usuarios = db.find_usuario(email_usuario=email)
        if success and usuarios:
            return jsonify({"success": False, "error": "Ya existe un usuario con ese email."}), 400

        success, usuario = db.add_usuario(email, nombre, apellidos, direccion, contrasena, telefono)
        return jsonify({"success": success, "data": usuario}), 200
    except Exception as e:
        print(f"Hubo un problema al insertar el producto. Motivo: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/remove/usuario", methods=["GET"])
def remove_usuario_route():
    args = request.args

    if not args:
        return jsonify({"success": False, "error": "Indica el email del usuario."}), 400

    try:
        email_usuario = args["email"]

        success = db.remove_usuario(email_usuario)
        return jsonify({"success": success}), 200
    except Exception as e:
        print(f"Hubo un problema al borrar el producto. Motivo: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/edit/usuario", methods=["GET"])
def edit_usuario_route():
    args = request.args

    if not args:
        return jsonify({"success": False, "error": "Indica los datos del usuario."}), 400

    try:
        email_usuario = args["email"]
        print("Hola, estoy editando un usuario")
        nombre_usuario = args.get("nombre", None)
        apellidos = args.get("apellidos", None)
        contrasena = args.get("contrasena", None)
        telefono = args.get("telefono", None)
        direccion = args.get("direccion", None)

        success, usuario = db.edit_usuario(
            email_usuario,
            nombre_usuario,
            apellidos,
            contrasena,
            telefono,
            direccion
        )
        return jsonify({"success": success, "data": usuario}), 200
    except Exception as e:
        print(f"Hubo un problema al editar el usuario. Motivo: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/login/usuario", methods=["GET"])
def find_usuario_route():
    args = request.args

    try:
        email = args.get("email", None)
        contrasena = args.get("contrasena", None)

        if not email or not contrasena:
            return jsonify({"success": False, "error": "Debes proporcionar email y contraseña."}), 400

        success, usuarios = db.find_usuario(email_usuario=email)
        if success and usuarios:
            usuario = usuarios[0]
            if usuario.get("contrasena") == contrasena:
                return jsonify({"success": True, "data": usuario}), 200
            else:
                return jsonify({"success": False, "error": "Contraseña incorrecta."}), 401
        else:
            return jsonify({"success": False, "error": "Usuario no encontrado."}), 404

    except Exception as e:
        print(f"Hubo un problema al obtener el producto. Motivo: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/add/pedido", methods=["GET"])
def add_pedido_route():
    args = request.args

    if not args:
        return jsonify({"success": False, "error": "Indica los datos del pedido."}), 400

    try:
        id_pedido = args["id_pedido"]
        email_usuario = args["email_usuario"]
        estado_pedido = args.get("estado_pedido", 'c')
        direccion = args.get("direccion", None)
        fecha_pedido = args.get("fecha_pedido", None)
        fecha_entrega = args.get("fecha_entrega", None)
        mensaje = args.get("mensaje", None)
        print(f"Recibidos los datos del pedido: {id_pedido}, {email_usuario}, {estado_pedido}, {direccion}, {fecha_pedido}, {fecha_entrega}, {mensaje}")

        success, pedido = db.add_pedido(id_pedido, email_usuario, estado_pedido, direccion, fecha_pedido, fecha_entrega, mensaje)
        return jsonify({"success": success, "data": pedido}), 200
    except Exception as e:
        print(f"Hubo un problema al insertar el producto. Motivo: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/remove/pedido", methods=["GET"])
def remove_pedido_route():
    args = request.args

    if not args:
        return jsonify({"success": False, "error": "Indica el ID del pedido."}), 400

    try:
        id_pedido = args["id_pedido"]

        success = db.remove_pedido(id_pedido)
        return jsonify({"success": success}), 200
    except Exception as e:
        print(f"Hubo un problema al borrar el producto. Motivo: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/edit/pedido", methods=["GET"])
def edit_pedido_route():
    args = request.args

    if not args:
        return jsonify({"success": False, "error": "Indica los datos del pedido."}), 400

    try:
        id_pedido = args["id_pedido"]
        email_usuario = args.get("email_usuario", None)
        estado_pedido = args.get("estado_pedido", None)
        direccion = args.get("direccion", None)
        fecha = args.get("fecha", None)
        fecha_entrega = args.get("fecha_entrega", None)
        mensaje = args.get("mensaje", None)

        success, pedido = db.edit_pedido(
            id_pedido,
            email_usuario,
            estado_pedido,
            direccion,
            fecha,
            fecha_entrega,
            mensaje
        )
        return jsonify({"success": success, "data": pedido}), 200
    except Exception as e:
        print(f"Hubo un problema al editar el pedido. Motivo: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/find/pedido", methods=["GET"])
def find_pedido_route():
    args = request.args

    try:
        id_pedido = args.get("id_pedido", None)
        email_usuario = args.get("email_usuario", None)
        if id_pedido is None:
            success, pedido = db.find_pedido(email_usuario=email_usuario)
        elif email_usuario is None:
            success, pedido = db.find_pedido(id_pedido=id_pedido)
        else:
            success, pedido = db.find_pedido(id_pedido, email_usuario)
        return jsonify({"success": success, "data": pedido}), 200
    except Exception as e:
        print(f"Hubo un problema al obtener el pedido. Motivo: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/add/pro_pedido", methods=["GET"])
def add_pro_pedido_route():
    args = request.args

    try:
        id_pedido = args["id_pedido"]
        id_producto = args["id_producto"]
        encontrado, precio = db.get_precio_producto(id_producto)

        success, error = db.add_pro_pedido(id_pedido, id_producto, precio)

        if success:
            return jsonify({"success": True, "message": "Producto añadido al pedido correctamente."}), 200
        else:
            return jsonify({"success": False, "error": error}), 400
    except Exception as e:
        print(f"Hubo un problema al añadir el producto al pedido. Motivo: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/remove/pro_pedido", methods=["GET"])
def remove_pro_pedido_route():
    args = request.args

    try:
        id_pedido = args["id_pedido"]
        id_producto = args["id_producto"]

        success, error = db.remove_pro_pedido(id_pedido, id_producto)
        if success:
            return jsonify({"success": True}), 200
        else:
            return jsonify({"success": False, "error": error}), 400
    except Exception as e:
        print(f"Hubo un problema al eliminar el pro_pedido. Motivo: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/pro_pedidos", methods=["GET"])
def get_all_pro_pedidos_route():
    try:
        success, data = db.get_all_pro_pedidos()
        return jsonify({"success": success, "data": data}), 200
    except Exception as e:
        print(f"Hubo un problema al obtener todos los pro_pedidos. Motivo: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/get/productos_por_pedido", methods=["GET"])
def get_productos_por_pedido_route():
    args = request.args

    try:
        id_pedido = args["id_pedido"]

        success, productos = db.get_productos_by_pedido(id_pedido)
        print(productos[0]["id_modelo"])
        if productos[0]["id_modelo"] == None:
            return jsonify({"success": success, "data": None}), 200
        return jsonify({"success": success, "data": productos}), 200
    except Exception as e:
        print(f"Hubo un problema al obtener productos del pedido. Motivo: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/add/item", methods=["GET"])
def add_item_route():
    args = request.args

    try:
        id_pedido = args["id_pedido"]
        id_modelo = args["id_modelo"]

        # Buscar un producto con ese id_modelo y estado 'd'
        success, productos = db.find_producto(id_modelo=id_modelo, id_estado="d")
        if not (success and productos):
            return jsonify({"success": False, "error": "No se encontró un producto disponible con ese modelo."}), 404
        id_producto = productos[0]["id_etiqueta"]
        print(f"Producto encontrado: {id_producto}")

        # Poner el estado del producto a 'v' (vendido)
        correct, products = db.edit_producto(id_etiqueta=id_producto, id_estado="c", fecha_venta=datetime.now().strftime("%Y-%m-%d"))

        encontrado, precio = db.get_precio_producto(id_producto)

        success, error = db.add_pro_pedido(id_pedido, id_producto, precio)

        if success:
            return jsonify({"success": True, "message": "Producto añadido al pedido correctamente."}), 200
        else:
            return jsonify({"success": False, "error": error}), 400
    except Exception as e:
        print(f"Hubo un problema al añadir el producto al pedido. Motivo: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/pedidos/gestor", methods=["GET"])
def get_all_pedidos_gestor_route():
    try:
        success, estados = db.get_all_pedidos_gestor()

        return jsonify({"success": success, "data": estados}), 200
    except Exception as e:
        print(f"Hubo un problema al obtener los estados. Motivo: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/pedidos_terminados/gestor", methods=["GET"])
def get_all_pedidos_terminados_gestor_route():
    try:
        success, estados = db.get_all_pedidos_terminados_gestor()

        return jsonify({"success": success, "data": estados}), 200
    except Exception as e:
        print(f"Hubo un problema al obtener los estados. Motivo: {e}")
        return jsonify({"success": False, "error": str(e)}), 500
