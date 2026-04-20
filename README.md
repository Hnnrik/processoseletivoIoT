# Detector de Níveis de Queimada - ESP32

Sistema de monitoramento ambiental que avalia o risco de incêndio florestal com base em temperatura, gases (simulando CO/VOC) e umidade. Utiliza um **ESP32**, sensor **DHT22**, sensor de gás **MQ-x** (simulado), **LDR** e display **OLED SSD1306**. Os **LEDs** indicam o nível de alerta em tempo real
<img width="782" height="802" alt="image" src="https://github.com/user-attachments/assets/a8617d0a-5b43-4d91-8a7c-485d355c2875" />

---
## 1 Visao Geral da Solucao

**Objetivo do projeto**  
Desenvolver um sistema embarcado de baixo custo para monitorar condicoes ambientais (temperatura, gases e luminosidade) e classificar o risco de incendio florestal em cinco niveis, utilizando LEDs e display para alerta local.

**O que o sistema embarcado simulado faz**  
- Le dados simulados de sensores (DHT22, sensor de gas, LDR) ou reais quando conectado.
- Classifica o risco em: `NORMAL`, `ALTERACAO`, `MEDIO`, `CRITICO` ou `EXTREMO`.
- Aciona LEDs coloridos (azul, amarelo, vermelho) com diferentes padroes (fixo/piscante).
- Exibe as leituras e o estado atual em um display OLED SSD1306.
- Envia uma mensagem de teste (`"Teste"`) pela serial para validacao em integracao continua (CI).

**Como o usuario interage**  
- Visualmente, atraves dos LEDs e do display.
- Futuramente, por meio de um modulo LoRa e um dashboard central (previsto em implementacoes futuras).

**Significado dos LEDs**

| LED      | Cor   | Significado                                                                 |
|----------|-------|-----------------------------------------------------------------------------|
| Azul     | 🔵    | **Tudo bem** – condições normais. Risco de queimada muito baixo ou inexistente. |
| Amarelo  | 🟡    | **Potencial de risco** – temperatura ou concentração de gases elevadas. Exige atenção. |
| Vermelho | 🔴    | **Muito provável queimada** – condições críticas. Risco iminente de incêndio. |

> Os LEDs podem piscar em alguns níveis para indicar alterações no estado atual do dispositivo (ex.: amarelo piscante + azul fixo no estado `ALTERACAO`).

---

## Auxílios Ambientais Proporcionados

Este sistema contribui diretamente para a proteção do meio ambiente:

- **Prevenção precoce** – Detecta condições que antecedem um incêndio, permitindo ação rápida.
- **Redução de emissões** – Evita que pequenos focos se tornem grandes queimadas, reduzindo a liberação de CO₂ e gases tóxicos.
- **Preservação da fauna e flora** – Ao alertar com antecedência, ajuda a proteger ecossistemas inteiros.
- **Conscientização comunitária** – Os LEDs e o display fornecem informação clara para moradores e brigadistas.
- **Baixo custo e fácil replicação** – Pode ser instalado em áreas remotas com placas solares, ampliando a cobertura de monitoramento.

---

## Componentes Necessários

| Componente          | Quantidade | Pinos no ESP32 (exemplo) |
|---------------------|------------|---------------------------|
| ESP32 DevKit V4     | 1          | –                         |
| Sensor DHT22        | 1          | GPIO4 (DATA)              |
| Sensor de gás (MQ-2/outro) | 1      | GPIO34 (AOUT)             |
| LDR (fotorresistor) | 1          | GPIO35 (AO)               |
| Display OLED SSD1306| 1          | I2C: SDA=18, SCL=19       |
| LED azul            | 1          | GPIO15                    |
| LED amarelo         | 1          | GPIO16                    |
| LED vermelho        | 1          | GPIO17                    |
| Resistor 10kΩ       | 1          | Pull‑up do DHT22          |
| Resistores 1kΩ      | 3          | Para os LEDs              |
| Jumpers e protoboard| –          | –                         |

---

## Como Funciona

1. **Leitura dos sensores** (simulada no CI / real no hardware):
   - **DHT22** → temperatura (°C) e umidade (%).
   - **Sensor de gás** → concentração de compostos orgânicos voláteis (CO, fumaça).
   - **LDR** → intensidade luminosa (auxiliar, pode indicar fogo ou luz solar).

2. **Lógica de classificação do risco** (baseada em temperatura e gás):

   | Estado        | Condição                                                                 | LEDs ativos                     |
   |---------------|--------------------------------------------------------------------------|---------------------------------|
   | `NORMAL`      | gás ≤ 10000 ou temp ≤ 30°C                                           | Azul fixo                       |
   | `ALTERACAO`   | (10000 < gás ≤ 20000) ou (30°C < temp ≤ 35°C)                        | Azul fixo + amarelo piscando    |
   | `MEDIO`       | (20000 < gás ≤ 30000) ou (35°C < temp ≤ 40°C)                        | Amarelo fixo                    |
   | `CRITICO`     | (30000 < gás ≤ 45000) ou (40°C < temp ≤ 45°C)                        | Amarelo fixo + vermelho piscando|
   | `EXTREMO`     | gás > 45000 ou temp > 45°C                                           | Vermelho fixo                   |

3. **Exibição no OLED**:
   - Temperatura, umidade, gás, luz e o estado atual.
   - Atualização a cada 0,4 segundos.

4. **Envio do resultado** (para CI/GitHub Actions):
   - Após uma iteração, o programa imprime `"Teste"` no monitor serial, indicando sucesso.

---
## Utilização na prática.
Em Utilização na real, a placa com seus componente seriam colocados dentro de uma caixa plástica de material reciclado, alimentados por uma bateria recarregável por uma placa solar. Além disso a comunicação seria feita por meio de um módulo Lora para longas distâncias.

<img width="1059" height="749" alt="image" src="https://github.com/user-attachments/assets/bb33e44f-20ae-4e61-88d9-dab21de65ac8" />

<img width="1188" height="735" alt="image" src="https://github.com/user-attachments/assets/2536dcf9-76a3-446a-aeff-946b6366e3fa" />

---
## 4 Decisoes Tecnicas Relevantes

### Organizacao do codigo
- **Modularizacao com funcoes** – `apagar_todos()` e `piscar()` para controle reutilizavel dos LEDs.
- **Classe SSD1306_I2C implementada internamente** – evita dependencia de bibliotecas externas (que nao estao disponiveis no ambiente MicroPython do Wokwi por padrao).
- **Separacao entre valores simulados e leituras reais** – linhas de leitura real comentadas, mantendo a simulacao funcional para CI.

### Uso de constantes e estados
- As faixas de decisao foram definidas como numeros inteiros diretos no codigo (simplificacao didatica).
- A logica de estados utiliza `if/elif/else` para garantir que apenas uma condicao seja aplicada (evita sobreposicao).

### Estrategia para temporizacao
- `time.sleep(0.4)` no loop para atualizacao dos sensores e display sem sobrecarga.
- O programa executa apenas **uma iteracao** (`break` apos `print("Teste")`) quando usado em CI, garantindo que o timeout nunca seja atingido.

### Por que usar valores simulados no CI?
- O driver do DHT22 no Wokwi pode travar se o sensor nao estiver perfeitamente conectado ou se houver bug no simulador. Para garantir robustez nos testes automatizados, optou-se por simular os valores matematicamente (seno/cosseno), mantendo a logica de classificacao totalmente funcional.

---

## 5 Resultados Obtidos

### O que funciona corretamente
- Classificacao dos cinco niveis de risco com base em valores simulados.
- Acionamento correto dos LEDs (fixo ou piscante) conforme o estado.
- Exibicao de temperatura, umidade, gas, luz e estado no display OLED.
- Impressao de `"Teste"` na serial dentro de 1 segundo, validando o CI.
- Execucao sem erros no simulador Wokwi e no GitHub Actions (apos correcao do `ImportError` do SSD1306).

### Requisitos atendidos
- Monitoramento continuo de parametros ambientais.
- Alerta visual local (LEDs + display).
- Baixo custo e possibilidade de alimentacao solar + LoRa (descrito como uso pratico futuro).
- Documentacao completa para reproducao e entendimento.

### Resultado observado na simulacao do Wokwi
- Ao executar o codigo no Wokwi, o display mostra valores variando periodicamente (temperatura entre 25°C e 45°C, gas entre 5k e 55k, etc.).
- Os LEDs mudam de acordo com o estado simulado a cada 0,4 segundos.
- O monitor serial exibe `"Teste"` imediatamente e a simulacao termina sem timeout.

---

## 6 Comentarios Adicionais

### Dificuldades encontradas
- **Importacao da biblioteca `ssd1306`** – o ambiente MicroPython do Wokwi nao a inclui; foi necessario reimplementar a classe internamente.
- **Travamento do DHT22 simulado** – a chamada `measure()` bloqueava para sempre. Solucao: usar valores simulados no CI.
- **Timeout de 5 minutos no plano gratuito** – exigiu que o programa imprimisse `"Teste"` o mais rapido possivel (apos 1 iteracao).

### Limitacoes da solucao atual
- Os valores dos sensores sao simulados; para uso real, e necessario descomentar as leituras e garantir o hardware correto.
- O codigo nao implementa comunicacao LoRa ou envio para dashboard (apenas indicado como melhoria futura).
- A classificacao e baseada apenas em temperatura e gas – umidade e luz sao exibidas mas nao influenciam o estado.

### Melhorias que seriam feitas com mais tempo
- Implementar um filtro de media movel para suavizar os valores dos sensores.
- Adicionar um modo de baixo consumo para operacao com bateria solar.
- Integrar um modulo LoRa real (ex.: SX1278) e um protocolo simples de transmissao.
- Criar um dashboard web (via ESP32 com Wi-Fi) para visualizacao remota.
