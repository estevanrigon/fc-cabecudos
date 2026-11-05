"""Controle de Xbox (Gamepad API): menu, partida (andar, pique, pulo, cavadinha, voleio, domínio,
especial), pausa, fim de jogo, telas da carreira e do vestiário, e no toque (botões da tela somem
com o controle e voltam ao tocar; dois controles liberam o modo 2 jogadores).

O controle é simulado: navigator.getGamepads devolve um ou dois controles no layout padrão do Xbox,
com os botões ajustados pelo teste em window.__pads.

Uso:  python testes/controle.py
"""
from comum import Checagens, abrir, pasta_capturas, sync_playwright, tela

C = Checagens("Controle: Xbox no computador e no celular")
cap = pasta_capturas()
erros_todos = []

FALSO = """(()=>{
  const mk=()=>({buttons:new Array(17).fill(0),axes:[0,0,0,0],on:false});
  window.__pads=[mk(),mk()];
  const fn=function(){ return window.__pads.map(function(p,i){ if(!p.on) return null;
    return {id:'Xbox Wireless Controller (teste)',index:i,connected:true,mapping:'standard',timestamp:performance.now(),
      axes:p.axes.slice(),buttons:p.buttons.map(function(v){ return {pressed:v>0.5,touched:v>0,value:v}; })}; }); };
  try{ Object.defineProperty(Navigator.prototype,'getGamepads',{value:fn,configurable:true}); }catch(e){}
  try{ Object.defineProperty(navigator,'getGamepads',{value:fn,configurable:true}); }catch(e){}
})();"""

A, B, X, Y, LB, RB, LT, RT, EXIBIR, MENU, CIMA, BAIXO, ESQ, DIR = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 12, 13, 14, 15


def abrir_com_controle(nav, **kw):
    pg, ctx, erros = abrir(nav, **kw)
    ctx.add_init_script(FALSO)
    pg.reload()
    pg.wait_for_timeout(900)
    pg.evaluate("__arena.SAVE.profile.tut=__arena.SAVE.profile.tut||1")
    return pg, ctx, erros


def ligar(pg, pad=0):
    pg.evaluate(f"__pads[{pad}].on=true")
    pg.wait_for_timeout(80)


def botao(pg, i, v=1, pad=0):
    pg.evaluate(f"__pads[{pad}].buttons[{i}]={v}")


def aperta(pg, i, pad=0, ms=90):
    botao(pg, i, 1, pad)
    pg.wait_for_timeout(ms)
    botao(pg, i, 0, pad)
    pg.wait_for_timeout(90)


def eixo(pg, i, v, pad=0):
    pg.evaluate(f"__pads[{pad}].axes[{i}]={v}")


def arrumar(pg, js=""):
    pg.evaluate("""(js)=>{const A=__arena; A.G.phase='play'; A.G.paused=false; A.G.banner=null; A.G.freezeBall=false;
      A.P[1].ai=null; A.P[1].x=A.W-120;
      const p=A.P[0]; p.x=A.W*0.4; p.y=A.GROUND_Y; p.vx=0; p.vy=0; p.onGround=true; p.kickT=-1; p.ctrlT=-1; p.poseT=-1;
      p.face=1; p.stam=1; p.tired=false; p.armT=0; p.spec=null; p.specCd=0;
      const b=A.ball; b.x=A.W-300; b.y=A.GROUND_Y-A.T.ballR; b.vx=0; b.vy=0; b.fx=null;
      (new Function('A',js))(A);}""", js)


def ev(pg, js):
    return pg.evaluate(js)


with sync_playwright() as pw:
    nav = pw.chromium.launch()

    # ---------------- computador ----------------
    pg, ctx, erros = abrir_com_controle(nav)
    ligar(pg)
    C.ok("sem apertar nada, o controle ainda não muda as dicas", ev(pg, "__arena.GPAD") is False)
    aperta(pg, BAIXO)
    C.ok("direcional para baixo desce no menu", ev(pg, "__arena.G.menuIdx") == 1, ev(pg, "__arena.G.menuIdx"))
    C.ok("controle em uso: dicas do controle", ev(pg, "__arena.GPAD") is True and ev(pg, "document.body.classList.contains('gp')"))
    pg.screenshot(path=str(cap / "controle_menu.png"))
    # A começa o amistoso; segurando o A, o jogador não pula sozinho
    botao(pg, A, 1)
    pg.wait_for_timeout(500)
    C.ok("A no menu começa o amistoso", ev(pg, "__arena.G.mode") == "match")
    C.ok("o A que começou a partida não vira pulo", ev(pg, "__arena.P[0].onGround&&__arena.P[0].y>=__arena.GROUND_Y-1"))
    botao(pg, A, 0)
    pg.wait_for_timeout(1300)

    arrumar(pg)
    eixo(pg, 0, 1)
    pg.wait_for_timeout(400)
    x1 = ev(pg, "__arena.P[0].x")
    eixo(pg, 0, 0)
    C.ok("analógico para a direita anda", x1 > ev(pg, "__arena.W*0.4") + 60, round(x1))
    arrumar(pg)
    botao(pg, DIR, 1)
    botao(pg, RT, 1)
    pg.wait_for_timeout(400)
    st = ev(pg, "__arena.P[0].stam")
    x2 = ev(pg, "__arena.P[0].x")
    botao(pg, DIR, 0)
    botao(pg, RT, 0)
    C.ok("direcional + RT: pique (gasta fôlego e corre mais)", st < 0.95 and x2 - ev(pg, "__arena.W*0.4") > x1 - ev(pg, "__arena.W*0.4"),
         {"folego": round(st, 2), "x_pique": round(x2), "x_normal": round(x1)})

    arrumar(pg)
    botao(pg, A, 1)
    pg.wait_for_timeout(120)
    C.ok("A pula", ev(pg, "__arena.P[0].y") < ev(pg, "__arena.GROUND_Y") - 20, round(ev(pg, "__arena.P[0].y")))
    botao(pg, A, 0)
    pg.wait_for_timeout(900)

    arrumar(pg, "A.ball.x=A.P[0].x+56;")
    aperta(pg, B)
    pg.wait_for_timeout(60)
    C.ok("B dá o voleio (bola sai forte)", ev(pg, "__arena.ball.vx") > 900, round(ev(pg, "__arena.ball.vx")))
    pg.wait_for_timeout(800)
    arrumar(pg, "A.ball.x=A.P[0].x+56;")
    aperta(pg, X)
    pg.wait_for_timeout(60)
    C.ok("X dá a cavadinha (bola sobe)", ev(pg, "__arena.ball.vy") < -150, round(ev(pg, "__arena.ball.vy")))
    pg.wait_for_timeout(800)
    arrumar(pg)
    aperta(pg, Y)
    C.ok("Y faz o domínio", ev(pg, "__arena.P[0].ctrlT") >= 0 or ev(pg, "__arena.P[0].poseT") >= 0,
         {"ctrlT": ev(pg, "__arena.P[0].ctrlT"), "poseT": ev(pg, "__arena.P[0].poseT")})
    arrumar(pg, "A.P[0].power=1;")
    aperta(pg, RB)
    C.ok("RB arma o especial", ev(pg, "__arena.P[0].armT>0||!!__arena.P[0].spec||__arena.P[0].power<1"))
    arrumar(pg, "A.P[0].power=1;")
    aperta(pg, LB)
    C.ok("LB também arma o especial", ev(pg, "__arena.P[0].armT>0||!!__arena.P[0].spec||__arena.P[0].power<1"))

    aperta(pg, MENU)
    C.ok("botão Menu pausa", ev(pg, "__arena.G.paused") is True)
    pg.wait_for_timeout(150)
    pg.screenshot(path=str(cap / "controle_pausa.png"))
    aperta(pg, A)
    C.ok("A volta da pausa (sem pular)", ev(pg, "!__arena.G.paused&&__arena.P[0].onGround"))
    aperta(pg, MENU)
    aperta(pg, Y)
    C.ok("Y na pausa reinicia o amistoso", ev(pg, "!__arena.G.paused&&__arena.G.score[0]===0&&__arena.G.phase==='kickoff'"),
         ev(pg, "__arena.G.phase"))
    pg.wait_for_timeout(1200)

    ev(pg, "(()=>{const A=__arena; A.G.phase='fulltime'; A.G.phaseT=0; A.G.score=[2,1];})()")
    pg.wait_for_timeout(150)
    pg.screenshot(path=str(cap / "controle_fim.png"))
    aperta(pg, B)
    C.ok("B no fim do jogo volta ao menu", ev(pg, "__arena.G.mode") == "menu")

    # vestiário: entrar, trocar de aba com RB, andar pelo foco e voltar com B
    idx = ev(pg, "__arena.MENU.findIndex(m=>m.id==='locker')")
    ev(pg, f"__arena.G.menuIdx={idx}")
    aperta(pg, A)
    pg.wait_for_timeout(200)
    C.ok("A no menu abre o vestiário", tela(pg) == "locker", tela(pg))
    aba0 = ev(pg, "__arena.UI.tab")
    aperta(pg, RB)
    aba1 = ev(pg, "__arena.UI.tab")
    C.ok("RB troca a aba do vestiário", aba1 != aba0, [aba0, aba1])
    C.ok("o foco fica na aba nova", ev(pg, "document.activeElement&&document.activeElement.dataset.act==='tab'&&document.activeElement.dataset.arg===__arena.UI.tab"))
    # as abas ocupam duas linhas: descendo, passa pela segunda linha e chega nos itens
    f1 = ""
    for _ in range(3):
        aperta(pg, BAIXO)
        f1 = ev(pg, "document.activeElement&&(document.activeElement.dataset.act+'|'+document.activeElement.dataset.arg)")
        if f1 and not f1.startswith("tab|"):
            break
    C.ok("direcional move o foco para baixo, até os itens", f1 and not f1.startswith("tab|"), f1)
    aperta(pg, DIR)
    f2 = ev(pg, "document.activeElement&&(document.activeElement.dataset.act+'|'+document.activeElement.dataset.arg)")
    C.ok("direcional para o lado troca de botão", f2 and f2 != f1, [f1, f2])
    pg.screenshot(path=str(cap / "controle_vestiario.png"))
    aperta(pg, B)
    C.ok("B sai do vestiário", tela(pg) is None and ev(pg, "__arena.G.mode") == "menu", tela(pg))

    # carreira: criar e jogar a primeira partida só com o controle
    ev(pg, "__arena.G.menuIdx=0")
    aperta(pg, A)
    pg.wait_for_timeout(200)
    C.ok("A em Carreira abre a criação", tela(pg) == "create", tela(pg))
    ev(pg, "document.getElementById('pname')&&(document.getElementById('pname').value='Controle')")
    for _ in range(12):
        if ev(pg, "!!document.activeElement&&document.activeElement.dataset.act==='create'"):
            break
        aperta(pg, BAIXO)
    ok_criar = ev(pg, "!!document.activeElement&&document.activeElement.dataset.act==='create'")
    aperta(pg, A)
    pg.wait_for_timeout(300)
    C.ok("só com o direcional e o A dá para criar a carreira", ok_criar and tela(pg) != "create", tela(pg))
    pg.screenshot(path=str(cap / "controle_carreira.png"))
    erros_todos += erros
    ctx.close()

    # ---------------- celular ----------------
    pg, ctx, erros = abrir_com_controle(nav, largura=844, altura=390, toque=True)
    ext0 = ev(pg, "__arena.EXT")
    pad_vis = "getComputedStyle(document.getElementById('pad')).display!=='none'"
    C.ok("celular sem controle: botões de toque na tela", ev(pg, pad_vis))
    C.ok("celular com um controle: sem modo 2 jogadores", ev(pg, "!__arena.MENU.some(m=>m.id==='2p')"))
    ligar(pg)
    aperta(pg, BAIXO)
    C.ok("celular: controle esconde os botões da tela", not ev(pg, pad_vis) and ev(pg, "__arena.GPAD"))
    aperta(pg, A)
    pg.wait_for_timeout(1400)
    C.ok("celular: A começa a partida", ev(pg, "__arena.G.mode") == "match")
    ext1 = ev(pg, "__arena.EXT")
    C.ok("celular: sem a faixa dos botões, o campo ganha espaço", ext1 < ext0, [ext0, ext1])
    arrumar(pg)
    eixo(pg, 0, -1)
    pg.wait_for_timeout(350)
    eixo(pg, 0, 0)
    C.ok("celular: analógico anda", ev(pg, "__arena.P[0].x") < ev(pg, "__arena.W*0.4") - 50)
    pg.screenshot(path=str(cap / "controle_celular.png"))
    pg.touchscreen.tap(400, 200)
    pg.wait_for_timeout(200)
    C.ok("celular: tocar na tela traz os botões de volta", ev(pg, pad_vis) and not ev(pg, "__arena.GPAD"))
    ev(pg, "__arena.G.paused=false")
    ligar(pg, 1)
    aperta(pg, MENU)
    aperta(pg, EXIBIR)
    pg.wait_for_timeout(200)
    C.ok("celular: Menu e Exibir levam ao menu", ev(pg, "__arena.G.mode") == "menu")
    C.ok("celular com dois controles: modo 2 jogadores aparece", ev(pg, "__arena.MENU.some(m=>m.id==='2p')"))
    idx = ev(pg, "__arena.MENU.findIndex(m=>m.id==='2p')")
    ev(pg, f"__arena.G.menuIdx={idx}")
    aperta(pg, A)
    pg.wait_for_timeout(1400)
    C.ok("dois controles: partida de 2 jogadores", ev(pg, "__arena.G.twoP&&__arena.P[1].human"))
    arrumar(pg, "A.P[1].x=A.W*0.7; A.P[1].vx=0;")
    eixo(pg, 0, -1, pad=1)
    pg.wait_for_timeout(350)
    eixo(pg, 0, 0, pad=1)
    x_p1 = ev(pg, "__arena.P[1].x")
    C.ok("o segundo controle move o jogador 2 (e não o 1)",
         x_p1 < ev(pg, "__arena.W*0.7") - 50 and abs(ev(pg, "__arena.P[0].x") - ev(pg, "__arena.W*0.4")) < 5,
         {"p1": round(x_p1), "p0": round(ev(pg, "__arena.P[0].x"))})
    erros_todos += erros
    ctx.close()
    nav.close()

C.fim(erros_todos)
