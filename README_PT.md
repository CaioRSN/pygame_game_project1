# 🎮 CIn Adventure: The CinSegura Challenge

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-Latest-green?style=for-the-badge)
![VS Code](https://img.shields.io/badge/VS%20Code-💻-blueviolet?style=for-the-badge)

---

## 📝 1. Introdução e Visão Geral do Projeto

O **CIn Adventure** é um jogo de plataforma bidimensional (2D) desenvolvido como projeto final para a disciplina de Introdução à Programação do Centro de Informática (CIn).

Adotando uma abordagem satírica e totalmente contextualizada na nossa rotina universitária, o jogo coloca o usuário no controle de um professor do centro. O enredo estabelece que as dependências físicas e os sistemas lógicos foram invadidos por uma horda de pinguins hostis de Linux. A missão do protagonista consiste em atravessar os cenários modulares dos blocos, erradicar a infestação utilizando disparos de código, coletar crachás de liberação estudantil para desbloquear os acessos das fases e, por fim, neutralizar o sistema de segurança corrompido, personificado pelo chefe final **"CinSegura"**.

---

## 👥 2. Identificação da Equipe (Grupo 7)

* Alvaro Claudio Bezerra da Silva – `<acbs5>`
* Arthur Martins da Silva – `<ams20>`
* Caio Riquelmy Santos do Nascimento – `<crsn>`
* Gabriela Vitória Vasco Alves – `<gvva>`
* Leticia Elany Rodrigues Gonçalves – `<lerg>`

---

## 🎯 3. Diretrizes e Objetivos do Sistema

### 3.1. Objetivo Geral
Desenvolver um jogo eletrônico de plataforma interativo, utilizando a linguagem Python e a biblioteca Pygame, que sirva como demonstração prática e integrada dos conceitos de Programação Orientada a Objetos (POO) ministrados ao longo do período letivo.

### 3.2. Objetivos Específicos
* **Física Aplicada:** Construir um motor matemático básico para simular gravidade vetorial, aceleração lateral e detecção precisa de colisões bidimensionais por caixas delimitadoras.
* **Modularidade:** Segmentar o sistema em módulos lógicos isolados para facilitar a legibilidade, manutenção e o desenvolvimento colaborativo.
* **Gerenciamento de Recursos:** Otimizar a gerência de memória RAM, eliminando redundâncias de carregamento de arquivos e administrando o ciclo de vida de objetos dinâmicos em tempo de execução.

---

## 🛠️ 4. Ferramentas, Frameworks e Bibliotecas Utilizadas

* **Python 3:** Linguagem de programação base utilizada para a modelagem de classes nativas, definição da lógica do software e suporte ao paradigma POO.
* **Pygame:** Framework gráfico voltado à manipulação do loop principal do jogo, renderização de sprites, controle de hitboxes (`pygame.Rect`) e estabilização da taxa de quadros por segundo (`pygame.time.Clock`).
* **Math (Biblioteca Nativa):** Suporte a operações e cálculos vetoriais bidimensionais para o gerenciamento da gravidade, deslocamentos físicos e cálculo de trajetórias dos projéteis de código.
* **OS (Biblioteca Nativa):** Utilizada para a manipulação dinâmica de caminhos de arquivos e diretórios. Garante a portabilidade do software ao permitir que os assets (imagens, sons e fontes) sejam localizados de forma relativa, evitando falhas de carregamento independentemente do sistema operacional utilizado (Windows, Linux ou macOS).
* **SYS (Biblioteca Nativa):** Responsável por interagir diretamente com o interpretador do Python. É utilizada em conjunto com as rotinas de encerramento do ambiente gráfico para executar o desligamento limpo e seguro do processo do jogo na memória RAM assim que o usuário opta por sair da aplicação.
* **Random (Biblioteca Nativa):** Implementação de algoritmos pseudoaleatórios para reger o sistema de recompensa de itens (*drops*) gerados probabilisticamente ao eliminar inimigos.
* **VS Code:** Ambiente de desenvolvimento integrado (IDE) adotado de forma unificada pela equipe para edição e depuração do código-fonte.

---

## 👾 5. Estrutura de Entidades do Jogo

Os elementos dinâmicos, objetos interativos e inteligências do jogo foram implementados no módulo `entidades/`, onde cada arquivo representa uma classe independente acoplada ao sistema do Pygame:

`main.py`: Arquivo centralizador do fluxo do software. Inicializa os subsistemas gráficos do Pygame, fixa a taxa de atualização de quadros (FPS) e executa a máquina de estados que decide qual tela renderizar a cada ciclo do laço principal.

`config.py`: Concentra todos os parâmetros estáticos e constantes do sistema, tais como a magnitude do vetor gravidade, força de impulso do salto, caminhos de diretórios e as matrizes que delimitam o posicionamento dos blocos em cada fase.

`jogador.py`: Encapsula a classe abstrata do protagonista, gerenciando a captura de inputs do teclado, equações de velocidade linear e a checagem mecânica de colisões verticais e horizontais.

`inimigo.py`: Define a classe dos inimigos, implementando suas coordenadas de spawn, ciclo de animações, taxas de dano e a lógica de inteligência artificial de aproximação.

`cenario.py`: Controla a criação física das plataformas flutuantes e dos obstáculos geométricos, além de supervisionar as condições lógicas para o surgimento do item de conclusão.

`recursos.py`: Atua como um buffer estático de memória. Carrega e armazena previamente na inicialização todas as spritesheets e efeitos sonoros, servindo-os como cache para evitar leituras repetitivas em disco rígido durante o gameplay.

`render.py`: Isolador de chamadas gráficas, responsável pela escrita de fontes em pixel art, atualização de barras de progresso e desenho geométrico de caixas de diálogo na tela.

---

## 🚀 6. Arquivo Principal e Como Rodar o Jogo

O arquivo `main.py` fica localizado diretamente na raiz do repositório, atuando como o ponto de entrada unificado que inicializa o Pygame, instancia o gerenciador de telas e executa o Game Loop principal.

### Pré-requisitos
Antes de executar o jogo, certifique-se de ter o **Python 3** instalado em sua máquina.

### Instalação Passo a Passo

1. **Clone o repositório:**
   
git clone https://github.com/CaioRSN/pygame_game_project1.git

2. **Navegue até a pasta do projeto:**
   
cd pygame_game_project1

3. **Instale a biblioteca Pygame:**
   
pip install pygame --- OU --- pip install pygame-ce (se a versão do seu Python for inferior a 3.13)

4. **Execute o jogo:**
   
python main.py
  
## 👥 7. Divisão de Trabalho Técnica
O projeto foi segmentado de forma modular, permitindo o desenvolvimento simultâneo por meio de divisões claras de responsabilidades técnicas:

Alvaro Claudio: Arquitetura do Level Design (cenário da Copa), modelagem de colisões físicas e plataformas ocultas. Configuração estrutural e artes dos itens consumíveis.

Arthur Martins: Desenvolvimento do sistema de áudio e efeitos sonoros, mapeamento de colisões secundárias de cenário e implementação lógica da mecânica de NPCs.

Caio Riquelmy: Algoritmos de movimentação vetorial do protagonista, física balística dos projéteis de código e a máquina de estados lógica do chefe final CinSegura.

Gabriela Vitória: Criação e integração estética dos sprites e animações do jogo (ciclos de movimentação das entidades), estruturação dos menus e transições de tela.

Leticia Elany: Desenvolvimento da lógica de inventário dinâmico, sistema estocástico de probabilidade para drops de itens coletáveis e vinculação de contagem na interface da HUD.

## 🎓 8. Conceitos Aplicados no Projeto

* **Programação Orientada a Objetos (POO):** Toda a infraestrutura lógica do sistema foi estruturada em classes independentes (como Jogador, Inimigo e Plataforma) com dados e comportamentos isolados em seus respectivos escopos, garantindo a modularização do software. 
* **Encapsulamento de Atributos:** Variáveis críticas de movimento e status de jogo foram blindadas dentro de suas classes, sendo modificadas estritamente por métodos validados (ex: aplicar_gravidade() e atualizar_posicao()) para evitar corrupção de dados por agentes externos. 
* **Laços de Repetição e Condicionais:** O laço de repetição principal while atua como o motor de renderização ativa, executando a atualização física de posições e checagem de eventos a cada quadro (frame). Estruturas condicionais (if/elif/else) controlam a máquina de estados das telas e os limites geométricos das colisões.  
* **Estruturas de Dados Dinâmicas (Listas):** Listas lineares foram empregadas para gerenciar e monitorar as entidades ativas em tela. O sistema realiza varreduras contínuas para excluir projéteis disparados que ultrapassem a borda de 1920 pixels horizontais, liberando dinamicamente o espaço ocupado na memória.  
* **Tuplas:** Por serem estruturas de dados imutáveis, as tuplas foram utilizadas no arquivo config.py para armazenar definições que não devem sofrer alteração em tempo de execução, tais como as dimensões fixas da resolução da tela (1920x1080) e os vetores de cores em formato RGB para a estilização da interface gráfica.  
* **Dicionários:** Empregados de forma estratégica no módulo recursos.py para mapear de forma eficiente chaves de identificação (strings) aos buffers de memória que contêm as imagens e efeitos sonoros pré-carregados. Também foram usados para estruturar o mapeamento das teclas do teclado em ações físicas do jogador.   

## ⚠️ 9. Desafios e Erros Enfrentados
Maior Erro Cometido (Gerenciamento de Entrada): Falta de esvaziamento e limpeza da fila de inputs/eventos do Pygame ao transicionar entre as telas do sistema. Isso gerava acúmulo de memória e vazamento indesejado de comandos e cliques de uma interface para a outra (ex: cliques no menu ativando comandos involuntários na gameplay).

Resolução: Implementação de uma rotina explícita de esvaziamento, descarte e reset da fila de inputs nas funções de transição de estado do jogo.

Maior Desafio Técnico (Responsividade e IA): Projetar interfaces gráficas adaptáveis a diferentes resoluções de tela e otimizar os cálculos matemáticos de distância Euclidiana computados em tempo real, mitigando quedas severas de performance (FPS) quando múltiplos pinguins inimigos estavam perseguindo o protagonista simultaneamente.

Resolução: Otimização estrutural dos cálculos vetoriais dentro do ciclo de atualização e refinamento nas rotinas de renderização condicional dos elementos visuais ativos.

## 🎛️ 10. Mapeamento de Comandos e Interface de Controle
A / D ou Setas Laterais (Esquerda e Direita): Controlam o deslocamento linear horizontal do protagonista pelo cenário.

Seta Superior ou Barra de Espaço: Ativa a força vetorial de pulo do personagem / Confirma seleções lógicas nos menus principais.

Tecla K: Dispara projéteis de código (Ataque básico do professor contra a infestação).

Tecla T: Interage com NPCs distribuídos pelos cenários (quando posicionado próximo a eles).

Teclas 1, 2 e 3: Ativam o consumo e uso imediato dos itens armazenados no inventário.

Tecla Esc: Pausa a partida em andamento e abre o menu de suspensão do sistema.

## 🎬 11. Sistema em Funcionamento
<img width="1596" height="897" alt="Captura de tela 2026-07-01 191454" src="https://github.com/user-attachments/assets/773a19b2-0344-40eb-8bd3-3e6ed9cd19e7" />

<img width="1595" height="898" alt="Captura de tela 2026-07-01 192324" src="https://github.com/user-attachments/assets/52c2084d-7084-46e7-9a5f-88644732d62f" />

<img width="1597" height="893" alt="Captura de tela 2026-07-01 192425" src="https://github.com/user-attachments/assets/796b111f-45c0-4bb2-bb47-9798368fe122" />

<img width="1596" height="892" alt="Captura de tela 2026-07-01 191624" src="https://github.com/user-attachments/assets/3a13b84b-77e3-4df2-bcdd-15f1a02d4b53" />

<img width="1596" height="897" alt="Captura de tela 2026-07-01 193845" src="https://github.com/user-attachments/assets/125106bd-4a8f-43de-afd8-2d1d3e0ee6ad" />


## 📝 12. Conclusão
O desenvolvimento do CIn Adventure foi muito mais do que a entrega de um projeto de Introdução à Programação, pois representou a nossa primeira experiência real ao transformar conceitos teóricos em software interativo, lúdico e com forte identidade própria. Ver ideias abstratas da disciplina, tais como herança, encapsulamento e dicionários, a funcionar na prática para dar vida a um professor enfrentando pinguins nos blocos do centro tornou o aprendizado significativamente mais concreto e estimulante.

Como em qualquer desenvolvimento real, o percurso envolveu problemas e exigiu resiliência. O grupo enfrentou falhas de memória causadas pela acumulação de eventos na fila do Pygame e perdas de desempenho quando a inteligência artificial dos inimigos tentava processar a distância Euclidiana em tempo real. Lidar com estas dificuldades obrigou a equipa a pensar criticamente como desenvolvedores, pois tivemos de nos unir para refatorar o código, reestruturar a matemática dos vetores de movimento e otimizar os ciclos de atualização até alcançar uma jogabilidade estável e fluida.

Além da óbvia evolução técnica e da consolidação do uso do ecossistema Git e GitHub para o desenvolvimento colaborativo, a principal lição adquirida foi a importância da cooperação humana no ecossistema de engenharia. Aprendemos a ouvir os diferentes pontos de vista, a distribuir tarefas com base na afinidade de cada um e a superar em conjunto as frustrações do processo de programação. O produto final reflete o orgulho do grupo, pois atende às exigências académicas e entrega uma simulação que representa, de forma divertida, a superação dos nossos primeiros grandes desafios no universo da computação.
