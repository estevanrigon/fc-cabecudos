# Histórico de versões

Resumo do que cada versão trouxe, na ordem em que foi pedida. As versões até a v0.12 foram feitas em conversas no Cowork (projeto "Head Soccer").

## v0.1 a v0.4: física
- Protótipo jogável em HTML + Canvas: dois bonecos, bola, gols, CPU e painel de ajuste com sliders.
- Bonecos só com cabeça e pé; bola menor e campo maior, para ficar mais perto do Head Soccer.
- Os valores que o Estêvan achou no painel viraram o padrão ("física v0.3").
- Sem atraso nem tremor de câmera no contato com a bola; campo mais largo e gol menor.
- Sem câmera lenta no gol. Dois chutes: cavadinha (bola alta) e voleio (forte e quase reto).

## v0.5 e v0.6: voleio e domínio
- Animação própria do voleio; voleio no ar com bônus de força e saída mais baixa, com leve curva para cima.
- Especial genérico desligado (cada personagem terá o seu).
- A bola não fica mais parada em cima do gol.
- Teclas F (cavadinha), G (voleio) e H (domínio). O domínio muda pelo ângulo da bola: sola, parte interna, coxa e peito, com janela de tempo e "perfeito".

## v0.7 e v0.8: sensação de jogo
- Cavadinha calculada por altura e distância do arco; recuando sai mais cavada, avançando sai mais direta.
- Gráficos melhores e sons sintetizados; o som da cabeçada não metralha ao fazer embaixadinha.
- O relógio só começa no primeiro toque; reposição de bola aleatória; apito mínimo; grito de esforço no voleio no ar.

## v0.9: identidade
- Nome FC Cabeçudos, escudo, fonte Lilita One e cores próprias.
- Campos: várzea ao entardecer (principal) e estádio noturno.
- Voleio com o pé virado de lado, vindo pela lateral.

## v0.10: domínio perfeito, pique e toque
- Domínio perfeito deixa o próximo voleio embalado (+15% de força por 0,8 s; não vale para a cavadinha).
- Pique com fôlego (Shift esquerdo), toques mais longos na condução, domínio pior correndo contra a bola. A CPU também usa.
- Controles de toque refeitos: trilha de deslizar (ponta = pique) e quatro botões, numa faixa abaixo da linha do chão.

## v0.11: carreira e vestiário
- Carreira em cinco degraus, da Copa da Vila (várzea) até a final da Liga Suprema, com tabela, mata-mata e propostas de clubes.
- Vestiário com loja de moedas; faixa de capitão e chuteira dourada só com título.
- Progresso salvo na conta (e no navegador).

## v0.12: versão pública, tela cheia e 120 Hz
- Quem abre pelo link vê só o jogo; o painel fica para o dono ("Ver como jogador" para conferir).
- Tela cheia sem achatar em qualquer monitor, com o placar numa faixa própria acima do campo.
- Desenho interpolado entre os passos da física (liso em 120 Hz ou mais); tecla 3 mostra os fps; resolução cai sozinha em aparelho fraco.
- Aberto direto do computador (arquivo local), o painel de ajuste aparece.

## v0.13: primeiros minutos
Primeira versão feita com o Claude Code, na pasta local (com git a partir daqui).
- Treino guiado em 8 passos (andar, pique, cabeçada, cavadinha, voleio, voleio no ar, domínio, voleio embalado), sem adversário em campo. Oferecido uma vez, na primeira partida de quem abre o jogo, e sempre disponível no menu. Dá para pular passos (Enter ou "pular").
- Nome do lance embaixo do "GOL!": de cabeça, de voleio, voleio no ar, voleio embalado, de cavadinha, de chapa/coxa/peito/sola (depois do domínio), de bico, com bola e tudo; e de longe, no ângulo, no travessão e entrou, do meio-campo. Gol do meio-campo ou voleio no ar de longe vira "GOLAÇO!". Gol contra tem letreiro próprio.
- Resumo da partida no fim do jogo (e na tela de resultado da carreira): chutes, posse de bola, domínios perfeitos e chute mais forte em km/h.
- Pausa mostra os controles (teclado ou botões de toque) e uma dica; a tabela da carreira também mostra uma dica.
- A estreia na carreira é sempre contra o adversário mais fraco da Copa da Vila.
- "Mandar opinião" no menu e no resultado da carreira: texto pronto (comentário, versão, aparelho e última partida) para copiar ou mandar pelo WhatsApp.
- Testes: novo `testes/treino.py`.

## v0.14: personagens e especiais (primeira parte)
Formato decidido pelo Estêvan: elenco fixo de personagens (v0.15) e, na carreira, o cabeçudo do vestiário liberando especiais.
- Barra do especial na plaquinha de cada lado do placar. Enche com chute ou cabeçada (+6%), domínio (+5%), domínio perfeito (+20%) e gol sofrido (+30%); do terceiro toque seguido do mesmo jogador em diante vale menos, para a embaixadinha não encher a barra sozinha.
- Com a barra cheia, Espaço (jogador 2: Ç ou Num 4) ou o botão ★ do toque arma o especial por até 1,5 s; ele sai sozinho quando a bola chega no ponto. Se não sair, a barra continua cheia.
- Quatro especiais: **folha seca** (sobe alto e despenca na boca do gol), **bicicleta** (pulo com cambalhota e bomba no gol, com a bola no alto), **caneta** (a bola passa por entre as pernas do adversário, ele fica tonto e tu atravessas junto) e **muralha** (cabeça 1,8× maior por 3 s).
- Gol de especial ganha nome: "DE FOLHA SECA", "DE BICICLETA" (sempre golaço), "DE CANETA" e "DEPOIS DA CANETA".
- A CPU usa o especial na hora certa: folha seca longe do gol com o goleiro adiantado, bicicleta perto do gol, caneta com o adversário na frente, muralha contra especial ou bola perigosa. CPU fraca demora mais para perceber.
- Amistoso: linha "Especial ‹ ›" no menu para escolher qualquer um; o adversário sorteia o dele. Revanche mantém os especiais.
- Carreira: o primeiro especial é escolhido na criação; título ou acesso da Copa da Vila, da Copa Regional e da Segunda Divisão libera o próximo. Aba "Especial" no vestiário para trocar. A tabela mostra o teu especial e o do adversário. Carreira antiga ganha um especial por degrau já vencido.
- Treino com um 9º passo (especial); dicas novas; "Especiais" no resumo da partida; grupo "Especiais" no painel.
- Por baixo: cada jogador tem atributos (velocidade, pulo, chute, tamanho da cabeça), todos 1 por enquanto, prontos para o elenco da v0.15. O especial genérico antigo (`SPECIALS`, `tryPower`) saiu.
- Testes: novo `testes/especiais.py`.
