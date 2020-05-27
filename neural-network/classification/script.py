# -*- coding: utf-8 -*-

try:
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
except ImportError as e:
    print("[FAILED] {}".format(e))

class originalSize():

    @staticmethod
    def data():

        try:

            # Import
            data = pd.read_csv('/home/vinhali/Desktop/arima/data/minute.csv')

            X = data.iloc[:, 0].values
            Y = data.iloc[:, 1].values
            
            print("[SUCESS] Created data")

            return X,Y
        
        except Exception as e:

            print("[FAILED] Caused by: {}".format(e))

    @staticmethod        
    def while_generator(start, n):
        i = start
        while i <= n:
            yield i
            i += 1

    @staticmethod
    def Kmodeling():

        try:

            X,Y = flow.data() # Create X and Y

            print ("[INFO] Data received for analysis:\n {}".format(Y))
            print ("[INFO] Range received for analysis:\n {}".format(X))
            print ("[INFO] Grouping data ...")

            total = len(Y)

            a1 = int((total / 100) * 20)
            a2 = int((total / 100) * 40)
            a3 = int((total / 100) * 60)
            a4 = int((total / 100) * 80)

            A = [Y[i] for i in flow.while_generator(0, a1)]
            B = [Y[i] for i in flow.while_generator(a1,a2)]
            C = [Y[i] for i in flow.while_generator(a2,a3)]
            D = [Y[i] for i in flow.while_generator(a3,a4)]
            E = [Y[i] for i in flow.while_generator(a4,(total - 1))]

            print("""Total of elements: {0}\n
            Conjunto A = {2} - Size {1}
            Conjunto B = {4} - Size {3}
            Conjunto C = {6} - Size {5}
            Conjunto D = {8} - Size {7}
            Conjunto E = {10} - Size {9}
            """.format(
                total,len(A),A,len(B),B,len(C),C,len(D),D,len(E),E
            ))

            print("[SUCESS] Complete data modeling")

            sns.set_style("white")
            kwargs = dict(hist_kws={'alpha':.6}, kde_kws={'linewidth':2})

            plt.figure(figsize=(10,4), dpi= 100)
            sns.distplot(A, color="dodgerblue", label="A 20%", **kwargs)
            sns.distplot(B, color="orange", label="B 20% - 40%", **kwargs)
            sns.distplot(C, color="deeppink", label="C 40% - 60%", **kwargs)
            sns.distplot(D, color="green", label="D 60% - 80%", **kwargs)
            sns.distplot(E, color="red", label="E 80% - 100%", **kwargs)
        
            plt.xlim(50,100)
            plt.legend(loc="upper right")
            plt.ylabel('Frequency')
            plt.xlabel('Consume')
            plt.title("Histogram")
            plt.show()
        
        except Exception as e:

            print("[FAILED] Caused by: {}".format(e))

flow = originalSize()
flow.Kmodeling()

 #A: 0 - 20% das leituras
 #B: 20% - 40% das leituras
 #C: 40% - 60% das leituras
 #D: 60% - 80% das leituras
 #E: 80% - 100% das leituras
 
 #Treinos:
 #Train A, B, C, D / Test E
 #Train A, B, C, E / Test D
 #Train A, B, D, E / Test C
 #Train A, C, D, E / Test B
 #Train B, C, D, E / Test A
