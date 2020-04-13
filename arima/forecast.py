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

class operationsArima():

    @staticmethod
    def ForecastingWithArima():

        try:

            # Import
            data = pd.read_csv('drugs.csv', parse_dates=['date'], index_col='date')

            # Plot
            fig, axes = plt.subplots(2, 1, figsize=(10,5), dpi=100, sharex=True)

            # Usual Differencing
            axes[0].plot(data[:], label='Original Series')
            axes[0].plot(data[:].diff(1), label='Usual Differencing')
            axes[0].set_title('Usual Differencing')
            axes[0].legend(loc='upper left', fontsize=10)
            print("[OK] Generated axes")

            # Seasonal
            axes[1].plot(data[:], label='Original Series')
            axes[1].plot(data[:].diff(12), label='Seasonal Differencing', color='green')
            axes[1].set_title('Seasonal Differencing')
            plt.legend(loc='upper left', fontsize=10)
            plt.suptitle('Drug Sales', fontsize=16)
            plt.show()

            # Seasonal - fit stepwise auto-ARIMA
            smodel = pm.auto_arima(data, start_p=1, start_q=1,
                                    test='adf',
                                    max_p=3, max_q=3, m=12,
                                    start_P=0, seasonal=True,
                                    d=None, D=1, trace=True,
                                    error_action='ignore',
                                    suppress_warnings=True,
                                    stepwise=True)

            smodel.summary()
            print("[OK] Generated model")

            # Forecast
            n_periods = 24
            fitted, confint = smodel.predict(n_periods=n_periods, return_conf_int=True)
            index_of_fc = pd.date_range(data.index[-1], periods = n_periods, freq='MS')

            # make series for plotting purpose
            fitted_series = pd.Series(fitted, index=index_of_fc)
            lower_series = pd.Series(confint[:, 0], index=index_of_fc)
            upper_series = pd.Series(confint[:, 1], index=index_of_fc)
            print("[OK] Generated series")

            # Plot
            plt.plot(data)
            plt.plot(fitted_series, color='darkgreen')
            plt.fill_between(lower_series.index,
                            lower_series,
                            upper_series,
                            color='k', alpha=.15)

            plt.title("ARIMA - Final Forecast - Drug Sales")
            plt.show()
            print("[SUCESS] Generated forecast")

        except Exception as e:

            print("[FAILED] Caused by: {}".format(e))

if __name__ == "__main__":
    flow = operationsArima()
    flow.ForecastingWithArima() # Init script
