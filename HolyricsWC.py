import tkinter as tk
import threading
from tkinter import scrolledtext, messagebox, Menu
from pystray import Icon, MenuItem as item
from PIL import Image, ImageDraw
from flask import Flask, render_template, request, jsonify, send_from_directory, session
import socket
import requests, os, json
import webbrowser

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        s.connect(('10.254.254.254', 1))
        ipLocal = s.getsockname()[0]
    except Exception:
        ipLocal = '127.0.0.1'  # Si no puede obtener la IP, usa localhost
    finally:
        s.close()
    return ipLocal


playing = None

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

app = Flask(__name__)

print(Colors.GREEN + "PARA LA GLORIA DE DIOS † ☝️" + Colors.END)
print()
print()
print(Colors.BLUE + "Iniciando el servidor..." + Colors.END)

app.secret_key = 'your_secret_key'

# Cargar la contraseña desde config.json
def load_password():
    with open('config.json') as config_file:
        config = json.load(config_file)
        return config.get("password")

@app.route('/', methods=['GET', 'POST'])
def index():
    if password == "":
        authenticated = True
    else:
        authenticated = session.get('authenticated', False)
    
    if request.method == 'POST':
        input_password = request.form['password']
        stored_password = load_password()  # función que carga la contraseña desde config.json
        
        if input_password == stored_password:
            session['authenticated'] = True
            authenticated = True
        else:
            return "Contraseña incorrecta", 403
    
    return render_template('index.html', authenticated=authenticated)

# selected_option = "/text3"  # Valor inicial por defecto

# Ruta API para enviar la configuración como JSON
@app.route('/api/config')
def get_config():
    with open('config.json') as config_file:
        config_data = json.load(config_file)
    # config_data["option"] = selected_option

    return jsonify(config_data)

# Cargar la configuración desde el archivo config.json
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Obtener la IP y el token del archivo JSON
ip = config.get('ip')
token = config.get('token')
puerto = config.get('puerto')
portServer = config.get('portServer')
password = config.get('password')
selected_option = config.get('option')

# Función para actualizar la selección de la opción
def actualizar_opcion():
    global selected_option
    selected_option = opcion_var.get()
    with open('config.json', 'w') as config_file:
        json.dump({"ip": ip, "token": token, "puerto": puerto, "portServer": portServer, "password": password, "option": selected_option}, config_file, indent=4)

# Función para actualizar la configuración
def update_config():
    global ip, token, puerto, portServer, password
    ip = entry_ip.get()
    token = entry_token.get()
    puerto = entry_puerto.get()
    portServer = entry_portServer.get()
    password = entry_password.get()
    selected_option = opcion_var.get()

    # Guardar los valores en config.json
    with open('config.json', 'w') as config_file:
        json.dump({"ip": ip, "token": token, "puerto": puerto, "portServer": portServer, "password": password, "option": selected_option}, config_file, indent=4)

    messagebox.showinfo("Información", "Configuración actualizada correctamente. Reinicie el servidor para aplicar los cambios.")

""" @app.route('/')
def index():
    return render_template('index.html') """

@app.route('/biblia', methods=['GET', 'POST'])
def biblia():
    if password == "":
        authenticated = True
    else:
        authenticated = session.get('authenticated', False)
    
    if request.method == 'POST':
        input_password = request.form['password']
        stored_password = load_password()  # función que carga la contraseña desde config.json
        
        if input_password == stored_password:
            session['authenticated'] = True
            authenticated = True
        else:
            return "Contraseña incorrecta", 403
    
    return render_template('Biblia.html', authenticated=authenticated)

@app.route('/ppt')
def ppt():
    if acceso_permitido:    
        return render_template('ppt.html')
    else:
        return jsonify({"message": "Acceso denegado a /ppt"}), 403
    
# Función para actualizar el acceso según el estado de la casilla de verificación
def actualizar_acceso():
    global acceso_permitido
    acceso_permitido = acceso_var.get() == 1  # 1 = acceso permitido, 0 = acceso denegado
    estado_texto.set("Permitido" if acceso_permitido else "Denegado")
    check_acceso.config(text="Activar acceso a /ppt: " + estado_texto.get())


# Ruta para servir bible.json
@app.route('/static/bible.json')
def bible_json():
    return send_from_directory('static', 'bible.json')

# Configuración para servir archivos estáticos (CSS, imágenes, etc.)
@app.route('/<path:path>')
def serve_static(path):
    root_dir = os.path.dirname(os.getcwd())
    return send_from_directory(os.path.join(root_dir, 'static'), path)

@app.route('/ToggleF8', methods=['POST'])
def ToggleF8():
    client_ip = request.remote_addr
    url = f'http://{ip}:{puerto}/api/ToggleF8?token={token}'
    headers = {'Content-Type': 'application/json'}
    data = {}

    try:
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            log_message(f"Acción \"FONDO DE PANTALLA\" ejecutada correctamente por {client_ip}")
            return jsonify(response.json())
        else:
            log_message(f"Error al realizar la solicitud: {response.status_code}")
            return jsonify({'error': 'Error al realizar la solicitud', 'status_code': response.status_code, 'text': response.text})
    except Exception as e:
        log_message(f"Error desde {client_ip}: {str(e)}")

@app.route('/ToggleF9', methods=['POST'])
def ToggleF9():
    client_ip = request.remote_addr
    url = f'http://{ip}:{puerto}/api/ToggleF9?token={token}'
    headers = {'Content-Type': 'application/json'}
    data = {}

    try:
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            log_message(f"Acción \"SIN LETRA\" ejecutada correctamente por {client_ip}")
            return jsonify(response.json())
        else:
            log_message(f"Error al realizar la solicitud: {response.status_code}")
            return jsonify({'error': 'Error al realizar la solicitud', 'status_code': response.status_code, 'text': response.text})
    except Exception as e:
        log_message(f"Error desde {client_ip}: {str(e)}")

@app.route('/ToggleF10', methods=['POST'])
def ToggleF10():
    client_ip = request.remote_addr
    url = f'http://{ip}:{puerto}/api/ToggleF10?token={token}'
    headers = {'Content-Type': 'application/json'}
    data = {}

    try:
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            log_message(f"Acción \"PANTALLA NEGRA\" ejecutada correctamente por {client_ip}")
            return jsonify(response.json())
        else:
            log_message(f"Error al realizar la solicitud: {response.status_code}")
            return jsonify({'error': 'Error al realizar la solicitud', 'status_code': response.status_code, 'text': response.text})
    except Exception as e:
        log_message(f"Error desde {client_ip}: {str(e)}")

@app.route('/actionNext', methods=['POST'])
def actionNext():
    client_ip = request.remote_addr
    url = f'http://{ip}:{puerto}/api/ActionNext?token={token}' # f'http://{ip}:{puerto}/api/ActionNext?token={token}'
    headers = {'Content-Type': 'application/json'}
    data = {}

    try:
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            log_message(f"Acción \"SIGUIENTE\" ejecutada correctamente por {client_ip}")
            return jsonify(response.json())
        else:
            log_message(f"Error al realizar la solicitud: {response.status_code}")
            return jsonify({'error': 'Error al realizar la solicitud', 'status_code': response.status_code, 'text': response.text})
    except Exception as e:
        log_message(f"Error desde {client_ip}: {str(e)}")

@app.route('/actionPrevious', methods=['POST'])
def actionPrevious():
    client_ip = request.remote_addr
    url = f'http://{ip}:{puerto}/api/ActionPrevious?token={token}'
    headers = {'Content-Type': 'application/json'}
    data = {}

    try:
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            log_message(f"Acción \"ANTERIOR\" ejecutada correctamente por {client_ip}")
            return jsonify(response.json())
        else:
            log_message(f"Error al realizar la solicitud desde {client_ip}: {response.status_code}")
            return jsonify({'error': 'Error al realizar la solicitud', 'status_code': response.status_code, 'text': response.text})
    except Exception as e:
        log_message(f"Error desde {client_ip}: {str(e)}")

@app.route('/CloseCurrentPresentation', methods=['POST'])
def CloseCurrentPresentation():
    client_ip = request.remote_addr
    url = f'http://{ip}:{puerto}/api/CloseCurrentPresentation?token={token}'
    headers = {'Content-Type': 'application/json'}
    data = {}

    try:
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            log_message(f"Acción \"CERRAR PRESENTACION\" ejecutada correctamente por {client_ip}")
            return jsonify(response.json())
        else:
            log_message(f"Error al realizar la solicitud desde {client_ip}: {response.status_code}")
            return jsonify({'error': 'Error al realizar la solicitud', 'status_code': response.status_code, 'text': response.text})
    except Exception as e:
        log_message(f"Error desde {client_ip}: {str(e)}")

@app.route('/GetMediaPlaylist', methods=['POST'])
def GetMediaPlaylist():
    client_ip = request.remote_addr
    url = f'http://{ip}:{puerto}/api/GetMediaPlaylist?token={token}'
    headers = {'Content-Type': 'application/json'}
    data = {}

    try:
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            log_message(f"Acción \"OBTENER PLAYLIST\" ejecutada correctamente por {client_ip}")
            return jsonify(response.json())
        else:
            log_message(f"Error al realizar la solicitud desde {client_ip}: {response.status_code}")
            return jsonify({'error': 'Error al realizar la solicitud', 'status_code': response.status_code, 'text': response.text})
    except Exception as e:
        log_message(f"Error desde {client_ip}: {str(e)}")

@app.route('/MediaPlaylistAction', methods=['POST'])
def MediaPlaylistAction():
    client_ip = request.remote_addr
    url = f'http://{ip}:{puerto}/api/MediaPlaylistAction?token={token}'
    headers = {'Content-Type': 'application/json'}

    # Obtener el dato del ID del elemento desde la solicitud POST
    data = request.get_json()
    element_id = data.get('id', '')

    # Crear los datos que se enviarán en el cuerpo de la solicitud POST
    data = {
        'id': element_id
    }

    try:
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            log_message(f"Acción \"PLAY\" ejecutada correctamente por {client_ip}")
            return jsonify(response.json())
        else:
            log_message(f"Error al realizar la solicitud desde {client_ip}: {response.status_code}")
            return jsonify({'error': 'Error al realizar la solicitud', 'status_code': response.status_code, 'text': response.text})
    except Exception as e:
        log_message(f"Error desde {client_ip}: {str(e)}")

def GetMediaPlayerInfo():
    client_ip = request.remote_addr
    url = f'http://{ip}:{puerto}/api/GetMediaPlayerInfo?token={token}'
    headers = {'Content-Type': 'application/json'}
    data = {}

    try:
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            data = response.json()

            global playing
            playing = data.get('data', {}).get('playing', None)
            log_message(f"El estado de reproducción es {playing}")
        else:
            return {'error': 'Error al realizar la solicitud', 'status_code': response.status_code, 'text': response.text}
    except Exception as e:
        log_message(f"Error desde {client_ip}: {str(e)}")

@app.route('/MediaPlayerActionPause', methods=['POST'])
def MediaPlayerActionPause():
    GetMediaPlayerInfo()
    client_ip = request.remote_addr

    if playing == True :
        url = f'http://{ip}:{puerto}/api/MediaPlayerAction?token={token}'
        headers = {'Content-Type': 'application/json'}
        data = {"action": "pause"}

        try:
            response = requests.post(url, headers=headers, json=data)

            if response.status_code == 200:
                log_message(f"Acción \"PAUSE\" ejecutada correctamente por {client_ip}")
                return jsonify(response.json())
            else:
                log_message(f"Error al realizar la solicitud desde {client_ip}: {response.status_code}")
                return jsonify({'error': 'Error al realizar la solicitud', 'status_code': response.status_code, 'text': response.text})
        except Exception as e:
            log_message(f"Error desde {client_ip}: {str(e)}")
    
    else:
        url = f'http://{ip}:{puerto}/api/MediaPlayerAction?token={token}'
        headers = {'Content-Type': 'application/json'}
        data = {"action": "play"}

        try:
            response = requests.post(url, headers=headers, json=data)

            if response.status_code == 200:
                log_message(f"Acción \"PLAY\" ejecutada correctamente por {client_ip}")
                return jsonify(response.json())
            else:
                log_message(f"Error al realizar la solicitud desde {client_ip}: {response.status_code}")
                return jsonify({'error': 'Error al realizar la solicitud', 'status_code': response.status_code, 'text': response.text})
        except Exception as e:
            log_message(f"Error desde {client_ip}: {str(e)}")

@app.route('/MediaPlayerActionStop', methods=['POST'])
def MediaPlayerActionStop():
    client_ip = request.remote_addr
    url = f'http://{ip}:{puerto}/api/MediaPlayerAction?token={token}'
    headers = {'Content-Type': 'application/json'}
    data = {"action": "stop"}

    try:
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            log_message(f"Acción \"STOP\" ejecutada correctamente por {client_ip}")
            return jsonify(response.json())
        else:
            log_message(f"Error al realizar la solicitud desde {client_ip}: {response.status_code}")
            return jsonify({'error': 'Error al realizar la solicitud', 'status_code': response.status_code, 'text': response.text})
    except Exception as e:
        log_message(f"Error desde {client_ip}: {str(e)}")


#-------------------------------------------
# Configurar la interfaz gráfica con Tkinter
root = tk.Tk()
root.title("Server - Holyrics Web Control")
root.resizable(False, False)
root.configure(bg="#f0f0f0")

root.option_add("*Font", "Arial 10")
root.option_add("*Button.Font", "Arial 10 bold")

bg_color = "#f0f0f0"
btn_color = "#007ACC"
btn_fg_color = "white"
frame_bg_color = "#e0e0e0"

def update_status():
    ipLocal = get_local_ip()
    port = portServer
    url = (f"http://{ipLocal}:{port}")
    status_text.set(f"Servidor corriendo en:\n{url}")
    global urlRun
    urlRun = tk.Label(root, text=url, font=("Arial", 12))

# Función para mostrar notificación temporal
def mostrar_notificacion(texto):
    notificacion = tk.Label(root, text=texto, background="lightgreen")
    notificacion.place(x=515, y=477)  # Ajusta la posición como necesites
    root.after(2000, notificacion.destroy)

# Función para copiar al portapapeles
def copiar_al_portapapeles():
    texto = urlRun.cget("text")
    root.clipboard_clear()
    root.clipboard_append(texto)
    mostrar_notificacion("Copiado")  # Muestra la notificación


def open_tutorial():
    # Enlace al video de YouTube
    webbrowser.open("https://youtu.be/ZxcN2IjycTs")

def show_about():
    about_message = (
        "☝️ PARA LA GLORIA DE DIOS ☝️\n\n"
        "Web Control para Holyrics\n"
        "Versión: 2.2.0\n\n\n"
        "Información de contacto:\n\n"
        "Telegram: @mark_ost7\n"
        "GitHub: https://github.com/wcmark\n"
        "YouTube personal: @Marcos-Tapia\n"
        "YouTube de la iglesia: @ice-lapaz\n\n"
        "San Miguel del Monte, Bs. As. - Argentina\n"
    )
    messagebox.showinfo("Acerca de...", about_message)

# Función para crear el ícono de la bandeja (simple ejemplo con un círculo)
def create_image():
    # Crear una imagen de 64x64
    image = Image.new('RGB', (64, 64), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)
    draw.ellipse((16, 16, 48, 48), fill='black')
    return image

# Función que muestra nuevamente la ventana de Tkinter
def show_window(icon, item):
    icon.stop()
    root.after(0, root.deiconify)

# Función que oculta la ventana de Tkinter y muestra el ícono en la bandeja
def hide_window():
    root.withdraw()  # Ocultar la ventana principal
    image = create_image()  # Crear un ícono
    menu = (item('Mostrar', show_window), item('Salir', close_cmd))
    icon = Icon("AppName", image, "My App", menu)
    threading.Thread(target=icon.run, daemon=True).start()


def close_cmd():
    # Cierra la ventana de CMD y finaliza la ejecución de Flask
    os._exit(0)

root.protocol("WM_DELETE_WINDOW", close_cmd)

# Crear el menú
menu_bar = Menu(root)
root.config(menu=menu_bar)

# Añadir la opción de minimizar al área de notificaciones
file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Minimizar a la bandeja del sistema", command=hide_window)
menu_bar.add_cascade(label="Opciones", menu=file_menu)

# Agregar el menú "Ayuda"
help_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Ayuda", menu=help_menu)
help_menu.add_command(label="Tutorial", command=open_tutorial)
help_menu.add_command(label="Acerca de...", command=show_about)

label_frame_title = tk.Label(root, text="Configuración", font=("Arial", 12), background="lightgray")
label_frame_title.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
# Frame para configuración
config_frame = tk.Frame(root, background=frame_bg_color)
config_frame.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

# Campos para config.json
tk.Label(config_frame, text="IP del equipo de Holyrics:", anchor="w", background=frame_bg_color).grid(row=0, column=0, padx=5, sticky="W")
entry_ip = tk.Entry(config_frame, justify="center")
entry_ip.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
entry_ip.insert(0, ip)

tk.Label(config_frame, text="Token (API Holyrics):", anchor="w", background=frame_bg_color).grid(row=1, column=0, padx=5, sticky="W")
entry_token = tk.Entry(config_frame, show="*", justify="center")
entry_token.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
entry_token.insert(0, token)

tk.Label(config_frame, text="Puerto (API Holyrics):", anchor="w", background=frame_bg_color).grid(row=2, column=0, padx=5, sticky="W")
entry_puerto = tk.Entry(config_frame, justify="center")
entry_puerto.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
entry_puerto.insert(0, puerto)

# Separador invisible en la siguiente fila
separator = tk.Label(config_frame, text="", background=frame_bg_color)
separator.grid(row=3, column=0, pady=5)

tk.Label(config_frame, text="Puerto para este servidor:", anchor="w", background=frame_bg_color).grid(row=4, column=0, padx=5, sticky="W")
entry_portServer = tk.Entry(config_frame, justify="center")
entry_portServer.grid(row=4, column=1, padx=5, pady=5, sticky="ew")
entry_portServer.insert(0, portServer)

tk.Label(config_frame, text="Contraseña (opcional):", anchor="w", background=frame_bg_color).grid(row=5, column=0, padx=5, sticky="W")
entry_password = tk.Entry(config_frame, show="*", justify="center")
entry_password.grid(row=5, column=1, padx=5, pady=5, sticky="ew")
entry_password.insert(0, password)

# Botón para guardar configuración
btn_save = tk.Button(config_frame, text="Guardar Configuración", command=update_config, bg=btn_color, fg=btn_fg_color)
btn_save.grid(row=6, column=0, columnspan=2, padx=5, pady=9)


label_frame2_title = tk.Label(root, text="Control de PPT", font=("Arial", 12), background="lightgray")
label_frame2_title.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
# Frame para configuración
config_frame2 = tk.Frame(root, background=frame_bg_color)
config_frame2.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

# Variable para controlar el estado de la casilla de verificación
acceso_var = tk.IntVar(value=1)  # 1 = acceso permitido por defecto
acceso_permitido = True

# Casilla de verificación para activar/desactivar acceso
estado_texto = tk.StringVar(value="Permitido")

check_acceso = tk.Checkbutton(config_frame2, text="Activar acceso a /ppt: " + estado_texto.get(), variable=acceso_var, command=actualizar_acceso, background=frame_bg_color)
check_acceso.grid(row=0, column=0, padx=5, pady=5, sticky="w")

# Crear los botones de opción (radio buttons)
opcion_var = tk.StringVar(value=selected_option)  # Valor inicial

opciones = [("Widescreen", "/widescreen"), 
            ("Text", "/text"), 
            ("Text 2", "/text2"), 
            ("Text 3", "/text3")]

tk.Label(config_frame2, text="Selecciona una proyección de holyrics\npara mostrar en el control de diapositivas:", anchor="w", justify="left", background=frame_bg_color).grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="w")

for i, (opcion_texto, opcion_valor) in enumerate(opciones):
    tk.Radiobutton(config_frame2, text=opcion_texto, variable=opcion_var, value=opcion_valor, command=actualizar_opcion, background=frame_bg_color).grid(row=2+i, column=0, padx=2, pady=5, sticky="w")


# Campo de texto grande para mensajes/errores
tk.Label(root, text="Logs:").grid(row=10, column=0, padx=5, pady=0, sticky="w")
txt_logs = scrolledtext.ScrolledText(root, width=40, height=10)
txt_logs.grid(row=11, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

def log_message(message):
    txt_logs.insert(tk.END, message + '\n')
    txt_logs.see(tk.END)

# Ejemplo de cómo agregar un mensaje de log
log_message("Servidor en ejecución...")

# Etiqueta para mostrar el estado del servidor
status_text = tk.StringVar()
status_label = tk.Label(root, textvariable=status_text, font=("Helvetica", 12))
status_label.grid(row=12, column=0, columnspan=2, padx=10, pady=0)

# Crear el botón con la imagen y el comando de copiar
boton_copiar = tk.Button(root, text="Copiar URL", command=copiar_al_portapapeles, bg=btn_color, fg=btn_fg_color)
boton_copiar.grid(row=12, column=1, columnspan=2, padx=0, pady=5, sticky="n")


# Actualizar el estado en la interfaz gráfica
update_status()


if __name__ == '__main__':
    flask_thread = threading.Thread(target=lambda: app.run(host='0.0.0.0', port=portServer, debug=False))
    flask_thread.start()

    root.mainloop()