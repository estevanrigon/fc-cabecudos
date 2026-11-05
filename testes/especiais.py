"""Especiais (v0.14): barra (toques, domínio perfeito, gol sofrido, toques seguidos), armar sem a bola,
folha seca, bicicleta, caneta, muralha, CPU usando cada um, menu do amistoso, carreira (escolha na
criação, liberação por título, aba do vestiário, salvamento antigo), botão de toque e painel.

Uso:  python testes/especiais.py
"""
import json

from comum import Checagens, abrir, iniciar_amistoso, pasta_capturas, sync_playwright, tela

C = Checagens("Especiais: barra, folha seca, bicicleta, caneta, muralha, CPU e carreira")
cap = pasta_capturas()
erros_todos = []

# grava, a cada quadro, o que o teste precisa olhar (bola, jogadores, fase e letreiro)
GRAVAR = """(ms)=>{const log=[]; window.__g=log; const t0=performance.now();
  (function rec(){ const A=__arena,b=A.ball,p=A.P[0],q=A.P[1];
    log.push({t:Math.round(performance.now()-t0),bx:Math.round(b.x),by:Math.round(b.y),bv:Math.round(Math.hypot(b.vx,b.vy)),bvx:Math.round(b.vx),
      fx:b.fx?b.fx.id+(b.fx.drop?'+':''):'',fw:b.fx?b.fx.who:-1,fase:A.G.phase,kind:A.G.banner&&A.G.banner.kind||'',txt:A.G.banner&&A.G.banner.text||'',
      p0:{x:Math.round(p.x),y:Math.round(p.y),r:Math.round(A.rHead(p)),pw:+p.power.toFixed(3),arm:+p.armT.toFixed(2),spec:p.spec?p.spec.id:'',tonto:+p.dizzy.toFixed(2),mura:+p.muraT.toFixed(2)},
      p1:{x:Math.round(q.x),y:Math.round(q.y),r:Math.round(A.rHead(q)),pw:+q.power.toFixed(3),arm:+q.armT.toFixed(2),spec:q.spec?q.spec.id:'',tonto:+q.dizzy.toFixed(2),mura:+q.muraT.toFixed(2)}});
    if(performance.now()-t0<ms) requestAnimationFrame(rec); })();}"""


def gravar(pg, ms):
    pg.evaluate(GRAVAR, ms)


def log(pg):
    return pg.evaluate("window.__g")


def montar(pg, js):
    """Arruma a cena: limpa estados do especial, põe os jogadores no chão e roda o trecho js."""
    pg.evaluate("""(js)=>{const A=__arena; A.G.phase='play'; A.G.freezeBall=false; A.G.banner=null; A.G.paused=false;
      for(const p of A.P){ p.y=A.GROUND_Y; p.vy=0; p.vx=0; p.onGround=true; p.kickT=-1; p.ctrlT=-1; p.poseT=-1; p.armT=0; p.spec=null;
        p.specCd=0; p.muraT=0; p.hrK=1; p.dizzy=0; p.streak=0; p.boostT=0; }
      const b=A.ball; b.vx=0; b.vy=0; b.spin=0; b.curve=0; b.fx=null; b.gScale=1; A.G.lastToucher=-1; A.G.caneta=0;
      (new Function('A',js))(A);}""", js)


def gol_pronto(pg, ms=2600):
    """Espera o fim do lance (gol ou bola parada) e devolve o que aconteceu."""
    pg.wait_for_timeout(ms)
    L = log(pg)
    g = next((r for r in L if r["fase"] == "goal" and r["txt"]), None)
    return L, g


with sync_playwright() as pw:
    nav = pw.chromium.launch()

    # ------------------------------------------------------------------ barra
    pg, ctx, erros = abrir(nav)
    iniciar_amistoso(pg)
    T = pg.evaluate("__arena.T")
    C.ok("partida começa com a barra vazia", pg.evaluate("__arena.P[0].power===0&&__arena.P[1].power===0"))

    def chute_seguido():
        """Voleio do jogador 1; logo depois a bola é parada longe, para não virar gol nem tocar em ninguém."""
        pg.evaluate("""(()=>{const A=__arena,p=A.P[0]; A.P[1].x=A.W-120; p.x=700; p.face=1; p.kickT=-1; p.y=A.GROUND_Y; p.vy=0; p.onGround=true;
          A.ball.x=740; A.ball.y=p.y-20; A.ball.vx=0; A.ball.vy=0; A.ball.fx=null;})()""")
        pg.keyboard.press("KeyG"); pg.wait_for_timeout(200)
        pg.evaluate("(()=>{const b=__arena.ball; b.vx=0; b.vy=0; b.x=1100; b.y=__arena.GROUND_Y-17;})()")
        pg.wait_for_timeout(250)
        return pg.evaluate("__arena.P[0].power")

    montar(pg, "A.P[0].power=0;")
    p1 = chute_seguido()
    C.ok("voleio enche a barra (specKick)", abs(p1 - T["specKick"]) < 1e-6, p1)
    p2 = chute_seguido()
    p3 = chute_seguido()
    C.dados["barra_toques_seguidos"] = [round(p1, 3), round(p2, 3), round(p3, 3)]
    C.ok("terceiro toque seguido do mesmo jogador vale menos (specStreak)",
         abs((p2 - p1) - T["specKick"]) < 1e-6 and abs((p3 - p2) - T["specKick"] * T["specStreak"]) < 1e-6, C.dados["barra_toques_seguidos"])

    # domínio perfeito
    pg.wait_for_timeout(800)
    pg.evaluate("""(()=>{const A=__arena; const p=A.P[0]; A.P[1].x=1600; p.x=700; p.y=A.GROUND_Y; p.vx=0; p.vy=0; p.onGround=true; p.power=0; p.streak=0; A.G.lastToucher=-1;
      p.kickT=-1; p.ctrlT=0; p.ctrlCd=0; p.ctrlGrace=0; p.poseT=-1; p.boostT=0;
      const b=A.ball; b.x=722; b.y=505; b.vx=-30; b.vy=950; b.spin=0; b.curve=0; b.fx=null;})()""")
    pg.wait_for_timeout(150)
    pp = pg.evaluate("__arena.P[0].power")
    C.ok("domínio perfeito enche mais (specPerf)", abs(pp - T["specPerf"]) < 1e-6, pp)

    # gol sofrido
    pg.wait_for_timeout(600)
    montar(pg, "A.P[0].power=0; A.P[0].x=700; A.P[1].x=1600; A.ball.x=36; A.ball.y=A.GROUND_Y-60; A.ball.vx=-200; A.ball.hit={who:1,kind:'voleio',x:900,post:false};")
    pg.wait_for_timeout(300)
    pg_ = pg.evaluate("({p:__arena.P[0].power,placar:__arena.G.score.slice()})")
    C.ok("quem sofre o gol ganha barra (specGoal)", abs(pg_["p"] - T["specGoal"]) < 1e-6 and pg_["placar"][1] >= 1, pg_)
    pg.wait_for_timeout(2600)

    # armar sem a bola: espera specArm e não perde a barra
    montar(pg, "A.P[0].special='folha'; A.P[0].power=1; A.P[0].x=400; A.P[1].x=A.W-120; A.ball.x=1500; A.ball.y=A.GROUND_Y-A.T.ballR;")
    pg.keyboard.press("Space"); pg.wait_for_timeout(150)
    a1 = pg.evaluate("__arena.P[0].armT")
    pg.wait_for_timeout(int(T["specArm"] * 1000) + 300)
    a2 = pg.evaluate("({arm:__arena.P[0].armT,pw:__arena.P[0].power,fx:!!__arena.ball.fx})")
    C.ok("Espaço com a barra cheia arma o especial", a1 > 0.5, a1)
    C.ok("sem a bola no ponto, desarma e a barra continua cheia", a2["arm"] == 0 and a2["pw"] == 1 and not a2["fx"], a2)

    # Espaço com um botão do topo em foco não aperta o botão
    som = pg.evaluate("__arena.Snd.get()")
    pg.evaluate("document.getElementById('btnSound').focus()")
    montar(pg, "A.P[0].power=1; A.ball.x=1500;")
    pg.keyboard.press("Space"); pg.wait_for_timeout(200)
    C.ok("Espaço com um botão em foco arma o especial sem mexer no botão",
         pg.evaluate("__arena.Snd.get()") == som and pg.evaluate("__arena.P[0].armT>0"), pg.evaluate("[__arena.Snd.get(),__arena.P[0].armT]"))
    pg.evaluate("document.activeElement&&document.activeElement.blur()")
    pg.wait_for_timeout(1800)

    # ------------------------------------------------------------------ folha seca
    montar(pg, "const p=A.P[0]; p.special='folha'; p.power=1; p.x=500; A.P[1].x=A.W-420; A.ball.x=560; A.ball.y=A.GROUND_Y-A.T.ballR;")
    gravar(pg, 3400)
    pg.keyboard.press("Space")
    pg.wait_for_function("__arena.ball.fx&&__arena.ball.fx.drop", timeout=3000)
    pg.wait_for_timeout(60)
    pg.screenshot(path=str(cap / "especial_folha_seca.png"))
    L, g = gol_pronto(pg, 2800)
    alto = min(r["by"] for r in L if r["fx"].startswith("folha"))
    sobre = next((r for r in L if r["fx"].startswith("folha") and r["bx"] >= r["p1"]["x"]), None)
    C.dados["folha_seca"] = {"altura_max_px": 716 - alto, "na_vertical_do_adversario_px": 716 - sobre["by"] if sobre else None, "gol": g and g["kind"]}
    C.ok("folha seca sobe bem alto (perto de folhaH)", 716 - alto > T["folhaH"] - 60, 716 - alto)
    C.ok("folha seca passa por cima do adversário", sobre is not None and 716 - sobre["by"] > 260, C.dados["folha_seca"])
    C.ok("folha seca despenca e entra: 'DE FOLHA SECA'", g is not None and "FOLHA SECA" in g["kind"] and g["txt"] == "GOLAÇO!", g and (g["txt"], g["kind"]))
    C.ok("folha seca gasta a barra", pg.evaluate("__arena.P[0].power") < 0.5)
    pg.wait_for_timeout(1500)

    # ------------------------------------------------------------------ bicicleta
    montar(pg, "const p=A.P[0]; p.special='bici'; p.power=1; p.x=A.W-760; A.P[1].x=400; A.ball.x=p.x+70; A.ball.y=A.GROUND_Y-330; A.ball.vy=-60;")
    gravar(pg, 3000)
    pg.keyboard.press("Space")
    pg.wait_for_function("__arena.P[0].spec&&__arena.P[0].spec.t>0.16", timeout=2000)
    pg.screenshot(path=str(cap / "especial_bicicleta.png"))
    L, g = gol_pronto(pg, 2600)
    pulo = min(r["p0"]["y"] for r in L)
    batida = next((r for r in L if r["fx"] == "bici"), None)
    C.dados["bicicleta"] = {"pulo_px": 716 - pulo, "vel_bola": batida and batida["bv"], "gol": g and g["kind"]}
    C.ok("bicicleta: o cabeçudo pula sozinho atrás da bola", 716 - pulo > 120, 716 - pulo)
    C.ok("bicicleta: bomba na direção do gol (> 2000 px/s)", batida is not None and batida["bv"] > 2000 and batida["bvx"] > 0, batida)
    C.ok("bicicleta entra: 'DE BICICLETA' é golaço", g is not None and "BICICLETA" in g["kind"] and g["txt"] == "GOLAÇO!", g and (g["txt"], g["kind"]))
    pg.wait_for_timeout(1500)

    # bicicleta no vazio: a barra continua
    montar(pg, "const p=A.P[0]; p.special='bici'; p.power=1; p.x=600; A.P[1].x=A.W-120; A.ball.x=p.x+220; A.ball.y=A.GROUND_Y-330; A.ball.vx=2400; A.ball.vy=-500;")
    pg.keyboard.press("Space"); pg.wait_for_timeout(1300)
    C.ok("bola longe na hora de armar: a bicicleta não sai e a barra continua", pg.evaluate("__arena.P[0].power") == 1)
    pg.wait_for_timeout(800)

    # ------------------------------------------------------------------ caneta
    montar(pg, "const p=A.P[0]; p.special='caneta'; p.power=1; p.x=700; p.face=1; A.P[1].x=960; A.P[1].face=-1; A.ball.x=748; A.ball.y=A.GROUND_Y-A.T.ballR;")
    gravar(pg, 2200)
    pg.keyboard.press("Space")
    pg.wait_for_function("__arena.P[1].dizzy>0.3", timeout=2000)
    pg.wait_for_timeout(140)
    pg.screenshot(path=str(cap / "especial_caneta.png"))
    pg.wait_for_timeout(2100)
    L = log(pg)
    tonto = max(r["p1"]["tonto"] for r in L)
    passou_bola = any(r["bx"] > r["p1"]["x"] + 40 for r in L)
    passou_eu = any(r["p0"]["x"] > r["p1"]["x"] + 20 for r in L)
    parou = [r for r in L if r["t"] > 1100]
    dist = parou[0]["bx"] - parou[0]["p1"]["x"] if parou else None
    C.dados["caneta"] = {"tonto_max_s": tonto, "bola_parou_atras_px": dist, "eu_passei": passou_eu}
    C.ok("caneta: a bola passa por entre as pernas do adversário", passou_bola, C.dados["caneta"])
    C.ok("caneta: o adversário fica tonto (~canetaTonto)", abs(tonto - T["canetaTonto"]) < 0.1, tonto)
    C.ok("caneta: a bola para logo atrás dele", dist is not None and 40 < dist < T["canetaDist"] + 160, dist)
    C.ok("caneta: quem dribla atravessa junto", passou_eu)
    # gol depois da caneta ganha nome
    pg.evaluate("""(()=>{const A=__arena,p=A.P[0]; p.x=A.ball.x-40; p.face=1; p.kickT=-1; A.ball.vx=0; A.ball.vy=0; A.ball.y=p.y-20; A.P[1].x=A.ball.x-300;})()""")
    gravar(pg, 2400)
    pg.keyboard.press("KeyG")
    L, g = gol_pronto(pg, 2300)
    C.ok("gol logo depois da caneta: 'DEPOIS DA CANETA'", g is not None and "DEPOIS DA CANETA" in g["kind"], g and g["kind"])
    pg.wait_for_timeout(1500)

    # ------------------------------------------------------------------ muralha
    montar(pg, "const p=A.P[0]; p.special='muralha'; p.power=1; p.x=60; A.P[1].x=A.W-300;")
    gravar(pg, 4200)
    pg.keyboard.press("Space"); pg.wait_for_timeout(450)
    r1 = pg.evaluate("__arena.rHead(__arena.P[0])")
    pg.screenshot(path=str(cap / "especial_muralha.png"))
    # chute forte no gol fechado
    pg.evaluate("""(()=>{const A=__arena,b=A.ball; b.x=700; b.y=A.GROUND_Y-110; b.vx=-1700; b.vy=0; b.fx=null; b.hit={who:1,kind:'voleio',x:700,post:false};})()""")
    pg.wait_for_timeout(1200)
    defendeu = pg.evaluate("__arena.G.score[1]")
    pg.wait_for_timeout(int(T["muraTime"] * 1000) - 1100)
    r2 = pg.evaluate("__arena.rHead(__arena.P[0])")
    C.dados["muralha"] = {"raio_com": round(r1), "raio_depois": round(r2), "gols_sofridos": defendeu}
    C.ok("muralha: a cabeça cresce perto de muraMul", abs(r1 / T["headR"] - T["muraMul"]) < 0.08, round(r1))
    C.ok("muralha: volta ao normal depois de muraTime", abs(r2 - T["headR"]) < 2, round(r2))
    C.ok("muralha dentro do gol segura um chute forte", defendeu == pg_["placar"][1], C.dados["muralha"])
    pg.wait_for_timeout(600)

    # ------------------------------------------------------------------ HUD com a barra cheia
    montar(pg, "A.P[0].special='folha'; A.P[0].power=1; A.P[1].power=0.55; A.P[0].x=600; A.P[1].x=1300; A.ball.x=960; A.ball.y=300;")
    pg.wait_for_timeout(300)
    pg.screenshot(path=str(cap / "especial_pronto.png"))
    erros_todos += erros
    ctx.close()

    # ------------------------------------------------------------------ CPU
    pg, ctx, erros = abrir(nav)
    pg.evaluate("__arena.G.aiLevel=2")
    iniciar_amistoso(pg, cpu_parada=False)

    def cpu(js, cond, ms=2500):
        montar(pg, js)
        try:
            pg.wait_for_function(cond, timeout=ms)
            return True
        except Exception:
            return False

    ok = cpu("const q=A.P[1]; q.special='folha'; q.power=1; q.x=1250; q.face=-1; A.P[0].x=520; A.ball.x=1205; A.ball.y=A.GROUND_Y-A.T.ballR;",
             "__arena.ball.fx&&__arena.ball.fx.id==='folha'&&__arena.ball.fx.who===1")
    C.ok("CPU solta a folha seca com a bola no pé, longe do gol", ok)
    pg.wait_for_timeout(2600)
    ok = cpu("const q=A.P[1]; q.special='caneta'; q.power=1; q.x=1250; q.face=-1; A.P[0].x=1000; A.P[0].face=1; A.ball.x=1205; A.ball.y=A.GROUND_Y-A.T.ballR;",
             "__arena.P[0].dizzy>0")
    C.ok("CPU dá a caneta quando o adversário está na frente", ok)
    pg.wait_for_timeout(1800)
    ok = cpu("const q=A.P[1]; q.special='bici'; q.power=1; q.x=900; q.face=-1; A.P[0].x=300; A.ball.x=870; A.ball.y=A.GROUND_Y-300; A.ball.vy=-40;",
             "__arena.ball.fx&&__arena.ball.fx.id==='bici'&&__arena.ball.fx.who===1")
    C.ok("CPU faz a bicicleta com a bola no alto perto dela", ok)
    pg.wait_for_timeout(2600)
    # muralha da CPU contra a folha seca do jogador
    montar(pg, "const q=A.P[1]; q.special='muralha'; q.power=1; q.x=A.W-260; const p=A.P[0]; p.special='folha'; p.power=1; p.x=520; A.ball.x=580; A.ball.y=A.GROUND_Y-A.T.ballR;")
    pg.keyboard.press("Space")
    try:
        pg.wait_for_function("__arena.P[1].muraT>0", timeout=2500); ok = True
    except Exception:
        ok = False
    C.ok("CPU responde à folha seca com a muralha", ok)
    erros_todos += erros
    ctx.close()

    # partida de fundo do menu (CPU contra CPU): os especiais acontecem sozinhos
    pg, ctx, erros = abrir(nav)
    pg.evaluate("(()=>{const A=__arena; A.G.clock=999; A.G.mstats.specs=[0,0]; A.P[0].power=0.7; A.P[1].power=0.7;})()")
    pg.wait_for_timeout(25000)
    usados = pg.evaluate("__arena.G.mstats.specs")
    C.dados["cpu_contra_cpu_25s_especiais"] = usados
    C.ok("CPU contra CPU (fundo do menu): especiais usados em 25 s", sum(usados) >= 1, usados)
    erros_todos += erros
    ctx.close()

    # ------------------------------------------------------------------ menu do amistoso
    pg, ctx, erros = abrir(nav, limpar_save=True)
    idx = pg.evaluate("__arena.MENU.findIndex(m=>m.id==='spec')")
    pg.evaluate("__arena.G.menuIdx=%d" % idx)
    pg.keyboard.press("KeyD"); pg.wait_for_timeout(100); pg.keyboard.press("KeyD"); pg.wait_for_timeout(100)
    fs = pg.evaluate("__arena.SAVE.profile.fspec")
    pg.screenshot(path=str(cap / "menu_especial.png"))
    C.ok("menu 'Especial ‹ ›' troca o especial do amistoso", fs == "caneta", fs)
    pg.evaluate("__arena.G.menuIdx=1"); pg.keyboard.press("Enter"); pg.wait_for_timeout(600)
    C.ok("amistoso usa o especial escolhido no menu", pg.evaluate("__arena.P[0].special") == "caneta")
    C.ok("o adversário do amistoso tem um especial", pg.evaluate("__arena.SPECIAL_IDS.indexOf(__arena.P[1].special)>=0"))

    # ------------------------------------------------------------------ painel
    n = pg.evaluate("document.querySelectorAll('#gSpec input[type=range]').length")
    dump = pg.evaluate("document.getElementById('dump').value")
    C.ok("painel tem o grupo Especiais com todos os números novos", n == 14 and "folhaH" in dump and "muraMul" in dump, n)
    erros_todos += erros
    ctx.close()

    # ------------------------------------------------------------------ carreira
    pg, ctx, erros = abrir(nav, limpar_save=True)
    pg.evaluate("__arena.G.menuIdx=0"); pg.keyboard.press("Enter"); pg.wait_for_timeout(300)
    pg.click('[data-act=look][data-arg="spec:caneta"]'); pg.wait_for_timeout(100)
    pg.fill("#pname", "Teste"); pg.wait_for_timeout(100)
    pg.screenshot(path=str(cap / "carreira_criacao.png"))
    pg.click("[data-act=create]"); pg.wait_for_timeout(200)
    sv = pg.evaluate("__arena.SAVE.profile")
    C.ok("criação: o especial escolhido é o primeiro liberado", sv["owned"].get("spec") == ["caneta"] and sv["look"]["spec"] == "caneta", sv["owned"].get("spec"))
    pg.click("[data-act=hub]"); pg.wait_for_timeout(200)
    hub = pg.inner_text("#ui")
    C.ok("tabela mostra o teu especial e o do adversário", "Teu especial: Caneta" in hub, hub[:300])
    pg.click("[data-act=play]"); pg.wait_for_timeout(600)
    esp = pg.evaluate("[__arena.P[0].special,__arena.P[1].special]")
    C.ok("na partida da carreira o cabeçudo usa o especial escolhido", esp[0] == "caneta" and esp[1] in ["folha", "bici", "caneta", "muralha"], esp)
    pg.evaluate("__arena.finish(3,1)"); pg.wait_for_timeout(200)
    # vence a Copa da Vila
    guarda = 0
    while guarda < 40:
        guarda += 1
        s = tela(pg)
        if s == "result":
            pg.click("[data-act=after]")
        elif s == "hub" and pg.query_selector("[data-act=play]"):
            pg.click("[data-act=play]"); pg.wait_for_timeout(120); pg.evaluate("__arena.finish(3,1)")
        elif s in ("season", "hub"):
            break
        pg.wait_for_timeout(60)
    novo = pg.evaluate("__arena.SAVE.career.season.newSpec")
    texto = pg.inner_text("#ui")
    pg.screenshot(path=str(cap / "carreira_novo_especial.png"))
    C.ok("título da Copa da Vila libera o próximo especial", novo == "folha" and "Novo especial liberado" in texto, novo)
    pg.click("[data-act=offers]"); pg.wait_for_timeout(150)
    pg.click('[data-act=sign][data-arg="0"]'); pg.wait_for_timeout(150)
    pg.click("[data-act=hub]"); pg.wait_for_timeout(150)
    pg.click("[data-act=locker]"); pg.wait_for_timeout(200)
    pg.click('[data-act=tab][data-arg="spec"]'); pg.wait_for_timeout(150)
    pg.screenshot(path=str(cap / "vestiario_especial.png"))
    n_it = pg.evaluate("document.querySelectorAll('[data-act=spec]').length")
    pg.click('[data-act=spec][data-arg="folha"]'); pg.wait_for_timeout(100)
    pg.click('[data-act=spec][data-arg="bici"]'); pg.wait_for_timeout(100)
    sv = pg.evaluate("__arena.SAVE")
    C.ok("vestiário: aba Especial com os quatro; trocar para um liberado funciona; bloqueado não",
         n_it == 4 and sv["profile"]["look"]["spec"] == "folha", (n_it, sv["profile"]["look"]["spec"]))

    def tem_array_em_array(o):
        if isinstance(o, list):
            return any(isinstance(x, list) or tem_array_em_array(x) for x in o)
        if isinstance(o, dict):
            return any(tem_array_em_array(v) for v in o.values())
        return False
    C.ok("salvamento continua sem arrays dentro de arrays", not tem_array_em_array(sv))
    # recarregar mantém
    pg.reload(); pg.wait_for_timeout(900)
    sv2 = pg.evaluate("__arena.SAVE.profile")
    C.ok("especiais liberados e o escolhido continuam depois de recarregar",
         sorted(sv2["owned"]["spec"]) == ["caneta", "folha"] and sv2["look"]["spec"] == "folha", sv2["owned"]["spec"])
    # salvamento de antes da v0.14, com a carreira na Primeira Divisão
    pg.evaluate("""(()=>{const s=JSON.parse(localStorage.getItem('fcc_save_v1')); delete s.profile.owned.spec; delete s.profile.look.spec;
      s.career.tier=3; s.career.season.tier=3; s.savedAt=Date.now(); localStorage.setItem('fcc_save_v1',JSON.stringify(s));})()""")
    pg.reload(); pg.wait_for_timeout(900)
    sv3 = pg.evaluate("__arena.SAVE.profile")
    C.ok("salvamento antigo na Primeira Divisão ganha os quatro especiais", sorted(sv3["owned"].get("spec", [])) == ["bici", "caneta", "folha", "muralha"],
         sv3["owned"].get("spec"))
    erros_todos += erros
    ctx.close()

    # ------------------------------------------------------------------ toque
    for w, h in [(844, 390), (667, 375)]:
        pg, ctx, erros = abrir(nav, w, h, toque=True)
        iniciar_amistoso(pg)
        cabe = pg.evaluate("""(()=>{const bs=[...document.querySelectorAll('#pad .acts button, #pad .stick, #pad .mid button')].map(b=>b.getBoundingClientRect());
          return {dir:Math.round(Math.max(...bs.map(r=>r.right))), esq:Math.round(Math.min(...bs.map(r=>r.left))), larg:innerWidth};})()""")
        C.ok("toque %dx%d: os cinco botões e a trilha cabem na tela" % (w, h), cabe["dir"] <= cabe["larg"] and cabe["esq"] >= 0, cabe)
        if w == 844:
            montar(pg, "const p=A.P[0]; p.special='folha'; p.power=1; p.x=500; A.ball.x=560; A.ball.y=A.GROUND_Y-A.T.ballR;")
            pg.wait_for_timeout(150)
            pronto = pg.evaluate("document.getElementById('tSpec').classList.contains('ready')")
            pg.screenshot(path=str(cap / "toque_especial.png"))
            b = pg.evaluate("(()=>{const r=document.getElementById('tSpec').getBoundingClientRect(); return [r.left+r.width/2,r.top+r.height/2];})()")
            cdp = ctx.new_cdp_session(pg)
            cdp.send("Input.dispatchTouchEvent", {"type": "touchStart", "touchPoints": [{"x": b[0], "y": b[1], "id": 1}]})
            pg.wait_for_timeout(60)
            cdp.send("Input.dispatchTouchEvent", {"type": "touchEnd", "touchPoints": []})
            pg.wait_for_timeout(120)
            saiu = pg.evaluate("!!(__arena.ball.fx&&__arena.ball.fx.id==='folha')")
            C.ok("botão ★ brilha com a barra cheia e solta o especial", pronto and saiu, (pronto, saiu))
        erros_todos += erros
        ctx.close()

    nav.close()

C.fim(erros_todos)
