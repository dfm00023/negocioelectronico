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
        url_imagen = args.get("url_imagen", None) # Optional, default to None
        estante = args.get("estante", None)  # Optional, default to None
        pasillo = args.get("pasillo", None)  # Optional, default to None

        success, modelo = db.add_modelo(id_modelo,
                                        nombre_modelo,
                                        precio,
                                        url_imagen if url_imagen else "NULL",
                                        int(estante) if estante else "NULL",
                                        int(pasillo) if pasillo else "NULL")
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
        url_imagen = args.get("url_imagen", None) # Optional, default to None
        estante = args.get("estante", None)  # Optional, default to None
        pasillo = args.get("pasillo", None)  # Optional, default to None

        success, modelo = db.edit_modelo(id_modelo,
                                        nombre_modelo,
                                        float(precio) if precio else None,
                                        url_imagen if url_imagen else None,
                                        int(estante) if estante else None,
                                        int(pasillo) if pasillo else None)
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