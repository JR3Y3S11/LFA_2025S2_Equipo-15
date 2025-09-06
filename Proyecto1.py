from datetime import datetime, date

class usuario:
    def __init__(self, id_persona, nombre):
        self.id_persona = id_persona
        self.nombre = nombre

class librito:
    def __init__(self, id_libro, titulo):
        self.id_libro = id_libro
        self.titulo = titulo

class prestamo_libros:
    def __init__(self, id_persona, nombre, id_libro, titulo, fecha_prestamo, fecha_devolucion):
        self.id_persona = id_persona
        self.nombre = nombre
        self.id_libro = id_libro
        self.titulo = titulo
        self.fecha_prestamo = fecha_prestamo
        self.fecha_devolucion = fecha_devolucion

class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None

class ListaEnlazada:
    def __init__(self):
        self.cabeza = None

    def agregar(self, dato):
        nuevo = Nodo(dato)
        if not self.cabeza:
            self.cabeza = nuevo
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo

    def __iter__(self):
        actual = self.cabeza
        while actual:
            yield actual.dato
            actual = actual.siguiente

    def __len__(self):
        contador = 0
        actual = self.cabeza
        while actual:
            contador += 1
            actual = actual.siguiente
        return contador

usuarios = ListaEnlazada()
libros = ListaEnlazada()
prestamos = ListaEnlazada()


def busqueda_usuarios(id_persona):
    for i in usuarios:
        if i.id_persona == id_persona:
            return i
    return None


def busqueda_libritos(id_libro):
    for j in libros:
        if j.id_libro == id_libro:
            return j
    return None


def carga_de_usuarios_lfa(ruta):
    cargas = 0
    with open(ruta, "r") as archivonombres_lfa:
        for num_linea, linea in enumerate(archivonombres_lfa, start= 1):
            linea = linea.strip()
            if linea == "" or linea.startswith("#"):
                continue

            div_texto = linea.split("|")
            if len(div_texto) != 2:
                print(f"en usuarios.lfa; línea {num_linea}: no tiene los 2 campos que se exigen")
                continue

            invalido = False
            for pos, char in enumerate(linea):
                if not (char.isalnum() or char in "| _-áéíóúÁÉÍÓÚ"):
                    print(f"Carácter inválido '{char}' en línea {num_linea}, posición {pos+1}")
                    invalido = True
                    break
            if invalido:
                continue

            id_usuario = div_texto[0].strip()
            nombre = div_texto[1].strip()
            usuarios.agregar(usuario(id_usuario, nombre))
            cargas += 1

    print(f"Los siguientes usuarios se cargaron correctamente: {cargas}")


def carga_de_libros_lfa(ruta):
    cargas = 0
    with open(ruta, "r") as archivolibros_lfa:
        for num_linea, linea in enumerate(archivolibros_lfa, start= 1):
            linea = linea.strip()
            if linea == "" or linea.startswith("#"):
                continue

            div_texto = linea.split("|")
            if len(div_texto) != 2:
                print(f"en libros.lfa; línea {num_linea}: no tiene los 2 campos que se exigen")
                continue

            invalido = False
            for pos, char in enumerate(linea):
                if not (char.isalnum() or char in "| _-áéíóúÁÉÍÓÚ"):
                    print(f"Carácter inválido '{char}' en línea {num_linea}, posición {pos+1}")
                    invalido = True
                    break
            if invalido:
                continue

            id_libro = div_texto[0].strip()
            titulo = div_texto[1].strip()
            libros.agregar(librito(id_libro, titulo))
            cargas += 1

    print(f"Los siguientes libros se cargaron correctamente: {cargas}")


def carga_de_prestamos_lfa(ruta):
    cargas = 0
    with open(ruta, "r") as archivoprestamos_lfa:
        for num_linea, linea in enumerate(archivoprestamos_lfa, start= 1):
            linea = linea.strip()
            if linea == "" or linea.startswith("#"):
                continue

            div_texto = linea.split("|")
            if len(div_texto) != 6:
                print(f"en prestamos.lfa; línea {num_linea}: no tiene los 6 campos que se exigen")
                continue

            invalido = False
            for pos, char in enumerate(linea):
                if not (char.isalnum() or char in "| _-áéíóúÁÉÍÓÚ:"):
                    print(f"Carácter inválido '{char}' en línea {num_linea}, posición {pos+1}")
                    invalido = True
                    break
            if invalido:
                continue

            id_persona = div_texto[0].strip()
            nombre = div_texto[1].strip()
            id_libro = div_texto[2].strip()
            titulo = div_texto[3].strip()
            fecha_prestamo = div_texto[4].strip()
            fecha_devolucion = div_texto[5].strip()

            if busqueda_usuarios(id_persona) is None:
                print(f"en prestamos.lfa; línea {num_linea}: el id de persona o la persona no existe")
                continue

            if busqueda_libritos(id_libro) is None:
                print(f"en prestamos.lfa; línea {num_linea}: el id de libro o el libro no existe")
                continue

            prestamos.agregar(prestamo_libros(id_persona, nombre, id_libro, titulo, fecha_prestamo, fecha_devolucion))
            cargas += 1

    print(f"Los siguientes prestamos se cargaron correctamente: {cargas}")


def fecha_actual(texto):
    texto = texto.strip()
    if texto == "":
        return None
    try:
        return datetime.strptime(texto, "%Y-%m-%d").date()
    except:
        return None


def mostrar_historial():
    print("-----Este es el historial de prestamos------")
    if len(prestamos) == 0:
        print("No hay prestamos por aca...")
        return

    for i in prestamos:
        print(i.id_persona, "|", i.nombre, "|", i.id_libro, "|", i.titulo, "|", i.fecha_prestamo, "|", i.fecha_devolucion)


def lista_de_usuarios():
    print("------Estos son los usuarios------")
    if len(usuarios) == 0:
        print("No hay usuarios")
        return

    repetidos = set()
    for i in usuarios:
        if i.id_persona not in repetidos:
            print(i.id_persona, "|", i.nombre)
            repetidos.add(i.id_persona)


def lista_de_libros_prestados():
    print("------Estos son los libros prestados------")
    if len(prestamos) == 0:
        print("No hay prestamos")
        return

    repetidos = set()
    for i in prestamos:
        if i.id_libro not in repetidos:
            print(i.id_libro, "|", i.titulo)
            repetidos.add(i.id_libro)


def estadisticas_de_prestamos():
    print("------Estadisticas de Prestamos-----")
    total_prestamos = len(prestamos)
    conteo_libros = {}
    conteo_usuarios = {}

    for i in prestamos:
        conteo_libros[i.id_libro] = conteo_libros.get(i.id_libro, 0) + 1
        conteo_usuarios[i.id_persona] = conteo_usuarios.get(i.id_persona, 0) + 1

    libro_mas_prestado = None
    titulo_libro_mas_prestado = ""
    if len(conteo_libros) > 0:
        libro_mas_prestado = max(conteo_libros, key=lambda k: conteo_libros[k])
        for i in prestamos:
            if i.id_libro == libro_mas_prestado:
                titulo_libro_mas_prestado = i.titulo
                break

    usuario_mas_activo = None
    nombre_usuario_mas_activo = ""
    if len(conteo_usuarios) > 0:
        usuario_mas_activo = max(conteo_usuarios, key=lambda k: conteo_usuarios[k])
        for i in usuarios:
            if i.id_persona == usuario_mas_activo:
                nombre_usuario_mas_activo = i.nombre
                break

    print("Este es el total de prestamos: ", total_prestamos)
    print("Este es el libro mas prestado: ", libro_mas_prestado, "Con el titulo de: ", titulo_libro_mas_prestado)
    print("Este es el usuario mas activo: ", usuario_mas_activo, "-", nombre_usuario_mas_activo)
    print("Este es el total de usuarios: ", len(conteo_usuarios))


def lista_de_prestamos_vencidos():
    print("-------Prestamos Vencidos por fecha ya pasada del límite-------")
    ahorita = date.today()
    existen_prestamos = False

    for i in prestamos:
        limite_fecha = fecha_actual(i.fecha_devolucion)
        if limite_fecha is not None and limite_fecha < ahorita:
            print(i.id_persona, "|", i.nombre, "|", i.id_libro, "|", i.titulo, "|", i.fecha_prestamo, "|", i.fecha_devolucion)
            existen_prestamos = True

    if not existen_prestamos:
        print("No hay préstamos vencidos.")


def exportar_a_html():
    html = """
<html>
<head>
    <title>Biblioteca Digital</title>
</head>
<body>
    <h1>Biblioteca Digital</h1>
    <h2>Usuarios</h2>
    <table border='1'>
        <tr><th>ID</th><th>Nombre</th></tr>"""
    repetidos = set()
    for u in usuarios:
        if u.id_persona not in repetidos:
            html += f"<tr><td>{u.id_persona}</td><td>{u.nombre}</td></tr>"
            repetidos.add(u.id_persona)
    html += "</table>"
    html += "<h2>Libros</h2><table border='1'><tr><th>ID</th><th>Título</th></tr>"
    repetidos = set()
    for l in libros:
        if l.id_libro not in repetidos:
            html += f"<tr><td>{l.id_libro}</td><td>{l.titulo}</td></tr>"
            repetidos.add(l.id_libro)
    html += "</table>"
    html += "<h2>Préstamos</h2><table border='1'><tr><th>ID Usuario</th><th>Nombre</th><th>ID Libro</th><th>Título</th><th>Fecha Préstamo</th><th>Fecha Devolución</th></tr>"
    for p in prestamos:
        html += f"<tr><td>{p.id_persona}</td><td>{p.nombre}</td><td>{p.id_libro}</td><td>{p.titulo}</td><td>{p.fecha_prestamo}</td><td>{p.fecha_devolucion}</td></tr>"
    html += "</table>"
    total_prestamos = len(prestamos)
    conteo_libros = {}
    conteo_usuarios = {}
    for p in prestamos:
        conteo_libros[p.id_libro] = conteo_libros.get(p.id_libro, 0) + 1
        conteo_usuarios[p.id_persona] = conteo_usuarios.get(p.id_persona, 0) + 1
    libro_mas_prestado = None
    titulo_libro_mas_prestado = ""
    if len(conteo_libros) > 0:
        libro_mas_prestado = max(conteo_libros, key=lambda k: conteo_libros[k])
        for p in prestamos:
            if p.id_libro == libro_mas_prestado:
                titulo_libro_mas_prestado = p.titulo
                break
    usuario_mas_activo = None
    nombre_usuario_mas_activo = ""
    if len(conteo_usuarios) > 0:
        usuario_mas_activo = max(conteo_usuarios, key=lambda k: conteo_usuarios[k])
        for u in usuarios:
            if u.id_persona == usuario_mas_activo:
                nombre_usuario_mas_activo = u.nombre
                break
    html += f"<h2>Estadísticas de Préstamos</h2>"
    html += f"<p>Total de préstamos: {total_prestamos}</p>"
    html += f"<p>Libro más prestado: {libro_mas_prestado} - {titulo_libro_mas_prestado}</p>"
    html += f"<p>Usuario más activo: {usuario_mas_activo} - {nombre_usuario_mas_activo}</p>"
    html += f"<p>Total de usuarios únicos: {len(conteo_usuarios)}</p>"
    html += "<h2>Préstamos Vencidos</h2><table border='1'><tr><th>ID Usuario</th><th>Nombre</th><th>ID Libro</th><th>Título</th><th>Fecha Préstamo</th><th>Fecha Devolución</th></tr>"
    ahorita = date.today()
    vencidos = 0
    for p in prestamos:
        limite_fecha = fecha_actual(p.fecha_devolucion)
        if limite_fecha is not None and limite_fecha < ahorita:
            html += f"<tr><td>{p.id_persona}</td><td>{p.nombre}</td><td>{p.id_libro}</td><td>{p.titulo}</td><td>{p.fecha_prestamo}</td><td>{p.fecha_devolucion}</td></tr>"
            vencidos += 1
    if vencidos == 0:
        html += "<tr><td colspan='6'>No hay préstamos vencidos.</td></tr>"
    html += "</table>"
    html += "</body></html>"
    with open("biblioteca_export.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Datos exportados a biblioteca_export.html")


def menu():
    while True:
        print("--------Menu Interactivo------")
        print("1. Cargar Usuarios")
        print("2. Cargar Libros")
        print("3. Cargar Prestamos")
        print("4. Mostrar historial de prestamos")
        print("5. Mostrar usuarios unicos")
        print("6. Mostrar libros prestados (sin duplicados)")
        print("7. Mostrar estadisticas de prestamos")
        print("8. Mostrar prestamos vencidos")
        print("9. Exportar todos los datos a HTML")
        print("10. Salir")
        opcion = input("Elige una opcion: ")
        if opcion == "1":
            ruta = input("Ingresa la ruta del archivo de usuarios: ")
            carga_de_usuarios_lfa(ruta)

        elif opcion == "2":
            ruta = input("Ingresa la ruta del archivo de libros: ")
            carga_de_libros_lfa(ruta)

        elif opcion == "3":
            ruta = input("Ingresa la ruta del archivo de prestamos: ")
            carga_de_prestamos_lfa(ruta)

        elif opcion == "4":
            mostrar_historial()

        elif opcion == "5":
            lista_de_usuarios()

        elif opcion == "6":
            lista_de_libros_prestados()

        elif opcion == "7":
            estadisticas_de_prestamos()

        elif opcion == "8":
            lista_de_prestamos_vencidos()

        elif opcion == "9":
            exportar_a_html()

        elif opcion == "10":
            print("Saliendo del sistema...")
            break

        else:
            print("Esta opcion no es correcta, vuelve a intentarlo...")

if __name__ == "__main__":
    menu()
