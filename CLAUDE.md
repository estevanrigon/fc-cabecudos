# FC Cabeçudos

Jogo de futebol de cabeça 1x1 (inspirado no Head Soccer, com identidade própria), feito em HTML + Canvas num arquivo só. O dono é o Estêvan; responda em português do Brasil, com tuteio ("podes", "queres").

- Jogo publicado: https://claude.ai/artifact/HE4S84cr7yxv7db5mkoL5G (o link que os amigos recebem; viewers veem cada nova versão na hora)
- Versão atual: v0.12
- Estado detalhado, decisões e números: @docs/estado.md
- Histórico de versões: @docs/historico.md
- Plano de ação (fases, ordem sugerida e decisões pendentes): docs/plano.md

## Como o projeto é organizado

- `index.html` é o jogo inteiro: HTML, CSS e JavaScript juntos, sem build e sem dependências (só as fontes do Google Fonts). Abrir com dois cliques já roda.
- O arquivo começa com o "esqueleto" que o claude.ai acrescenta ao publicar (`<!doctype html>...<body>`). Mantenha esse esqueleto como está: na hora de republicar, a ferramenta reconhece e substitui.
- `testes/` tem testes automáticos em Python + Playwright (ver abaixo).
- `docs/` guarda o estado do projeto e o histórico.

### Mapa do `index.html` (procure pelos marcadores `/* ==== ... ==== */`)

| Seção | O que tem |
| - | - |
| campo | constantes do mundo (W=1920 × H=810, GROUND_Y=716), `DEF` (física padrão), `T` (valores atuais) |
| áudio | `Snd`: síntese em tempo real (WebAudio), sem arquivos de som |
| input / util / estado | teclado (`held`/`edge`), `G` (estado global), `mkPlayer`, `mkBall`, `newMatch`, `demoMatch` |
| física: jogador | `stepPlayer` (corrida, pique e fôlego, pulo, chute, domínio), `updateLeg`, voleio de lado (`volleyRel`) |
| física: bola | `resolveBall`, `ballWorld` (gravidade, arrasto, curva do voleio no ar, travessão) |
| contatos jogador × bola | `kickCheck` (cavadinha `chipLaunch` e voleio, bônus embalado), `controlCheck` (domínio), `bodyCheck`, `conduct` |
| CPU | `aiInput` (força em escala contínua, ver `aiParams`/`AI_ANCH`) |
| fluxo da partida | `update` (passo fixo de 1/120 s), gol, fim de jogo, morte súbita, empate na carreira |
| menu / render | menu do canvas, `render`, campos (`STAGES`, `paintVarzea`, `paintStadium`), jogador (`drawPlayer`, cabelos e acessórios), bola, HUD |
| loop | `layout` (proporção, faixas de placar e de gramado, modo toque), `resize`, `frame`, interpolação, medidor de fps, resolução dinâmica |
| visual do jogador e clubes / salvamento / carreira / interface | catálogos (`SHOP`, `SKINS`, `CLUBS`, `TIERS`), `SAVE` (localStorage + conta), temporadas, partidas da carreira, telas HTML (`SCREENS`, `ACT`) |
| painel | `SPEC`: sliders do painel de ajuste (cada parâmetro novo de física entra aqui e em `DEF`) |
| UI / toque / boot | botões do topo, controles de toque, `initOwner` (painel só para o dono), gancho de depuração `window.__arena`, `start` |

## Regras do projeto

- Continua sendo um arquivo único autocontido. Nada de bundler, framework ou script externo.
- Textos do jogo em português do Brasil.
- Clubes, campeonatos e marcas sempre inventados (a copa continental é a "Liga Suprema"). Nada de nomes, escudos ou marcas reais.
- Personagens originais; não copiar o visual do Head Soccer.
- Preferências de jogo já decididas: sem atraso nem tremor de câmera no contato com a bola, sem câmera lenta no gol, apito mínimo, especial genérico desligado (`SPECIALS=false`, cada personagem terá o seu).
- Física: os valores padrão ficam em `DEF` e só mudam quando o Estêvan pedir (ele ajusta pelo painel e manda o bloco "física vX"). Parâmetro novo: acrescentar em `DEF` e em `SPEC`.
- Ao fechar uma versão: atualizar o número em três lugares (tagline no topo, `'física vX'` no `dumpValues` e o rodapé "Nesta versão"), mais `docs/historico.md` e `docs/estado.md`.
- Salvamento (`SAVE`, formato v1): nunca usar arrays dentro de arrays (o banco da conta não aceita). Rodadas da tabela ficam como texto ("0-3,1-2").
- O artifact publicado declara as capacidades `db` e `user` (salvamento na conta). Quem não é dono vê a versão pública (sem painel, hitboxes e notas). Aberto localmente (`file://` ou localhost), o painel aparece.
- Gancho `window.__arena` é usado pelos testes; mantenha os campos que eles leem.

## Testes

Pré-requisito (uma vez): `pip install -r testes/requirements.txt` e depois `python -m playwright install chromium`.

```
python testes/carreira.py   # carreira inteira (27 jogos), empate, eliminação, abandono, vestiário, salvamento
python testes/fisica.py     # pique e fôlego, condução, domínio perfeito, voleio embalado
python testes/telas.py      # tela cheia 16:9 / 16:10 / 21:9, toque no celular e tablet, versão pública
```

Cada teste imprime OK/FALHOU por verificação e salva capturas em `testes/capturas/`. Rode os três antes de considerar uma versão pronta, e olhe as capturas quando mexer em desenho.

## Publicar uma versão nova

O link compartilhado só muda quando o `index.html` é publicado no artifact acima. Se a ferramenta de artifacts estiver disponível nesta sessão, publique o `index.html` na URL do artifact (atualizar no lugar, sem mudar as capacidades). Se não estiver, avise o Estêvan: ele abre o projeto "Head Soccer" no Cowork e pede para publicar o `index.html` desta pasta.

## Pendências conhecidas

- Especial de cada personagem (ideia: domínio perfeito também carrega a barra; ativar tocando na barra).
- Campos novos para os degraus de cima (hoje: várzea nos dois primeiros, estádio noturno nos três últimos).
- Talvez: atributos do jogador evoluindo na carreira; CPU ainda não usa domínio.
- Oferecido e não pedido: "código de salvamento" para levar a carreira de um aparelho para outro.
