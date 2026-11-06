# FC Cabeçudos: como o jogo funciona hoje

Estado da v0.14. Este é o único lugar para o funcionamento e as decisões já tomadas. O que falta fazer está em `plano.md`, o que cada versão trouxe está em `historico.md`, e os números da física estão em `DEF`, no `index.html`.

## Publicação e salvamento
- O link dos amigos é o GitHub Pages deste repositório, servido da branch `main` (endereço no README). Cada push na `main` publica.
- Salvamento: `SAVE`, formato v1, no localStorage (`fcc_save_v1`). No GitHub Pages, a carreira de cada um fica só no navegador dele.
- Versão pública: fora do computador, ninguém vê o painel de ajuste, o botão de hitboxes nem as notas de versão. Aberto localmente (arquivo ou localhost), o painel aparece, com o botão "Ver como jogador" para conferir a versão pública.
- Link antigo: https://claude.ai/artifact/HE4S84cr7yxv7db5mkoL5G, parado na v0.14 (publicada em 05/11/2026). Ele declara as capacidades `db` e `user`: o dono vê o painel e a carreira dele fica também na conta (data/users/<id>/save, privado; vale o salvamento mais recente). Quem abre pelo link público fica no nível "view" e salva só no navegador.

## Personagens e especiais (v0.14)
- Formato decidido pelo Estêvan (05/11/2026): os dois. Elenco fixo de personagens originais, cada um com atributos e especial próprio, usado no amistoso e pelos adversários da carreira (fica para a v0.15). O jogador da carreira é o cabeçudo do vestiário: escolhe o primeiro especial ao criar a carreira e libera os outros com título ou acesso da Copa da Vila, da Copa Regional e da Segunda Divisão (na ordem folha seca, bicicleta, caneta, muralha, pulando o que já tem); troca qual usar na aba "Especial" do vestiário.
- Especiais aprovados: folha seca (chute de longe que sobe a folhaH e despenca a folhaDist da boca do gol, entrando a ~45% da altura do gol), bicicleta (pulo calculado para a cabeça encontrar a bola, cambalhota, chute de biciPow mirando a ~38% da altura do gol), caneta (bola rola por entre as pernas, freia canetaDist atrás do adversário; ele fica canetaTonto segundos tonto; quem dribla atravessa junto) e muralha (cabeça muraMul× por muraTime segundos).
- Barra: chute/cabeçada specKick, domínio specCtrl, domínio perfeito specPerf, gol sofrido specGoal; do 3º toque seguido do mesmo jogador em diante, × specStreak. Cabeçada só conta com a bola chegando a 150 px/s ou mais. A barra continua entre os gols e zera a cada partida.
- Disparo: tecla Espaço (jogador 2: Ç ou Num 4) ou botão ★ (toque) com a barra cheia arma por specArm segundos; sai sozinho quando a bola chega no ponto (folha seca e caneta: bola no pé; caneta: adversário na frente, a até 460 px; bicicleta: bola acima da cabeça a até biciRange). Muralha sai na hora. Se não sair, a barra continua cheia.
- CPU: cada adversário da carreira tem um especial sorteado pelo nome do clube (até o elenco chegar); no amistoso, sorteado a cada partida. Reação pela força (specDelay de 1 s na mais fraca a 0,08 s na mais forte); segura o chute comum enquanto espera a hora do especial.
- Os números dos especiais ainda são os iniciais, sem ajuste do Estêvan (grupo "Especiais" do painel).
- Salvamento (v1): `profile.owned.spec` (lista de textos), `profile.look.spec` (o escolhido para a carreira), `profile.fspec` (o do amistoso), `career.season.newSpec` (o liberado naquela temporada). Salvamento antigo com carreira ganha 1 + um por degrau já vencido.
- Base para a v0.15: `mkPlayer` recebe o especial e cada jogador tem `attr` (spd, jump, kick, head; todos 1) e `hrK` (escala da cabeça); `rHead(p)` dá o raio da cabeça de cada um.

## Controle de Xbox (v0.14)
- Gamepad API, layout padrão: analógico ou direcional anda, A pula, X cavadinha, B voleio, Y domínio, RT/LT pique, RB/LB especial, Menu pausa, Exibir (treino: pula o passo; pausa: menu ou abandonar). Pausa: A volta, Y reinicia o amistoso. Fim do amistoso: A revanche, B menu. Telas HTML: direcional move o foco (o botão mais próximo naquela direção), A aperta, B volta, LB/RB trocam a aba do vestiário.
- Primeiro controle = jogador 1; no modo 2 jogadores, o segundo controle é o jogador 2 (com um controle só, o jogador 2 continua no teclado). O botão que veio apertado de uma tela (o A que começou a partida) só vale depois de solto.
- No celular, controle em uso esconde os botões da tela e a faixa deles (o campo cresce); tocar na tela traz de volta. Com dois controles, o "2 jogadores" aparece no menu do toque.
- Testado só com controle simulado (`testes/controle.py`). No claude.ai o jogo roda dentro de um quadro, e o navegador pode bloquear o controle ali; no GitHub Pages não há quadro.

## Primeiros minutos (v0.13)
- Treino guiado: 9 passos sem adversário (o P2 fica como "fantasma", fora do campo e sem colisão). Oferecido uma vez (`SAVE.profile.tut`: 1 = oferecido, 2 = concluído) na primeira vez que a pessoa escolhe Carreira ou Amistoso; sempre no menu.
- Nome do lance: o último toque fica em `ball.hit` (quem, tipo, de onde, se bateu no travessão). "De longe" a partir de 620 px do gol; "do meio-campo" de trás da linha do meio (80 px ou mais). Golaço: do meio-campo, bicicleta, ou de longe com voleio no ar, voleio embalado, cabeçada, folha seca ou no ângulo.
- Resumo da partida: chutes (contato de cavadinha ou voleio), posse (tempo com o último toque), domínios perfeitos, especiais usados, chute mais forte (px/s × 0,048 = km/h, só para dar a ideia).
- Opinião: só texto copiado ou compartilhado pela própria pessoa (WhatsApp ou menu de compartilhar do celular); nada é enviado sozinho.

## Carreira (v0.11)
- Itens por moedas + loja; raros só por título. Carreira média (~27 jogos). Tabela + mata-mata (eliminado repete o torneio). Propostas de 3 clubes para escolher ao subir.
- Degraus: Copa da Vila (várzea, 4 times, final entre os 2 primeiros) → Copa Regional (grupo de 4 + semi + final) → Segunda Divisão (6 times, 2 sobem) → Primeira Divisão (8 times, 2 vão à Liga Suprema) → Liga Suprema (grupo de 4 + quartas + semi + final). Empate só na fase de pontos; mata-mata com morte súbita. Abandonar = derrota por 3 a 0. A estreia é sempre contra o adversário mais fraco da Copa da Vila.
- Força da CPU em escala contínua (0 a 1,15); amistoso fácil/normal/difícil = 0,35/0,65/0,95. Final da Liga Suprema = 1,08.
- Moedas por partida: vitória 100, empate 40, derrota 20, +15 por gol, +10 por domínio perfeito (até 10), × peso da competição (1; 1,5; 2; 3; 4) × bônus do contrato. Prêmio por título (300 a 3000) e metade pelo acesso. Propostas: luvas maiores ou bônus por partida (+15% ou +30%).
- Vestiário: 8 cortes de cabelo, 9 cores, 6 tons de pele, olhos, faixas (normal, sem, larga, bandana, capitão por título da Primeira Divisão), chuteiras (dourada por título da Liga Suprema), rosto (curativo, bigode, cavanhaque, barba, pintura), acessório (brinco, óculos), rastro do chute (fogo, neon, arco-íris). Loja inteira custa ~15,8 mil moedas.
- Campos: várzea nos dois primeiros degraus, estádio noturno nos três últimos.

## Domínio perfeito e pique (v0.10)
- Domínio perfeito deixa o próximo voleio embalado: +15% de força por 0,8 s. Não vale para a cavadinha (ela é calculada por altura e distância; mais velocidade a faria passar por cima do gol).
- Pique com fôlego: Shift esquerdo (P2: Shift direito ou Num 0); ×1,45, fôlego cheio dura 2,2 s e recupera em 4 s. A CPU usa pique.
- Toque: trilha de deslizar na esquerda (ponta = pique), botões na direita, controles numa faixa abaixo da linha do chão, tela inteira por padrão.

## Tela e desempenho (v0.12)
- O campo nunca estica: a largura manda e a sobra de altura vira faixa de placar em cima (o placar sai de cima do campo quando ela tem 90+ unidades) e gramado em sombra embaixo. Vale para tela cheia em qualquer monitor (16:9, 16:10, 21:9) e para o modo imersivo do toque.
- Física fixa a 120 passos por segundo; o desenho acompanha a taxa da tela (requestAnimationFrame) e interpola entre passos, então fica liso a 120/144 Hz. Tecla 3 mostra fps. Se o aparelho ficar abaixo de ~55 fps, a resolução interna cai até 60% (só reduz).

## Decisões de direção
- Nome FC Cabeçudos; carreira começando na várzea, dificuldade subindo; vários campos para torneios (várzea ao entardecer, estádio noturno).
- Personagens originais (não copiar Head Soccer). Nada de especial genérico: cada personagem tem o seu.
- Sem atraso ou tremor de câmera no contato com a bola; sem câmera lenta no gol; apito mínimo.
- Foco atual: um jogador contra a CPU.
- Clubes e a copa continental com nomes inventados (nada de marcas reais). A copa final se chama Liga Suprema.
- Física: os valores padrão ficam em `DEF` e só mudam quando o Estêvan manda o bloco "física vX" do painel.
