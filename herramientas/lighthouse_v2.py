# -*- coding: utf-8 -*-
"""Lighthouse móvil de la v2 con el servidor en un hilo del mismo proceso (los procesos en segundo plano mueren).
Uso:  python3 herramientas/lighthouse_v2.py [--veces 3] / /seo-local/
Da la mediana de rendimiento, accesibilidad y SEO, y LCP, TBT y CLS. Local, sin compresión (http.server)."""
import argparse, functools, http.server, json, os, socketserver, statistics, subprocess, threading

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ap = argparse.ArgumentParser()
ap.add_argument("rutas", nargs="*", default=["/"])
ap.add_argument("--veces", type=int, default=3)
ap.add_argument("--puerto", type=int, default=8791)
a = ap.parse_args()


class Silencioso(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *x):
        pass


socketserver.TCPServer.allow_reuse_address = True
srv = socketserver.ThreadingTCPServer(("127.0.0.1", a.puerto), functools.partial(Silencioso, directory=os.path.join(RAIZ, "sitio")))
threading.Thread(target=srv.serve_forever, daemon=True).start()
env = dict(os.environ, CHROME_PATH=os.environ.get("CHROME_PATH", "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"))
for ruta in a.rutas:
    r = []
    for i in range(a.veces):
        out = f"/tmp/lh-v2-{i}.json"
        subprocess.run(["npx", "--no-install", "lighthouse", f"http://127.0.0.1:{a.puerto}{ruta}", "--quiet", "--form-factor=mobile",
                        "--chrome-flags=--headless=new --no-sandbox", "--output=json", f"--output-path={out}"],
                       env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=240)
        r.append(json.load(open(out)))
    cat = lambda k: [round(x["categories"][k]["score"] * 100) for x in r]
    aud = lambda k: [x["audits"][k]["numericValue"] for x in r]
    print(f"{ruta}  rendimiento {statistics.median(cat('performance'))} ({'/'.join(map(str, cat('performance')))})"
          f" · accesibilidad {statistics.median(cat('accessibility'))} · SEO {statistics.median(cat('seo'))}"
          f" · FCP {statistics.median(aud('first-contentful-paint'))/1000:.1f} s · LCP {statistics.median(aud('largest-contentful-paint'))/1000:.1f} s"
          f" · TBT {statistics.median(aud('total-blocking-time')):.0f} ms · CLS {statistics.median(aud('cumulative-layout-shift')):.3f}")
    x = r[-1]
    fallos = [f"{k}: {v['title']}" for k, v in x["audits"].items() if v.get("score") is not None and v["score"] < .9
              and v.get("scoreDisplayMode") in ("binary", "numeric", "metricSavings") and k not in ("uses-text-compression",)]
    for f in fallos[:14]:
        print("   ·", f)
srv.shutdown()
