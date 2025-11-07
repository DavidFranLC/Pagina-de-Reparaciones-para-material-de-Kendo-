from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
from database.db_connection import get_db_connection
import sys
import traceback


# Crear la app Flask
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "clave_secreta_super_segura")

# ----------------------------------------
# 🔹 Registrar actividad
# ----------------------------------------
def registrar_actividad(usuario_id, accion):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO actividad (usuario_id, accion, fecha) VALUES (%s, %s, %s)",
            (usuario_id, accion, datetime.now())
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"⚠️ Error al registrar actividad: {e}")


# ----------------------------------------
# 🔹 Página principal (login)
# ----------------------------------------
@app.route('/')
def index():
    return render_template('login.html')


# ----------------------------------------
# 🔹 Registro de usuarios
# ----------------------------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form['nombre']
        edad = request.form['edad']
        dojo = request.form['dojo']
        sensei = request.form['sensei']
        rango = request.form['rango']
        correo = request.form['correo']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO usuarios (nombre, edad, dojo, sensei, rango, correo, password)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
        """, (nombre, edad, dojo, sensei, rango, correo, password))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    
    return render_template('register.html')


# ----------------------------------------
# 🔹 Inicio de sesión
# ----------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form.get('correo')
        password = request.form.get('password')

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE correo=%s", (correo,))
        user = cursor.fetchone()
        conn.close()

        if user:
            if user['password'] == password:
                session['usuario'] = user
                registrar_actividad(user['id_usuario'], 'Inicio sesión')
                if user['rol'] == 'admin':
                    return redirect(url_for('admin_dashboard'))
                else:
                    return redirect(url_for('cliente_dashboard'))
            else:
                return render_template('login.html', error="Correo o contraseña incorrectos")
        else:
            return render_template('login.html', error="Correo o contraseña incorrectos")

    return render_template('login.html')


# ----------------------------------------
# 🔹 Dashboard del cliente
# ----------------------------------------
@app.route('/cliente_dashboard')
def cliente_dashboard():
    if 'usuario' not in session or session['usuario']['rol'] != 'cliente':
        return redirect(url_for('index'))

    usuario_id = session['usuario']['id_usuario']
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT id_solicitud, articulo, descripcion, estado, fecha
        FROM solicitudes
        WHERE id_usuario = %s
        ORDER BY fecha DESC
    """, (usuario_id,))
    solicitudes = cursor.fetchall()
    conn.close()

    registrar_actividad(usuario_id, "Ingresó al panel de cliente")

    return render_template('cliente_dashboard.html',
                           usuario=session['usuario'],
                           solicitudes=solicitudes)


# ----------------------------------------
# 🔹 Dashboard del administrador 
# ----------------------------------------
@app.route('/admin_dashboard')
def admin_dashboard():
    if 'usuario' not in session or session['usuario']['rol'] != 'admin':
        return redirect(url_for('index'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT s.id_solicitud, s.articulo, s.descripcion, s.estado, s.fecha, u.nombre AS cliente
        FROM solicitudes s
        JOIN usuarios u ON s.id_usuario = u.id_usuario
        ORDER BY s.fecha DESC
    """)
    solicitudes = cursor.fetchall()

    cursor.execute("""
        SELECT a.id, a.accion, a.fecha, u.nombre AS usuario
        FROM actividad a
        JOIN usuarios u ON a.usuario_id = u.id_usuario
        ORDER BY a.fecha DESC
    """)
    actividades = cursor.fetchall()
    conn.close()

    registrar_actividad(session['usuario']['id_usuario'], "Ingresó al panel de administrador")

    return render_template('admin_dashboard.html',
                           usuario=session['usuario'],
                           solicitudes=solicitudes,
                           actividades=actividades)


# ----------------------------------------
# 🔹 Actualizar estado de solicitudes
# ----------------------------------------
@app.route('/actualizar_estado/<int:id_solicitud>', methods=['POST'])
def actualizar_estado(id_solicitud):
    if 'usuario' not in session or session['usuario']['rol'] != 'admin':
        return redirect(url_for('index'))

    nuevo_estado = request.form['estado']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE solicitudes SET estado = %s WHERE id_solicitud = %s",
                   (nuevo_estado, id_solicitud))
    conn.commit()
    conn.close()

    registrar_actividad(session['usuario']['id_usuario'],
                        f"Actualizó estado de solicitud #{id_solicitud} a '{nuevo_estado}'")

    return redirect(url_for('admin_dashboard'))


# ----------------------------------------
# 🔹 Enviar solicitud de reparación (cliente)
# ----------------------------------------
@app.route('/enviar_solicitud', methods=['POST'])
def enviar_solicitud():
    if 'usuario' not in session or session['usuario']['rol'] != 'cliente':
        return redirect(url_for('index'))

    articulo = request.form['articulo']
    descripcion = request.form['descripcion']
    usuario_id = session['usuario']['id_usuario']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO solicitudes (id_usuario, articulo, descripcion)
        VALUES (%s, %s, %s)
    """, (usuario_id, articulo, descripcion))
    conn.commit()
    conn.close()

    registrar_actividad(usuario_id, f"Envió solicitud de reparación del artículo: {articulo}")

    return redirect(url_for('cliente_dashboard'))


# ----------------------------------------
# 🔹 Cerrar sesión
# ----------------------------------------
@app.route('/logout')
def logout():
    if 'usuario' in session:
        registrar_actividad(session['usuario']['id_usuario'], 'Cerró sesión')
        session.clear()
    return redirect(url_for('index'))


# ----------------------------------------
# 🔹 Configuración para Vercel
# ----------------------------------------
def handler(event, context):
    """Compatibilidad con Vercel"""
    return app(event, context)


# ----------------------------------------
# 🔹 Ejecución local
# ----------------------------------------
    
if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
    except Exception:
        traceback.print_exc(file=sys.stdout)

