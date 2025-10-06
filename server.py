#!/usr/bin/env python3
"""
Ejecutar en el nodo Servidor con: python3 server.py
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs

HTML_FORM = """
<!DOCTYPE html>
<html>
<head>
    <title>Login - Lab Sniffing</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background-color: #f0f0f0;
        }
        .login-container {
            background-color: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h2 {
            text-align: center;
            color: #333;
        }
        input {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            border: 1px solid #ddd;
            border-radius: 4px;
            box-sizing: border-box;
        }
        button {
            width: 100%;
            padding: 10px;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
        }
        button:hover {
            background-color: #0056b3;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <h2>Sistema de Login</h2>
        <form method="POST" action="/login">
            <input type="text" name="usuario" placeholder="Usuario" required>
            <input type="password" name="password" placeholder="Contraseña" required>
            <button type="submit">Iniciar Sesión</button>
        </form>
    </div>
</body>
</html>
"""

HTML_SUCCESS = """
<!DOCTYPE html>
<html>
<head>
    <title>Login Exitoso</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background-color: #d4edda;
        }}
        .message {{
            background-color: white;
            padding: 30px;
            border-radius: 8px;
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="message">
        <h2>Login Exitoso</h2>
        <p>Usuario: <strong>{usuario}</strong></p>
        <p><a href="/">Volver</a></p>
    </div>
</body>
</html>
"""

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(HTML_FORM.encode())
    
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        
        # Parsear datos del formulario
        params = parse_qs(post_data)
        usuario = params.get('usuario', [''])[0]
        password = params.get('password', [''])[0]
        
        print(f"\n[+] Login recibido:")
        print(f"    Usuario: {usuario}")
        print(f"    Password: {password}")

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        response = HTML_SUCCESS.format(usuario=usuario)
        self.wfile.write(response.encode())
    
    def log_message(self, format, *args):
        """Override para mostrar logs más limpios"""
        print(f"[INFO] {self.address_string()} - {format % args}")

def run_server(port=80):
    server_address = ('', port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print(f'[*] Servidor web iniciado en puerto {port}')
    print(f'[*] Esperando conexiones...\n')
    httpd.serve_forever()

if __name__ == '__main__':
    try:
        run_server()
    except PermissionError:
        print("[!] Error: Se necesitan permisos de root para usar el puerto 80")
        print("[*] Intentando con puerto 8080...")
        run_server(8080)
    except KeyboardInterrupt:
        print("\n[*] Servidor detenido")
