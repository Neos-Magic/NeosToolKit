# NeosToolKit
Neos Toolkit es una aplicación de escritorio con interfaz gráfica (GUI) moderna escrita en Python que consolida herramientas matemáticas y utilidades de auditoría/diagnóstico de red en un solo panel interactivo.

🚀 Cómo Arrancarlo (Requisitos)
Instalar Python: Necesitas tener instalado Python 3.x en tu sistema. Al instalarlo en Windows, es vital marcar la casilla que dice "Add Python to PATH".

Instalar Dependencias: La aplicación requiere el módulo externo customtkinter. Puedes instalarlo manualmente abriendo tu consola y ejecutando:

Bash
pip install customtkinter
(Nota: El archivo .bat que te dejaré abajo intentará validar e instalar esto de forma automática por ti).

🎯 Explicación de los Módulos de la Aplicación
La interfaz se divide en una barra de navegación lateral izquierda y un contenedor dinámico a la derecha:


Dashboard: La pantalla de bienvenida estándar. Sirve para limpiar el espacio visual y dar una presentación limpia al iniciar el software.

<img width="1919" height="1039" alt="dashboard" src="https://github.com/user-attachments/assets/e4d500bb-db4e-45ca-9440-99f7cc2f0799" />

Calculadora: Módulo aritmético tradicional. Captura los valores ingresados en dos cajas de texto, los convierte a números flotantes (float) y ejecuta operaciones de suma, resta, multiplicación o división a través de funciones vinculadas a botones. Si se ingresa una letra o se intenta dividir entre cero, maneja el error mostrando un cuadro de diálogo (messagebox.showerror).

<img width="1919" height="1039" alt="calculadora" src="https://github.com/user-attachments/assets/7b5b940a-a1f0-4566-932b-f46db2590fc4" />

Escaneo Red (Network Scanner): * Cómo funciona por dentro: Este módulo toma el segmento de red (ej. 192.168.1.0/24) y utiliza la librería ipaddress para desglosar la lista completa de todas las IPs posibles de la subred (de la .1 a la .254).

Rendimiento: Para evitar que la ventana se congele o se quede "colgada", utiliza hilos en segundo plano (threading.Thread) combinados con un pool de ejecución rápida (ThreadPoolExecutor) configurado con un límite de 50 trabajadores simultáneos. Cada hilo ejecuta un comando ping del sistema operativo de manera ultra rápida. Si el host responde (código de salida 0), se añade a la lista de dispositivos activos en tiempo real.

<img width="1919" height="1039" alt="escaneo de red" src="https://github.com/user-attachments/assets/046c3952-b1f9-4908-93ca-0f408c55bfbf" />

Port Scanner (Escáner de Puertos):

Cómo funciona por dentro: Envía peticiones de conexión directa TCP mediante sockets (socket.connect_ex) a una dirección IP en los puertos indicados. Tiene un temporizador límite (timeout) de 1 segundo para no ralentizar el proceso.

<img width="1919" height="1039" alt="escaneo de puertos" src="https://github.com/user-attachments/assets/1eb66eeb-6882-4d18-9d53-198c2847ad58" />
Uso: Puedes indicarle una sola IP o un rango CIDR. En el campo de puertos puedes ingresar los que tú desees separados por comas (ejemplo: 22,80,443). Si dejas el campo de puertos vacío, el script usará automáticamente su diccionario interno de 16 puertos comunes (FTP, SSH, HTTP, HTTPS, etc.).

Exportación: Incluye un botón para volcar los resultados exitosos estructurándolos en un archivo .json mediante el módulo nativo json y la ventana nativa de guardado de archivos (filedialog).
