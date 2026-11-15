from playwright.sync_api import sync_playwright
shots=[("home","/",[700]),("n3l","/problems/no-three-in-line-75",[250,1100]),("tdc","/problems/two-deletion-code-16",[250]),("memory","/memory",[0,600]),("learning","/learning",[100]),("gallery","/gallery",[0,1500]),("d211","/decisions?agent=proposer&focus=211",[None]),("d219","/decisions?agent=referee&focus=219",[None]),("d120","/decisions?problem=no-three-in-line-75&focus=120",[None])]
with sync_playwright() as p:
    b=p.chromium.launch()
    c=b.new_context(viewport={"width":1920,"height":1080})
    for k,u,ys in shots:
        pg=c.new_page(); pg.goto("http://127.0.0.1:8787"+u); pg.wait_for_timeout(5000)
        info=pg.evaluate("""()=>{const out=[];for(const e of [document.scrollingElement,...document.querySelectorAll('main,div')]){if(e.scrollHeight>e.clientHeight+50&&['auto','scroll'].includes(getComputedStyle(e).overflowY)||e===document.scrollingElement)out.push([e.tagName,e.className.slice(0,40),e.scrollHeight,e.clientHeight,e.scrollTop])}return out.slice(0,5)}""")
        print(k,info, pg.evaluate("window.scrollY"))
        for y in ys:
            if y is not None: pg.evaluate(f"window.scrollTo(0,{y})"); pg.wait_for_timeout(1200)
            pg.screenshot(path=f"survey/{k}_{y}.jpg",quality=60,type="jpeg")
        pg.close()
    b.close()
