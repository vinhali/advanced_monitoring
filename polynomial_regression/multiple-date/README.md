## Regressão polinomial para consumo de CPU com série temporal

Visualizando regressão linear simples:

<img src="https://github.com/vinhali/advanced_monitoring/blob/master/polynomial_regression/img/linear_multiple.png?raw=true"/>

Visualizando regressão polinomial grau 4:

<img src="https://github.com/vinhali/advanced_monitoring/blob/master/polynomial_regression/img/forecast_multiple.png?raw=true"/>

Previsão para o tempo de 20 minutos com valor único:

    68.50463233
    
Realizada com o trecho:

    # 20 = time
    print(pol_reg.predict(poly_reg.fit_transform([[20]])))

Referência: https://towardsdatascience.com/machine-learning-polynomial-regression-with-python-5328e4e8a386
