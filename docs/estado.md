# FC Cabeçudos: estado do protótipo

Jogo publicado (sempre atualizar este link): https://claude.ai/artifact/HE4S84cr7yxv7db5mkoL5G, versão v0.12. Arquivo único HTML + Canvas (`index.html` nesta pasta). Capacidades declaradas no artifact: db e user (salvamento da carreira em data/users/<id>/save, privado de cada jogador, com cópia em localStorage; vale o salvamento mais recente).

Este arquivo espelha o documento "claude/fc-cabecudos-estado.md" do projeto Head Soccer no claude.ai. Ao mudar algo importante aqui, vale avisar o Estêvan para atualizar lá também (ou atualizar pelo Cowork).

## Pasta local
- Fica em Documentos\FC Cabecudos, no computador do Estêvan (desk-est, Windows 11). Criada em 05/11/2026 para trabalhar com o Claude Code.
- Testes: `python testes/carreira.py`, `python testes/fisica.py`, `python testes/telas.py` (Playwright + Chromium).

## Compartilhamento
- Para amigos: link público pelo menu de compartilhamento do artifact (só visualização). Quem abre por link público fica no nível "view" e não grava na conta: a carreira dele fica só no navegador (localStorage), separada da do Estêvan.
- Desde a v0.12, quem não é dono vê só o jogo (sem painel de ajuste, botão de hitboxes e notas de versão). O dono vê tudo e tem o botão "Ver como jogador" para conferir a versão pública. Aberto localmente (arquivo ou localhost), o painel aparece.
- Ideia oferecida e ainda não pedida: "código de salvamento" para levar a carreira de um aparelho para outro.

## Decisões de direção
- Nome FC Cabeçudos; carreira começando na várzea, dificuldade subindo; vários campos para torneios (várzea ao entardecer, estádio noturno).
- Personagens originais (não copiar Head Soccer). Especial genérico desligado: cada personagem terá o seu.
- Sem atraso ou tremor de câmera no contato com a bola; sem câmera lenta no gol; apito mínimo.
- Foco atual: um jogador (contra a CPU). Dois jogadores no mesmo tablet ficou para depois.
- Clubes e a copa continental com nomes inventados (nada de marcas reais). A copa final se chama Liga Suprema.

## Tela e desempenho (v0.12)
- O campo nunca estica: a largura manda e a sobra de altura vira faixa de placar em cima (o placar sai de cima do campo quando ela tem 90+ unidades) e gramado em sombra embaixo. Vale para tela cheia em qualquer monitor (16:9, 16:10, 21:9) e para o modo imersivo do toque.
- Física fixa a 120 passos por segundo; o desenho acompanha a taxa da tela (requestAnimationFrame) e interpola entre passos, então fica liso a 120/144 Hz. Tecla 3 mostra fps. Se o aparelho ficar abaixo de ~55 fps, a resolução interna cai até 60% (só reduz).

## Carreira (v0.11): escolhas do Estêvan
- Itens por moedas + loja; raros só por título. Carreira média (~27 jogos). Tabela + mata-mata (eliminado repete o torneio). Propostas de 3 clubes para escolher ao subir.
- Degraus: Copa da Vila (várzea, 4 times, final entre os 2 primeiros) → Copa Regional (grupo de 4 + semi + final) → Segunda Divisão (6 times, 2 sobem) → Primeira Divisão (8 times, 2 vão à Liga Suprema) → Liga Suprema (grupo de 4 + quartas + semi + final). Empate só na fase de pontos; mata-mata com morte súbita. Abandonar = derrota por 3 a 0.
- Força da CPU em escala contínua (0 a 1,15); amistoso fácil/normal/difícil = 0,35/0,65/0,95. Final da Liga Suprema = 1,08.
- Moedas por partida: vitória 100, empate 40, derrota 20, +15 por gol, +10 por domínio perfeito (até 10), × peso da competição (1; 1,5; 2; 3; 4) × bônus do contrato. Prêmio por título (300 a 3000) e metade pelo acesso. Propostas: luvas maiores ou bônus por partida (+15% ou +30%).
- Vestiário: 8 cortes de cabelo, 9 cores, 6 tons de pele, olhos, faixas (normal, sem, larga, bandana, capitão por título da Primeira Divisão), chuteiras (dourada por título da Liga Suprema), rosto (curativo, bigode, cavanhaque, barba, pintura), acessório (brinco, óculos), rastro do chute (fogo, neon, arco-íris). Loja inteira custa ~15,8 mil moedas.

## v0.10
- Domínio perfeito deixa o próximo voleio embalado: +15% de força por 0,8 s. Não vale para a cavadinha (ela é calculada por altura e distância; mais velocidade a faria passar por cima do gol).
- Pique com fôlego: Shift esquerdo (P2: Shift direito ou Num 0); ×1,45, fôlego cheio dura 2,2 s e recupera em 4 s. A CPU usa pique.
- Toque: trilha de deslizar na esquerda (ponta = pique), quatro botões na direita, controles numa faixa abaixo da linha do chão, tela inteira por padrão.

## Física padrão
pGrav 2740, jump 730, jumpCut 1, pSpeed 430, pAccel 20000, airCtl 1, headR 44, ballR 17, bGrav 800, bRest 0.82, bDrag 0.25, bRoll 0.35, magnus 0, chipH 330, chipD 900, chipMove 40, kickArc -10, drivePow 1900, driveAngle 3, driveAirMul 1.20, driveAirAngle -4, driveAirCurve 2800, driveArc 10, dribble 60, ctrlWindow 0.25, ctrlPerfect 0.12, ctrlCool 0.35, ctrlCoxa 50, ctrlPeito 78, boostMul 1.15, boostTime 0.8, sprintMul 1.45, stamina 2.2, stamRegen 4.0, sprintDribble 220, reach 72, headRest 0.70, headPop 0, headCarry 0.65, fieldW 1920, goalH 208, goalD 60, keeperDepth 100, matchTime 60.

## Pendências
- Especial de cada personagem (ideia: domínio perfeito também carrega a barra do especial; especial ativado tocando na barra).
- Campos novos para os degraus de cima (hoje: várzea nos dois primeiros, estádio noturno nos três últimos).
- Possível: atributos do jogador evoluindo na carreira; CPU ainda não usa domínio.
