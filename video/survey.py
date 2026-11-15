from playwright.sync_api import sync_playwright
pages={"home":"/","n3l":"/problems/no-three-in-line-75","tdc":"/problems/two-deletion-code-16","decisions":"/decisions","memory":"/memory","literature":"/literature","learning":"/learning","gallery":"/gallery"}
with sync_playwright() as p:
    b=p.chromium.launch()
    c=b.new_context(viewport={"width":1920,"height":1080})
    for k,u in pages.items():
        pg=c.new_page(); pg.goto("http://127.0.0.1:8787"+u); pg.wait_for_timeout(5000)
        h=pg.evaluate("document.documentElement.scrollHeight")
        pg.screenshot(path=f"survey/{k}.png")
        open(f"survey/{k}.txt","w").write(pg.inner_text("body"))
        print(k,h,len(pg.inner_text("body")))
        pg.close()
    b.close()
