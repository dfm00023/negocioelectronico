import sqlite3
from idlelib.pyshell import use_subprocess
from typing import Optional

class DataBase:
    def __init__(self, database_file: str):
        self.database_file = database_file
        self.__init_db()

    def __get_db_connection(self):
        """Establece una conexión a la base de datos SQLite."""
        conn = sqlite3.connect(self.database_file)
        conn.row_factory = sqlite3.Row # Para acceder a los resultados como diccionarios
        conn.execute("PRAGMA foreign_keys = 1;")
        return conn

    def __init_db(self) -> None:
        """Inicializa la base de datos (crea tablas si no existen)."""
        try:
            with self.__get_db_connection() as conn:
                cursor = conn.cursor()

                cursor.execute("PRAGMA foreign_keys = 1;")

                try:
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS estado (
                            id_estado VARCHAR(1) PRIMARY KEY,
                            nombre_estado VARCHAR(15) NOT NULL
                        );
                    """)
                except sqlite3.OperationalError:
                    pass

                try:
                    cursor.execute("INSERT INTO estado (id_estado, nombre_estado) VALUES ('d', 'disponible')")
                except sqlite3.IntegrityError:
                    pass
                try:
                    cursor.execute("INSERT INTO estado (id_estado, nombre_estado) VALUES ('c', 'comprado')")
                except sqlite3.IntegrityError:
                    pass
                try:
                    cursor.execute("INSERT INTO estado (id_estado, nombre_estado) VALUES ('r', 'robado')")
                except sqlite3.IntegrityError:
                    pass

                try:
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS modelo (
                            id_modelo VARCHAR(5) PRIMARY KEY,
                            nombre_modelo TEXT NOT NULL,
                            precio NUMBER(6,2) NOT NULL,
                            descripcion TEXT,
                            categoria VARCHAR(20),
                            url_imagen TEXT,
                            estante INTEGER,
                            pasillo INTEGER
                        );
                    """)
                except sqlite3.OperationalError:
                    pass

                try:
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS producto (
                            id_etiqueta VARCHAR(20) PRIMARY KEY,
                            id_modelo VARCHAR(5) NOT NULL,
                            id_estado VARCHAR(1) NOT NULL,
                            fecha_venta DATE,
                            FOREIGN KEY (id_modelo) REFERENCES modelo(id_modelo),
                            FOREIGN KEY (id_estado) REFERENCES estado(id_estado)
                        );
                    """)
                except sqlite3.OperationalError:
                    pass

                try:
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS usuario (
                        email_usuario VARCHAR(254) PRIMARY KEY,
                        nombre_usuario TEXT NOT NULL,
                        apellidos TEXT NOT NULL,
                        contrasena TEXT NOT NULL,
                        telefono VARCHAR(9),
                        direccion TEXT NOT NULL
                    );
                    """)
                except sqlite3.OperationalError:
                    pass

                try:
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS estado_pedido (
                        id_estado_pedido VARCHAR(10) PRIMARY KEY,
                        estado_pedido TEXT NOT NULL
                    );
                    """)
                except sqlite3.OperationalError:
                    pass

                try:
                    cursor.execute("INSERT INTO estado_pedido (id_estado_pedido, estado_pedido) VALUES ('p', 'preparando')")
                except sqlite3.IntegrityError:
                    pass

                try:
                    cursor.execute("INSERT INTO estado_pedido (id_estado_pedido, estado_pedido) VALUES ('e', 'enviado')")
                except sqlite3.IntegrityError:
                    pass

                try:
                    cursor.execute("INSERT INTO estado_pedido (id_estado_pedido, estado_pedido) VALUES ('t', 'terminado')")
                except sqlite3.IntegrityError:
                    pass

                try:
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS pedido (
                        id_pedido VARCHAR(10) PRIMARY KEY,
                        email_usuario VARCHAR(254) REFERENCES usuario(email_usuario),
                        estado VARCHAR(10) REFERENCES estado_pedido(id_estado_pedido),
                        direccion TEXT NOT NULL,
                        fecha DATE NOT NULL,
                        fecha_entrega DATE,
                        mensaje TEXT
                    );
                    """)
                except sqlite3.OperationalError:
                    pass

                try:
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS pro_pedidos (
                        id_pedido VARCHAR(10),
                        id_producto VARCHAR(20),
                        precio NUMBER(6,2) NOT NULL,
                        PRIMARY KEY (id_pedido, id_producto),
                        FOREIGN KEY (id_pedido) REFERENCES pedido(id_pedido),
                        FOREIGN KEY (id_producto) REFERENCES producto(id_etiqueta)
                    );
                    """)
                except sqlite3.OperationalError:
                    pass

                conn.commit()

                print("Base de datos lista.")
        except sqlite3.Error as e:
            print(f"Error al inicializar la base de datos. Motivo: {e}")

    def get_all_estados(self) -> tuple[bool, Optional[list[dict]]]:
        """
        Obtiene todos los estados posibles.

        Returns:
            tuple: Una tupla donde el primer elemento indica si hubo éxito o no y el segundo un diccionario con los estados posibles o None en caso de error.
        """
        try:
            with self.__get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM estado")
                rows = cursor.fetchall()
                row_list = [dict(row) for row in rows]
                return True, row_list
        except sqlite3.Error as e:
            print(f"Hubo un problema con la base de datos. Motivo: {e}")
            return False, None

    def get_all_estados_pedidos(self) -> tuple[bool, Optional[list[dict]]]:
        """
        Obtiene todos los estados de los pedidos posibles.

        Returns:
            tuple: Una tupla donde el primer elemento indica si hubo éxito o no y el segundo un diccionario con los estados posibles o None en caso de error.
        """
        try:
            with self.__get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM estado_pedido")
                rows = cursor.fetchall()
                row_list = [dict(row) for row in rows]
                return True, row_list
        except sqlite3.Error as e:
            print(f"Hubo un problema con la base de datos. Motivo: {e}")
            return False, None

    def get_all_usuarios(self) -> tuple[bool, Optional[list[dict]]]:
        """
        Obtiene todos los usuarios posibles.

        Returns:
            tuple: Una tupla donde el primer elemento indica si hubo éxito o no y el segundo un diccionario con los usuarios posibles o None en caso de error.
        """
        try:
            with self.__get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM usuario")
                rows = cursor.fetchall()
                row_list = [dict(row) for row in rows]
                return True, row_list
        except sqlite3.Error as e:
            print(f"Hubo un problema con la base de datos. Motivo: {e}")
            return False, None

    def get_all_pedidos(self) -> tuple[bool, Optional[list[dict]]]:
        """
        Obtiene todos los pedidos posibles.

        Returns:
            tuple: Una tupla donde el primer elemento indica si hubo éxito o no y el segundo un diccionario con los pedidos posibles o None en caso de error.
        """
        try:
            with self.__get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM pedido")
                rows = cursor.fetchall()
                row_list = [dict(row) for row in rows]
                return True, row_list
        except sqlite3.Error as e:
            print(f"Hubo un problema con la base de datos. Motivo: {e}")
            return False, None

    def get_all_modelos(self) -> tuple[bool, Optional[list[dict]]]:
        """
        Obtiene todos los modelos.

        Returns:
            tuple: Una tupla donde el primer elemento indica si hubo éxito o no y el segundo un diccionario con los modelos o None en caso de error.
        """
        try:
            with self.__get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT
                        m.id_modelo,
                        m.nombre_modelo,
                        m.precio,
                        m.descripcion,
                        m.categoria,
                        m.url_imagen,
                        m.estante,
                        m.pasillo,
                        COUNT(p.id_modelo) AS "stock"
                    FROM
                        modelo m
                    LEFT JOIN -- Asegura que todos los modelos estén presentes
                        producto p ON m.id_modelo = p.id_modelo AND p.id_estado = 'd'
                    GROUP BY
                        m.id_modelo,
                        m.nombre_modelo,
                        m.precio,
                        m.descripcion,
                        m.categoria,
                        m.url_imagen,
                        m.estante,
                        m.pasillo
                    ORDER BY
                        m.nombre_modelo;
                """)
                rows = cursor.fetchall()
                row_list = [dict(row) for row in rows]
                return True, row_list
        except sqlite3.Error as e:
            print(f"Hubo un problema con la base de datos. Motivo: {e}")
            return False, None

    def get_all_productos(self) -> tuple[bool, Optional[list[dict]]]:
        """
        Obtiene todos los productos de la tabla producto.

        Returns:
            tuple: Una tupla que contiene un booleano indicando éxito (True) o fallo (False), y un diccionario con los productos o None en caso de error.
        """
        try:
            with self.__get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM producto")
                rows = cursor.fetchall()
                row_list = [dict(row) for row in rows]
                return True, row_list
        except sqlite3.Error as e:
            print(f"Hubo un problema con la base de datos. Motivo: {e}")
            return False, None

    def add_modelo(self, id_modelo: str, nombre_modelo: str, precio: float, descripcion: Optional[str] = "NULL", categoria: Optional[str] = "NULL", url_imagen: Optional[str] = "NULL", estante: Optional[int] = "NULL",
                   pasillo: Optional[int] = "NULL") -> tuple[bool, Optional[list[dict]]]:
        """
        Agrega un nuevo modelo a la base de datos.

        Args:
            id_modelo (str): El ID único del modelo. Debe ser una cadena.
            nombre_modelo (str): El nombre del modelo. Debe ser una cadena.
            precio (float): El precio del modelo. Debe ser un número flotante.
            descripcion (Optional[str]): Una descripción del modelo. Opcional, puede ser None.
            categoria (Optional[str]): La categoría del modelo. Opcional, puede ser None.
            url_imagen (Optional[str]): Enlace a la imagen. Opcional, puede ser None.
            estante (Optional[int]): El número de estante donde se ubica el modelo. Opcional, puede ser None.
            pasillo (Optional[int]): El número de pasillo donde se ubica el modelo. Opcional, puede ser None.

        Returns:
            tuple[bool, Optional[list[dict]]]: Una tupla que indica si la operación fue exitosa (True/False) y, en caso de éxito, una cadena JSON con los detalles del modelo insertado. Si falla, devuelve None.
        """
        try:
            with self.__get_db_connection() as conn:
                cursor = conn.cursor()
                query = "INSERT INTO modelo (id_modelo, nombre_modelo, precio, descripcion, categoria, url_imagen, estante, pasillo) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
                values = (id_modelo, nombre_modelo, precio, descripcion, categoria, url_imagen, estante, pasillo)
                cursor.execute(query, values)
                conn.commit()
                # Una vez confirmados los cambios se obtiene el elemento insertado para devolverlo en la confirmación.
                cursor.execute("SELECT * FROM modelo ORDER BY rowid DESC LIMIT 1")
                rows = cursor.fetchall()
                row_list = [dict(row) for row in rows]
                return True, row_list
        except sqlite3.Error as e:
            print(f"Hubo un problema con la base de datos. Motivo: {e}")
            return False, None

    def edit_modelo(self, id_modelo: str, nombre_modelo: str = None, precio: Optional[float] = None, descripcion: Optional[str] = None, categoria: Optional[str] = None, url_imagen: Optional[str] = None, estante: Optional[int] = None,
                   pasillo: Optional[int] = None) -> tuple[bool, Optional[list[dict]]]:
        """
        Edita un modelo de la base de datos.

        Args:
            id_modelo (str): El ID único del modelo. Debe ser una cadena.
            nombre_modelo (str): El nombre del modelo. Debe ser una cadena.
            precio (Optional[float]): El precio del modelo. Opcional, puede ser None.
            descripcion (Optional[str]): La descripción del modelo. Opcional, puede ser None.
            categoria (Optional[str]): La categoría del modelo. Opcional, puede ser None.
            url_imagen (Optional[str]): Enlace a la imagen. Opcional, puede ser None.
            estante (Optional[int]): El número de estante donde se ubica el modelo. Opcional, puede ser None.
            pasillo (Optional[int]): El número de pasillo donde se ubica el modelo. Opcional, puede ser None.

        Returns:
            tuple[bool, Optional[list[dict]]]: Una tupla que indica si la operación fue exitosa (True/False) y, en caso de éxito, una cadena JSON con los detalles del modelo insertado. Si falla, devuelve None.
        """
        try:
            with self.__get_db_connection() as conn:
                cursor = conn.cursor()

                # Se guardan el nombre de la columna y su valor en pares.
                pairs = zip(
                    ['nombre_modelo', 'precio', 'descripcion', 'categoria', 'url_imagen', 'estante', 'pasillo'], # Nombre columna
                    [nombre_modelo, precio,descripcion, categoria, url_imagen, estante, pasillo] # Valor
                )

                # Se filtran por los que sí tienen un valor que modificar.
                filtered_pairs = [pair for pair in pairs if pair[1] is not None]

                if len(filtered_pairs) == 0:
                    print("Se ha intentado editar un modelo sin proporcionar datos")
                    return False, None

                # Se agrupan las columnas con el formato para evitar la inyección SQL.
                columns = [f'{pair[0]} = ?' for pair in filtered_pairs]
                # También los values
                values = tuple([pair[1] for pair in filtered_pairs])
                values = values + (id_modelo,)

                query = f"UPDATE modelo SET {', '.join(columns)} WHERE id_modelo = ?"
                cursor.execute(query, values)
                conn.commit()
                # Una vez confirmados los cambios se obtiene el elemento editado para devolverlo en la confirmación.
                cursor.execute("SELECT * FROM modelo WHERE id_modelo = ?", (id_modelo,))
                rows = cursor.fetchall()
                row_list = [dict(row) for row in rows]
                return True, row_list
        except sqlite3.Error as e:
            print(f"Hubo un problema con la base de datos. Motivo: {e}")
            return False, None

    def remove_modelo(self, id_modelo: str, delete_productos: Optional[bool] = True) -> bool:
        """
        Elimina un modelo de la base de datos y todos los productos que estén asociados.

        Args:
            id_modelo (str): El ID único del modelo a eliminar. Debe ser una cadena.
            delete_productos (bool): Flag para eliminar también los productos asociados. Opcional, puede ser True.

        Returns:
            bool: Un valor indicando si la operación fue exitosa (True/False).
        """
        try:
            with self.__get_db_connection() as conn:
                cursor = conn.cursor()
                if delete_productos:
                    query = "DELETE FROM producto WHERE id_modelo = ?"
                    values = (id_modelo,)
                    cursor.execute(query, values)

                query = "DELETE FROM modelo WHERE id_modelo = ?"
                values = (id_modelo,)
                cursor.execute(query, values)
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"Hubo un problema con la base de datos. Motivo: {e}")
            return False

    def find_modelo(self, id_modelo: Optional[str] = None, nombre_modelo: Optional[str] = None,
                    precio: Optional[float] = None, url_imagen: Optional[str] = None, estante: Optional[int] = None,
                    pasillo: Optional[int] = None) -> tuple[bool, Optional[list[dict]]]:
        """
        Obtiene un modelo de la base de datos.

        Args:
            id_modelo (Optional[str]): El ID único del modelo. Opcional, puede ser None.
            nombre_modelo (Optional[str]): El nombre del modelo. Opcional, puede ser None.
            precio (Optional[float]): El precio del modelo. Opcional, puede ser None.
            url_imagen (Optional[str]): Enlace a la imagen. Opcional, puede ser None.
            estante (Optional[int]): El número de estante donde se ubica el modelo. Opcional, puede ser None.
            pasillo (Optional[int]): El número de pasillo donde se ubica el modelo. Opcional, puede ser None.

        Returns:
            tuple[bool, Optional[list[dict]]]: Una tupla que indica si la operación fue exitosa (True/False) y, en caso de éxito, una cadena JSON con los detalles del modelo insertado. Si falla, devuelve None.
        """
        try:
            with self.__get_db_connection() as conn:
                cursor = conn.cursor()

                # Se guardan el nombre de la columna y su valor en pares.
                pairs = zip(
                    ['m.id_modelo', 'm.nombre_modelo', 'm.precio', 'm.url_imagen', 'm.estante', 'm.pasillo'],
                    [id_modelo, nombre_modelo, precio, url_imagen, estante, pasillo]
                )

                # Se filtran por los que sí tienen un valor que modificar.
                filtered_pairs = [pair for pair in pairs if pair[1] is not None]

                # Se agrupan las columnas con el formato para evitar la inyección SQL.
                columns = [f"{pair[0]} = ?" for pair in filtered_pairs]
                # También los valores
                values = [pair[1] for pair in filtered_pairs]
                # Se crea la condición si se indica al menos un valor para buscar.
                condition = f"{' and '.join(columns)}" if len(columns) > 0 else ''
                query = f"""
                    SELECT
                        m.id_modelo,
                        m.nombre_modelo,
                        m.precio,
                        m.url_imagen,
                        m.estante,
                        m.pasillo,
                        COUNT(p.id_modelo) AS "stock"
                    FROM
                        modelo m 
                    LEFT JOIN -- Hacemos LEFT JOIN para incluir modelos sin stock disponible
                        producto p ON m.id_modelo = p.id_modelo AND p.id_estado = 'd'
                    WHERE
                        {condition}
                    GROUP BY
                        m.id_modelo,
                        m.nombre_modelo,
                        m.precio,
                        m.url_imagen,
                        m.estante,
                        m.pasillo
                    ORDER BY
                        m.nombre_modelo;
                """
                cursor.execute(query, values)
                rows = cursor.fetchall()
                row_list = [dict(row) for row in rows]
                return True, row_list
        except sqlite3.Error as e:
            print(f"Hubo un problema con la base de datos. Motivo: {e}")
            return False, None

    def add_producto(self, id_etiqueta: str, id_modelo: str, id_estado: str, fecha_venta: Optional[str] = "NULL") \
            -> tuple[bool, Optional[list[dict]]]:
        """
        Agrega un nuevo producto a la base de datos.

        Args:
            id_etiqueta (str): El ID único de la etiqueta del producto. Debe ser una cadena.
            id_modelo (str): El ID del modelo asociado al producto. Debe coincidir con el valor de 'id_modelo' en la tabla 'modelo'.
            id_estado (str): El ID del estado actual del producto. Debe coincidir con el valor de 'id_estado' en la tabla 'estado'.
            fecha_venta (Optional[str]): La fecha de venta del producto. Opcional, puede ser None.

        Returns:
            tuple[bool, Optional[list[dict]]]: Una tupla que indica si la operación fue exitosa (True/False) y, en caso de éxito, una cadena JSON con los detalles del producto insertado. Si falla, devuelve None.
        """
        try:
            with self.__get_db_connection() as conn:
                cursor = conn.cursor()
                query = "INSERT INTO producto (id_etiqueta, id_modelo, id_estado, fecha_venta) VALUES (?, ?, ?, ?)"
                values = (id_etiqueta, id_modelo, id_estado, fecha_venta)
                cursor.execute(query, values)
                conn.commit()
                cursor.execute("SELECT * FROM producto ORDER BY rowid DESC LIMIT 1")
                rows = cursor.fetchall()
                row_list = [dict(row) for row in rows]
                return True, row_list
        except sqlite3.Error as e:
            print(f"Hubo un problema con la base de datos. Motivo: {e}")
            return False, None

    def edit_producto(self, id_etiqueta: str, id_modelo: Optional[str] = None, id_estado: Optional[str] = None,
                      fecha_venta: Optional[str] = None) -> tuple[bool, Optional[list[dict]]]:
        """
        Edita un producto de la base de datos.

        Args:
            id_etiqueta (str): El ID único de la etiqueta del producto. Debe ser una cadena.
            id_modelo (Optional[str]): El ID del modelo asociado al producto. Debe coincidir con el valor de 'id_modelo' en la tabla 'modelo' aunque es opcional y puede ser None.
            id_estado (Optional[str]): El ID del estado actual del producto. Debe coincidir con el valor de 'id_estado' en la tabla 'estado' aunque es opcional y puede ser None.
            fecha_venta (Optional[str]): La fecha de venta del producto. Opcional, puede ser None.

        Returns:
            tuple[bool, Optional[list[dict]]]: Una tupla que indica si la operación fue exitosa (True/False) y, en caso de éxito, una cadena JSON con los detalles del producto insertado. Si falla, devuelve None.
        """
        try:
            with self.__get_db_connection() as conn:
                cursor = conn.cursor()

                # Almacena los pares (columna, valor).
                pairs = zip(
                    ['id_modelo', 'id_estado', 'fecha_venta'],
                    [id_modelo, id_estado, fecha_venta]
                )

                # Filtran los pares manteniendo los que sí tienen un valor a cambiar.
                filtered_pairs = [pair for pair in pairs if pair[1] is not None]

                if len(filtered_pairs) == 0:
                    print("Se ha intentado editar un producto sin proporcionar datos")
                    return False, None

                # Se extraen las columnas y se aplica el formato necesario para evitar la inyección SQL.
                columns = [f"{pair[0]} = ?" for pair in filtered_pairs]
                # Igual con los valores de las columnas.
                values = tuple([pair[1] for pair in filtered_pairs])
                values = values + (id_etiqueta,)

                query = f"UPDATE producto SET {', '.join(columns)} WHERE id_etiqueta = ?"
                cursor.execute(query, values)
                conn.commit()
                cursor.execute("SELECT * FROM producto WHERE id_etiqueta = ?", (id_etiqueta,))
                rows = cursor.fetchall()
                row_list = [dict(row) for row in rows]
                return True, row_list
        except sqlite3.Error as e:
            print(f"Hubo un problema con la base de datos. Motivo: {e}")
            return False, None

    def remove_producto(self, id_etiqueta: str) -> bool:
        """
        Elimina un producto de la base de datos.

        Args:
            id_etiqueta (str): El ID único del producto a eliminar. Debe ser una cadena.

        Returns:
            bool: Un valor indicando si la operación fue exitosa (True/False).
        """
        try:
            with self.__get_db_connection() as conn:
                cursor = conn.cursor()
                query = "DELETE FROM producto WHERE id_etiqueta = ?"
                values = (id_etiqueta,) # Importante: La coma crea una tupla de un solo elemento
                cursor.execute(query, values)
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"Hubo un problema con la base de datos. Motivo: {e}")
            return False

    def find_producto(self, id_etiqueta: Optional[str] = None, id_modelo: Optional[str] = None,
                      id_estado: Optional[str] = None, fecha_venta: Optional[str] = None) \
            -> tuple[bool, Optional[list[dict]]]:
        """
        Obtiene un producto de la base de datos.

        Args:
            id_etiqueta (Optional[str]): El ID único de la etiqueta del producto. Opcional, puede ser None.
            id_modelo (Optional[str]): El ID del modelo asociado al producto. Opcional, puede ser None.
            id_estado (Optional[str]): El ID del estado actual del producto. Opcional, puede ser None.
            fecha_venta (Optional[str]): La fecha de venta del producto. Opcional, puede ser None.

        Returns:
            tuple[bool, Optional[list[dict]]]: Una tupla que indica si la operación fue exitosa (True/False) y, en caso de éxito, una cadena JSON con los detalles del modelo insertado. Si falla, devuelve None.
        """
        try:
            with self.__get_db_connection() as conn:
                cursor = conn.cursor()

                # Almacena los pares (columna, valor).
                pairs = zip(
                    ['id_etiqueta', 'id_modelo', 'id_estado', 'fecha_venta'],
                    [id_etiqueta, id_modelo, id_estado, fecha_venta]
                )

                # Filtran los pares manteniendo los que sí tienen un valor a cambiar.
                filtered_pairs = [pair for pair in pairs if pair[1] is not None]

                # Se extraen las columnas y se aplica el formato necesario para evitar la inyección SQL.
                columns = [f"{pair[0]} = ?" for pair in filtered_pairs]
                # Igual con los valores de las columnas.
                values = tuple([pair[1] for pair in filtered_pairs])
                # Se crea la condición si se indica al menos un valor para buscar.
                condition = f"WHERE {' and '.join(columns)}" if len(columns) > 0 else ''

                query = f"SELECT * FROM producto {condition}"
                cursor.execute(query, values)
                rows = cursor.fetchall()
                row_list = [dict(row) for row in rows]
                return True, row_list
        except sqlite3.Error as e:
            print(f"Hubo un problema con la base de datos. Motivo: {e}")
            return False, None

    def get_stock(self, id_modelo: str) -> tuple[bool, Optional[int]]:
        """
        Obtiene el stock actual de un producto dado su ID de modelo.

        Args:
            id_modelo (str): El ID del modelo del producto para el cual se desea obtener el stock.

        Returns:
            tuple[bool, Optional[int]]: Una tupla que indica si la operación fue exitosa (True/False) y, en caso de éxito, el stock actual como un entero. Si falla, devuelve False y None.
        """
        try:
            with self.__get_db_connection() as conn:
                cursor = conn.cursor()
                query = """
                    SELECT COUNT(*)
                    FROM producto p
                    WHERE p.id_modelo = ? and p.id_estado = 'd'
                """
                values = (id_modelo,)
                cursor.execute(query, values)
                resultado = cursor.fetchone()
                print(resultado)
                stock = resultado[0]
                return True, stock
        except sqlite3.Error as e:
            print(f"Hubo un problema con la base de datos. Motivo: {e}")
            return False, None

    def add_usuario(self, email:str, nombre: str, apellidos: str, direccion: str, contrasena:str, telefono: Optional[str] = "NULL") \
            -> tuple[bool, Optional[list[dict]]]:
        """
    Agrega un nuevo usuario a la base de datos.

    Args:
        email (str): El correo electrónico del usuario.
        nombre (str): El nombre del usuario.
        apellidos (str): Los apellidos del usuario.
        direccion (str): La dirección del usuario.
        contrasena (str): La contraseña del usuario.
        telefono (Optional[str]): El teléfono del usuario. Opcional, puede ser None.

    Returns:
        tuple[bool, Optional[list[dict]]]: Una tupla que indica si la operación fue exitosa (True/False) y, en caso de éxito, una lista con los detalles del usuario insertado. Si falla, devuelve None.
    """
        try:
            with self.__get_db_connection() as conn:
                cursor = conn.cursor()
                query = "INSERT INTO usuario (email_usuario, nombre_usuario, apellidos, contrasena, telefono, direccion) VALUES (?, ?, ?, ?, ?, ?)"
                values = (email, nombre, apellidos, contrasena, telefono, direccion)
                cursor.execute(query, values)
                conn.commit()
                cursor.execute("SELECT * FROM producto ORDER BY rowid DESC LIMIT 1")
                rows = cursor.fetchall()
                row_list = [dict(row) for row in rows]
                return True, row_list
        except sqlite3.Error as e:
            print(f"Hubo un problema con la base de datos. Motivo: {e}")
            return False, None

    def edit_usuario(self, email_usuario: str, nombre_usuario: Optional[str] = None, apellidos: Optional[str] = None,
                     contrasena: Optional[str] = None, telefono: Optional[str] = None,
                     direccion: Optional[str] = None) -> tuple[bool, Optional[list[dict]]]:
        """
        Edita un usuario de la base de datos.

        Args:
            email_usuario (str): El ID único del usuario. Debe ser una cadena.
            nombre_usuario (Optional[str]): El nombre del usuario. Opcional, puede ser None.
            apellidos (Optional[str]): Los apellidos del usuario. Opcional, puede ser None.
            contrasena (Optional[str]): La contraseña del usuario. Opcional, puede ser None.
            telefono (Optional[str]): El teléfono del usuario. Opcional, puede ser None.
            direccion (Optional[str]): La dirección del usuario. Opcional, puede ser None.

        Returns:
            tuple[bool, Optional[list[dict]]]: Una tupla que indica si la operación fue exitosa (True/False) y, en caso de éxito, una lista con los detalles del usuario editado. Si falla, devuelve None.
        """
        try:
            with self.__get_db_connection() as conn:
                cursor = conn.cursor()

                pairs = zip(
                    ['nombre_usuario', 'apellidos', 'contrasena', 'telefono', 'direccion'],
                    [nombre_usuario, apellidos, contrasena, telefono, direccion]
                )

                filtered_pairs = [pair for pair in pairs if pair[1] is not None]

                if len(filtered_pairs) == 0:
                    print("Se ha intentado editar un usuario sin proporcionar datos")
                    return False, None

                columns = [f"{pair[0]} = ?" for pair in filtered_pairs]
                values = tuple([pair[1] for pair in filtered_pairs])
                values = values + (email_usuario,)

                query = f"UPDATE usuario SET {', '.join(columns)} WHERE email_usuario = ?"
                cursor.execute(query, values)
                conn.commit()
                cursor.execute("SELECT * FROM usuario WHERE email_usuario = ?", (email_usuario,))
                rows = cursor.fetchall()
                row_list = [dict(row) for row in rows]
                return True, row_list
        except sqlite3.Error as e:
            print(f"Hubo un problema con la base de datos. Motivo: {e}")
            return False, None

    def remove_usuario(self, email_usuario: str) -> bool:
        """
        Elimina un usuario de la base de datos.

        Args:
            email_usuario (str): El email del usuario a eliminar. Debe ser una cadena.

        Returns:
            bool: Un valor indicando si la operación fue exitosa (True/False).
        """
        try:
            with self.__get_db_connection() as conn:
                cursor = conn.cursor()
                query = "DELETE FROM usuario WHERE email_usuario = ?"
                values = (email_usuario,)  # Importante: La coma crea una tupla de un solo elemento
                print(values)
                cursor.execute(query, values)
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"Hubo un problema con la base de datos. Motivo: {e}")
            return False

    def find_usuario(self, email_usuario: Optional[str] = None) -> tuple[bool, Optional[list[dict]]]:
        """
        Busca un usuario en la base de datos por su email.

        Args:
            email_usuario (Optional[str]): El email del usuario a buscar. Opcional, puede ser None.

        Returns:
            tuple[bool, Optional[list[dict]]]: Una tupla que indica si la operación fue exitosa (True/False) y, en caso de éxito, una lista con los detalles del usuario encontrado. Si falla, devuelve None.
        """
        try:
            with self.__get_db_connection() as conn:
                cursor = conn.cursor()
                if email_usuario is not None:
                    query = "SELECT * FROM usuario WHERE email_usuario = ?"
                    cursor.execute(query, (email_usuario,))
                else:
                    query = "SELECT * FROM usuario"
                    cursor.execute(query)
                rows = cursor.fetchall()
                row_list = [dict(row) for row in rows]
                return True, row_list
        except sqlite3.Error as e:
            print(f"Hubo un problema con la base de datos. Motivo: {e}")
            return False, None

    def add_pedido(self, id_pedido: str, email_usuario: str, estado: str, direccion:str, fecha: str, fecha_entrega: Optional[str] = "NULL", mensaje: Optional[str] = "NULL") \
            -> tuple[bool, Optional[list[dict]]]:
        """
        Agrega un nuevo pedido a la base de datos.

        Args:
            id_pedido (str): El ID único del pedido. Debe ser una cadena.
            email_usuario (str): El email del usuario que realiza el pedido. Debe coincidir con el valor de 'email_usuario' en la tabla 'usuario'.
            estado (str): El estado del pedido. Debe coincidir con el valor de 'id_estado_pedido' en la tabla 'estado_pedido'.
            direccion (str): La dirección de envío del pedido.
            fecha (str): La fecha del pedido.
            fecha_entrega (Optional[str]): La fecha de entrega del pedido. Opcional, puede ser None.
            mensaje (Optional[str]): Un mensaje opcional asociado al pedido. Opcional, puede ser None.

        Returns:
            tuple[bool, Optional[list[dict]]]: Una tupla que indica si la operación fue exitosa (True/False) y, en caso de éxito, una lista con los detalles del pedido insertado. Si falla, devuelve None.
        """
        try:
            with self.__get_db_connection() as conn:
                cursor = conn.cursor()
                query = "INSERT INTO pedido (id_pedido, email_usuario, estado, direccion, fecha, fecha_entrega, mensaje) VALUES (?, ?, ?, ?, ?, ?, ?)"
                values = (id_pedido, email_usuario, estado, direccion, fecha, fecha_entrega, mensaje)
                cursor.execute(query, values)
                conn.commit()
                cursor.execute("SELECT * FROM pedido ORDER BY rowid DESC LIMIT 1")
                rows = cursor.fetchall()
                row_list = [dict(row) for row in rows]
                return True, row_list
        except sqlite3.Error as e:
            print(f"Hubo un problema con la base de datos. Motivo: {e}")
            return False, None

    def edit_pedido(self, id_pedido: str, email_usuario: Optional[str] = None, estado: Optional[str] = None, direccion: Optional[str] = None,
                    fecha: Optional[str] = None, fecha_entrega: Optional[str] = None,
                    mensaje: Optional[str] = None) -> tuple[bool, Optional[list[dict]]]:
        """
        Edita un pedido de la base de datos.

        Args:
            id_pedido (str): El ID único del pedido. Debe ser una cadena.
            email_usuario (Optional[str]): El email del usuario que realiza el pedido. Opcional, puede ser None.
            estado (Optional[str]): El estado del pedido. Opcional, puede ser None.
            direccion (Optional[str]): La dirección de envío del pedido. Opcional, puede ser None.
            fecha (Optional[str]): La fecha del pedido. Opcional, puede ser None.
            fecha_entrega (Optional[str]): La fecha de entrega del pedido. Opcional, puede ser None.
            mensaje (Optional[str]): Un mensaje opcional asociado al pedido. Opcional, puede ser None.

        Returns:
            tuple[bool, Optional[list[dict]]]: Una tupla que indica si la operación fue exitosa (True/False) y, en caso de éxito, una lista con los detalles del pedido editado. Si falla, devuelve None.
        """
        try:
            with self.__get_db_connection() as conn:
                cursor = conn.cursor()

                pairs = zip(
                    ['email_usuario', 'estado', 'direccion', 'fecha', 'fecha_entrega', 'mensaje'],
                    [email_usuario, estado, direccion, fecha, fecha_entrega, mensaje]
                )

                filtered_pairs = [pair for pair in pairs if pair[1] is not None]

                if len(filtered_pairs) == 0:
                    print("Se ha intentado editar un pedido sin proporcionar datos")
                    return False, None

                columns = [f"{pair[0]} = ?" for pair in filtered_pairs]
                values = tuple([pair[1] for pair in filtered_pairs])
                values = values + (id_pedido,)

                query = f"UPDATE pedido SET {', '.join(columns)} WHERE id_pedido = ?"
                cursor.execute(query, values)
                conn.commit()
                cursor.execute("SELECT * FROM pedido WHERE id_pedido = ?", (id_pedido,))
                rows = cursor.fetchall()
                row_list = [dict(row) for row in rows]
                return True, row_list
        except sqlite3.Error as e:
            print(f"Hubo un problema con la base de datos. Motivo: {e}")
            return False, None

    def remove_pedido(self, id_pedido: str) -> bool:
        """
        Elimina un pedido de la base de datos.

        Args:
            id_pedido (str): El ID único del pedido a eliminar. Debe ser una cadena.

        Returns:
            bool: Un valor indicando si la operación fue exitosa (True/False).
        """
        try:
            with self.__get_db_connection() as conn:
                cursor = conn.cursor()
                # Primero comrpobamos el estado del pedido para eliminar los productos asociados.
                cursor.execute("SELECT estado FROM pedido WHERE id_pedido = ?", (id_pedido,))
                rows = cursor.fetchall()
                estado = rows[0]['estado'] if rows else None
                if len(rows) == 0:
                    print(f"No se encontró el pedido con ID {id_pedido}.")
                    return False
                elif estado == 'c':
                    print(f"El pedido con ID {id_pedido} esta en carrito.")
                    cursor = conn.cursor()
                    query = "UPDATE producto SET id_estado = 'd' WHERE id_etiqueta = (SELECT id_producto FROM pro_pedidos WHERE id_pedido = ?)"
                    values = (id_pedido,)  # Importante: La coma crea una tupla de un solo elemento
                    cursor.execute(query, values)
                    conn.commit()
                    cursor = conn.cursor()
                    query = "DELETE FROM pro_pedidos WHERE id_pedido = ?"
                    values = (id_pedido,)  # Importante: La coma crea una tupla de un solo elemento
                    cursor.execute(query, values)
                    conn.commit()
                elif estado == 't':
                    print(f"El pedido con ID {id_pedido} esta terminado.")
                    cursor = conn.cursor()
                    query = "DELETE FROM pro_pedido WHERE id_pedido = ?"
                    values = (id_pedido,)  # Importante: La coma crea una tupla de un solo elemento
                    cursor.execute(query, values)
                    conn.commit()
                    cursor = conn.cursor()
                    query = "DELETE FROM producto WHERE id_etiqueta = (SELECT id_producto FROM pro_pedidos WHERE id_pedido = ?)"
                    values = (id_pedido,)  # Importante: La coma crea una tupla de un solo elemento
                    cursor.execute(query, values)
                    conn.commit()
                else:
                    print(f"El pedido con ID {id_pedido} esta en estado {estado}. No se eliminarán los productos asociados.")
                    return False
                # Finalmente eliminamos el pedido.
                cursor = conn.cursor()
                query = "DELETE FROM pedido WHERE id_pedido = ?"
                values = (id_pedido,)  # Importante: La coma crea una tupla de un solo elemento
                cursor.execute(query, values)
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"Hubo un problema con la base de datos. Motivo: {e}")
            return False

    def find_pedido(self, id_pedido: Optional[str] = None, email_usuario: Optional[str] = None) -> tuple[bool, Optional[list[dict]]]:
        """
        Busca un pedido en la base de datos.

        Args:
            id_pedido (Optional[str]): El ID único del pedido. Opcional, puede ser None.
            email_usuario (Optional[str]): El email del usuario a buscar. Opcional, puede ser None.

        Returns:
            tuple[bool, Optional[list[dict]]]: Una tupla que indica si la operación fue exitosa (True/False) y, en caso de éxito, una lista con los detalles del usuario encontrado. Si falla, devuelve None.
        """
        try:
            with self.__get_db_connection() as conn:
                cursor = conn.cursor()
                if id_pedido:
                    query = "SELECT p.id_pedido, p.direccion, p.email_usuario, p.fecha, p.fecha_entrega, p.mensaje, e.estado_pedido FROM pedido p, estado_pedido e WHERE e.id_estado_pedido = p.estado AND TRIM(email_usuario) = TRIM(?)"
                    cursor.execute(query, (id_pedido,))
                elif email_usuario is not None:
                    query = "SELECT p.id_pedido, p.direccion, p.email_usuario, p.fecha, p.fecha_entrega, p.mensaje, e.estado_pedido FROM pedido p, estado_pedido e WHERE e.id_estado_pedido = p.estado AND TRIM(email_usuario) = TRIM(?)"
                    cursor.execute(query, (email_usuario,))
                else:
                    query = "SELECT p.id_pedido, p.direccion, p.email_usuario, p.fecha, p.fecha_entrega, p.mensaje, e.estado_pedido FROM pedido p, estado_pedido e WHERE e.id_estado_pedido = p.estado"
                    cursor.execute(query)
                rows = cursor.fetchall()
                row_list = [dict(row) for row in rows]
                return True, row_list
        except sqlite3.Error as e:
            print(f"Hubo un problema con la base de datos. Motivo: {e}")
            return False, None

    def get_all_pro_pedidos(self) -> tuple[bool, Optional[list[dict]]]:
        """
        Obtiene todos los registros de la tabla pro_pedidos.

        Returns:
            tuple: Una tupla que contiene un booleano indicando éxito (True/False), y una lista de diccionarios con los registros o None en caso de error.
        """
        try:
            with self.__get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM pro_pedidos")
                rows = cursor.fetchall()
                row_list = [dict(row) for row in rows]
                return True, row_list
        except sqlite3.Error as e:
            print(f"Hubo un problema al obtener los pro_pedidos. Motivo: {e}")
            return False, None

    def add_pro_pedido(self, id_pedido: str, id_producto: str, precio: float) -> tuple[bool, Optional[list[dict]]]:
        """
        Agrega un producto a un pedido en la tabla pro_pedidos.

        Args:
            id_pedido (str): ID del pedido.
            id_producto (str): ID del producto.
            precio (float): Precio del producto en el momento de la compra.

        Returns:
            tuple: Una tupla con un booleano indicando éxito y un mensaje de error o None.
        """
        try:
            with self.__get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO pro_pedidos (id_pedido, id_producto, precio)
                    VALUES (?, ?, ?);
                """, (id_pedido, id_producto, precio))
                conn.commit()
                cursor.execute("SELECT * FROM pedido ORDER BY rowid DESC LIMIT 1")
                rows = cursor.fetchall()
                row_list = [dict(row) for row in rows]
                return True, row_list
        except sqlite3.IntegrityError as e:
            print(f"Error de integridad: {e}")
            return False, None
        except sqlite3.Error as e:
            print(f"Error de base de datos: {e}")
            return False, None

    def remove_pro_pedido(self, id_pedido: str, id_producto: str) -> tuple[bool, Optional[str]]:
        """
        Elimina un producto de un pedido en la tabla pro_pedidos.

        Args:
            id_pedido (str): ID del pedido.
            id_producto (str): ID del producto.

        Returns:
            tuple: Una tupla con un booleano indicando éxito y un mensaje de error o None.
        """
        try:
            with self.__get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    DELETE FROM pro_pedidos
                    WHERE id_pedido = ? AND id_producto = ?;
                """, (id_pedido, id_producto))
                conn.commit()
                if cursor.rowcount == 0:
                    return False, "No se encontró el producto en el pedido."
                return True, None
        except sqlite3.Error as e:
            return False, f"Error de base de datos: {e}"

    def get_productos_by_pedido(self, id_pedido: str) -> tuple[bool, Optional[list[dict]]]:
        """
        Obtiene los productos asociados a un pedido específico.

        Args:
            id_pedido (str): ID del pedido.

        Returns:
            tuple: Una tupla que contiene un booleano indicando éxito (True/False), y una lista de diccionarios con los productos o None en caso de error.
        """
        try:
            with self.__get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT m.id_modelo, m.nombre_modelo, COUNT(p.id_etiqueta) AS cantidad, pr.precio FROM modelo m, producto p, pro_pedidos pr WHERE m.id_modelo = p.id_modelo AND p.id_etiqueta = pr.id_producto AND pr.id_pedido = ?", (id_pedido,))
                rows = cursor.fetchall()
                row_list = [dict(row) for row in rows]
                return True, row_list
        except sqlite3.Error as e:
            print(f"Hubo un problema al obtener los productos del pedido '{id_pedido}'. Motivo: {e}")
            return False, None

    def get_precio_producto(self, id_producto: str) -> tuple[bool, Optional[float]]:
        """
        Obtiene el precio de un producto específico dado su ID.

        Args:
            id_producto (str): ID del producto.

        Returns:
            tuple: Una tupla que contiene un booleano indicando éxito (True/False), y el precio como float o None en caso de error.
        """
        try:
            with self.__get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT m.precio
                    FROM producto p
                    JOIN modelo m ON p.id_modelo = m.id_modelo
                    WHERE p.id_etiqueta = ?
                """, (id_producto,))
                row = cursor.fetchone()
                if row:
                    return True, row['precio']
                else:
                    return False, None
        except sqlite3.Error as e:
            print(f"Hubo un problema al obtener el precio del producto '{id_producto}'. Motivo: {e}")
            return False, None


