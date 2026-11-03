"""Render index.html at 390/700/930/1600, save PNGs to renders/, report overflow + broken images + tabs working."""
import pathlib, http.server, threading, socketserver, functools
from playwright.sync_api import sync_playwright
H=pathlib.Path(__file__).parent; (H/"renders").mkdir(exist_ok=True)
Handler=functools.partial(http.server.SimpleHTTPRequestHandler,directory=str(H))
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*a): pass
srv=socketserver.TCPServer(("127.0.0.1",0),functools.partial(Q,directory=str(H))); port=srv.server_address[1]
threading.Thread(target=srv.serve_forever,daemon=True).start()
with sync_playwright() as p:
    b=p.chromium.launch()
    for w in (390,700,930,1600):
        pg=b.new_page(viewport={"width":w,"height":900 if w>700 else 844},device_scale_factor=1)
        pg.goto(f"http://127.0.0.1:{port}/index.html",wait_until="networkidle")
        pg.evaluate("document.querySelectorAll('.reveal').forEach(e=>e.classList.add('in'))")
        info=pg.evaluate("""()=>{const sw=document.documentElement.scrollWidth,cw=document.documentElement.clientWidth;
          const over=[...document.querySelectorAll('body *')].filter(e=>{const r=e.getBoundingClientRect();return r.right>cw+1&&r.width>0}).slice(0,6).map(e=>e.tagName+'.'+e.className);
          const broken=[...document.images].filter(i=>i.complete&&i.naturalWidth===0).map(i=>i.src.split('/').pop());
          const h=document.documentElement.scrollHeight; return {sw,cw,over,broken,h}}""")
        pg.click('.tab[data-tab="tacos"]'); shown=pg.evaluate("[...document.querySelectorAll('.panel')].filter(p=>!p.hidden).map(p=>p.id)")
        pg.click('.tab[data-tab="entrees"]')
        pg.screenshot(path=str(H/f"renders/{w}.png"),full_page=True)
        print(w,info,"tabs->",shown)
    b.close()
