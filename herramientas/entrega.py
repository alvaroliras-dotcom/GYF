#!/usr/bin/env python3
"""Prepara la entrega de una versión en 08-WEB, como dice el protocolo (paso 27).

Crea en la carpeta de salida:
  <cliente>/        copia completa del repositorio, con sitio/ partido en TANDA-n/sitio/ (<= 95 archivos)
  vN-CAMBIOS/       solo los archivos que cambian desde el commit indicado, con el árbol del repo.
                    Si pasan de 95, se parte en TANDA-1 (código) y TANDA-2.. (sitio).
  LEEME.txt         el orden de arrastre para subirlo por la web de GitHub.

Uso:
  python3 entrega.py --repo /ruta/al/repo --cliente <cliente> --version 2 --desde <commit> --salida /ruta/08-WEB
  (--desde: el último commit que Álvaro confirmó subido; si hay duda, uno anterior: es un superconjunto seguro)

GitHub web no sube archivos que empiezan por punto (.htaccess, .gitignore): se copian igual, pero
el .htaccess va al hosting a mano el día de publicar.
"""
import argparse, os, shutil, subprocess

MAX = 95


def git(repo, *a):
    return subprocess.run(["git", "-C", repo, *a], capture_output=True, text=True, check=True).stdout


def trozos(lista, n=MAX):
    return [lista[i:i + n] for i in range(0, len(lista), n)]


def copia(repo, rel, destino):
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    shutil.copy2(os.path.join(repo, rel), destino)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--cliente", required=True)
    ap.add_argument("--version", required=True)
    ap.add_argument("--desde", required=True, help="commit de la última versión subida")
    ap.add_argument("--salida", required=True, help="carpeta 08-WEB (se crea si no existe)")
    a = ap.parse_args()
    repo, sal = os.path.abspath(a.repo), os.path.abspath(a.salida)

    # 1. Copia completa, con sitio/ en tandas
    todos = [f for f in git(repo, "ls-files", "-co", "--exclude-standard").splitlines() if f and "__pycache__" not in f]
    comp = os.path.join(sal, a.cliente)
    if os.path.exists(comp):
        shutil.rmtree(comp)
    sitio = sorted(f for f in todos if f.startswith("sitio/"))
    # los archivos con punto no los lista git si están ignorados; se añaden a mano
    for r, _, fs in os.walk(os.path.join(repo, "sitio")):
        for f in fs:
            rel = os.path.relpath(os.path.join(r, f), repo)
            if rel not in sitio:
                sitio.append(rel)
    sitio.sort()
    for f in todos:
        if not f.startswith("sitio/"):
            copia(repo, f, os.path.join(comp, f))
    for i, t in enumerate(trozos(sitio), 1):
        for f in t:
            copia(repo, f, os.path.join(comp, "sitio", f"TANDA-{i}", f))
    n_tandas = len(trozos(sitio))

    # 2. Solo lo que cambia
    cambios = [f for f in git(repo, "diff", "--name-only", a.desde, "HEAD").splitlines()
               if f and os.path.exists(os.path.join(repo, f))]
    dv = os.path.join(sal, f"v{a.version}-CAMBIOS")
    if os.path.exists(dv):
        shutil.rmtree(dv)
    codigo = [f for f in cambios if not f.startswith("sitio/")]
    web = [f for f in cambios if f.startswith("sitio/")]
    if len(cambios) <= MAX:
        grupos = [("", cambios)]
    else:
        grupos = [(f"TANDA-{i}", g) for i, g in enumerate(trozos(codigo) + trozos(web), 1) if g]
    for nombre, g in grupos:
        for f in g:
            copia(repo, f, os.path.join(dv, nombre, f))

    # 3. LEEME
    lineas = [f"08-WEB · {a.cliente.upper()} · v{a.version}", "",
              f"{a.cliente}/   El repositorio completo y al día. sitio/ va partido en TANDA-1..{n_tandas}.",
              f"v{a.version}-CAMBIOS/   {len(cambios)} archivos que cambian desde la versión anterior.", "",
              "CÓMO SUBIRLO A GITHUB (página principal del repositorio > Add file > Upload files):"]
    for nombre, g in grupos:
        base = os.path.join(dv, nombre)
        carpetas = sorted({f.split("/")[0] for f in g})
        donde = f"v{a.version}-CAMBIOS/{nombre}" if nombre else f"v{a.version}-CAMBIOS"
        lineas.append(f"  - Abre {donde}, selecciona sus carpetas ({', '.join(carpetas)}), arrástralas juntas y Commit changes.")
    lineas += ["", "GitHub no sube los archivos que empiezan por punto (.htaccess): van al hosting el día de publicar."]
    open(os.path.join(sal, "LEEME.txt"), "w", encoding="utf-8").write("\n".join(lineas) + "\n")
    print(f"Copia completa: {len(todos)} archivos ({n_tandas} tandas de sitio) · v{a.version}-CAMBIOS: {len(cambios)} archivos en {len(grupos)} subida(s)")


if __name__ == "__main__":
    main()
