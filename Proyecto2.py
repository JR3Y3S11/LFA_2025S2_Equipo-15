OPERACIONES = {"SUMA", "RESTA", "MULTIPLICACION", "DIVISION", "POTENCIA", "RAIZ", "INVERSO", "MOD"}

archivin_entrada = "entrada.txt"
archivito_resultados = "RESULTADOS.html"
archivito_errores = "ERRORES_Equipo.html"

estados_aceptacion_num = {"q2", "q3", "q4", "q5", "q6", "q7"}
trans_num = {
    "q0": {"S": "q1", "D": "q2", "P": "q3"},
    "q1": {"S": None,  "D": "q2", "P": "q3"},
    "q2": {"S": None,  "D": "q4", "P": "q5"},
    "q3": {"S": None,  "D": "q6", "P": None},
    "q4": {"S": None,  "D": "q4", "P": "q5"},
    "q5": {"S": None,  "D": "q7", "P": None},
    "q6": {"S": None,  "D": "q6", "P": None},
    "q7": {"S": None,  "D": "q7", "P": None},
}

def es_letra(ch):
    return ("a" <= ch <= "z") or ("A" <= ch <= "Z") or ch == "_"

def es_digito(ch):
    return "0" <= ch <= "9"

def clase_numero(ch):
    if ch in "+-":
        return "S"
    if es_digito(ch):
        return "D"
    if ch == ".":
        return "P"
    return None

class DatoToken:
    def __init__(self, tipo, lexema, fila, col):
        self.tipo = tipo
        self.lexema = lexema
        self.fila = fila
        self.col = col

class DatoError:
    def __init__(self, numero, lexema, tipo, fila, col):
        self.numero = numero
        self.lexema = lexema
        self.tipo = tipo
        self.fila = fila
        self.col = col

class Escaner:
    def __init__(self, texto):
        self.texto = texto
        self.i = 0
        self.fila = 1
        self.col = 1
        self.lista_tokens = []
        self.lista_errores = []
        self.cont_error = 0

    def ver(self):
        if self.i >= len(self.texto):
            return ""
        return self.texto[self.i]

    def avanzar(self):
        ch = self.ver()
        if ch == "":
            return ""
        self.i += 1
        if ch == "\n":
            self.fila += 1
            self.col = 1
        else:
            self.col += 1
        return ch

    def empieza_con_ci(self, s):
        seg = self.texto[self.i:self.i+len(s)]
        return seg.lower() == s.lower()

    def tomar_literal_ci(self, s):
        if not self.empieza_con_ci(s):
            return None
        recogido = []
        for _ in range(len(s)):
            recogido.append(self.avanzar())
        return "".join(recogido)

    def soltar_token(self, tipo, lexema, fila, col):
        self.lista_tokens.append(DatoToken(tipo, lexema, fila, col))

    def soltar_error(self, lexema, fila, col, tipo="DESCONOCIDO"):
        self.cont_error += 1
        self.lista_errores.append(DatoError(self.cont_error, lexema, tipo, fila, col))

    def probar_tag_operacion_abre(self):
        pos_i, pos_f, pos_c = self.i, self.fila, self.col
        if self.ver() != "<":
            return None
        if self.tomar_literal_ci("<Operacion=") is None:
            self.i, self.fila, self.col = pos_i, pos_f, pos_c
            return None
        nombre = []
        while True:
            ch = self.ver()
            if ch == "" or ch == ">" or ch == "<" or ch == "\n":
                break
            if not es_letra(ch):
                break
            nombre.append(self.avanzar())
        op = "".join(nombre).upper()
        if op not in OPERACIONES:
            self.i, self.fila, self.col = pos_i, pos_f, pos_c
            return None
        if self.ver() != ">":
            self.i, self.fila, self.col = pos_i, pos_f, pos_c
            return None
        self.avanzar()
        return DatoToken("TAG_OP_ABRE", f"<Operacion={op}>", pos_f, pos_c)

    def probar_tag_operacion_cierra(self):
        pos_i, pos_f, pos_c = self.i, self.fila, self.col
        if self.tomar_literal_ci("</Operacion>") is None:
            self.i, self.fila, self.col = pos_i, pos_f, pos_c
            return None
        return DatoToken("TAG_OP_CIERRA", "</Operacion>", pos_f, pos_c)

    def probar_tag_num_abre(self):
        pos_i, pos_f, pos_c = self.i, self.fila, self.col
        if self.tomar_literal_ci("<Numero>") is None:
            self.i, self.fila, self.col = pos_i, pos_f, pos_c
            return None
        return DatoToken("TAG_NUM_ABRE", "<Numero>", pos_f, pos_c)

    def probar_tag_num_cierra(self):
        pos_i, pos_f, pos_c = self.i, self.fila, self.col
        if self.tomar_literal_ci("</Numero>") is None:
            self.i, self.fila, self.col = pos_i, pos_f, pos_c
            return None
        return DatoToken("TAG_NUM_CIERRA", "</Numero>", pos_f, pos_c)

    def probar_operacion_nombre(self):
        if not es_letra(self.ver()):
            return None
        pos_i, pos_f, pos_c = self.i, self.fila, self.col
        nombre = []
        while es_letra(self.ver()):
            nombre.append(self.avanzar())
        op = "".join(nombre).upper()
        if op in OPERACIONES:
            return DatoToken("OPERACION_NOMBRE", op, pos_f, pos_c)
        self.i, self.fila, self.col = pos_i, pos_f, pos_c
        return None

    def probar_numero(self):
        pos_i, pos_f, pos_c = self.i, self.fila, self.col
        estado = "q0"
        ultimo_ok = -1
        j = self.i
        while j < len(self.texto):
            c = self.texto[j]
            cl = clase_numero(c)
            if cl is None:
                break
            nxt = trans_num[estado].get(cl, None)
            if nxt is None:
                break
            estado = nxt
            j += 1
            if estado in estados_aceptacion_num:
                ultimo_ok = j
        if ultimo_ok == -1:
            return None
        lex = self.texto[self.i:ultimo_ok]
        for _ in range(ultimo_ok - self.i):
            self.avanzar()
        return DatoToken("NUMERO", lex, pos_f, pos_c)

    def escanear(self):
        while self.i < len(self.texto):
            ch = self.ver()
            if ch in " \t\r\n":
                self.avanzar()
                continue
            t = (self.probar_tag_operacion_cierra()
                 or self.probar_tag_operacion_abre()
                 or self.probar_tag_num_cierra()
                 or self.probar_tag_num_abre())
            if t is not None:
                self.soltar_token(t.tipo, t.lexema, t.fila, t.col)
                continue
            t = self.probar_numero()
            if t is not None:
                self.soltar_token(t.tipo, t.lexema, t.fila, t.col)
                continue
            t = self.probar_operacion_nombre()
            if t is not None:
                self.soltar_token(t.tipo, t.lexema, t.fila, t.col)
                continue
            f0, c0 = self.fila, self.col
            if ch == "=":
                self.avanzar()
                self.soltar_token("IGUAL", "=", f0, c0)
                continue
            if ch == "<":
                self.avanzar()
                self.soltar_token("MENOR", "<", f0, c0)
                continue
            if ch == ">":
                self.avanzar()
                self.soltar_token("MAYOR", ">", f0, c0)
                continue
            if ch == "/":
                self.avanzar()
                self.soltar_token("SLASH", "/", f0, c0)
                continue
            self.soltar_error(self.avanzar(), f0, c0, "DESCONOCIDO")

    def html_inicio(self, titulo):
        return "<!DOCTYPE html>\n<html><head><meta charset=\"utf-8\"><title>" + titulo + "</title>\n<style>\n" + \
               "table{border-collapse:collapse;font-family:Arial,Helvetica,sans-serif;font-size:14px}" + \
               "th,td{border:1px solid #999;padding:6px 10px}" + \
               "th{background:#eee}\n</style>\n</head><body>\n<h2>" + titulo + "</h2>\n"

    def html_fin(self):
        return "</body></html>"

    def guardar_tokens_html(self, ruta):
        partes = [self.html_inicio("RESULTADOS - TOKENS")]
        partes.append("<table>")
        partes.append("<tr><th>#</th><th>Tipo</th><th>Lexema</th><th>Fila</th><th>Columna</th></tr>")
        for k, t in enumerate(self.lista_tokens, 1):
            partes.append(f"<tr><td>{k}</td><td>{t.tipo}</td><td>{t.lexema}</td><td>{t.fila}</td><td>{t.col}</td></tr>")
        partes.append("</table>")
        partes.append(self.html_fin())
        with open(ruta, "w", encoding="utf-8") as f:
            f.write("\n".join(partes))

    def guardar_errores_html(self, ruta):
        partes = [self.html_inicio("ERRORES LEXICOS")]
        partes.append("<table>")
        partes.append("<tr><th>#</th><th>Lexema</th><th>Tipo</th><th>Fila</th><th>Columna</th></tr>")
        for e in self.lista_errores:
            partes.append(f"<tr><td>{e.numero}</td><td>{e.lexema}</td><td>{e.tipo}</td><td>{e.fila}</td><td>{e.col}</td></tr>")
        partes.append("</table>")
        partes.append(self.html_fin())
        with open(ruta, "w", encoding="utf-8") as f:
            f.write("\n".join(partes))

def main():
    try:
        with open(archivin_entrada, "r", encoding="utf-8") as f:
            texto = f.read()
    except FileNotFoundError:
        print("No se encontro 'entrada.txt'. Crea ese archivo con tu prueba.")
        return
    esc = Escaner(texto)
    esc.escanear()
    esc.guardar_tokens_html(archivito_resultados)
    esc.guardar_errores_html(archivito_errores)
    print("Listo. Revisa RESULTADOS.html y ERRORES_Equipo.html.")

if __name__ == "__main__":
    main()
