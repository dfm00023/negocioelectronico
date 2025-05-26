import sqlite3
from typing import Optional

class DataBase:
    def __init__(self, database_file: str):
        self.database_file = database_file
        self.__init_db()

    def __get_db_connection(self):
        """Establece una conexión a la base de datos SQLite."""
        conn = sqlite3.connect(self.database_file)
        conn.row_factory = sqlite3.Row # Para acceder a los resultados como diccionarios
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
                            id_estado TEXT PRIMARY KEY,
                            nombre_estado TEXT NOT NULL
                        )
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
                            id_modelo TEXT PRIMARY KEY,
                            nombre_modelo TEXT NOT NULL,
                            precio REAL NOT NULL,
                            url_imagen TEXT,
                            estante INTEGER,
                            pasillo INTEGER
                        )
                    """)
                except sqlite3.OperationalError:
                    pass

                try:
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS producto (
                            id_etiqueta TEXT PRIMARY KEY,
                            id_modelo TEXT NOT NULL,
                            id_estado TEXT NOT NULL,
                            fecha_venta DATE,
                            FOREIGN KEY (id_modelo) REFERENCES modelo(id_modelo),
                            FOREIGN KEY (id_estado) REFERENCES estado(id_estado)
                        )
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

    def add_modelo(self, id_modelo: str, nombre_modelo: str, precio: float, url_imagen: Optional[str] = "NULL", estante: Optional[int] = "NULL",
                   pasillo: Optional[int] = "NULL") -> tuple[bool, Optional[list[dict]]]:
        """
        Agrega un nuevo modelo a la base de datos.

        Args:
            id_modelo (str): El ID único del modelo. Debe ser una cadena.
            nombre_modelo (str): El nombre del modelo. Debe ser una cadena.
            precio (float): El precio del modelo. Debe ser un número flotante.
            url_imagen (Optional[str]): Enlace a la imagen. Opcional, puede ser None.
            estante (Optional[int]): El número de estante donde se ubica el modelo. Opcional, puede ser None.
            pasillo (Optional[int]): El número de pasillo donde se ubica el modelo. Opcional, puede ser None.

        Returns:
            tuple[bool, Optional[list[dict]]]: Una tupla que indica si la operación fue exitosa (True/False) y, en caso de éxito, una cadena JSON con los detalles del modelo insertado. Si falla, devuelve None.
        """
        try:
            with self.__get_db_connection() as conn:
                cursor = conn.cursor()
                query = "INSERT INTO modelo (id_modelo, nombre_modelo, precio, url_imagen, estante, pasillo) VALUES (?, ?, ?, ?, ?, ?)"
                values = (id_modelo, nombre_modelo, precio, url_imagen, estante, pasillo)
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

    def edit_modelo(self, id_modelo: str, nombre_modelo: str = None, precio: Optional[float] = None, url_imagen: Optional[str] = None, estante: Optional[int] = None,
                   pasillo: Optional[int] = None) -> tuple[bool, Optional[list[dict]]]:
        """
        Edita un modelo de la base de datos.

        Args:
            id_modelo (str): El ID único del modelo. Debe ser una cadena.
            nombre_modelo (str): El nombre del modelo. Debe ser una cadena.
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
                    ['nombre_modelo', 'precio', 'url_imagen', 'estante', 'pasillo'], # Nombre columna
                    [nombre_modelo, precio, url_imagen, estante, pasillo] # Valor
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