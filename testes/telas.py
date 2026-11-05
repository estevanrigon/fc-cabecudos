"""Telas: tela cheia sem distorção (16:9, 16:10, 21:9), toque no celular e no tablet,
versão pública sem painel e custo de desenho. Salva capturas em testes/capturas/.

Uso:  python testes/telas.py
"""
from comum import Checagens, abrir, iniciar_amistoso, pasta_capturas, sync_playwright

C = Checagens("Telas: tela cheia, toque e versão pública")
erros_todos = []
cap = pasta_capturas()

GEO = """(()=>{const A=__arena; const cv=document.getElementById('cv').getBoundingClientRect();
  const s=cv.width/A.W, chao=cv.top+(A.EXT_TOP+A.GROUND_Y)*s;
  const pad=document.getElementById('pad');
  const ctr=[...pad.querySelectorAll('.acts button, .stick')].map(b=>b.getBoundingClientRect().top);
  return {imm:document.body.classList.contains('imm'), modo:A.G.mode, ext_top:A.EXT_TOP, ext:A.EXT,
    folga_controles_px:ctr.length?Math.round(Math.min(...ctr)-chao):null};})()"""

with sync_playwright() as pw:
    nav = pw.chromium.launch()

    # tela cheia em três formatos de monitor
    for nome, (w, h) in [("16x9", (1920, 1080)), ("16x10", (1920, 1200)), ("21x9", (2560, 1080))]:
        pg, ctx, erros = abrir(nav, w, h)
        iniciar_amistoso(pg, cpu_parada=False)
        pg.keyboard.press("Digit2"); pg.wait_for_timeout(800)
        r = pg.evaluate("""(()=>{const c=document.getElementById('cv').getBoundingClientRect(); const A=__arena;
          return {cheia:!!document.fullscreenElement, css:[Math.round(c.width),Math.round(c.height)], ext_top:A.EXT_TOP, ext:A.EXT,
                  escala_x:c.width/A.W, escala_y:c.height/(810+A.EXT_TOP+A.EXT)};})()""")
        C.dados["tela_cheia_" + nome] = r
        C.ok("tela cheia %s sem distorção" % nome, r["cheia"] and abs(r["escala_x"] - r["escala_y"]) < 0.005, r)
        if nome == "16x9":
            C.ok("em 16:9 o placar ganha faixa própria acima do campo", r["ext_top"] >= 90, r["ext_top"])
            pg.keyboard.press("Digit3"); pg.wait_for_timeout(1200)
            custo = pg.evaluate("__arena.renderCost(30)")
            C.dados["custo_desenho_ms_1080p_cpu"] = round(custo, 2)
            C.ok("desenho cabe folgado num quadro de 120 Hz (CPU)", custo < 8.3, round(custo, 2))
        pg.screenshot(path=str(cap / ("tela_cheia_%s.png" % nome)))
        erros_todos += erros
        ctx.close()

    # toque: celular deitado, tablet e celular em pé
    for nome, (w, h) in [("celular", (844, 390)), ("tablet", (1180, 820)), ("celular_em_pe", (390, 844))]:
        pg, ctx, erros = abrir(nav, w, h, toque=True)
        if nome != "celular_em_pe":
            iniciar_amistoso(pg, cpu_parada=False)
            g = pg.evaluate(GEO)
            C.dados["toque_" + nome] = g
            C.ok("%s: controles abaixo da linha do chão" % nome, g["imm"] and g["folga_controles_px"] is not None and g["folga_controles_px"] >= 0, g)
        else:
            vis = pg.evaluate("getComputedStyle(document.getElementById('rotate')).display")
            C.ok("celular em pé pede para girar o aparelho", vis != "none", vis)
        pg.screenshot(path=str(cap / ("toque_%s.png" % nome)))
        erros_todos += erros
        ctx.close()

    # pique pela trilha de toque (arrastar até a ponta) e pulo com o segundo dedo
    pg, ctx, erros = abrir(nav, 844, 390, toque=True)
    iniciar_amistoso(pg)
    cdp = ctx.new_cdp_session(pg)
    pg.evaluate("(()=>{const A=__arena; A.P[0].x=400; A.P[0].stam=1;})()")
    r = pg.evaluate("(()=>{const r=document.getElementById('stick').getBoundingClientRect(); return [r.left,r.top,r.width,r.height];})()")
    cx, cy = r[0] + r[2] / 2, r[1] + r[3] / 2
    cdp.send("Input.dispatchTouchEvent", {"type": "touchStart", "touchPoints": [{"x": cx, "y": cy, "id": 1}]})
    for i in range(1, 9):
        cdp.send("Input.dispatchTouchEvent", {"type": "touchMove", "touchPoints": [{"x": cx + 0.95 * (r[2] / 2) * i / 8, "y": cy, "id": 1}]})
        pg.wait_for_timeout(20)
    pg.wait_for_timeout(300)
    pq = pg.evaluate("({vx:Math.round(__arena.P[0].vx),pique:__arena.P[0].sprinting})")
    C.ok("trilha de toque: ponta ativa o pique", pq["pique"], pq)
    jb = pg.evaluate("(()=>{const r=document.querySelector('.acts button[data-k=KeyW]').getBoundingClientRect(); return [r.left+r.width/2,r.top+r.height/2];})()")
    cdp.send("Input.dispatchTouchEvent", {"type": "touchStart", "touchPoints": [{"x": cx + 0.95 * (r[2] / 2), "y": cy, "id": 1}, {"x": jb[0], "y": jb[1], "id": 2}]})
    pg.wait_for_timeout(120)
    C.ok("pula com o segundo dedo sem soltar o pique", pg.evaluate("!__arena.P[0].onGround"))
    cdp.send("Input.dispatchTouchEvent", {"type": "touchEnd", "touchPoints": []})
    erros_todos += erros
    ctx.close()

    # versão pública: painel some, botão alterna
    pg, ctx, erros = abrir(nav)
    C.ok("aberto localmente, o painel de ajuste aparece", pg.evaluate("getComputedStyle(document.getElementById('tuner')).display") != "none")
    pg.click("#btnView"); pg.wait_for_timeout(100)
    pub = pg.evaluate("({pub:document.body.classList.contains('pub'),painel:getComputedStyle(document.getElementById('tuner')).display})")
    C.ok("'Ver como jogador' esconde o painel", pub["pub"] and pub["painel"] == "none", pub)
    pg.screenshot(path=str(cap / "versao_publica.png"))
    erros_todos += erros
    ctx.close()
    nav.close()

C.fim(erros_todos)
