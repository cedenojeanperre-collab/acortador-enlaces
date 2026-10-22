import random
import string
from flask import Flask, request, jsonify, redirect, render_template
from database import conectar, crear_tabla
from urllib.parse import urlparse 

app = Flask(__name__)
crear_tabla()

def generar_codigo(longitud=6):
    caracteres = string.ascii_letters + string.digits
    return "".join(random.choices(caracteres, k=longitud))

class URLInvalida(Exception):
    pass

def validar_url(url):
    partes = urlparse(url)
    if partes.scheme not in ("http", "https") or not partes.netloc:
        raise URLInvalida("URL no válida. Debe empezar con http:// o https://")

@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/acortar", methods=["POST"])
def acortar():
    datos = request.get_json()
    url = datos.get("url") if datos else None

    if not url:
        return jsonify({"error": "Ups!. Parece que falta ingresar la URL 😿"}), 400

    codigo = generar_codigo()
    
    try:
        validar_url(url)
    except URLInvalida as e:
        return jsonify({"error": str(e)}), 400

    conn = conectar()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO links (codigo, url_original) VALUES (?, ?)",
        (codigo, url)
    )
    conn.commit()
    conn.close()

    return jsonify({
        "codigo": codigo,
        "enlace_corto": request.host_url + codigo
    }), 201

@app.route("/<codigo>")
def redirigir(codigo):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT url_original FROM links WHERE codigo = ?", (codigo,))
    fila = cur.fetchone()

    if fila is None:
        conn.close()
        return jsonify({"error": "Enlace no encontrado"}), 404

    cur.execute("UPDATE links SET clics = clics + 1 WHERE codigo = ?", (codigo,))
    conn.commit()
    conn.close()

    return redirect(fila["url_original"])

if __name__ == "__main__":
    app.run(debug=True)