# Plano de ação: do protótipo a um jogo legal de verdade

Feito em 05/11/2026, a partir da v0.12, lendo o código e os docs (sem rodada de jogo nesta análise).

Legenda: **P** = um pedido curto · **M** = uma sessão de trabalho · **G** = várias sessões · ❓ = precisa da tua decisão antes.

## Onde o jogo está

**Já está bom:** física ajustada à mão (cavadinha, voleio, domínio, pique), desempenho (120 Hz, resolução que se ajusta), carreira completa em cinco degraus, vestiário com loja, controles de toque, salvamento na conta.

**O que falta para ficar legal de verdade:**

1. **Todo mundo joga igual.** Os dois bonecos têm a mesma física; o rival só muda de cara. Não há personagens, atributos nem especiais, e é isso que mais faz falta num jogo desse gênero.
2. **Quem abre pela primeira vez não sabe jogar.** Não tem treino. No celular as teclas nem aparecem, e a diferença entre cavadinha, voleio e domínio só se descobre tentando.
3. **A CPU é previsível.** Ela segue a bola, chuta e pula, mas não domina, não tem estilo próprio e não muda de plano pelo placar. Depois de algumas partidas dá para achar o "jeito" de ganhar sempre.
4. **Pouca variedade.** Dois campos, um formato de partida, e a carreira acaba depois de uns 27 jogos ("Defender o título" só repete a Liga Suprema).
5. **Som sem trilha.** Os efeitos são bons, mas não há música nem torcida reagindo ao lance; o silêncio entre as jogadas deixa a partida fria.
6. **Nada para fazer com os amigos.** O link é para jogar sozinho; não dá para comparar resultado nem desafiar ninguém.
7. **Sem rede de segurança.** A pasta ainda não tem git: se uma mudança estragar algo, não há como voltar.

## Fase 0: fundação (antes de tudo)

- [ ] Iniciar o git e fazer o primeiro commit, para cada versão virar um ponto de volta. **P**
- [ ] Instalar e rodar os três testes; guardar as capturas como referência. **P**
- [ ] Rodada com 3 a 5 amigos: mandar o link, pedir que joguem 10 minutos sem explicação e contem onde travaram, o que acharam chato e do que mais gostaram. Assistir alguém jogando vale ainda mais. **P** (do teu lado)
- [ ] Botão "Mandar opinião" no fim da partida, que copia um texto pronto (versão, placar, aparelho) para colar no WhatsApp. **P**

## Fase 1: os primeiros 5 minutos

Objetivo: quem abre o link entende os controles e faz um gol bonito no primeiro minuto.

- [ ] Treino guiado curto: mover, pular, cabeçada, cavadinha, voleio, domínio, domínio perfeito + voleio embalado. Cada passo com um alvo no campo e opção de pular. **M**
- [ ] Oferecer o treino na primeira vez que alguém abre o jogo, e deixar no menu depois. **P**
- [ ] Mostrar os controles na tela de pausa (hoje só aparecem embaixo do campo, no computador). **P**
- [ ] Dicas curtas no "PREPARAR" e na pausa ("domínio perfeito deixa o voleio 15% mais forte"). **P**
- [ ] Estreia da carreira sempre contra o adversário mais fraco da Copa da Vila. **P**
- [ ] Dar nome ao lance embaixo do "GOL!": de cabeça, de voleio, de cavadinha, de longe, no ângulo, no rebote da trave. **P**
- [ ] Resumo no fim da partida: chutes, gols por tipo, domínios perfeitos, chute mais forte. **P/M**

## Fase 2: personagens e especiais (a identidade do jogo)

É a pendência mais antiga e a que mais muda a sensação de cada partida.

- [ ] ❓ Decidir o formato: (a) elenco de personagens fixos, cada um com atributos e especial; (b) o teu jogador da carreira escolhe um especial e vai desbloqueando outros; ou (c) os dois (carreira com o teu cabeçudo, amistoso com o elenco).
- [ ] Barra do especial: carrega com toques na bola, domínios perfeitos e gols sofridos; ativa tocando na barra ou numa tecla. **M**
- [ ] Primeiros quatro especiais, bem diferentes entre si e com cara de futebol brasileiro. Ideias: **folha seca** (sobe e despenca na frente do gol), **bicicleta** (salto automático e chute por cima da cabeça), **caneta** (a bola atravessa o adversário), **muralha** (cabeça gigante por 3 s), **pombo sem asa** (rasteiro fortíssimo). **M** cada
- [ ] Atributos por personagem (velocidade, pulo, força do chute, tamanho da cabeça), com diferenças pequenas para não desequilibrar. **M**
- [ ] Elenco de 8 personagens originais (nome, visual, especial); os adversários da carreira passam a usar o elenco. **G**
- [ ] CPU usando o especial na hora certa. **P/M**
- [ ] Números de cada especial em `DEF` e `SPEC`, para ajustares no painel. **P**

## Fase 3: CPU com cabeça

- [ ] Estilos de CPU: atacante (pressiona), retranqueiro (fica no gol), cavador (abusa da cavadinha), equilibrado. Cada clube recebe um. **M**
- [ ] CPU usando o domínio, e o voleio embalado nos níveis altos (pendência). **M**
- [ ] CPU reagindo ao placar: perdendo no fim, se arrisca; ganhando, segura. **P**
- [ ] Defesa melhor: voltar para o gol em bola alta e não ficar vendida na cavadinha. **M**
- [ ] Caçar as jogadas que sempre funcionam contra a CPU (teste automático medindo de onde saem os gols) e fechar as brechas. **M**
- [ ] Simular a carreira com CPU contra CPU para conferir a curva de dificuldade de cada degrau. **M**

## Fase 4: variedade de partida

- [ ] Campos novos para os degraus de cima (pendência): estádio de dia lotado para as divisões, estádio continental para a Liga Suprema. **M** cada
- [ ] Campos para amistoso: praia, quadra de rua, terrão na chuva. **M** cada
- [ ] ❓ Terreno e clima mexendo na física (chuva: bola escorrega; areia: quica menos; vento leve). Parâmetros novos em `DEF` e `SPEC`. **M**
- [ ] ❓ Itens que caem no campo e dão um efeito curto a quem tocar primeiro (comum no gênero; com itens próprios, tipo bola de chiclete ou chuteira de mola). **M/G**
- [ ] Modos rápidos no menu: primeiro a 5 gols, morte súbita direto, torneio rápido de mata-mata com troféu. **M**
- [ ] Desafios com prêmio em moedas: "3 gols de voleio", "ganhar sem sofrer gol", "5 domínios perfeitos". **M**
- [ ] Modo festa para 2 jogadores: cabeção, bola pesada, gol pequeno, gravidade baixa (só amistoso). **M**

## Fase 5: carreira que prende

- [ ] ❓ Atributos do jogador evoluindo com treinos ou moedas (pendência), com teto para a física não sair do controle. **M**
- [ ] Depois do título da Liga Suprema: um "Mundial" com adversário chefe e temporadas de lenda na força máxima, com recompensas novas. **M**
- [ ] Rival de carreira: um adversário que reaparece em vários degraus, com comemoração própria. **M**
- [ ] Manchetes entre as rodadas ("Cabeçudo decide no fim e o Poeirão perde a ponta"). **P/M**
- [ ] Armário de troféus, com uma taça diferente por competição. **M**
- [ ] Mais coisas no vestiário: uniformes alternativos, comemorações de gol, efeitos de gol. **M**
- [ ] Conquistas (30 a 40) com moedas e itens exclusivos. **M**

## Fase 6: som e espetáculo

- [ ] Música sintetizada, sem arquivos: tema do menu, tensão nos 10 s finais, vinheta de título. **M**
- [ ] Torcida de fundo: murmúrio constante, "uuuh" na bola na trave, subindo quando a bola chega perto do gol, festa no gol da casa (mais forte nos estádios). **M**
- [ ] Comemorações de gol dos bonecos (dancinha, joelhada no gramado, braço para cima). **M**
- [ ] Contagem sonora nos 5 s finais. **P**
- [ ] Volume separado para música e efeitos. **P**
- [ ] ❓ Replay do gol em velocidade normal, pulável com qualquer tecla. Precisa da tua palavra por causa do "sem câmera lenta no gol". **M**

## Fase 7: jogar com os amigos

- [ ] Desafio do dia: todo mundo joga a mesma partida (adversário e reposições sorteados pela data) e copia o resultado num texto para o grupo. **M**
- [ ] Código de salvamento para levar a carreira de um aparelho para outro (pendência oferecida). **P/M**
- [ ] Dois jogadores no mesmo tablet, cada um com metade dos controles. **M**
- [ ] Controle de videogame no computador (um por jogador). **P/M**
- [ ] Investigar se dá para ter ranking entre amigos: hoje quem abre pelo link público não grava na conta. **P** (só investigar)
- [ ] Longo prazo: online 1x1 precisa de servidor, então fica fora do arquivo único por enquanto.

## Fase 8: polimento e cuidado

- [ ] Trocar as teclas numa tela de opções. **M**
- [ ] Opção de cores para daltonismo nos uniformes; ligar/desligar dicas. **P**
- [ ] Vibração curta no celular (Android) no chute e no gol. **P**
- [ ] Abertura com o escudo enquanto as fontes carregam. **P**
- [ ] Testar em celular de verdade (Android e iPhone) a cada versão grande. **P** (do teu lado)
- [ ] Manter o código arrumado conforme cresce (arquivo único, marcadores de seção, um bloco próprio para personagens e especiais). **P**
- [ ] Teste automático para cada sistema novo (especiais, estilos de CPU, modos). Vai junto de cada item.

## Ordem sugerida

| Versão | O que entra | Por quê |
| - | - | - |
| v0.13 | Fase 0 + Fase 1 (git, rodada com amigos, treino, nome do lance, resumo) | o primeiro contato decide se o amigo volta |
| v0.14 | barra do especial + 4 especiais + CPU usando | o que mais muda cada partida |
| v0.15 | elenco de personagens com atributos | dá cara e escolha ao jogo |
| v0.16 | CPU com estilos, domínio, defesa melhor + simulação da dificuldade | partidas deixam de ser repetidas |
| v0.17 | música, torcida, comemorações | barato e muda muito a sensação |
| v0.18 | campos dos degraus de cima + modos rápidos | variedade |
| v0.19 | carreira: pós-título, rival, troféus, conquistas | motivo para continuar jogando |
| v0.20 | desafio do dia, código de salvamento, controle de videogame | o jogo já tem o que mostrar aos amigos |

## Decisões que são tuas (❓)

1. Formato dos personagens e especiais (elenco fixo, especial do teu jogador, ou os dois).
2. Itens caindo no campo: sim ou não.
3. Terreno e clima mexendo na física.
4. Atributos do jogador evoluindo na carreira.
5. Replay do gol em velocidade normal.
