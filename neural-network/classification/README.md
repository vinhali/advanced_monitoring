# Classificação de picos de consumo:

Este projeto tem como objetivo prever picos de consumo de CPU baseado na relação entre as varíaveis das 60 primeiras ocorrências (1 hora) com os picos das próximas 60 ocorrências.

### O ciclo de treino

<img src="https://github.com/vinhali/advanced_monitoring/blob/master/neural-network/classification/img/estrutura.png?raw=true" width="400px" height="600px">

### Formúla para cada item

<img src="https://github.com/vinhali/advanced_monitoring/blob/master/neural-network/classification/img/mat.png?raw=true"/>

### Rectified Linear Unit

<img src="https://github.com/vinhali/advanced_monitoring/blob/master/neural-network/classification/img/mat2.png?raw=true"/>
<img src="https://github.com/vinhali/advanced_monitoring/blob/master/neural-network/classification/img/mat3.jpeg?raw=true"/>

### Input Layer:

<img src="https://github.com/vinhali/advanced_monitoring/blob/master/neural-network/classification/img/input_layer.png?raw=true" width="600px" height="300px"/>

### Output Layer:

<img src="https://github.com/vinhali/advanced_monitoring/blob/master/neural-network/classification/img/output_layer.png?raw=true" width="600px" height="300px"/>

### Normalize:

                 m1,d1           m2,d2           m3,d3           m4,d4           m5,d5   0-20  20-40  40-60  60-80  80-100
    0   [0.573, 0.699]  [0.412, 0.224]  [0.696, 0.512]  [0.326, 0.314]   [0.79, 0.685]  1.000    0.5      0      0       0
    1   [0.456, 0.251]  [0.629, 0.523]  [0.344, 0.286]    [0.8, 0.699]    [0.721, 1.0]  1.000    0.5      0      0       0
    2   [0.658, 0.531]  [0.339, 0.282]  [0.592, 0.614]    [0.859, 1.0]  [0.365, 0.283]  1.000    0.5      0      0       0
    3   [0.396, 0.314]   [0.29, 0.201]      [1.0, 1.0]   [0.34, 0.288]  [0.886, 0.647]  1.000    0.5      0      0       0
    4   [0.379, 0.315]      [1.0, 1.0]  [0.302, 0.248]  [0.929, 0.655]  [0.328, 0.308]  1.000    0.5      0      0       0
    5       [1.0, 1.0]  [0.274, 0.249]  [0.679, 0.536]   [0.52, 0.413]  [0.382, 0.337]  1.000    0.5      0      0       0

    Até a linha 47 ...
    
 ### Explicação da normalização:

> *m1 = Média de 12 leituras (Em uma janela de 60 dados) - Exemplo ((2 + 5 + 7 ...) / 12*

> *d1 = desvio padrão dos 12 dados*

E assim sucessivamente até formar m5, d5 (12x5 = 60)

> *0-20 = Quantas vezes os valores são repetidos no intervalo de 0 a 20 nas próximas 30 leituras (Linha 61,62,62 ...)*

E assim sucessivamente até formar 20-40.40-60.60-80.80-100

### Sumário

    Layer (type)                 Output Shape              Param #
    =================================================================
    
### Treino

<img src="">

### Resultado

<img src="">
