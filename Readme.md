# Hlrcs-WebControl

Una herramienta para facilitar el control remoto de Holyrics a través de un servidor web.

---

## 📂 Archivo de Configuración

### `config.json`
El archivo de configuración se encuentra en la carpeta raíz de esta aplicación y contiene los siguientes elementos:

```json
{
    "ip": "127.0.0.1",
    "token": "9270UeTNfOf2M6Id",
    "puerto": "8091",
    "portServer": "5000",
    "password": "1234",
    "option": "/text3"
}
```

#### Descripción de los parámetros:
- **`ip`**: Especificar la dirección IP de Holyrics.
- **`token`**: El token configurado previamente en Holyrics. (Ir a `Archivo > Configuraciones > API Server > Administrar permisos > Añadir`). Asegúrate de habilitar los permisos necesarios en la columna "Local".
- **`puerto`**: El puerto configurado en Holyrics (por defecto `8091`).
- **`portServer`**: Puerto utilizado por el servidor web de la aplicación (por defecto `5000`).
- **`password`** *(opcional)*: Contraseña para proteger el acceso al servidor.
- **`option`**: Define la opción de transmisión web elegida para diapositivas, para usar el control remoto. Se accede a él por  `http://IP:PUERTO/ppt`.

#### Ejemplo de acceso a la Biblia:
La Biblia se encuentra en: `http://IP:PUERTO/biblia`
- Ejemplo: `http://192.168.100.187:5000/biblia`

---

## 🚀 Guía de Uso

### Primeros Pasos
La primera vez que ejecutes `Hlrcs-WebControl.exe` deberás completar todos los campos de configuración, guardar, cerrar el programa y volver a ejecutar.

Si el archivo `config.json` es borrado o eliminado por error, crea uno nuevo con un editor de texto y guárdalo en la misma carpeta que el ejecutable. (copiar los datos de ejemplo de esta página).


### Notas Importantes
- Durante la primera ejecución, Windows solicitará permiso a través del Firewall para permitir la comunicación por el puerto configurado. **Asegúrate de aceptar.**
- La carpeta `_internal` y su contenido son esenciales para el funcionamiento del programa. No la elimines ni modifiques su estructura.

---

## ✉️ Información de Contacto
Si necesitas asistencia, tienes dudas, o deseas colaborar con el proyecto, no dudes en contactarme:

- **Telegram**: [@mark_ost7](https://t.me/mark_ost7)

Abrazo cordial. Espero que sea de bendición.  
Marcos Tapia - Iglesia Cristiana Evangélica La Paz.

---