# FC Cabeçudos: estado do protótipo

Jogo publicado (sempre atualizar este link): https://claude.ai/artifact/HE4S84cr7yxv7db5mkoL5G, versão v0.14 (publicada em 05/11/2026). Arquivo único HTML + Canvas (`index.html` nesta pasta). Capacidades declaradas no artifact: db e user (salvamento da carreira em data/users/<id>/save, privado de cada jogador, com cópia em localStorage; vale o salvamento mais recente).

Este arquivo espelha o documento "claude/fc-cabecudos-estado.md" do projeto Head Soccer no claude.ai. Ao mudar algo importante aqui, vale avisar o Estêvan para atualizar lá também (ou atualizar pelo Cowork).

## Pasta local
- Fica em Documentos\FC Cabecudos, no computador do Estêvan (desk-est, Windows 11). Criada em 05/11/2026 para trabalhar com o Claude Code.
- Testes: `python testes/carreira.py`, `python testes/fisica.py`, `python testes/telas.py`, `python testes/treino.py`, `python testes/especiais.py`, `python testes/controle.py` (Playwright + Chromium; Python 3.12 instalado para o usuário em 05/11/2026).
- Git iniciado em 05/11/2026 (branch main, primeiro commit = v0.12).
- Plano de ação com as próximas versões: `docs/plano.md`.

## Personagens e especiais (v0.14)
- Formato decidido pelo Estêvan (05/11/2026): os dois. Elenco fixo de personagens originais, cada um com atributos e especial próprio, usado no amistoso e pelos adversários da carreira (fica para a v0.15). O jogador da carreira é o cabeçudo do vestiário: escolhe o primeiro especial ao criar a carreira e libera os outros com título ou acesso da Copa da Vila, da Copa Regional e da Segunda Divisão (na ordem folha seca, bicicleta, caneta, muralha, pulando o que já tem); troca qual usar na aba "Especial" do vestiário.
- Especiais aprovados: folha seca (chute de longe que sobe a folhaH e despenca a folhaDist da boca do gol, entrando a ~45% da altura do gol), bicicleta (pulo calculado para a cabeça encontrar a bola, cambalhota, chute de biciPow mirando a ~38% da altura do gol), caneta (bola rola por entre as pernas, freia canetaDist atrás do adversário; ele fica canetaTonto segundos tonto; quem dribla atravessa junto) e muralha (cabeça muraMul× por muraTime segundos).
- Barra: chute/cabeçada specKick, domínio specCtrl, domínio perfeito specPerf, gol sofrido specGoal; do 3º toque seguido do mesmo jogador em diante, × specStreak. Cabeçada só conta com a bola chegando a 150 px/s ou mais. A barra continua entre os gols e zera a cada partida.
- Disparo: tecla Espaço (jogador 2: Ç ou Num 4) ou botão ★ (toque) com a barra cheia arma por specArm segundos; sai sozinho quando a bola chega no ponto (folha seca e caneta: bola no pé; caneta: adversário na frente, a até 460 px; bicicleta: bola acima da cabeça a até biciRange). Muralha sai na hora. Se não sair, a barra continua cheia.
- CPU: cada adversário da carreira tem um especial sorteado pelo nome do clube (até o elenco chegar); no amistoso, sorteado a cada partida. Reação pela força (specDelay de 1 s na mais fraca a 0,08 s na mais forte); segura o chute comum enquanto espera a hora do especial.
- Salvamento (v1): `profile.owned.spec` (lista de textos), `profile.look.spec` (o escolhido para a carreira), `profile.fspec` (o do amistoso), `career.season.newSpec` (o liberado naquela temporada). Salvamento antigo com carreira ganha 1 + um por degrau já vencido.
- Base para a v0.15: `mkPlayer` recebe o especial e cada jogador tem `attr` (spd, jump, kick, head; todos 1) e `hrK` (escala da cabeça); `rHead(p)` dá o raio da cabeça de cada um.

## Controle de Xbox (v0.14)
- Gamepad API, layout padrão: analógico ou direcional anda, A pula, X cavadinha, B voleio, Y domínio, RT/LT pique, RB/LB especial, Menu pausa, Exibir (treino: pula o passo; pausa: menu ou abandonar). Pausa: A volta, Y reinicia o amistoso. Fim do amistoso: A revanche, B menu. Telas HTML: direcional move o foco (o botão mais próximo naquela direção), A aperta, B volta, LB/RB trocam a aba do vestiário.
- Primeiro controle = jogador 1; no modo 2 jogadores, o segundo controle é o jogador 2 (com um controle só, o jogador 2 continua no teclado). O botão que veio apertado de uma tela (o A que começou a partida) só vale depois de solto.
- No celular, controle em uso esconde os botões da tela e a faixa deles (o campo cresce); tocar na tela traz de volta. Com dois controles, o "2 jogadores" aparece no menu do toque.
- Não confirmado no link publicado: o claude.ai mostra o jogo dentro de um quadro, e o navegador pode bloquear o controle ali. Testado só com controle simulado (`testes/controle.py`).

## Primeiros minutos (v0.13)
- Treino guiado: 8 passos sem adversário (o P2 fica como "fantasma", fora do campo e sem colisão). Oferecido uma vez (`SAVE.profile.tut`: 1 = oferecido, 2 = concluído) na primeira vez que a pessoa escolhe Carreira ou Amistoso; sempre no menu.
- Nome do lance: o último toque fica em `ball.hit` (quem, tipo, de onde, se bateu no travessão). "De longe" a partir de 620 px do gol; "do meio-campo" de trás da linha do meio (80 px ou mais). Golaço: do meio-campo, ou de longe com voleio no ar, voleio embalado, cabeçada ou no ângulo.
- Resumo da partida: chutes (contato de cavadinha ou voleio), posse (tempo com o último toque), domínios perfeitos, chute mais forte (px/s × 0,048 = km/h, só para dar a ideia).
- Opinião: só texto copiado ou compartilhado pela própria pessoa (WhatsApp ou menu de compartilhar do celular); nada é enviado sozinho.

## Compartilhamento
- Para amigos: link público pelo menu de compartilhamento do artifact (só visualização). Quem abre por link público fica no nível "view" e não grava na conta: a carreira dele fica só no navegador (localStorage), separada da do Estêvan.
- Desde a v0.12, quem não é dono vê só o jogo (sem painel de ajuste, botão de hitboxes e notas de versão). O dono vê tudo e tem o botão "Ver como jogador" para conferir a versão pública. Aberto localmente (arquivo ou localhost), o painel aparece.
- Ideia oferecida e ainda não pedida: "código de salvamento" para levar a carreira de um aparelho para outro.

## Decisões de direção
- Nome FC Cabeçudos; carreira começando na várzea, dificuldade subindo; vários campos para torneios (várzea ao entardecer, estádio noturno).
- Personagens originais (não copiar Head Soccer). Especial genérico removido na v0.14: cada personagem tem o seu (ver "Personagens e especiais").
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
Especiais (v0.14, valores iniciais, ainda sem ajuste do Estêvan): specKick 0.06, specCtrl 0.05, specPerf 0.20, specGoal 0.30, specStreak 0.4, specArm 1.5, folhaH 440, folhaDist 330, biciPow 2500, biciRange 260, canetaDist 150, canetaTonto 0.9, muraMul 1.8, muraTime 3.

## Pendências
- Elenco de 8 personagens com atributos e especial próprio (v0.15); os adversários da carreira passam a usar o elenco.
- Ajustar os números dos especiais jogando (painel, grupo "Especiais").
- Campos novos para os degraus de cima (hoje: várzea nos dois primeiros, estádio noturno nos três últimos).
- Possível: atributos do jogador evoluindo na carreira; CPU ainda não usa domínio.
