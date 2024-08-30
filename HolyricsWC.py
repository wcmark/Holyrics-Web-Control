from flask import Flask, render_template, request, jsonify, send_from_directory
import requests, os, json

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

app = Flask(__name__)

print(Colors.GREEN + "█░█ █▀█ █░░ █▄█ █▀█ █ █▀▀ █▀   ▄▄   █░█░█ █▀▀ █▄▄   █▀▀ █▀█ █▄░█ ▀█▀ █▀█ █▀█ █░░   █▄▄ █▄█   █▀▄▀█ ▄▀█ █▀█ █▄▀   █▀█ █▀\n█▀█ █▄█ █▄▄ ░█░ █▀▄ █ █▄▄ ▄█   ░░   ▀▄▀▄▀ ██▄ █▄█   █▄▄ █▄█ █░▀█ ░█░ █▀▄ █▄█ █▄▄   █▄█ ░█░   █░▀░█ █▀█ █▀▄ █░█   █▄█ ▄█" + Colors.END)
print()
print("Para consultas o informe de fallos escriba por Telegram a @mark_ost7")
print()
print()
print(Colors.BLUE + "Iniciando el servidor..." + Colors.END)



# Cargar la configuración desde el archivo config.json
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Obtener la IP y el token del archivo JSON
ip = config.get('ip')
token = config.get('token')
puerto = config.get('puerto')

@app.route('/')
def index():
    return render_template('index.html')

# Configuración para servir archivos estáticos (CSS, imágenes, etc.)
@app.route('/<path:path>')
def serve_static(path):
    root_dir = os.path.dirname(os.getcwd())
    return send_from_directory(os.path.join(root_dir, 'static'), path)

@app.route('/actionNext', methods=['POST'])
def actionNext():
    url = f'http://{ip}:{puerto}/api/ActionNext?token={token}' # f'http://{ip}:{puerto}/api/ActionNext?token={token}'
    headers = {'Content-Type': 'application/json'}
    data = {}

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({'error': 'Error al realizar la solicitud', 'status_code': response.status_code, 'text': response.text})


@app.route('/actionPrevious', methods=['POST'])
def actionPrevious():
    url = f'http://{ip}:{puerto}/api/ActionPrevious?token={token}'
    headers = {'Content-Type': 'application/json'}
    data = {}

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({'error': 'Error al realizar la solicitud', 'status_code': response.status_code, 'text': response.text})

@app.route('/CloseCurrentPresentation', methods=['POST'])
def CloseCurrentPresentation():
    url = f'http://{ip}:{puerto}/api/CloseCurrentPresentation?token={token}'
    headers = {'Content-Type': 'application/json'}
    data = {}

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({'error': 'Error al realizar la solicitud', 'status_code': response.status_code, 'text': response.text})

@app.route('/GetMediaPlaylist', methods=['POST'])
def GetMediaPlaylist():
    url = f'http://{ip}:{puerto}/api/GetMediaPlaylist?token={token}'
    headers = {'Content-Type': 'application/json'}
    data = {}

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({'error': 'Error al realizar la solicitud', 'status_code': response.status_code, 'text': response.text})


@app.route('/MediaPlaylistAction', methods=['POST'])
def MediaPlaylistAction():
    url = f'http://{ip}:{puerto}/api/MediaPlaylistAction?token={token}'
    headers = {'Content-Type': 'application/json'}

    # Obtener el dato del ID del elemento desde la solicitud POST
    data = request.get_json()
    element_id = data.get('id', '')

    # Crear los datos que se enviarán en el cuerpo de la solicitud POST
    data = {
        'id': element_id
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({'error': 'Error al realizar la solicitud', 'status_code': response.status_code, 'text': response.text})


@app.route('/MediaPlayerAction', methods=['POST'])
def MediaPlayerAction():
    url = f'http://{ip}:{puerto}/api/MediaPlayerAction?token={token}'
    headers = {'Content-Type': 'application/json'}
    data = {"action": "stop"}

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({'error': 'Error al realizar la solicitud', 'status_code': response.status_code, 'text': response.text})


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)


