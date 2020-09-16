#!/usr/bin/env python
# coding: utf-8

# ## Conversion of a CPU consumption time series into means and standard deviation to calculate the next peak occurrences using a neural network

# ### Imports

# In[22]:


import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from keras.initializers import VarianceScaling
from keras.regularizers import l2
from keras.models import Sequential
from keras.layers import Dense
from sklearn.model_selection import KFold
from sklearn.metrics import cohen_kappa_score


# ### Read the data

# In[23]:


df = pd.read_csv('../data/cpu-7day.csv')
data = df.iloc[:, 1].values


# In[24]:


pd.DataFrame(data)


# ### Divide the data into blocks of 50 elements, where each new block it moves 10 elements

# In[25]:


blocks_data = []
for i in np.arange(0, int(data.shape[0]-40), 10):
    blocks_data.append(data[i:i+50])
blocks_data = np.array(blocks_data)


# ### Then divide the blocks into 5 parts (10x5 = 50)

# In[26]:


parts_data = blocks_data.reshape(-1, 5, 10)


# ### Calculate average and deviation of each part

# In[27]:


mean_parts_data = np.mean(parts_data, axis = -1)
std_parts_data = np.std(parts_data, axis = -1, ddof = 1)


# ### Take the next 20 elements from each block of 50 elements

# In[28]:


next_data = []
for i in np.arange(50, int(data.shape[0]-10), 10):
    next_data.append(data[i:i+20])
next_data = np.array(next_data)


# ### Calculate how many readings there are from 0 to 100, grouping every 20

# In[29]:


count_groups = np.array([np.sum(((0<=next_data) & (next_data<20))*1, axis = -1),
                         np.sum(((20<=next_data) & (next_data<40))*1, axis = -1),
                         np.sum(((40<=next_data) & (next_data<60))*1, axis = -1),
                         np.sum(((60<=next_data) & (next_data<80))*1, axis = -1),
                         np.sum(((80<=next_data) & (next_data<100))*1, axis = -1)]).T


# ### Collect all and merge in new dataframe

# In[30]:


mean_std = np.append(mean_parts_data.reshape(-1, 1), std_parts_data.reshape(-1, 1), axis = -1).reshape(-1, 10)
pad_count_groups = np.pad(count_groups, (0, mean_std.shape[0]-count_groups.shape[0]))[:, :5]
res_data = np.append(mean_std, pad_count_groups, axis = 1)


# ### View data

# In[31]:


columns = ['mean_1', 'std_1', 'mean_2', 'std_2', 'mean_3', 'std_3', 'mean_4', 'std_4', 'mean_5', 'std_5',
           '0_20', '20_40', '40_60', '60_80', '80_100']
DF = pd.DataFrame(res_data, columns = columns)


# In[32]:


DF


# ### Normalization, dividing all column elements by the highest occurrence of the column itself (0,1)

# In[33]:


revert = DF.max()
DF.max()


# In[34]:


DF.divide(DF.max())


# In[35]:


DF = DF.divide(DF.max())


# ## Dividing averages/deviation in X and counts in Y

# ### Viewing the neuron input

# In[36]:


X = DF.iloc[:, 0:10]

X.plot(kind='line', stacked=True); X


# ### Visualizing the output of the neuron

# In[37]:


Y = DF.iloc[:, 10:15];

Y.plot(kind='line', stacked=True);
pd.DataFrame(count_groups, columns = ['0-20','20-40','40-60','60-80','80-100']).sum().plot(kind='bar', stacked=True)


# ### Visualizing the shape of the axes

# In[38]:


X.shape, Y.shape


# ### Preparing cross validation k = 5

# In[39]:


kfold = KFold(5, False, 1)


# ### Training:

# In[40]:


cvscores = []
for train, test in kfold.split(X,Y):

    model = Sequential()
    model.add(Dense(10,
                kernel_regularizer=l2(0.001),
                kernel_initializer=VarianceScaling(), 
                activation='sigmoid',
                name='hidden-input'))
    model.add(Dense(5, 
                kernel_regularizer=l2(0.001),
                kernel_initializer=VarianceScaling(),                 
                activation='sigmoid',
                name='output'))
    
    model.compile(loss='mse', optimizer='adam', metrics=['mse'])
    
    model.fit(X.iloc[train].values, Y.iloc[train].values, epochs=100, batch_size=5, verbose = 0, shuffle=False,
              validation_data=(X.iloc[test].values, Y.iloc[test].values))

    scores = model.evaluate(X.iloc[test].values, Y.iloc[test].values, verbose=0)
    print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
    cvscores.append(scores[1] * 100)

print("%.2f%% (+/- %.2f%%)" % (np.mean(cvscores), np.std(cvscores)))


# ### Viewing the network structure

# In[41]:


model.summary()


# ### Generating prediction based on X readings

# In[42]:


y = model.predict(X)


# In[43]:


len(X)


# In[44]:


result = pd.DataFrame(y); result


# ### Reverting binary values to decimals

# In[45]:


maxOccurrence = revert[10:15]; maxOccurrence


# In[46]:


speak = result.multiply(maxOccurrence.values);speak


# ### Grouping data into occurrences for sum

# In[47]:


next_data = np.array(speak)
count_groups = np.array([np.sum(((0<=next_data) & (next_data<20))*1, axis = -1),
                         np.sum(((20<=next_data) & (next_data<40))*1, axis = -1),
                         np.sum(((40<=next_data) & (next_data<60))*1, axis = -1),
                         np.sum(((60<=next_data) & (next_data<80))*1, axis = -1),
                         np.sum(((80<=next_data) & (next_data<100))*1, axis = -1)]).T


# ### Forecasting next peaks based on grouping

# In[48]:


count_groups.sum(axis=0)


# ### Generating histogram of readings

# In[49]:


columns = ['0-20','20-40','40-60','60-80','80-100']
peaks = pd.DataFrame(count_groups, columns = columns)


# In[50]:


peaks.sum().plot(kind='bar', stacked=True)

