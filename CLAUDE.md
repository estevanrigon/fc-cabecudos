# FC Cabeçudos

Jogo de futebol de cabeça 1x1 (inspirado no Head Soccer, com identidade própria), feito em HTML + Canvas num arquivo só. O dono é o Estêvan; responda em português do Brasil, com tuteio ("podes", "queres").

- Jogo no ar: https://estevanrigon.github.io/fc-cabecudos/ (GitHub Pages, servido da branch `main` de https://github.com/estevanrigon/fc-cabecudos). Push na `main` = versão nova no link dos amigos em cerca de um minuto.
- Versão atual: v0.14.
- Onde está cada coisa (leia só quando a tarefa pedir):
  - `docs/estado.md`: como cada sistema funciona hoje e as decisões já tomadas.
  - `docs/plano.md`: próximos passos, pendências e decisões em aberto.
  - `docs/historico.md`: o que cada versão trouxe.

## Para gastar menos

- Não leia o `index.html` inteiro (passa de 5 mil linhas). Ache a seção pelo mapa abaixo ou com Grep e leia só o trecho.
- Os números da física ficam em `DEF`, no `index.html`. Não há cópia deles nos docs.
- Cada informação mora num lugar só: funcionamento em `docs/estado.md`, pendências em `docs/plano.md`, versões em `docs/historico.md`. Não repita em outro arquivo.
- Publicar é `git push`. Não use a ferramenta de artifacts para publicar o jogo (ver "Link antigo do claude.ai").
- Notas desta máquina (caminho do Python etc.) ficam em `CLAUDE.local.md`, fora do git.

## Como o projeto é organizado

- `index.html` é o jogo inteiro: HTML, CSS e JavaScript juntos, sem build e sem dependências (só as fontes do Google Fonts). Abrir com dois cliques já roda. O GitHub Pages serve esse mesmo arquivo.
- O arquivo começa com o "esqueleto" que o claude.ai acrescenta ao publicar (`<!doctype html>...<body>`). Mantenha esse esqueleto como está: ele não atrapalha no GitHub Pages e deixa o arquivo pronto para o link antigo.
- `.nojekyll` faz o GitHub Pages servir os arquivos como estão, sem processar nada.
- `testes/` tem testes automáticos em Python + Playwright (ver abaixo).
- `docs/` guarda o estado, o plano e o histórico; `docs/img/` tem a imagem do README.

### Mapa do `index.html` (procure pelos marcadores `/* ==== ... ==== */`)

| Seção | O que tem |
| - | - |
| campo | constantes do mundo (W=1920 × H=810, GROUND_Y=716), `DEF` (física padrão), `T` (valores atuais) |
| áudio | `Snd`: síntese em tempo real (WebAudio), sem arquivos de som |
| input / util / estado | teclado (`held`/`edge`), `G` (estado global), `mkPlayer`, `mkBall`, `newMatch`, `demoMatch` |
| física: jogador | `stepPlayer` (corrida, pique e fôlego, pulo, chute, domínio, armar o especial), `updateLeg`, voleio de lado (`volleyRel`), raio da cabeça de cada um (`rHead`, `HO(p)`) |
| física: bola | `resolveBall`, `ballWorld` (gravidade, arrasto, curva do voleio no ar, travessão), `ball.fx` (bola de especial) |
| contatos jogador × bola | `kickCheck` (cavadinha `chipLaunch` e voleio, bônus embalado), `controlCheck` (domínio), `bodyCheck`, `conduct` |
| especiais | `SPECIAL` (catálogo), barra (`charge`), `armSpecial`, `specialTick`, `fireFolha`/`fireBici`/`biciStrike`/`fireCaneta`/`fireMuralha`, `ballSpecial` (queda da folha seca, rolada da caneta) |
| CPU | `aiInput` (força em escala contínua, ver `aiParams`/`AI_ANCH`), `aiSpecialWant`/`dangerFor` (quando usar o especial) |
| fluxo da partida | `update` (passo fixo de 1/120 s), gol e nome do lance (`goalCall`, `KIND_TXT`), fim de jogo, resumo (`matchStats`), morte súbita, empate na carreira |
| treino | `TRAIN` (os passos), `startTrain`, `trainSetup`/`trainTick`/`trainEvent`, painel `drawTrain` |
| menu / render | menu do canvas, `render`, campos (`STAGES`, `paintVarzea`, `paintStadium`), jogador (`drawPlayer`, cabelos e acessórios), bola, HUD |
| loop | `layout` (proporção, faixas de placar e de gramado, modo toque), `resize`, `frame`, interpolação, medidor de fps, resolução dinâmica |
| visual do jogador e clubes / salvamento / carreira / interface | catálogos (`SHOP`, `SKINS`, `CLUBS`, `TIERS`), `SAVE` (localStorage + conta), temporadas, partidas da carreira, telas HTML (`SCREENS`, `ACT`) |
| painel | `SPEC`: sliders do painel de ajuste (cada parâmetro novo de física entra aqui e em `DEF`) |
| UI / toque / boot | botões do topo, controles de toque, controle de Xbox (`padPoll`/`padNav`: vira "teclas" `GP0L`, `GP0J`... lidas em `humanInput`; `GPAD` = controle em uso), `initOwner` (painel só para o dono), gancho de depuração `window.__arena`, `start` |

## Regras do projeto

- Continua sendo um arquivo único autocontido. Nada de bundler, framework ou script externo.
- Textos do jogo em português do Brasil.
- Clubes, campeonatos e marcas sempre inventados (a copa continental é a "Liga Suprema"). Nada de nomes, escudos ou marcas reais.
- Personagens originais; não copiar o visual do Head Soccer.
- Preferências de jogo já decididas: sem atraso nem tremor de câmera no contato com a bola, sem câmera lenta no gol, apito mínimo, nada de especial genérico: cada personagem tem o seu (catálogo `SPECIAL`).
- Personagens: elenco fixo no amistoso e nos adversários da carreira (v0.15); na carreira, o cabeçudo do vestiário libera e escolhe especiais. Atributos de cada jogador ficam em `p.attr` (multiplicadores sobre `DEF`).
- Física: os valores padrão ficam em `DEF` e só mudam quando o Estêvan pedir (ele ajusta pelo painel e manda o bloco "física vX"). Parâmetro novo: acrescentar em `DEF` e em `SPEC`.
- Salvamento (`SAVE`, formato v1): nunca usar arrays dentro de arrays (o banco da conta do claude.ai não aceita). Rodadas da tabela ficam como texto ("0-3,1-2").
- Versão pública: fora do computador (GitHub Pages ou link do claude.ai) aparece só o jogo, sem painel, hitboxes e notas. Aberto localmente (`file://` ou localhost), o painel aparece.
- Gancho `window.__arena` é usado pelos testes; mantenha os campos que eles leem.

## Testes

Pré-requisito (uma vez): `pip install -r testes/requirements.txt` e depois `python -m playwright install chromium`.

```
python testes/carreira.py   # carreira inteira (27 jogos), empate, eliminação, abandono, vestiário, salvamento
python testes/fisica.py     # pique e fôlego, condução, domínio perfeito, voleio embalado
python testes/telas.py      # tela cheia 16:9 / 16:10 / 21:9, toque no celular e tablet, versão pública
python testes/treino.py     # treino guiado, nome do lance, resumo, pausa, opinião, estreia fácil
python testes/especiais.py  # barra, folha seca, bicicleta, caneta, muralha, CPU, carreira, botão de toque, painel
python testes/controle.py   # controle de Xbox simulado: menu, partida, pausa, vestiário, carreira, celular, 2 controles
```

`comum.abrir()` marca o treino como já oferecido (`treino_visto=True`), senão a primeira partida para na pergunta do treino. Cada teste imprime OK/FALHOU por verificação e salva capturas em `testes/capturas/` (fora do git). Olhe as capturas quando mexer em desenho.

Em `especiais.py`, a verificação "CPU contra CPU (fundo do menu)" depende de sorteio: se só ela falhar, rode de novo antes de investigar.

## Começo e fim de cada sessão

O Estêvan pode trabalhar de mais de uma máquina (ou pelo Claude Code na web), então o GitHub é o ponto de encontro. Os pedidos de cada versão estão em `docs/plano.md`, seção "Pedidos prontos".

- No começo: `git pull`. Se houver uma branch de versão em andamento (`git branch -a`, nome `vX.Y`), continue nela (`git switch vX.Y`).
- Versão em andamento fica na branch `vX.Y`, com commit e push dela no fim de cada sessão. O GitHub Pages só publica a `main`, então nada disso chega aos amigos.
- Mudança só nos docs, sem mexer no jogo, pode ir direto para a `main`.
- Máquina nova: o e-mail dos commits fica na configuração local do git, que não vem com o clone. Antes do primeiro commit, confira `git config user.email`: deve ser `284153649+estevanrigon@users.noreply.github.com` (nome: Estêvan). Para os testes, instale as dependências (ver "Testes").

## Fechar e publicar uma versão ("fecha e publica")

1. Rodar os seis testes; todos OK.
2. Atualizar o número da versão em três lugares do `index.html`: a tagline no topo, a constante `VERSION` no começo do script (usada no bloco "física vX" e no texto de opinião) e o rodapé "Nesta versão".
3. Atualizar os docs: `historico.md` (o que entrou), `estado.md` (o que mudou no funcionamento), `plano.md` (marcar o que foi feito) e a "Versão atual" aqui em cima.
4. Commit na branch da versão com a mensagem "vX.Y: resumo" e juntar na `main` (`git switch main`, `git merge vX.Y`).
5. `git push` da `main` (o GitHub Pages publica sozinho em cerca de um minuto) e apagar a branch da versão, aqui e no GitHub.

## Link antigo do claude.ai

https://claude.ai/artifact/HE4S84cr7yxv7db5mkoL5G está parado na v0.14. Ele declara as capacidades `db` e `user`, então ali a carreira do dono também fica salva na conta. Só republique se o Estêvan pedir: numa sessão nova, a ferramenta de artifacts obriga a ler o jogo inteiro e a versão no ar inteira (mais de 150 mil tokens). Nesse caso, publique o `index.html` na URL, sem mudar as capacidades.
