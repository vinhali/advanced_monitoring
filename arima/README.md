## Arima

ARIMA é um acrônimo que significa Média Móvel Integrada autorregressiva. É uma classe de modelo que captura um conjunto de diferentes estruturas temporais padrão em dados de séries temporais.

Esse acrônimo é descritivo, capturando os principais aspectos do próprio modelo. Resumidamente, eles são:
  - AR: Regressão automática. Um modelo que usa a relação dependente entre uma observação e algum número de observações atrasadas.
  - I: Integrado. O uso da diferenciação de observações brutas (por exemplo, subtraindo uma observação de uma observação na etapa temporal anterior), a fim de tornar a série temporal estacionária.
  - MA: Média Móvel. Um modelo que usa a dependência entre uma observação e um erro residual de um modelo de média móvel aplicado a observações atrasadas.

Cada um desses componentes é explicitamente especificado no modelo como um parâmetro. Uma notação padrão é usada para ARIMA (p, d, q), em que os parâmetros são substituídos por valores inteiros para indicar rapidamente o modelo ARIMA específico que está sendo usado.

Os parâmetros do modelo ARIMA são definidos da seguinte maneira:

  - p: O número de observações de atraso incluídas no modelo, também chamado de ordem de atraso.
  - d: O número de vezes que as observações brutas são diferenciadas, também chamado de grau de diferenciação.
  - q: O tamanho da janela da média móvel, também chamada de ordem da média móvel.

## Modelo de média móvel integrada autorregressiva

Um modelo ARIMA é uma classe de modelos estatísticos para analisar e prever dados de séries temporais.

Ele explicitamente atende a um conjunto de estruturas padrão em dados de séries temporais e, como tal, fornece um método simples, porém poderoso, para fazer previsões hábeis de séries temporais.

## Forecast

<img src="https://raw.githubusercontent.com/vinhali/advanced_monitoring/master/arima/img/arima.png">
