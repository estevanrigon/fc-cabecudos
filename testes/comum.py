"""Utilidades comuns dos testes do FC Cabeçudos.

Os testes abrem o index.html num Chromium controlado pelo Playwright e usam o gancho
de depuração `window.__arena` (exposto pelo próprio jogo) para ler e ajustar o estado.
"""
import json
import pathlib
import sys

from playwright.sync_api import sync_playwright  # noqa: F401  (reexportado para os testes)

RAIZ = pathlib.Path(__file__).resolve().parent.parent
JOGO = (RAIZ / "index.html").as_uri()
CAPTURAS = RAIZ / "testes" / "capturas"


def pasta_capturas():
    CAPTURAS.mkdir(parents=True, exist_ok=True)
    return CAPTURAS


def abrir(navegador, largura=1180, altura=900, toque=False, limpar_save=False):
    """Abre o jogo numa aba nova e devolve (página, contexto, lista de erros de JS)."""
    if toque:
        ctx = navegador.new_context(viewport={"width": largura, "height": altura},
                                    has_touch=True, is_mobile=True, device_scale_factor=2)
    else:
        ctx = navegador.new_context(viewport={"width": largura, "height": altura})
    pg = ctx.new_page()
    erros = []
    pg.on("pageerror", lambda e: erros.append("erro de página: " + str(e)))
    pg.on("console", lambda m: erros.append("console: " + m.text)
          if m.type == "error" and "Failed to load resource" not in m.text else None)
    pg.goto(JOGO)
    pg.wait_for_timeout(900)
    if limpar_save:
        pg.evaluate("localStorage.clear()")
        pg.reload()
        pg.wait_for_timeout(900)
    return pg, ctx, erros


def tela(pg):
    """Tela atual da carreira/vestiário (None quando a camada está fechada)."""
    return pg.evaluate("__arena.UI.screen")


def iniciar_amistoso(pg, cpu_parada=True):
    """Do menu principal, começa um amistoso. Com cpu_parada, o adversário fica imóvel."""
    pg.evaluate("__arena.G.menuIdx=1")
    pg.keyboard.press("Enter")
    pg.wait_for_timeout(1400)
    if cpu_parada:
        pg.evaluate("(()=>{const A=__arena; A.P[1].ai=null; A.P[1].x=A.W-120;})()")


class Checagens:
    """Junta as verificações de um teste e imprime o relatório no fim."""

    def __init__(self, nome):
        self.nome = nome
        self.itens = []
        self.dados = {}

    def ok(self, descricao, condicao, detalhe=None):
        self.itens.append((descricao, bool(condicao), detalhe))

    def fim(self, erros_js=()):
        print("=" * 70)
        print(self.nome)
        print("=" * 70)
        if self.dados:
            print(json.dumps(self.dados, ensure_ascii=False, indent=1))
            print("-" * 70)
        falhas = 0
        for desc, cond, det in self.itens:
            marca = "OK     " if cond else "FALHOU "
            if not cond:
                falhas += 1
            print(marca + desc + ("" if det is None else "  ->  " + str(det)))
        erros_js = list(erros_js)
        if erros_js:
            falhas += 1
            print("FALHOU erros de JavaScript:")
            for e in erros_js:
                print("        " + e)
        print("-" * 70)
        print("Resultado: " + ("tudo certo" if falhas == 0 else str(falhas) + " falha(s)"))
        sys.exit(1 if falhas else 0)
