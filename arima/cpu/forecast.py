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
    
if __name__ == "__main__":
    view = originalSize()
    view.printDataset()
    flow = operationsArima()
    flow.ForecastingWithArima() # Init script
