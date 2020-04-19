```python
# -*- coding: utf-8 -*-

try:
    import pandas as pd
    import numpy as np
    import pmdarima as pm
    import matplotlib.pyplot as plt
    from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
    from statsmodels.tsa.arima_model import ARIMA
    from statsmodels.tsa.seasonal import seasonal_decompose
    from dateutil.parser import parse
except ImportError as e:
    print("[FAILED] {}".format(e))
```


```python
class originalSize():

    @staticmethod
    def printDataset():

        try:

            # Import
            data = pd.read_csv('/home/vinhali/Desktop/arima/data/minute.csv')

            X = data.iloc[:, 0].values
            Y = data.iloc[:, 1].values
            
            plt.xticks(rotation=90)
            plt.plot(X, Y, color='blue')
            plt.title('Consume CPU')
            plt.xlabel('Time range')
            plt.ylabel('Consume')
            
            print("[SUCESS] Generated graphic")

            return plt.show()
        
        except Exception as e:

            print("[FAILED] Caused by: {}".format(e))
```


```python
class operationsArima():

    @staticmethod
    def ForecastingWithArima():

        try:

            # Import
            data = pd.read_csv('/home/vinhali/Desktop/arima/data/minute.csv', parse_dates=['date'], index_col='date')

            # Create X for view in graphic
            dataView = pd.read_csv('/home/vinhali/Desktop/arima/data/minute.csv')
            X = dataView.iloc[:, 0].values
            
            # Seasonal - fit stepwise auto-ARIMA
            smodel = pm.auto_arima(data, start_p=1, start_q=1,
                                    test='adf',
                                    max_p=3, max_q=3, m=11,
                                    start_P=0, seasonal=True,
                                    d=None, D=1, trace=True,
                                    error_action='ignore',
                                    suppress_warnings=True,
                                    stepwise=True)

            smodel.summary()
            print(smodel.summary())
            print("[OK] Generated model")

            # Forecast
            n_periods = 11
            fitted, confint = smodel.predict(n_periods=n_periods, return_conf_int=True)
            index_of_fc = pd.date_range(data.index[-1], periods = n_periods, freq='T')

            # make series for plotting purpose
            fitted_series = pd.Series(fitted, index=index_of_fc)
            lower_series = pd.Series(confint[:, 0], index=index_of_fc)
            upper_series = pd.Series(confint[:, 1], index=index_of_fc)
            print("[OK] Generated series")
            


            # Plot
            plt.xticks(rotation=90)
            plt.plot(fitted_series, color='darkgreen')
            plt.fill_between(lower_series.index,
                            lower_series,
                            upper_series,
                            color='k', alpha=.15)

            plt.title("ARIMA - Final Forecast - CPU consume")
            plt.show()
            print("[SUCESS] Generated forecast")

        except Exception as e:

            print("[FAILED] Caused by: {}".format(e))
```


```python
if __name__ == "__main__":
    view = originalSize()
    view.printDataset()
    flow = operationsArima()
    flow.ForecastingWithArima() # Init script
```

    [SUCESS] Generated graphic



![png](output_3_1.png)


    Fit ARIMA: order=(0, 0, 0) seasonal_order=(0, 1, 0, 11); AIC=nan, BIC=nan, Fit time=0.034 seconds
    Total fit time: 0.036 seconds
                                    SARIMAX Results                                 
    ================================================================================
    Dep. Variable:                        y   No. Observations:                   22
    Model:             SARIMAX(0, 1, 0, 11)   Log Likelihood                     nan
    Date:                  Sun, 19 Apr 2020   AIC                                nan
    Time:                          15:08:20   BIC                                nan
    Sample:                               0   HQIC                               nan
                                       - 22                                         
    Covariance Type:                    opg                                         
    ==============================================================================
                     coef    std err          z      P>|z|      [0.025      0.975]
    ------------------------------------------------------------------------------
    intercept           0   5.33e-13          0      1.000   -1.05e-12    1.05e-12
    sigma2          1e-10   5.81e-10      0.172      0.863   -1.04e-09    1.24e-09
    ===================================================================================
    Ljung-Box (Q):                         nan   Jarque-Bera (JB):                  nan
    Prob(Q):                               nan   Prob(JB):                          nan
    Heteroskedasticity (H):                nan   Skew:                              nan
    Prob(H) (two-sided):                   nan   Kurtosis:                          nan
    ===================================================================================
    
    Warnings:
    [1] Covariance matrix calculated using the outer product of gradients (complex-step).
    [OK] Generated model
    [OK] Generated series


![png](output_3_4.png)


    [SUCESS] Generated forecast



```python

```
