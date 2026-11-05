"""Carreira e vestiário: percorre a carreira inteira, testa empate, eliminação, abandono,
compras no vestiário, salvamento após recarregar e o amistoso com morte súbita.

Uso:  python testes/carreira.py
"""
from comum import Checagens, abrir, pasta_capturas, sync_playwright, tela

C = Checagens("Carreira e vestiário")
erros_todos = []

with sync_playwright() as pw:
    nav = pw.chromium.launch()
    pg, ctx, erros = abrir(nav, limpar_save=True)
    cap = pasta_capturas()

    # criação do jogador
    pg.evaluate("__arena.G.menuIdx=0")
    pg.keyboard.press("Enter"); pg.wait_for_timeout(300)
    C.ok("menu Carreira abre a criação do jogador", tela(pg) == "create", tela(pg))
    pg.click('[data-act=look][data-arg="hair:raspado"]'); pg.wait_for_timeout(100)
    pg.fill("#pname", "Teste"); pg.wait_for_timeout(100)
    pg.screenshot(path=str(cap / "carreira_criacao.png"))
    pg.click("[data-act=create]"); pg.wait_for_timeout(200)
    C.ok("criar leva à apresentação da temporada", tela(pg) == "intro", tela(pg))
    pg.click("[data-act=hub]"); pg.wait_for_timeout(200)
    pg.screenshot(path=str(cap / "carreira_tabela.png"))

    # primeira partida de verdade
    pg.click("[data-act=play]"); pg.wait_for_timeout(1500)
    em_jogo = pg.evaluate("({mode:__arena.G.mode,career:!!__arena.G.career,label:__arena.MC.label,skill:__arena.P[1].ai.skill})")
    C.dados["primeira_partida"] = em_jogo
    C.ok("partida da carreira começa com rótulo da competição", em_jogo["mode"] == "match" and em_jogo["career"] and "COPA DA VILA" in em_jogo["label"])
    pg.screenshot(path=str(cap / "carreira_partida.png"))
    pg.evaluate("__arena.finish(2,1)"); pg.wait_for_timeout(300)
    C.ok("fim da partida mostra o resultado", tela(pg) == "result", tela(pg))

    # carreira inteira vencendo tudo por 3 a 1
    jogadas, temporadas, guarda = 1, [], 0
    while guarda < 400:
        guarda += 1
        s = tela(pg)
        if s == "result":
            pg.click("[data-act=after]")
        elif s == "hub":
            if pg.query_selector("[data-act=play]"):
                pg.click("[data-act=play]"); pg.wait_for_timeout(150)
                pg.evaluate("__arena.finish(3,1)"); jogadas += 1
            elif pg.query_selector("[data-act=offers]"):
                pg.click("[data-act=offers]")
            elif pg.query_selector("[data-act=final]"):
                pg.click("[data-act=final]")
            else:
                break
        elif s == "season":
            temporadas.append(pg.evaluate("__arena.SAVE.career.season.status+':'+__arena.SAVE.career.season.tier"))
            if pg.query_selector("[data-act=offers]"):
                pg.click("[data-act=offers]")
            elif pg.query_selector("[data-act=final]"):
                pg.click("[data-act=final]")
            else:
                pg.click("[data-act=retry]")
        elif s == "offers":
            if len(temporadas) == 1:
                pg.screenshot(path=str(cap / "carreira_propostas.png"))
            pg.click('[data-act=sign][data-arg="1"]')
        elif s == "intro":
            pg.click("[data-act=hub]")
        elif s == "final":
            pg.screenshot(path=str(cap / "carreira_campeao.png"))
            break
        else:
            C.ok("tela inesperada durante a carreira", False, s)
            break
        pg.wait_for_timeout(60)
    sv = pg.evaluate("__arena.SAVE")
    C.dados["partidas_ate_o_titulo"] = jogadas
    C.dados["temporadas"] = temporadas
    C.dados["moedas"] = sv["profile"]["coins"]
    C.ok("carreira completa tem 27 partidas", jogadas == 27, jogadas)
    C.ok("cinco títulos, terminando na Liga Suprema",
         [t["comp"] for t in sv["career"]["titles"]] == ["Copa da Vila", "Copa Regional", "Segunda Divisão", "Primeira Divisão", "Liga Suprema"])
    C.ok("títulos liberam faixa de capitão e chuteira dourada",
         "capitao" in sv["profile"]["owned"].get("band", []) and "dourada" in sv["profile"]["owned"].get("boot", []))

    # vestiário: compra e equipa
    pg.click("[data-act=locker]"); pg.wait_for_timeout(200)
    for aba, item in [("hair", "black"), ("hairCol", "ruivo"), ("face", "barba"), ("extra", "oculos"),
                      ("boot", "dourada"), ("band", "capitao"), ("trail", "arco")]:
        pg.click('[data-act=tab][data-arg="%s"]' % aba); pg.wait_for_timeout(60)
        sel = '[data-act=item][data-arg="%s:%s"]' % (aba, item)
        pg.click(sel); pg.wait_for_timeout(60)
        if pg.evaluate("__arena.UI.ask") == "%s:%s" % (aba, item):
            pg.click(sel); pg.wait_for_timeout(60)
    pg.wait_for_timeout(300)
    look = pg.evaluate("__arena.SAVE.profile.look")
    pg.screenshot(path=str(cap / "vestiario.png"))
    C.ok("itens comprados ficam equipados",
         look["hair"] == "black" and look["face"] == "barba" and look["boot"] == "dourada" and look["trail"] == "arco", look)

    # salvamento sobrevive ao recarregar
    pg.reload(); pg.wait_for_timeout(900)
    rec = pg.evaluate("({nome:__arena.SAVE.profile.name,campeao:!!(__arena.SAVE.career&&__arena.SAVE.career.champion)})")
    C.ok("salvamento local volta depois de recarregar", rec["nome"] == "Teste" and rec["campeao"], rec)
    erros_todos += erros
    ctx.close()

    # empate na tabela, eliminação, abandono e amistoso
    pg, ctx, erros = abrir(nav, limpar_save=True)
    pg.evaluate("__arena.G.menuIdx=0"); pg.keyboard.press("Enter"); pg.wait_for_timeout(200)
    pg.click("[data-act=create]"); pg.wait_for_timeout(100); pg.click("[data-act=hub]"); pg.wait_for_timeout(100)
    pg.click("[data-act=play]"); pg.wait_for_timeout(300)
    pg.evaluate("(()=>{const A=__arena; A.P[1].ai=null; A.P[1].x=1500;})()")
    pg.wait_for_timeout(1300)
    pg.evaluate("(()=>{const A=__arena; A.G.clockOn=true; A.G.clock=0.3; A.G.score=[1,1];})()")
    pg.wait_for_timeout(3600)
    me = pg.evaluate("__arena.SAVE.career.season.table.me")
    C.ok("empate no tempo normal vale 1 ponto na fase de pontos", tela(pg) == "result" and me["p"] == 1 and me["e"] == 1, me)
    pg.click("[data-act=after]"); pg.wait_for_timeout(100)
    for _ in range(2):
        pg.click("[data-act=play]"); pg.wait_for_timeout(150); pg.evaluate("__arena.finish(0,2)"); pg.wait_for_timeout(100)
        pg.click("[data-act=after]"); pg.wait_for_timeout(100)
    st = pg.evaluate("__arena.SAVE.career.season.status")
    C.ok("fora da zona de classificação, temporada termina eliminada", tela(pg) == "season" and st == "eliminado", st)
    pg.click("[data-act=retry]"); pg.wait_for_timeout(100); pg.click("[data-act=hub]"); pg.wait_for_timeout(100)
    nova = pg.evaluate("({no:__arena.SAVE.career.season.no,round:__arena.SAVE.career.season.round})")
    C.ok("eliminado recomeça a temporada do mesmo degrau", nova["no"] == 2 and nova["round"] == 0, nova)
    pg.click("[data-act=play]"); pg.wait_for_timeout(1500)
    pg.keyboard.press("Escape"); pg.wait_for_timeout(100); pg.keyboard.press("KeyQ"); pg.wait_for_timeout(150)
    C.ok("Esc + Q pede confirmação para abandonar", tela(pg) == "abandon", tela(pg))
    pg.click("[data-act=doAbandon]"); pg.wait_for_timeout(200)
    me = pg.evaluate("__arena.SAVE.career.season.table.me")
    C.ok("abandono conta como derrota por 3 a 0", me["d"] == 1 and me["gc"] == 3, me)
    pg.click("[data-act=after]"); pg.wait_for_timeout(100)
    pg.click("[data-act=menu]"); pg.wait_for_timeout(200)
    pg.evaluate("__arena.G.menuIdx=1"); pg.keyboard.press("Enter"); pg.wait_for_timeout(1500)
    pg.evaluate("(()=>{const A=__arena; A.G.clockOn=true; A.G.clock=0.2; A.G.score=[0,0];})()"); pg.wait_for_timeout(600)
    am = pg.evaluate("({career:__arena.G.career,golden:__arena.G.golden})")
    C.ok("amistoso empatado vai para a morte súbita", am["career"] is None and am["golden"], am)
    erros_todos += erros
    ctx.close()
    nav.close()

C.fim(erros_todos)
