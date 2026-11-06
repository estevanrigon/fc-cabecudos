# Plano: do protótipo à 1.0

Atualizado em 05/11/2026, com a v0.14 no ar no GitHub Pages. Este arquivo é o único lugar das pendências e das decisões em aberto; o que já foi feito está em `historico.md`.

Legenda: **P** = um pedido curto · **M** = uma sessão de trabalho · **G** = várias sessões · ❓ = precisa da tua decisão antes · *(teu lado)* = só tu podes fazer.

## O que é a 1.0

Um jogo completo que um amigo abre pelo link, entende sozinho e joga a carreira do começo ao fim sem travar. Na prática:

- **Cada partida é diferente:** elenco de personagens com atributos e especial próprio, e uma CPU com estilos que não se vence sempre do mesmo jeito.
- **A carreira prende:** campo próprio em cada degrau, algo para fazer depois do título, rival e troféus.
- **Tem clima de jogo:** música, torcida reagindo ao lance, comemorações.
- **O progresso não se perde:** código de salvamento para levar a carreira de um aparelho para outro (no GitHub Pages ela fica só no navegador).
- **Funciona de verdade:** testado com amigos, em celular e com controle de verdade, sem erro conhecido.

O que não entra na 1.0 está em "Depois da 1.0", no fim.

## Agora *(teu lado)*

Antes da v0.15, porque o que os amigos disserem pode mudar a ordem do resto:

- [ ] Mandar o link novo (https://estevanrigon.github.io/fc-cabecudos/) para 3 a 5 amigos, inclusive quem tinha o do claude.ai. Pedir que joguem 10 minutos sem explicação e contem onde travaram, o que acharam chato e do que mais gostaram (o botão "Mandar opinião" já monta o texto). Ver alguém jogando vale ainda mais.
- [ ] Ajustar os números dos especiais jogando (painel, grupo "Especiais") e mandar o bloco "física vX".
- [ ] Testar no celular de verdade e com um controle de Xbox de verdade no link novo (até aqui, só controle simulado).

## Caminho até a 1.0

Uma versão por linha da tabela; cada uma fecha com os testes passando e os docs atualizados. As sessões são uma estimativa.

| Versão | Tema | Tamanho |
| - | - | - |
| v0.15 | personagens | G (2 a 3 sessões) |
| v0.16 | CPU com cabeça | G (2 a 3) |
| v0.17 | som e espetáculo | M/G (1 a 2) |
| v0.18 | campos e modos rápidos | G (2 a 3) |
| v0.19 | carreira que prende | G (2 a 3) |
| v0.20 | opções e polimento | M (1 a 2) |
| v1.0 | rodada final e correções | M + rodada *(teu lado)* |

### v0.15 · Personagens
O que mais muda a sensação de cada partida; o modelo de dados (`p.attr`, `rHead`) já está pronto.
- [ ] Atributos por personagem (velocidade, pulo, força do chute, tamanho da cabeça), com diferenças pequenas para não desequilibrar. **M**
- [ ] Elenco de 8 personagens originais (nome, visual, atributos, especial). Escolha do personagem no amistoso; os adversários da carreira passam a usar o elenco. **G**
- [ ] ❓ Mais especiais para o elenco ter 8 diferentes (hoje são 4; o "pombo sem asa", rasteiro fortíssimo, está de reserva). **M**
- [ ] Código de salvamento: um texto curto para copiar e colar a carreira em outro aparelho. Vem cedo porque, no GitHub Pages, limpar o navegador apaga a carreira. **P/M**

### v0.16 · CPU com cabeça
- [ ] Estilos de CPU: atacante (pressiona), retranqueiro (fica no gol), cavador (abusa da cavadinha), equilibrado. Cada clube e cada personagem recebe um. **M**
- [ ] CPU usando o domínio, e o voleio embalado nos níveis altos. **M**
- [ ] CPU reagindo ao placar: perdendo no fim, se arrisca; ganhando, segura. **P**
- [ ] Defesa melhor: voltar para o gol em bola alta e não ficar vendida na cavadinha. **M**
- [ ] Teste automático que caça as jogadas que sempre funcionam contra a CPU (medindo de onde saem os gols), para fechar as brechas. **M**
- [ ] Simular a carreira com CPU contra CPU para conferir a curva de dificuldade de cada degrau. **M**

### v0.17 · Som e espetáculo
Barato e muda muito a sensação.
- [ ] Música sintetizada, sem arquivos: tema do menu, tensão nos 10 s finais, vinheta de título. **M**
- [ ] Torcida de fundo: murmúrio constante, "uuuh" na bola na trave, subindo quando a bola chega perto do gol, festa no gol (mais forte nos estádios). **M**
- [ ] Comemorações de gol dos bonecos (dancinha, joelhada no gramado, braço para cima). **M**
- [ ] Contagem sonora nos 5 s finais. **P**
- [ ] Volume separado para música e efeitos. **P**

### v0.18 · Campos e modos rápidos
- [ ] Campos para os degraus de cima: estádio de dia lotado para as divisões e estádio continental para a Liga Suprema. **M** cada
- [ ] Modos rápidos no menu: primeiro a 5 gols, morte súbita direto, torneio rápido de mata-mata com troféu. **M**

### v0.19 · Carreira que prende
- [ ] Depois do título da Liga Suprema: um "Mundial" com adversário chefe e temporadas de lenda na força máxima, com recompensas novas. **M**
- [ ] Rival de carreira: um adversário que reaparece em vários degraus, com comemoração própria. **M**
- [ ] Manchetes entre as rodadas ("Cabeçudo decide no fim e o Poeirão perde a ponta"). **P/M**
- [ ] Armário de troféus, com uma taça diferente por competição. **M**
- [ ] Mais coisas no vestiário: uniformes alternativos, comemorações e efeitos de gol. **M**
- [ ] ❓ Atributos do jogador da carreira evoluindo com treinos ou moedas, com teto para a física não sair do controle. **M**

### v0.20 · Opções e polimento
- [ ] Tela de opções: trocar as teclas, cores para daltonismo nos uniformes, ligar e desligar as dicas. **M**
- [ ] Abertura com o escudo enquanto as fontes carregam. **P**
- [ ] Vibração curta no celular (Android) no chute e no gol. **P**
- [ ] ❓ Instalar no celular como aplicativo (ícone na tela inicial, abre em tela cheia, funciona sem internet). Precisa de dois arquivos pequenos além do `index.html`, uma exceção à regra do arquivo único. **P/M**

### v1.0 · Rodada final
Sem novidade nesta versão, só acabamento.
- [ ] Rodada com amigos jogando a carreira inteira, no celular e no computador. *(teu lado)*
- [ ] Corrigir tudo o que aparecer, conferir o desempenho em celular fraco e os testes de todos os sistemas.
- [ ] Tirar o "protótipo jogável" da tagline e escrever a nota da 1.0.

## Pedidos prontos (um por conversa nova)

Cada pedido abaixo é uma sessão: abre uma conversa nova para cada um (sai bem mais barato do que continuar uma conversa longa) e cola o texto. O que está entre colchetes depende de uma decisão tua; apaga a parte que não valer. "Fecha e publica" quer dizer testes, docs, commit e push na `main`, ou seja, o link dos amigos atualiza.

**A qualquer momento**
```
Atualiza os padrões da física com este bloco do painel: [cola o bloco "física vX"]
```
```
Estas são as opiniões dos amigos: [cola]. Resume o que apareceu e propõe mudanças no docs/plano.md, sem programar ainda.
```

**v0.15 · Personagens**
```
Começa a v0.15 (seção "v0.15 · Personagens" do docs/plano.md). Antes de programar, me propõe o elenco de 8 personagens originais (nome, visual, atributos e especial de cada um) [e os 4 especiais novos]. Quando eu aprovar, anota no plano e envia (só docs).
```
```
Continua a v0.15: programa o elenco aprovado (atributos, escolha do personagem no amistoso, adversários da carreira usando o elenco), com testes.
```
```
Termina a v0.15: [os especiais novos aprovados e] o código de salvamento. Depois fecha e publica a v0.15.
```

**v0.16 · CPU com cabeça**
```
Começa a v0.16 (docs/plano.md): estilos de CPU, domínio e voleio embalado da CPU, reação ao placar e defesa melhor, com testes.
```
```
Termina a v0.16: o teste que caça as jogadas que sempre funcionam contra a CPU e a simulação da carreira CPU contra CPU. Me mostra o que apareceu, ajusta e fecha e publica a v0.16.
```

**v0.17 · Som e espetáculo**
```
Faz a v0.17 inteira (seção "v0.17 · Som e espetáculo" do docs/plano.md). Antes de publicar, me avisa para eu ouvir no computador; depois fecha e publica.
```

**v0.18 · Campos e modos rápidos**
```
Começa a v0.18 (docs/plano.md): os dois campos novos para os degraus de cima. Me mostra as capturas antes de seguir.
```
```
Termina a v0.18: os modos rápidos no menu. Fecha e publica a v0.18.
```

**v0.19 · Carreira que prende**
```
Começa a v0.19 (docs/plano.md): o Mundial e as temporadas de lenda depois da Liga Suprema, e o rival de carreira.
```
```
Termina a v0.19: manchetes, armário de troféus e itens novos no vestiário [e atributos do jogador evoluindo na carreira]. Fecha e publica a v0.19.
```

**v0.20 · Opções e polimento**
```
Faz a v0.20 (seção "v0.20 · Opções e polimento" do docs/plano.md) [com o instalar no celular como aplicativo]. Fecha e publica.
```

**v1.0 · Rodada final** (depois que os amigos jogarem a carreira inteira)
```
Fiz a rodada final com os amigos; as opiniões estão abaixo. Corrige o que apareceu, confere o desempenho e os testes, e fecha e publica a 1.0: [cola as opiniões]
```

## Regras do caminho
- Cada sistema novo vem com teste automático.
- Testar no celular de verdade a cada versão grande. *(teu lado)*
- O código continua num arquivo só, com os marcadores de seção e um bloco próprio por sistema.

## Depois da 1.0 (ideias guardadas)
- Campos para amistoso: praia, quadra de rua, terrão na chuva. **M** cada
- ❓ Terreno e clima mexendo na física (chuva: bola escorrega; areia: quica menos; vento leve). **M**
- ❓ Itens que caem no campo e dão um efeito curto a quem tocar primeiro (com itens próprios, tipo bola de chiclete ou chuteira de mola). **M/G**
- Desafios com prêmio em moedas ("3 gols de voleio", "ganhar sem sofrer gol"). **M**
- Conquistas (30 a 40) com moedas e itens exclusivos. **M**
- Modo festa para 2 jogadores: cabeção, bola pesada, gol pequeno, gravidade baixa. **M**
- Desafio do dia: todo mundo joga a mesma partida (sorteada pela data) e compara o resultado no grupo. **M**
- Dois jogadores no mesmo tablet, cada um com metade dos controles. **M**
- ❓ Replay do gol em velocidade normal, pulável com qualquer tecla (precisa da tua palavra por causa do "sem câmera lenta no gol"). **M**
- Investigar um ranking entre amigos (no GitHub Pages não há conta nem servidor; precisaria de um serviço à parte). **P** (só investigar)
- Online 1x1: precisa de servidor, então fica fora do arquivo único.

## Decisões que são tuas (❓)
1. Mais especiais na v0.15, para cada um dos 8 personagens ter o seu, ou especiais repetidos entre personagens. *Sugestão: mais quatro, um de cada tipo (chute, drible, defesa, bola alta).*
2. Atributos do jogador da carreira evoluindo (v0.19). *Sugestão: sim, pouco e com teto.*
3. Instalar no celular como aplicativo (v0.20). *Sugestão: sim; é o jeito de jogar sem a barra do navegador.*
4. Itens caindo no campo, terreno e clima, replay do gol: ficam para depois da 1.0, se quiseres.
