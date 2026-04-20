# Detector de Níveis de Queimada - ESP32

Sistema de monitoramento ambiental que avalia o risco de incêndio florestal com base em temperatura, gases (simulando CO/VOC) e umidade. Utiliza um **ESP32**, sensor **DHT22**, sensor de gás **MQ-x** (simulado), **LDR** e display **OLED SSD1306**. Os **LEDs** indicam o nível de alerta em tempo real
<img width="782" height="802" alt="image" src="https://github.com/user-attachments/assets/a8617d0a-5b43-4d91-8a7c-485d355c2875" />

---

## Significado dos LEDs

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
## Implementações futuras.
Criação de um dispositivo central ligado a um dashboard. Os sipositivos de coleta seriam conectado ao dispositivo servidor via conexão sem fio.
