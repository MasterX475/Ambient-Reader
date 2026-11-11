# Leitor de Ambientes

**Sistema de monitoramento ambiental com alertas locais para estufas e ambientes de cuidado de pessoas idosas e animais.**

> Projeto acadêmico desenvolvido para a atividade **GS2026.2 – CitizenTech**, da disciplina **Computer Organization and Architecture**, com Raspberry Pi Pico, MicroPython e simulação na plataforma Wokwi.

## Identificação do projeto

| Integrante | RM |
|---|---|
| Gabriel Silveira | 568910 |
| André Felix | 571691 |
| Isabela Souza | 569196 |

| Campo | Informação |
|---|---|
| Projeto | Leitor de Ambientes |
| Atividade | GS2026.2 – CitizenTech |
| Disciplina | Computer Organization and Architecture |
| Plataforma de desenvolvimento | Wokwi |
| Microcontrolador | Raspberry Pi Pico |
| Linguagem | Python (MicroPython) |
| Professor | Prof. Dr. Marcus Grilo |

## 1. Contextualização e problema identificado

A manutenção de condições ambientais adequadas é importante em diferentes contextos. Em estufas agrícolas, variações de temperatura e luminosidade, assim como alterações na concentração de gases, podem comprometer as condições de cultivo. Em residências e espaços destinados ao cuidado de pessoas idosas ou animais de estimação, mudanças no ambiente também podem passar despercebidas, especialmente quando não há alguém observando continuamente o local.

O problema abordado pelo projeto é, portanto, a dificuldade de acompanhar continuamente algumas condições do ambiente e perceber alterações que mereçam atenção. A ausência de um acompanhamento simples pode atrasar a identificação de situações fora dos parâmetros estabelecidos para determinado espaço.

O público potencialmente beneficiado inclui agricultores e responsáveis por estufas, cuidadores de pessoas idosas, tutores de animais de estimação e demais pessoas que desejem acompanhar as condições de um ambiente interno.

## 2. Objetivo da solução

Desenvolver um protótipo de baixo custo que faça a leitura periódica de variáveis ambientais e do estado de uma porta, apresente os valores em displays e indique, por meio de sinais visuais e sonoros, quando as condições monitoradas estiverem fora dos limites configurados.

A proposta utiliza conceitos de Internet das Coisas (IoT) e computação física para transformar leituras de sensores em informações de fácil interpretação. O objetivo é apoiar a observação do ambiente e chamar a atenção do responsável quando o sistema identificar uma condição de alerta ou emergência.

## 3. Descrição geral do funcionamento

O sistema utiliza a **Raspberry Pi Pico** como unidade central de processamento. Os sensores fornecem informações sobre gás, luminosidade e temperatura, enquanto uma entrada digital representa a condição de uma porta monitorada. O programa, desenvolvido em MicroPython, lê essas entradas, calcula ou obtém os valores correspondentes e compara cada leitura com limites definidos no próprio código.

As informações são apresentadas em sete displays LCD de comunicação I²C: um display mostra a leitura atual de cada variável monitorada, outro apresenta os limites mínimo e máximo correspondentes, e um display informa se a porta está aberta ou fechada. Quando uma leitura ultrapassa os limites definidos, o display correspondente apresenta uma marcação visual com caracteres `X`.

Após avaliar as condições, o programa classifica o ambiente em um dos três estados — **Normal**, **Alerta** ou **Emergência** — e atualiza um LED RGB. No estado de emergência, o alto-falante também é acionado. O estado identificado é impresso no monitor serial do simulador.

## 4. Componentes utilizados

| Componente | Função no projeto | Conexão utilizada no código |
|---|---|---|
| Raspberry Pi Pico | Processar as leituras, executar as regras de classificação e controlar as saídas | Unidade central |
| Sensor de gás | Fornecer uma leitura analógica utilizada para estimar a concentração indicada em ppm | GP28 (ADC) |
| Fotoresistor (LDR) | Medir a luminosidade do ambiente por meio de uma entrada analógica | GP27 (ADC) |
| Sensor de temperatura DS18B20 | Realizar a leitura da temperatura em graus Celsius | GP22 (OneWire) |
| Chave/entrada digital da porta | Representar se a porta monitorada está aberta ou fechada | GP18 |
| Displays LCD 16x2 com interface I²C | Exibir leituras, limites e estado da porta | SDA: GP20; SCL: GP21 |
| LED RGB | Indicar visualmente o estado geral do ambiente | GP2 (R), GP3 (G) e GP4 (B) |
| Alto-falante | Emitir sinal sonoro quando o estado for classificado como emergência | GP0 |

### 4.1 Displays e endereços I²C

O código instancia sete displays LCD 16x2 no mesmo barramento I²C. Cada módulo recebe um endereço próprio:

| Informação apresentada | Endereço I²C |
|---|---:|
| Leitura de gás | `0x21` |
| Limites de gás | `0x20` |
| Leitura de luminosidade | `0x22` |
| Limites de luminosidade | `0x23` |
| Leitura de temperatura | `0x26` |
| Limites de temperatura | `0x25` |
| Estado da porta | `0x27` |

## 5. Parâmetros de monitoramento

Os valores abaixo são os parâmetros configurados atualmente no código do projeto. Eles podem ser alterados para representar as necessidades de um ambiente específico.

| Variável | Limite mínimo | Limite máximo | Unidade exibida | Origem da informação |
|---|---:|---:|---|---|
| Gás | 1.000 | 25.000 | ppm | Valor estimado a partir da leitura analógica do sensor de gás |
| Luminosidade | 30 | 75 | % | Valor percentual calculado a partir da leitura analógica do LDR |
| Temperatura | 15 | 35 | °C | Leitura do sensor DS18B20 |
| Porta | — | — | Aberta/Fechada | Estado lógico de uma entrada digital |

As faixas apresentadas são parâmetros definidos no código para a simulação. Elas não devem ser interpretadas como limites universais de segurança, recomendações agronômicas para qualquer cultura ou referências médicas/veterinárias. A configuração adequada depende do local, da finalidade de uso, dos equipamentos e dos sensores efetivamente instalados.

## 6. Lógica de classificação do ambiente

O programa executa continuamente as seguintes etapas:

1. Inicializa os sensores, os displays, o LED RGB e o alto-falante.
2. Solicita a conversão da temperatura e aguarda aproximadamente um segundo.
3. Lê o sensor de gás, o fotoresistor, o sensor de temperatura e a entrada digital da porta.
4. Atualiza os displays com os valores obtidos e com os limites configurados.
5. Verifica quais variáveis estão dentro ou fora de suas respectivas faixas.
6. Classifica o ambiente como Normal, Alerta ou Emergência.
7. Atualiza o LED RGB, aciona ou desliga o sinal sonoro e imprime o estado no monitor serial.
8. Repete o ciclo de monitoramento.

### 6.1 Regras de decisão implementadas

A classificação segue as condições presentes na função `Verificacao()` do código:

| Estado | Condição implementada | Resposta do sistema |
|---|---|---|
| **Normal** | Gás, luminosidade e temperatura dentro das faixas configuradas e porta fechada | Indicação visual verde; alto-falante desligado |
| **Alerta** | Apenas a luminosidade ou apenas a temperatura está fora da faixa, sem condição de emergência | Indicação visual de alerta; alto-falante desligado |
| **Emergência** | Gás fora da faixa; **ou** porta aberta; **ou** luminosidade e temperatura simultaneamente fora das faixas | Indicação visual vermelha e acionamento do alto-falante |

Na configuração demonstrada, o LED RGB apresenta verde para Normal, amarelo para Alerta e vermelho para Emergência. O alto-falante reproduz um sinal sonoro (`C2`) enquanto a classificação for Emergência e é desligado nos demais estados.

**Observação importante sobre a lógica:** uma leitura de gás fora dos limites ou a abertura da porta é suficiente para gerar Emergência. Para luminosidade e temperatura, uma única variável fora da faixa gera Alerta; quando as duas estão fora da faixa ao mesmo tempo, o resultado passa a ser Emergência. Essa regra é a lógica atual do programa e pode ser ajustada conforme a aplicação pretendida.

## 7. Demonstração e resultados observados

Durante a demonstração no Wokwi, os valores dos componentes são alterados para simular diferentes condições ambientais. As leituras são atualizadas nos displays, permitindo observar como as regras do programa respondem a cada mudança.

Entre as situações demonstradas estão:

- **Condição normal:** valores de gás, luminosidade e temperatura dentro das faixas configuradas, com a porta fechada. O monitor serial apresenta `Estado: Normal` e a indicação visual permanece verde.
- **Temperatura fora da faixa:** ao elevar a leitura de temperatura acima do limite máximo, o display de temperatura apresenta a marcação `X` e o sistema classifica a situação como Alerta, desde que a luminosidade permaneça dentro de sua faixa e não exista outra condição de emergência.
- **Luminosidade e temperatura fora da faixa:** quando as duas variáveis ficam fora dos limites simultaneamente, o estado passa a Emergência.
- **Gás acima do limite:** quando a leitura calculada de gás supera o máximo configurado, o display sinaliza a condição e o sistema entra em Emergência.
- **Porta aberta:** a entrada digital muda para o estado de porta aberta, o display correspondente apresenta a condição e o sistema classifica o ambiente como Emergência.

Esses resultados evidenciam a relação entre **entradas** (sensores e estado da porta), **processamento** (comparação com parâmetros e aplicação das condições lógicas) e **saídas** (displays, LED RGB, alto-falante e monitor serial), atendendo ao propósito demonstrativo da atividade.

## 8. Aplicações e contribuição social

### 8.1 Apoio ao monitoramento de estufas agrícolas

Em uma estufa, o leitor pode auxiliar o agricultor a acompanhar temperatura, luminosidade e a variável de gás monitorada. A visualização contínua dos valores e a sinalização de condições fora das faixas definidas podem facilitar a identificação de mudanças no ambiente e apoiar a decisão de verificar o local ou ajustar seus equipamentos.

Para uso em uma cultura real, os limites devem ser configurados conforme a espécie cultivada, a etapa de desenvolvimento, as condições locais e a especificação dos sensores. O protótipo apresentado não realiza controle automático de ventilação, iluminação, irrigação ou climatização.

### 8.2 Apoio ao cuidado de pessoas idosas e animais de estimação

Em ambientes residenciais, o dispositivo pode auxiliar familiares, cuidadores e tutores no acompanhamento de temperatura, luminosidade, gás e abertura de uma porta monitorada. Os displays permitem consultar as leituras e os sinais visual e sonoro chamam a atenção quando a lógica identifica uma condição de alerta ou emergência.

A indicação de porta aberta pode ser útil em espaços nos quais o acesso precise ser acompanhado, por exemplo, para verificar uma possível saída não percebida de um animal. A utilidade dessa regra depende do local e da finalidade do monitoramento; em determinadas aplicações, a abertura da porta pode ser uma ocorrência normal e a lógica deverá ser adaptada.

### 8.3 Relação com o conceito CitizenTech

A proposta se relaciona ao conceito de Tecnologia Cidadã porque utiliza computação física e sensores para responder a necessidades cotidianas, com potencial de contribuir para o bem-estar, o cuidado, a atividade agrícola e a observação de ambientes. A solução demonstra como uma plataforma acessível pode transformar dados coletados no espaço físico em informações compreensíveis e alertas locais.

## 9. Acesso ao protótipo e demonstração

- **Projeto no Wokwi:** [Leitor de Ambiente](https://wokwi.com/projects/479956180486049793)
- **Vídeo demonstrativo:** [Ver](https://youtu.be/ggJSjKShN9U)

Para visualizar o funcionamento, abra o projeto no Wokwi, inicie a simulação e altere os valores dos sensores ou o estado da entrada que representa a porta. Observe a atualização dos displays, do LED RGB, do alto-falante e do monitor serial.
