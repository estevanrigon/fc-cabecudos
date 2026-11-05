# FC Cabeçudos

Futebol de cabeça 1x1, da várzea até a final da Liga Suprema. O jogo inteiro está no `index.html`.

## Jogar

Dois cliques no `index.html` abrem o jogo no navegador. Aberto daqui, o painel de ajuste aparece embaixo do campo; o botão **Ver como jogador** mostra a versão que os amigos veem pelo link.

O progresso da carreira aberto por este arquivo fica salvo só neste navegador. A carreira da tua conta é a do link publicado.

## Trabalhar com o Claude Code

**1. Instalar (uma vez só).** Abre o PowerShell e cola:

```powershell
irm https://claude.ai/install.ps1 | iex
```

Depois fecha e abre o PowerShell de novo e confere com `claude --version`. O [Git para Windows](https://git-scm.com/downloads/win) é recomendado, para o Claude Code usar o terminal Bash e guardar versões.

**2. Abrir nesta pasta.** No PowerShell:

```powershell
cd "$HOME\Documents\FC Cabecudos"
claude
```

Na primeira vez ele pede login com a tua conta do Claude.

**3. Primeiros pedidos que valem a pena:**

- "Inicia o git aqui e faz o primeiro commit" (assim cada versão fica guardada e dá para voltar atrás).
- "Prepara os testes" (ele instala o Playwright: precisa do Python, que dá para instalar com `winget install Python.Python.3.12`).
- Daí em diante, pede as mudanças no jogo como fazias no Cowork. O arquivo `CLAUDE.md` já explica para ele como o projeto funciona, as regras e as decisões tomadas.

## Testes automáticos

```powershell
pip install -r testes/requirements.txt
python -m playwright install chromium
python testes/carreira.py
python testes/fisica.py
python testes/telas.py
python testes/treino.py
python testes/especiais.py
```

Cada um imprime OK ou FALHOU por verificação e salva capturas de tela em `testes/capturas`.

## Atualizar o link dos amigos

Mudar o `index.html` aqui não muda o jogo publicado. Para atualizar o link, publica o `index.html` no artifact do jogo: pelo Claude Code, se ele tiver a ferramenta de artifacts, ou numa conversa do Cowork no projeto "Head Soccer", pedindo para publicar o `index.html` desta pasta.

## O que tem aqui

| Arquivo | Para quê |
| - | - |
| `index.html` | o jogo (mesmo conteúdo do link publicado) |
| `CLAUDE.md` | instruções e mapa do código para o Claude Code |
| `docs/estado.md` | decisões, números da física e da carreira, pendências |
| `docs/historico.md` | o que cada versão trouxe |
| `testes/` | testes automáticos com Playwright |
