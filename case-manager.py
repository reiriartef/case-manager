import sqlite3
import os
from fpdf import FPDF
import datetime

# Conectar a la base de datos
connection = sqlite3.connect("casos-oati.db")

# Crear el cursor
cursor = connection.cursor()

# Activar claves foráneas en SQLite
cursor.execute("PRAGMA foreign_keys = ON;")

# Crear tabla 'casos' con claves foráneas
cursor.execute("""
CREATE TABLE IF NOT EXISTS casos (
  id_caso integer PRIMARY KEY AUTOINCREMENT,
  id_dependencia int(25),
  id_analista int(25),
  descripcion varchar(50),
  id_estatus int(24),
  created_at datetime,
  finished_at datetime,
  FOREIGN KEY (id_dependencia) REFERENCES dependencias (id_dependencia),
  FOREIGN KEY (id_analista) REFERENCES analista (id_analista),
  FOREIGN KEY (id_estatus) REFERENCES estatus (id_estatus)
);
""")
connection.commit()

# Crear tabla 'dependencias'
cursor.execute("""
CREATE TABLE IF NOT EXISTS dependencias (
  id_dependencia integer PRIMARY KEY AUTOINCREMENT,
  nombre varchar(100)
);
""")
connection.commit()

# Crear tabla 'analista' con claves foráneas
cursor.execute("""
CREATE TABLE IF NOT EXISTS analista (
  id_analista integer PRIMARY KEY AUTOINCREMENT,
  nombre varchar(50),
  id_especialidad int(25),
  id_disponibilidad int(25),
  FOREIGN KEY (id_especialidad) REFERENCES especialidad (id_especialidad),
  FOREIGN KEY (id_disponibilidad) REFERENCES disponibilidad (id_disponibilidad)
);
""")
connection.commit()

# Crear tabla 'estatus'
cursor.execute("""
CREATE TABLE IF NOT EXISTS estatus (
  id_estatus integer PRIMARY KEY AUTOINCREMENT,
  nombre varchar(20)
);
""")
connection.commit()

# Crear tabla 'especialidad'
cursor.execute("""
CREATE TABLE IF NOT EXISTS especialidad (
  id_especialidad integer PRIMARY KEY AUTOINCREMENT,
  descripcion varchar(50)
);
""")
connection.commit()

# Crear tabla 'disponibilidad'
cursor.execute("""
CREATE TABLE IF NOT EXISTS disponibilidad (
  id_disponibilidad integer PRIMARY KEY AUTOINCREMENT,
  descripcion varchar(50)
);
""")
connection.commit()


# Insertar disponibilidad
""" 
cursor.execute("INSERT INTO disponibilidad VALUES (null, 'No Disponible')")
connection.commit()

cursor.execute("SELECT * FROM disponibilidad")
disponibilidad = cursor.fetchall()

for disponible in disponibilidad:
    print(disponible) """

# Insertar especialidad

""" cursor.execute("INSERT INTO especialidad VALUES (null, 'Soporte Tecnico')")
connection.commit()

cursor.execute("SELECT * FROM especialidad")
especialidades = cursor.fetchall()

for especialidad in especialidades:
    print(especialidad) """

# Insertar estatus

""" cursor.execute("INSERT INTO estatus VALUES (null, 'Resuelto')")
connection.commit()

cursor.execute("SELECT * FROM estatus")
especialidades = cursor.fetchall()

for especialidad in especialidades:
    print(especialidad) """


# Insertar analista
""" cursor.execute("INSERT INTO analista VALUES (null, 'Jose Gonzalez', 4, 1)")
connection.commit()

cursor.execute("SELECT * FROM analista")
especialidades = cursor.fetchall()

for especialidad in especialidades:
    print(especialidad) """

# Insert dependencias

""" numeros = {
    "1": "Primero de",
    "2": "Segundo de",
    "3": "Tercero de",
    "4": "Cuarto de",
    "5": "Quinto de",
    "6": "Sexto de",
    "7": "Septimo de",
    "8": "Octavo de",
    "9": "Noveno de",
    "10": "Decimo de",
    "11": "Undecimo de",
    "12": "Duodecimo de",
    "13": "Decimo Tercero de",
    "14": "Decimo Cuarto de",
    "15": "Decimo Quinto de",
} """

# for x in range(1, 2):
""" cursor.execute(
    "INSERT INTO dependencias VALUES (null, 'Coordinacion Judicial Violencia contra la Mujer')"
)
connection.commit()

cursor.execute("SELECT * FROM dependencias")
especialidades = cursor.fetchall()

for especialidad in especialidades:
    print(especialidad) """

# Insertar casos

""" cursor.execute(
    "INSERT INTO casos VALUES (null, 3, 1, 'Prueba Insert DB casos', 1, CURRENT_TIMESTAMP, NULL)"
)

connection.commit()

cursor.execute("SELECT * FROM casos")
casos = cursor.fetchall()

for caso in casos:
    print(caso) """


def casos_finalizados():
    cursor.execute("""SELECT 
    casos.id_caso, 
    dependencias.nombre AS dependencia, 
    analista.nombre AS analista, 
    casos.descripcion, 
    estatus.nombre AS estatus, 
    casos.created_at, 
    casos.finished_at
    FROM 
    casos
    INNER JOIN 
    dependencias ON casos.id_dependencia = dependencias.id_dependencia
    INNER JOIN 
    analista ON casos.id_analista = analista.id_analista
    INNER JOIN 
    estatus ON casos.id_estatus = estatus.id_estatus
    WHERE 
    casos.id_estatus = 2;
""")
    connection.commit()
    casos_finalizados = cursor.fetchall()
    return casos_finalizados


def casos_en_proceso():
    cursor.execute("""SELECT 
    casos.id_caso, 
    dependencias.nombre AS dependencia, 
    analista.nombre AS analista, 
    casos.descripcion, 
    estatus.nombre AS estatus, 
    casos.created_at, 
    casos.finished_at
    FROM 
    casos
    INNER JOIN 
    dependencias ON casos.id_dependencia = dependencias.id_dependencia
    INNER JOIN 
    analista ON casos.id_analista = analista.id_analista
    INNER JOIN 
    estatus ON casos.id_estatus = estatus.id_estatus
    WHERE 
    casos.id_estatus = 1;
""")
    connection.commit()
    casos_en_proceso = cursor.fetchall()
    return casos_en_proceso


def comenzar_caso(
    id_dependencia,
    id_analista,
    descripcion,
):
    # Usar parámetros de consulta para evitar errores de sintaxis e inyecciones SQL
    cursor.execute(
        """INSERT INTO casos (id_caso, id_dependencia, id_analista, descripcion, id_estatus, created_at, finished_at)
        VALUES (null, ?, ?, ?, 1, CURRENT_TIMESTAMP, NULL)""",
        (id_dependencia, id_analista, descripcion),
    )
    connection.commit()

    # Obtener el ID del caso generado
    id_generado = cursor.lastrowid

    cursor.execute(
        f"UPDATE analista SET id_disponibilidad = 2 WHERE id_analista = {id_analista}"
    )
    connection.commit()

    # Devolver o mostrar el ID del caso
    print("------------------------------------------")
    print(f"El ID del caso generado es: {id_generado}")
    print("------------------------------------------")


def modificar_caso(id_caso, descripcion):
    cursor.execute(
        "UPDATE casos SET descripcion = ? WHERE id_caso = ?", (descripcion, id_caso)
    )
    connection.commit()


def finalizar_caso(id_caso, id_analista):
    cursor.execute(
        f"UPDATE casos SET id_estatus = 2, finished_at = CURRENT_TIMESTAMP WHERE id_caso= {id_caso}"
    )
    connection.commit()
    cursor.execute(
        f"UPDATE analista SET id_disponibilidad = 1 WHERE id_analista = {id_analista}"
    )
    connection.commit()
    print("-----------------------------")
    print("Caso finalizado correctamente")
    print("-----------------------------")


def analistas_disponibles():
    cursor.execute("""
    SELECT 
        analista.id_analista, 
        analista.nombre AS analista_nombre, 
        especialidad.descripcion AS especialidad_descripcion, 
        disponibilidad.descripcion AS disponibilidad_descripcion
    FROM 
        analista
    INNER JOIN 
        especialidad ON analista.id_especialidad = especialidad.id_especialidad
    INNER JOIN 
        disponibilidad ON analista.id_disponibilidad = disponibilidad.id_disponibilidad
    WHERE 
        analista.id_disponibilidad = 1
    """)

    connection.commit()
    analistas_disponibles = cursor.fetchall()
    return analistas_disponibles


def analistas_no_disponibles():
    cursor.execute("""
    SELECT 
        analista.id_analista, 
        analista.nombre AS analista_nombre, 
        especialidad.descripcion AS especialidad_descripcion, 
        disponibilidad.descripcion AS disponibilidad_descripcion
    FROM 
        analista
    INNER JOIN 
        especialidad ON analista.id_especialidad = especialidad.id_especialidad
    INNER JOIN 
        disponibilidad ON analista.id_disponibilidad = disponibilidad.id_disponibilidad
    WHERE 
        analista.id_disponibilidad = 2
    """)

    connection.commit()
    analistas_no_disponibles = cursor.fetchall()
    return analistas_no_disponibles


def ver_dependencias():
    cursor.execute("SELECT * FROM dependencias")
    connection.commit()
    dependencias = cursor.fetchall()
    return dependencias


def casos_hoy():
    cursor.execute("""
    SELECT 
        casos.id_caso,
        dependencias.nombre AS dependencia,
        analista.nombre AS analista,
        casos.descripcion,
        estatus.nombre AS estatus,
        casos.created_at,
        casos.finished_at
    FROM 
        casos
    INNER JOIN 
        dependencias ON casos.id_dependencia = dependencias.id_dependencia
    INNER JOIN 
        analista ON casos.id_analista = analista.id_analista
    INNER JOIN 
        estatus ON casos.id_estatus = estatus.id_estatus
    WHERE 
        DATE(casos.created_at) = DATE(CURRENT_DATE)
""")
    connection.commit()
    casos_hoy = cursor.fetchall()
    return casos_hoy


def generar_pdf(datos):
    pdf = FPDF(orientation="P", unit="mm", format="Letter")
    pdf.add_page()

    # Logo
    pdf.image(
        "./logo.png", 10, 8, 33
    )  # Cambia 'ruta_al_logo.png' por la ruta de tu logo

    # Membrete
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Oficina de Apoyo Técnico Informático Zulia", ln=True, align="C")

    # Título centrado
    pdf.set_font("Arial", "B", 16)
    pdf.ln(20)  # Espacio antes del título
    pdf.cell(
        0,
        10,
        f"Reporte de Casos del Día {datetime.datetime.today().strftime('%d/%m/%Y')}",
        ln=True,
        align="C",
    )

    # Espacio antes de la tabla
    pdf.ln(10)

    # Encabezados de la tabla
    pdf.set_font("Arial", "B", 12)
    pdf.cell(60, 10, "Dependencia", border=1, align="C")
    pdf.cell(60, 10, "Analista Asignado", border=1, align="C")
    pdf.cell(70, 10, "Descripción del Caso", border=1, ln=True, align="C")

    # Contenido de la tabla
    pdf.set_font("Arial", "", 8)
    for fila in datos:
        dependencia = fila[1]  # Nombre de la dependencia
        analista = fila[2]  # Nombre del analista
        descripcion = fila[3]  # Descripción del caso

        pdf.cell(60, 10, dependencia, border=1, align="C")
        pdf.cell(60, 10, analista, border=1, align="C")
        pdf.cell(70, 10, descripcion, border=1, ln=True, align="C")

    # Guardar el PDF
    pdf.output("reporte_casos.pdf")
    print("---------------------------------------------------")
    print("PDF con casos del día de hoy generado correctamente")
    print("---------------------------------------------------")


def menu():
    while True:
        print("Seleccione una opción:")
        print("1. Agregar caso")
        print("2. Modificar caso")
        print("3. Finalizar caso")
        print("4. Ver analistas disponibles")
        print("5. Ver casos en proceso")
        print("6. Ver casos finalizados")
        print("7. Imprimir casos finalizados del día")

        print("0. Salir")

        opcion = input("Ingrese el número de la opción: ")
        os.system("cls")
        match opcion:
            case "1":
                os.system("cls")
                print("--- Agregar un nuevo caso ---")
                dependencias = ver_dependencias()
                print("--- Dependencias ---")
                for dependencia in dependencias:
                    print(f"ID: {dependencia[0]} - Nombre: {dependencia[1]}")
                print("\n")
                depencencia_seleccionada = input(
                    "Ingrese el ID de la dependencia que está solicitando apoyo: "
                )
                analistas = analistas_disponibles()
                print("\n--- Analistas disponibles ---")
                for analista in analistas:
                    print(
                        f"ID: {analista[0]} - Nombre: {analista[1]} - Especialidad: {analista[2]}"
                    )
                print("\n")
                analista_seleccionado = input(
                    "Ingrese el ID del analista que será asignado para atender el caso: "
                )
                descripcion_caso = input(
                    "Ingrese una breve descripcion del caso que será atendido por el analista: "
                )
                comenzar_caso(
                    int(depencencia_seleccionada),
                    int(analista_seleccionado),
                    descripcion_caso,
                )
            case "2":
                casos = casos_en_proceso()
                print("\n--- Casos en proceso ---")

                for caso in casos:
                    fecha_hora_inicio_str = caso[5]

                    # Convertir el string a un objeto datetime
                    fecha_hora_inicio_obj = datetime.datetime.strptime(
                        fecha_hora_inicio_str, "%Y-%m-%d %H:%M:%S"
                    )

                    # Formatear la hora a "%H:%M"
                    hora_inicio_formateada = fecha_hora_inicio_obj.strftime("%H:%M")

                    print(
                        f"ID: {caso[0]} - Dependencia: {caso[1]} - Analista asignado: {caso[2]} - Descripcion: {caso[3]} - Hora de Inicio: {hora_inicio_formateada}"
                    )
                caso_seleccionado = input(
                    "Ingrese el ID del caso que desea modificar su descripcion: "
                )
                descripcion = input("Ingrese la nueva descripcion del caso: ")
                modificar_caso(caso_seleccionado, descripcion)
                print("----------------------------")
                print("Caso modificado con éxito")
                print("----------------------------")

            case "3":
                os.system("cls")
                print("--- Finalizar casos en proceso ---")
                casos = casos_en_proceso()
                print("--- Casos en proceso ---")
                for caso in casos:
                    fecha_hora_inicio_str = caso[5]

                    # Convertir el string a un objeto datetime
                    fecha_hora_inicio_obj = datetime.datetime.strptime(
                        fecha_hora_inicio_str, "%Y-%m-%d %H:%M:%S"
                    )

                    # Formatear la hora a "%H:%M"
                    hora_inicio_formateada = fecha_hora_inicio_obj.strftime("%H:%M")

                    print(
                        f"ID: {caso[0]} - Dependencia: {caso[1]} - Analista asignado: {caso[2]} - Descripcion: {caso[3]} - Hora de Inicio: {hora_inicio_formateada}"
                    )
                caso_seleccionado = input(
                    "Ingrese el ID del caso que desea finalizar: "
                )
                print("--- Analistas en casos ---")
                analistas = analistas_no_disponibles()
                for analista in analistas:
                    print(
                        f"ID: {analista[0]} - Nombre: {analista[1]} - Especialidad: {analista[2]}"
                    )
                print("\n")
                analista_seleccionado = input(
                    "Ingrese el ID del analista asignado al caso que será marcado como finalizado: "
                )
                finalizar_caso(int(caso_seleccionado), int(analista_seleccionado))
            case "4":
                os.system("cls")
                analistas = analistas_disponibles()
                print("\n--- Analistas disponibles ---")
                for analista in analistas:
                    print(
                        f"ID: {analista[0]} - Nombre: {analista[1]} - Especialidad: {analista[2]}"
                    )
                print("\n")

            case "5":
                os.system("cls")
                casos = casos_en_proceso()
                print("\n--- Casos en proceso ---")

                for caso in casos:
                    fecha_hora_inicio_str = caso[5]

                    # Convertir el string a un objeto datetime
                    fecha_hora_inicio_obj = datetime.datetime.strptime(
                        fecha_hora_inicio_str, "%Y-%m-%d %H:%M:%S"
                    )

                    # Formatear la hora a "%H:%M"
                    hora_inicio_formateada = fecha_hora_inicio_obj.strftime("%H:%M")

                    print(
                        f"ID: {caso[0]} - Dependencia: {caso[1]} - Analista asignado: {caso[2]} - Descripcion: {caso[3]} - Hora de Inicio: {hora_inicio_formateada}"
                    )

            case "6":
                os.system("cls")
                print("\n--- Casos Finalizados ---")
                casos = casos_finalizados()
                for caso in casos:
                    fecha_hora_inicio_str = caso[5]

                    # Convertir el string a un objeto datetime
                    fecha_hora_inicio_obj = datetime.datetime.strptime(
                        fecha_hora_inicio_str, "%Y-%m-%d %H:%M:%S"
                    )

                    # Formatear la hora a "%H:%M"
                    hora_inicio_formateada = fecha_hora_inicio_obj.strftime("%H:%M")

                    fecha_hora_finalizacion_str = caso[6]

                    # Convertir el string a un objeto datetime
                    fecha_hora_finalizacion_obj = datetime.datetime.strptime(
                        fecha_hora_finalizacion_str, "%Y-%m-%d %H:%M:%S"
                    )

                    # Formatear la hora a "%H:%M"
                    hora_finalizacion_formateada = fecha_hora_finalizacion_obj.strftime(
                        "%H:%M"
                    )

                    # Calcular la diferencia de tiempo (timedelta)
                    diferencia = fecha_hora_finalizacion_obj - fecha_hora_inicio_obj

                    # Convertir la diferencia en minutos
                    diferencia_en_minutos = diferencia.total_seconds() / 60

                    print(
                        f"ID: {caso[0]} - Dependencia: {caso[1]} - Analista asignado: {caso[2]} - Hora de Inicio: {hora_inicio_formateada} - Hora de Finalización: {hora_finalizacion_formateada} - Duración del Caso: {diferencia_en_minutos} minutos"
                    )
            case "7":
                os.system("cls")
                casos = casos_hoy()
                generar_pdf(casos)
            case "0":
                print("Saliendo del programa...")
                break
            case _:
                print("Opción no válida, por favor intente de nuevo.")


menu()

# Cerrar la conexión
connection.close()
