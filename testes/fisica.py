"""Física: pique e fôlego, condução, voleio embalado (domínio perfeito) e altura dos chutes.

Uso:  python testes/fisica.py
"""
import math

from comum import Checagens, abrir, iniciar_amistoso, sync_playwright

C = Checagens("Física: pique, condução, domínio perfeito e voleio")
G_Y = 716


def pique(pg):
    pg.evaluate("""(()=>{const A=__arena,p=A.P[0]; p.x=300; p.vx=0; p.stam=1; p.tired=false; p.sprinting=false;
      A.ball.x=A.W-300; A.ball.y=200; A.ball.vx=0; A.ball.vy=0;
      const log=[]; window.__s=log; const t0=performance.now();
      (function rec(){ const p=__arena.P[0]; log.push([Math.round(performance.now()-t0),Math.round(p.vx),+p.stam.toFixed(3),p.tired]); if(performance.now()-t0<6500) requestAnimationFrame(rec); })();
    })()""")
    pg.keyboard.down("ShiftLeft"); pg.keyboard.down("KeyD")
    pg.wait_for_timeout(1300)
    pg.keyboard.up("KeyD"); pg.wait_for_timeout(250)
    pg.evaluate("__arena.P[0].x=300")
    pg.keyboard.down("KeyD"); pg.wait_for_timeout(1500)
    pg.keyboard.up("KeyD"); pg.keyboard.up("ShiftLeft")
    pg.wait_for_timeout(3600)
    L = pg.evaluate("window.__s")
    cansou = next((r[0] for r in L if r[3]), None)
    voltou = next((r[0] for r in L if cansou and r[0] > cansou and not r[3]), None)
    return {"vel_max": max(r[1] for r in L), "cansou_em_ms": cansou, "saiu_do_cansaco_ms": voltou}


def conducao(pg, em_pique):
    pg.evaluate("""(s)=>{const A=__arena,p=A.P[0]; p.x=260; p.vx=0; p.stam=1; p.tired=false; p.ctrlT=-1; p.kickT=-1;
      const b=A.ball; b.x=340; b.y=A.GROUND_Y-A.T.ballR; b.vx=0; b.vy=0; b.spin=0;
      const log=[]; window.__d=log; const t0=performance.now();
      (function rec(){ const A=__arena,p=A.P[0],b=A.ball; log.push([performance.now()-t0,b.x-p.x,p.x]); if(performance.now()-t0<1500) requestAnimationFrame(rec); })();
    }""", em_pique)
    if em_pique:
        pg.keyboard.down("ShiftLeft")
    pg.keyboard.down("KeyD"); pg.wait_for_timeout(1500); pg.keyboard.up("KeyD")
    if em_pique:
        pg.keyboard.up("ShiftLeft")
    L = pg.evaluate("window.__d")
    gaps = [r[1] for r in L if r[0] > 300]
    return {"bola_a_frente_min": round(min(gaps)), "bola_a_frente_max": round(max(gaps)), "andou_px": round(L[-1][2] - L[0][2])}


def voleio(pg, embalado, x0, dx=40, dy=20):
    pg.evaluate("""([boost,dx,dy,x0])=>{const A=__arena,p=A.P[0]; A.P[1].x=150; A.P[1].vx=0;
      p.x=x0; p.vx=0; p.kickT=-1; p.kickHit=false; p.ctrlT=-1; p.poseT=-1; p.y=A.GROUND_Y; p.vy=0; p.onGround=true;
      p.boostT=boost?0.8:0;
      const b=A.ball; b.x=x0+dx; b.y=p.y-dy; b.vx=0; b.vy=0; b.spin=0; b.curve=0;
      const log=[]; window.__v=log; const t0=performance.now();
      (function rec(){ const A=__arena,b=A.ball,p=A.P[0]; if(!p.kickHit){ b.vx=0; b.vy=0; b.x=x0+dx; b.y=p.y-dy; }
        log.push([performance.now()-t0,b.x,b.y,b.vx,b.vy,p.kickHit]); if(performance.now()-t0<1800) requestAnimationFrame(rec); })();
    }""", [embalado, dx, dy, x0])
    pg.keyboard.press("KeyG"); pg.wait_for_timeout(1900)
    L = pg.evaluate("window.__v")
    k = next((i for i, r in enumerate(L) if r[5]), None)
    if k is None:
        return None
    r = L[min(k + 1, len(L) - 1)]
    W = pg.evaluate("__arena.W"); GD = pg.evaluate("__arena.GOAL_D")
    yg = next((q[2] for q in L[k:] if q[1] >= W - GD - 17), None)
    return {"vel_saida": round(math.hypot(r[3], r[4])), "altura_na_boca_do_gol": round(G_Y - yg) if yg else None}


with sync_playwright() as pw:
    nav = pw.chromium.launch()
    pg, ctx, erros = abrir(nav)
    iniciar_amistoso(pg)

    pq = pique(pg)
    C.dados["pique"] = pq
    pspeed = pg.evaluate("__arena.T.pSpeed*__arena.T.sprintMul")
    C.ok("pique chega a pSpeed × sprintMul", abs(pq["vel_max"] - pspeed) < 5, (pq["vel_max"], round(pspeed)))
    C.ok("fôlego acaba perto de 'stamina' segundos de pique", pq["cansou_em_ms"] is not None and 2200 <= pq["cansou_em_ms"] <= 3000, pq["cansou_em_ms"])
    C.ok("sai do cansaço depois de recuperar um pouco", pq["saiu_do_cansaco_ms"] is not None)

    pg.wait_for_timeout(300)
    cn = conducao(pg, False); pg.wait_for_timeout(500); cp = conducao(pg, True)
    C.dados["conducao_normal"] = cn; C.dados["conducao_pique"] = cp
    C.ok("condução normal mantém a bola colada (até ~90 px)", cn["bola_a_frente_max"] <= 90, cn)
    C.ok("em pique o toque é mais longo e se anda mais", cp["bola_a_frente_max"] > cn["bola_a_frente_max"] and cp["andou_px"] > cn["andou_px"], cp)

    # domínio de peito perfeito ativa o bônus
    pg.evaluate("""(()=>{const A=__arena; const p=A.P[0]; A.P[1].x=1600; p.x=700; p.y=A.GROUND_Y; p.vx=0; p.vy=0; p.onGround=true;
      p.kickT=-1; p.ctrlT=0; p.ctrlCd=0; p.ctrlGrace=0; p.poseT=-1; p.boostT=0;
      const b=A.ball; b.x=722; b.y=505; b.vx=-30; b.vy=950; b.spin=0; b.curve=0; A.G.floats.length=0;})()""")
    pg.wait_for_timeout(120)
    dp = pg.evaluate("({texto:(__arena.G.floats.slice(-1)[0]||{}).text,boostT:+__arena.P[0].boostT.toFixed(2)})")
    C.dados["dominio_peito"] = dp
    C.ok("domínio de peito perfeito deixa o voleio embalado", dp["texto"] == "PEITO · PERFEITO" and dp["boostT"] > 0.5, dp)

    # voleio no chão: embalado sai mais forte e chega igual ou mais baixo no gol
    mul = pg.evaluate("__arena.T.boostMul")
    for x0 in (1320, 900):
        pg.wait_for_timeout(2200); n = voleio(pg, False, x0)
        pg.wait_for_timeout(2200); b = voleio(pg, True, x0)
        C.dados["voleio_a_%dpx_do_gol" % (1860 - x0)] = {"normal": n, "embalado": b}
        if n and b:
            C.ok("voleio embalado ≈ %.2f× mais rápido (%d px do gol)" % (mul, 1860 - x0), abs(b["vel_saida"] / n["vel_saida"] - mul) < 0.04,
                 (n["vel_saida"], b["vel_saida"]))
            if b["altura_na_boca_do_gol"] is not None:
                trave = pg.evaluate("__arena.T.goalH-__arena.T.ballR")
                C.ok("voleio embalado passa por baixo do travessão (%d px do gol)" % (1860 - x0),
                     b["altura_na_boca_do_gol"] < trave, "normal %s px, embalado %s px, travessão %d px" % (n["altura_na_boca_do_gol"], b["altura_na_boca_do_gol"], trave))
        else:
            C.ok("voleio acertou a bola na montagem do teste (%d px do gol)" % (1860 - x0), False, (n, b))

    ctx.close(); nav.close()

C.fim(erros)
