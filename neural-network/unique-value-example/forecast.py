try:
    import sys
    import datetime
    import numpy as np
    import pandas as pd
    import tensorflow as tf
    from sklearn.metrics import mean_absolute_error
except ImportError as e:
    print("[ALERT] Error import caused by: {}".format(e))
    sys.exit()

base = pd.read_csv('csv/cpu.csv')
base = base.dropna()

date = base.iloc[:,5].values
base = base.iloc[:,4].values
periodos = 1
previsao_futura = 1

X = base[0:(len(base) - (len(base) % periodos))]
X_batches = X.reshape(-1, periodos, 1)

y = base[0:(len(base) - (len(base) % periodos)) + previsao_futura]
y_batches = y.reshape(-1, periodos, 1)

X_teste = base[-(periodos + previsao_futura):]
X_teste = X_teste[:periodos]
X_teste = X_teste.reshape(-1, periodos, 1)
y_teste = base[-(periodos):]
y_teste = y_teste.reshape(-1, periodos, 1)

tf.reset_default_graph()

entradas = 1
neuronios_oculta = 2000
neuronios_saida = 1

xph = tf.placeholder(tf.float32, [None, periodos, entradas])
yph = tf.placeholder(tf.float32, [None, periodos, neuronios_saida])

def cria_uma_celula():
    return tf.contrib.rnn.LSTMCell(num_units = neuronios_oculta, activation = tf.nn.relu)

def cria_varias_celulas():
    celulas =  tf.nn.rnn_cell.MultiRNNCell([cria_uma_celula() for i in range(4)])
    return tf.contrib.rnn.DropoutWrapper(celulas, output_keep_prob = 0.1)

celula = cria_varias_celulas()

celula = tf.contrib.rnn.OutputProjectionWrapper(celula, output_size = 1)

saida_rnn, _ = tf.nn.dynamic_rnn(celula, xph, dtype = tf.float32)
erro = tf.losses.mean_squared_error(labels = yph, predictions = saida_rnn)
otimizador = tf.train.AdamOptimizer(learning_rate = 0.001)
treinamento = otimizador.minimize(erro)

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    
    for epoca in range(200):
        _, custo = sess.run([treinamento, erro], feed_dict = {xph: X_batches, yph: y_batches})
        if epoca % 100 == 0:
            print(epoca + 1, ' erro: ', custo)
    
    previsoes = sess.run(saida_rnn, feed_dict = {xph: X_teste})
    
y_teste.shape
y_teste2 = np.ravel(y_teste)

previsoes2 = np.ravel(previsoes)

mae = mean_absolute_error(y_teste2, previsoes2)

print("[INFO] Base Shape: {0}".format(np.shape(base)))
print("[INFO] X Shape: {0}".format(np.shape(X)))
print("[INFO] X_batches Shape: {0}".format(np.shape(X_batches)))
print("[INFO] Y Shape: {0}".format(np.shape(y)))
print("[INFO] y_batches Shape: {0}".format(np.shape(y_batches)))
print("[INFO] X_teste Shape: {0}".format(np.shape(X_teste)))
print("[INFO] y_teste Shape: {0}".format(np.shape(y_teste)))
print("[INFO] Mean absolute Error: {0}".format(mae))
print("[RESULT] Treshold: {0} at {1}".format(previsoes2,datetime.datetime.now()))
