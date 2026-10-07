"""
Punto de entrada principal para el Dashboard IPM Colombia.
Ejecuta el servidor interactivo Dash / Flask.

Uso:
    python app.py
    o
    gunicorn app:server
"""
import os
from mapa_agua import app, server

if __name__ == "__main__":
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", 8050))
    debug = os.environ.get("DASH_DEBUG", "false").lower() == "true"
    app.run(host=host, port=port, debug=debug)
