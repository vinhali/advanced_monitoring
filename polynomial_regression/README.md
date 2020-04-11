## Regressão polinomial para consumo de CPU

Visualizando regressão linear simples:

<img src="https://github.com/vinhali/advanced_monitoring/blob/master/polynomial_regression/img/linear.png?raw=true"/>

Visualizando regressão polinomial grau 4:

<img src="https://github.com/vinhali/advanced_monitoring/blob/master/polynomial_regression/img/poly.png?raw=true"/>

Previsão para o tempo de 20 minutos com valor único:

    77.27450056
    
Realizada com o trecho:

    # 20 = time
    print(pol_reg.predict(poly_reg.fit_transform([[20]])))
