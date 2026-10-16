#!/usr/bin/env python3
"""Servidor HTTP local para el comparador. Solo escucha en 127.0.0.1."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit
import json
import os

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)
os.chdir(ROOT)

class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if urlsplit(self.path).path == "/api/data-files":
            files = sorted(p.relative_to(DATA).as_posix()
                           for p in DATA.rglob("*") if p.is_file() and p.suffix.lower() == ".csv")
            payload = json.dumps(files, ensure_ascii=False).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(payload)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(payload)
            return
        super().do_GET()

if __name__ == "__main__":
    print("Abre http://127.0.0.1:8765/index.html")
    print("Copia los CSV a la carpeta data/ y recarga la página.")
    ThreadingHTTPServer(("127.0.0.1", 8765), Handler).serve_forever()
