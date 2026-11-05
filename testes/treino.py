"""Primeiros minutos (v0.13, com o passo do especial da v0.14): oferta e passos do treino guiado, nome do lance no gol,
resumo da partida, pausa com controles, opinião, estreia fácil na carreira e o painel
do treino no celular. Salva capturas em testes/capturas/.

Uso:  python testes/treino.py
"""
from comum import Checagens, abrir, pasta_capturas, sync_playwright, tela

C = Checagens("Treino guiado, nome do lance, resumo, pausa e opinião")
cap = pasta_capturas()
erros_todos = []


def esperar(pg, expr, ms=4000):
    """Espera até a expressão JS ficar verdadeira (ou estourar o tempo)."""
    t = 0
    while t < ms:
        if pg.evaluate(expr):
            return True
        pg.wait_for_timeout(50)
        t += 50
    return False


PASSO = "(__arena.G.train&&__arena.TRAIN[__arena.G.train.i]||{}).id"


def passo(pg):
    return pg.evaluate(PASSO)


def ir_para(pg, ident):
    return esperar(pg, PASSO + "==='" + ident + "'", 4000)


def menu_idx(pg, ident):
    return pg.evaluate("__arena.MENU.findIndex(m=>m.id==='%s')" % ident)


def prender_bola_no_pe(pg, ar=False):
    """Bola parada na frente do pé até o chute (como no teste de física)."""
    pg.evaluate("""(ar)=>{const A=__arena,p=A.P[0];
      if(A.G.train){ A.G.train.hold=null; A.G.train.again=0; } A.G.freezeBall=false;
      p.kickT=-1; p.kickHit=false; p.ctrlT=-1; p.poseT=-1; p.face=1;
      if(ar){ p.y=A.GROUND_Y-90; p.vy=-200; p.onGround=false; } else { p.y=A.GROUND_Y; p.vy=0; p.onGround=true; }
      const t0=performance.now();
      (function rec(){ const A=__arena,b=A.ball,p=A.P[0];
        if(!p.kickHit){ b.x=p.x+40; b.y=p.y-20; b.vx=0; b.vy=0; b.spin=0; b.curve=0; }
        if(!p.kickHit&&performance.now()-t0<1500) requestAnimationFrame(rec); })();
    }""", ar)


def dominio_perfeito(pg):
    """Bola caindo no peito com a janela do domínio recém-aberta: sai perfeito."""
    pg.evaluate("""(()=>{const A=__arena,p=A.P[0];
      if(A.G.train){ A.G.train.hold=null; A.G.train.again=0; } A.G.freezeBall=false;
      p.y=A.GROUND_Y; p.vx=0; p.vy=0; p.onGround=true; p.face=1; p.kickT=-1; p.ctrlT=0; p.ctrlCd=0; p.ctrlGrace=0; p.poseT=-1; p.boostT=0;
      const b=A.ball; b.x=p.x+22; b.y=505; b.vx=-30; b.vy=950; b.spin=0; b.curve=0;})()""")


def chute_do_campo(pg, x0):
    """Amistoso: voleio rasteiro da posição x0, com o adversário longe, atrás do jogador."""
    esperar(pg, "__arena.G.phase==='play'", 4000)
    pg.evaluate("""(x0)=>{const A=__arena,p=A.P[0]; A.P[1].ai=null; A.P[1].x=150; A.P[1].vx=0; p.x=x0; p.vx=0;}""", x0)
    prender_bola_no_pe(pg)
    pg.keyboard.press("KeyG")
    gol = esperar(pg, "__arena.G.phase==='goal'", 3000)
    pg.wait_for_timeout(300)
    b = pg.evaluate("__arena.G.banner&&{text:__arena.G.banner.text,kind:__arena.G.banner.kind}")
    return gol, b


with sync_playwright() as pw:
    nav = pw.chromium.launch()

    # ---------- treino completo no computador ----------
    pg, ctx, erros = abrir(nav, limpar_save=True, treino_visto=False)
    pg.screenshot(path=str(cap / "menu.png"))
    pg.evaluate("__arena.G.menuIdx=1"); pg.keyboard.press("Enter"); pg.wait_for_timeout(300)
    C.ok("primeira partida oferece o treino", tela(pg) == "askTrain", tela(pg))
    pg.screenshot(path=str(cap / "treino_oferta.png"))
    pg.click("[data-act=trainGo]"); pg.wait_for_timeout(300)
    C.ok("treino começa no passo 'andar', sem adversário em campo",
         passo(pg) == "andar" and pg.evaluate("__arena.P[1].ghost===true"), passo(pg))
    pg.screenshot(path=str(cap / "treino_andar.png"))

    pg.keyboard.down("KeyD"); esperar(pg, "__arena.G.train.n>=1", 3000); pg.keyboard.up("KeyD")
    pg.keyboard.down("KeyA"); ok = ir_para(pg, "pique"); pg.keyboard.up("KeyA")
    C.ok("andar até as duas marcas passa para o pique", ok, passo(pg))

    pg.keyboard.down("ShiftLeft"); pg.keyboard.down("KeyD"); pg.wait_for_timeout(1300)
    pg.keyboard.up("KeyD"); pg.keyboard.up("ShiftLeft")
    C.ok("pique de quase 1 s passa para a cabeçada", ir_para(pg, "cabeca"), passo(pg))

    pg.wait_for_timeout(700)
    pg.screenshot(path=str(cap / "treino_cabecada.png"))
    C.ok("três cabeçadas na bola que cai passam para a cavadinha", esperar(pg, PASSO + "==='cava'", 12000), passo(pg))

    pg.wait_for_timeout(200)
    pg.keyboard.press("KeyF")
    gol = esperar(pg, "__arena.G.phase==='goal'", 5000)
    pg.wait_for_timeout(250)
    pg.screenshot(path=str(cap / "treino_gol_cavadinha.png"))
    kind = pg.evaluate("(__arena.G.banner||{}).kind")
    C.ok("cavadinha parada vira gol de cavadinha", gol and kind and kind.startswith("DE CAVADINHA"), kind)
    C.ok("gol de cavadinha passa para o voleio", ir_para(pg, "voleio"), passo(pg))

    pg.wait_for_timeout(200)
    pg.keyboard.press("KeyG")
    gol = esperar(pg, "__arena.G.phase==='goal'", 5000)
    C.ok("voleio parado vira gol de voleio", gol and (pg.evaluate("(__arena.G.banner||{}).kind") or "").startswith("DE VOLEIO"),
         pg.evaluate("(__arena.G.banner||{}).kind"))
    C.ok("gol de voleio passa para o voleio no ar", ir_para(pg, "voleioAr"), passo(pg))

    pg.wait_for_timeout(300)
    prender_bola_no_pe(pg, ar=False)
    pg.keyboard.press("KeyG"); pg.wait_for_timeout(250)
    C.ok("voleio no chão não vale no passo do voleio no ar (e explica)",
         passo(pg) == "voleioAr" and "ar" in (pg.evaluate("__arena.G.train.msg") or ""), pg.evaluate("__arena.G.train.msg"))
    pg.wait_for_timeout(500)
    esperar(pg, "__arena.G.phase==='play'", 3000)   # o voleio no chão pode ter virado gol
    prender_bola_no_pe(pg, ar=True)
    pg.keyboard.press("KeyG")
    C.ok("voleio no ar passa para o domínio", ir_para(pg, "dominio"), passo(pg))

    # o passe do "treinador" precisa chegar no jogador
    esperar(pg, "__arena.G.train.hold===null&&__arena.G.freezeBall===false", 2500)
    pg.evaluate("""(()=>{window.__pd=1e9; const t0=performance.now();
      (function rec(){ const A=__arena,b=A.ball,p=A.P[0]; const d=Math.hypot(b.x-p.x,b.y-(p.y-A.T.headR-16));
        window.__pd=Math.min(window.__pd,d); if(performance.now()-t0<1700) requestAnimationFrame(rec); })();})()""")
    pg.wait_for_timeout(1800)
    pd = pg.evaluate("window.__pd")
    alcance = pg.evaluate("__arena.T.headR+__arena.T.ballR+40")
    C.ok("passe do treino chega no jogador", pd < alcance, "%d px (limite %d)" % (pd, alcance))
    pg.screenshot(path=str(cap / "treino_dominio.png"))

    for _ in range(2):
        pg.wait_for_timeout(200)
        dominio_perfeito(pg)
        pg.wait_for_timeout(400)
    C.ok("dois domínios passam para o voleio embalado", ir_para(pg, "embalado"), passo(pg))

    pg.wait_for_timeout(300)
    dominio_perfeito(pg); pg.wait_for_timeout(150)
    boost = pg.evaluate("__arena.P[0].boostT")
    prender_bola_no_pe(pg)
    pg.keyboard.press("KeyG"); pg.wait_for_timeout(200)
    C.ok("domínio perfeito + voleio embalado passa para o especial", boost > 0 and ir_para(pg, "especial"), {"boostT": boost, "passo": passo(pg)})
    pg.wait_for_timeout(400)
    C.ok("passo do especial começa com a barra cheia e a bola no pé", pg.evaluate("__arena.P[0].power===1&&__arena.P[0].special==='folha'"))
    pg.screenshot(path=str(cap / "treino_especial.png"))
    pg.keyboard.press("Space")
    C.ok("folha seca no gol fecha o treino", esperar(pg, "__arena.UI.screen==='trainDone'", 7000), tela(pg))
    C.ok("treino completo fica registrado no salvamento", pg.evaluate("__arena.SAVE.profile.tut") == 2)
    pg.screenshot(path=str(cap / "treino_fim.png"))

    # pular todos os passos com Enter
    pg.click("[data-act=trainAgain]"); pg.wait_for_timeout(300)
    for _ in range(pg.evaluate("__arena.TRAIN.length")):
        pg.keyboard.press("Enter"); pg.wait_for_timeout(120)
    C.ok("Enter pula os passos do treino até o fim", esperar(pg, "__arena.UI.screen==='trainDone'", 2000), tela(pg))

    # ---------- amistoso: nome do lance e resumo ----------
    pg.click("[data-act=goFriendly]"); pg.wait_for_timeout(300)
    lances = {}
    for x0, nome in [(1500, "perto"), (1100, "longe"), (840, "meio")]:
        gol, b = chute_do_campo(pg, x0)
        lances[nome] = b
        if nome != "perto":
            pg.screenshot(path=str(cap / ("gol_%s.png" % nome)))
    C.dados["lances"] = lances
    C.ok("voleio de perto: 'GOL!' e 'DE VOLEIO'", lances["perto"] == {"text": "GOL!", "kind": "DE VOLEIO"}, lances["perto"])
    C.ok("voleio de longe: 'DE VOLEIO · DE LONGE'", (lances["longe"] or {}).get("kind") == "DE VOLEIO · DE LONGE", lances["longe"])
    C.ok("voleio do próprio campo: 'GOLAÇO!' e 'DO MEIO-CAMPO'",
         (lances["meio"] or {}).get("text") == "GOLAÇO!" and "DO MEIO-CAMPO" in ((lances["meio"] or {}).get("kind") or ""), lances["meio"])

    esperar(pg, "__arena.G.phase==='play'", 4000)
    pg.evaluate("(()=>{const A=__arena; A.G.clockOn=true; A.G.clock=0.2;})()")
    esperar(pg, "__arena.G.phase==='fulltime'", 2000); pg.wait_for_timeout(400)
    st = pg.evaluate("__arena.matchStats()")
    C.dados["resumo"] = st
    C.ok("resumo conta chutes, chute mais forte e posse que soma 100%",
         st["shots"][0] >= 3 and st["top"][0] > 50 and sum(st["poss"]) == 100 and len(st["goals"]) == 3, st)
    pg.screenshot(path=str(cap / "fim_de_jogo_resumo.png"))

    # ---------- pausa com controles ----------
    pg.keyboard.press("KeyR"); pg.wait_for_timeout(1300)
    pg.keyboard.press("Escape"); pg.wait_for_timeout(200)
    C.ok("Esc pausa o amistoso", pg.evaluate("__arena.G.paused"))
    pg.screenshot(path=str(cap / "pausa.png"))
    pg.keyboard.press("Escape"); pg.wait_for_timeout(100)

    # ---------- opinião ----------
    pg.click("#btnMenu"); pg.wait_for_timeout(200)
    pg.evaluate("__arena.G.menuIdx=%d" % menu_idx(pg, "feedback")); pg.keyboard.press("Enter"); pg.wait_for_timeout(300)
    C.ok("menu 'Mandar opinião' abre a tela de opinião", tela(pg) == "feedback", tela(pg))
    pg.fill("#fbtxt", "Achei muito bom, mas o voleio no ar é difícil.")
    txt = pg.evaluate("__arena.fbText()")
    versao = pg.evaluate("(document.querySelector('.tagline').textContent.match(/v\\d+\\.\\d+/)||[''])[0]")
    C.dados["texto_opiniao"] = txt
    C.ok("texto da opinião leva comentário, versão (a mesma da tagline), aparelho e última partida",
         versao and "voleio no ar" in txt and versao in txt and "Aparelho: computador" in txt and "Última partida:" in txt, (versao, txt))
    pg.screenshot(path=str(cap / "opiniao.png"))
    pg.click("[data-act=back]"); pg.wait_for_timeout(200)
    C.ok("voltar da opinião leva ao menu", pg.evaluate("__arena.G.mode") == "menu" and tela(pg) is None)
    erros_todos += erros
    ctx.close()

    # ---------- carreira: estreia fácil e resumo no resultado ----------
    pg, ctx, erros = abrir(nav, limpar_save=True)
    pg.evaluate("__arena.G.menuIdx=0"); pg.keyboard.press("Enter"); pg.wait_for_timeout(200)
    pg.click("[data-act=create]"); pg.wait_for_timeout(100); pg.click("[data-act=hub]"); pg.wait_for_timeout(100)
    pg.screenshot(path=str(cap / "carreira_tabela_dica.png"))
    pg.click("[data-act=play]"); pg.wait_for_timeout(600)
    est = pg.evaluate("""(()=>{const A=__arena,S=A.SAVE.career.season; const o=S.teams.filter(t=>t.id!=='me').map(t=>t.skill);
      return {skill:A.P[1].ai.skill,menor:Math.min(...o)};})()""")
    C.ok("estreia da carreira é contra o adversário mais fraco", abs(est["skill"] - est["menor"]) < 1e-9, est)
    pg.evaluate("__arena.finish(2,1)"); pg.wait_for_timeout(300)
    C.ok("resultado da carreira mostra o resumo e o botão de opinião",
         pg.query_selector(".ms") is not None and pg.query_selector("[data-act=feedback]") is not None)
    pg.screenshot(path=str(cap / "carreira_resultado.png"))
    pg.click("[data-act=feedback]"); pg.wait_for_timeout(150); pg.click("[data-act=back]"); pg.wait_for_timeout(150)
    C.ok("opinião aberta do resultado volta para o resultado", tela(pg) == "result", tela(pg))
    erros_todos += erros
    ctx.close()

    # ---------- celular: painel do treino, "pular" por toque e pausa ----------
    pg, ctx, erros = abrir(nav, 844, 390, toque=True)
    pg.screenshot(path=str(cap / "menu_celular.png"))
    pg.evaluate("__arena.G.menuIdx=%d" % menu_idx(pg, "train")); pg.keyboard.press("Enter"); pg.wait_for_timeout(500)
    pg.screenshot(path=str(cap / "treino_celular.png"))
    pos = pg.evaluate("""(()=>{const A=__arena,r=document.getElementById('cv').getBoundingClientRect(),q=A.G.train.pill;
      const sx=r.width/A.W, sy=r.height/(810+A.EXT_TOP+A.EXT);
      return [r.left+(q.x0+q.x1)/2*sx, r.top+((q.y0+q.y1)/2+A.EXT_TOP)*sy];})()""")
    pg.touchscreen.tap(pos[0], pos[1]); pg.wait_for_timeout(200)
    C.ok("no celular, tocar em 'pular' avança o passo", passo(pg) == "pique", passo(pg))
    pg.click("#tPause"); pg.wait_for_timeout(200)
    pg.screenshot(path=str(cap / "pausa_celular.png"))
    C.ok("botão de pausa pausa o treino", pg.evaluate("__arena.G.paused"))
    erros_todos += erros
    ctx.close()
    nav.close()

C.fim(erros_todos)
