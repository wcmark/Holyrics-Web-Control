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
        ipLocal = '127.0.0.1'
    finally:
        s.close()
    return ipLocal

playing = None
app = Flask(__name__)
app.secret_key = 'key'

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
        stored_password = load_password()
        if input_password == stored_password:
            session['authenticated'] = True
            authenticated = True
        else:
            return "Contraseña Incorrecta", 403
    return render_template('index.html', authenticated=authenticated)

@app.route('/api/config')
def get_config():
    with open('config.json') as config_file:
        config_data = json.load(config_file)
    return jsonify(config_data)
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

ip = config.get('ip')
token = config.get('token')
puerto = config.get('puerto')
portServer = config.get('portServer')
password = config.get('password')
selected_option = config.get('option')

def actualizar_opcion():
    global selected_option
    selected_option = opcion_var.get()
    with open('config.json', 'w') as config_file:
        json.dump({"ip": ip, "token": token, "puerto": puerto, "portServer": portServer, "password": password, "option": selected_option}, config_file, indent=4)

def update_config():
    global ip, token, puerto, portServer, password
    ip = entry_ip.get()
    token = entry_token.get()
    puerto = entry_puerto.get()
    portServer = entry_portServer.get()
    password = entry_password.get()
    selected_option = opcion_var.get()
    with open('config.json', 'w') as config_file:
        json.dump({"ip": ip, "token": token, "puerto": puerto, "portServer": portServer, "password": password, "option": selected_option}, config_file, indent=4)
    messagebox.showinfo("Información", "Configuración actualizada. Reinicie el servidor.")

@app.route('/biblia', methods=['GET', 'POST'])
def biblia():
    if password == "":
        authenticated = True
    else:
        authenticated = session.get('authenticated', False)
    if request.method == 'POST':
        input_password = request.form['password']
        stored_password = load_password()
        if input_password == stored_password:
            session['authenticated'] = True
            authenticated = True
        else:
            return "Contraseña Incorrecta", 403
    return render_template('Biblia.html', authenticated=authenticated)

@app.route('/ppt')
def ppt():
    if acceso_permitido:    
        return render_template('ppt.html')
    else:
        return jsonify({"message": "Acceso denegado a /ppt"}), 403
    
def actualizar_acceso():
    global acceso_permitido
    acceso_permitido = acceso_var.get() == 1
    estado_texto.set("Permitido" if acceso_permitido else "Denegado")
    check_acceso.config(text="Activar acceso a /ppt: " + estado_texto.get())

@app.route('/static/bible.json')
def bible_json():
    return send_from_directory('static', 'bible.json')

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
    url = f'http://{ip}:{puerto}/api/ActionNext?token={token}'
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
    data = request.get_json()
    element_id = data.get('id', '')
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

# Ruta para obtener las diapositivas de la presentación actual
@app.route('/loadSlides', methods=['GET'])
def get_slides():
    url = f'http://{ip}:{puerto}/api/GetCurrentPresentation?token={token}'
    data = {
        "include_slides": True,
        "include_slide_comment": True,
        "include_slide_preview": True,
        "slide_preview_size": "320x180"
    }
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            result = response.json()
            if result.get('data') and result['data'].get('slides'):
                song_name = result['data'].get('name')
                slide_number = result['data'].get('slide_number')
                slides = result['data']['slides']
                presentation_type = result['data'].get('type')
                return jsonify({
                    "name": song_name,
                    "slide_number": slide_number,
                    "type": presentation_type,
                    "slides": slides
                })
            else:
                return jsonify({"error": "No se encontraron diapositivas."})
        else:
            return jsonify({"error": f"Error al obtener las diapositivas: {response.status_code}", "text": response.text})
    except Exception as e:
        return jsonify({"error": f"Error en la solicitud: {str(e)}"})

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

@app.route('/goToSlide', methods=['POST'])
def go_to_slide():
    client_ip = request.remote_addr
    index = request.json.get('index')  # Obtener el índice desde el cuerpo de la solicitud
    url = f'http://{ip}:{puerto}/api/ActionGoToIndex?token={token}'
    headers = {'Content-Type': 'application/json'}
    data = {'index': index}
    
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            log_message(f"Slide cambiado al índice {index} por {client_ip}")
            return jsonify({'message': f'Slide cambiado al índice {index}'})
        else:
            log_message(f"Error al cambiar el slide: {response.status_code}")
            return jsonify({'error': 'Error al cambiar el slide', 'status_code': response.status_code, 'text': response.text})
    except Exception as e:
        log_message(f"Error desde {client_ip}: {str(e)}")
        return jsonify({'error': 'Error interno', 'details': str(e)})


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
def mostrar_notificacion(texto):
    notificacion = tk.Label(root, text=texto, background="lightgreen")
    notificacion.place(x=515, y=477)
    root.after(2000, notificacion.destroy)
def copiar_al_portapapeles():
    texto = urlRun.cget("text")
    root.clipboard_clear()
    root.clipboard_append(texto)
    mostrar_notificacion("Copiado")
def open_tutorial():
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
    image = Image.new('RGB', (64, 64), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)
    draw.ellipse((16, 16, 48, 48), fill='black')
    return image
def show_window(icon, item):
    icon.stop()
    root.after(0, root.deiconify)
def hide_window():
    root.withdraw()
    image = create_image()
    menu = (item('Mostrar', show_window), item('Salir', close_cmd))
    icon = Icon("AppName", image, "My App", menu)
    threading.Thread(target=icon.run, daemon=True).start()
def close_cmd():
    os._exit(0)
root.protocol("WM_DELETE_WINDOW", close_cmd)
menu_bar = Menu(root)
root.config(menu=menu_bar)
file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Minimizar a la bandeja del sistema", command=hide_window)
menu_bar.add_cascade(label="Opciones", menu=file_menu)
help_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Ayuda", menu=help_menu)
help_menu.add_command(label="Tutorial", command=open_tutorial)
help_menu.add_command(label="Acerca de...", command=show_about)
label_frame_title = tk.Label(root, text="Configuración", font=("Arial", 12), background="lightgray")
label_frame_title.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
config_frame = tk.Frame(root, background=frame_bg_color)
config_frame.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
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
btn_save = tk.Button(config_frame, text="Guardar Configuración", command=update_config, bg=btn_color, fg=btn_fg_color)
btn_save.grid(row=6, column=0, columnspan=2, padx=5, pady=9)
label_frame2_title = tk.Label(root, text="Control de PPT", font=("Arial", 12), background="lightgray")
label_frame2_title.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
config_frame2 = tk.Frame(root, background=frame_bg_color)
config_frame2.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
acceso_var = tk.IntVar(value=1)
acceso_permitido = True
estado_texto = tk.StringVar(value="Permitido")
check_acceso = tk.Checkbutton(config_frame2, text="Activar acceso a /ppt: " + estado_texto.get(), variable=acceso_var, command=actualizar_acceso, background=frame_bg_color)
check_acceso.grid(row=0, column=0, padx=5, pady=5, sticky="w")
opcion_var = tk.StringVar(value=selected_option)
opciones = [("Widescreen", "/widescreen"), 
            ("Text", "/text"), 
            ("Text 2", "/text2"), 
            ("Text 3", "/text3")]
tk.Label(config_frame2, text="Selecciona una proyección de holyrics\npara mostrar en el control de diapositivas:", anchor="w", justify="left", background=frame_bg_color).grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="w")
for i, (opcion_texto, opcion_valor) in enumerate(opciones):
    tk.Radiobutton(config_frame2, text=opcion_texto, variable=opcion_var, value=opcion_valor, command=actualizar_opcion, background=frame_bg_color).grid(row=2+i, column=0, padx=2, pady=5, sticky="w")
tk.Label(root, text="Logs:").grid(row=10, column=0, padx=5, pady=0, sticky="w")
txt_logs = scrolledtext.ScrolledText(root, width=40, height=10)
txt_logs.grid(row=11, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

def log_message(message):
    txt_logs.insert(tk.END, message + '\n')
    txt_logs.see(tk.END)

log_message("Servidor en ejecución...")
status_text = tk.StringVar()
status_label = tk.Label(root, textvariable=status_text, font=("Helvetica", 12))
status_label.grid(row=12, column=0, columnspan=2, padx=10, pady=0)
boton_copiar = tk.Button(root, text="Copiar URL", command=copiar_al_portapapeles, bg=btn_color, fg=btn_fg_color)
boton_copiar.grid(row=12, column=1, columnspan=2, padx=0, pady=5, sticky="n")
update_status()
if __name__ == '__main__':
    flask_thread = threading.Thread(target=lambda: app.run(host='0.0.0.0', port=portServer, debug=False))
    flask_thread.start()
    root.mainloop()