# -*- coding: utf-8 -*-
"""convlstm_1_.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1i8gnTsRQIKTD1mq6RgLfk5xfgN4-ntLk

layer 7, epoch 10, batchsize 32,
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy.io

mat = scipy.io.loadmat('/content/drive/MyDrive/mtech/project/spatial/sla_bob/years/sla_1993.mat')
print(len(mat))

print(mat.keys())

sla_1993=mat['sla_1993']
sshx_grid=mat['sshx_grid']
sshy_grid=mat['sshy_grid']
theta_1993=mat['theta_1993']
u_geos_1993=mat['u_geos_1993']
v_geos_1993=mat['v_geos_1993']

d=30000 #19/5/2012 10 am-28/7/2018 11pm
data=pd.read_csv('/content/drive/MyDrive/mtech/project/lstm_sst_2/moored_buoy_data/bd10/combined_3.csv')
df=data.iloc[:d,:]
data_matrix=df.to_numpy()
data_sliced=data_matrix[:,3:]

l=30#lookback
n=1#number of days predicting
#slice of data; this data is from #19-5-2012 3am - 19/5/2018 3 am

features_set = [] # Input Matrix
labels = []       # Output Array
for i in range(l, d-n+1):

    labels.append(data_sliced[i+n-1:i+n, 0])
'''for i in range(l, 30000):
    features_set.append(data_sliced[i][1:])
    labels.append(data_sliced[i][0])'''
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler(feature_range = (0, 1))
data_scaled = scaler.fit_transform(data_sliced)

for i in range(l, d-n+1):
    features_set.append(data_scaled[i-l:i, 0:data_sliced.shape[1]])


features_set, labels = np.array(features_set), np.array(labels)
features_set,labels=np.asarray(features_set).astype(np.float32),np.asarray(labels).astype(np.float32)

#features_set = np.reshape(features_set, (features_set.shape[0], features_set.shape[1],1))

# Shared Feature Extraction Layer
import tensorflow as tf
# from tf.keras.models import Sequential
from tensorflow.keras.utils import plot_model
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import concatenate
visible=Input(shape=(l,len(data_scaled[0])))
extract1=LSTM(5,return_sequences=True,activation='relu')(visible)
extract2=LSTM(6,return_sequences=True,activation='relu')(extract1)
merge=concatenate([extract2,visible])
extract3=LSTM(5)(merge)
output=Dense(1)(extract3)
model=Model(inputs=visible,outputs=output)
print(model.summary())
plot_model(model, to_file='shared_feature_extractor.png',show_shapes=True,
    show_dtype=True,
    show_layer_names=True,
    rankdir='TB',
    expand_nested=False,
    dpi=96,
    layer_range=None,
    show_layer_activations=True)

model.compile(optimizer = 'adam', loss = 'mean_squared_error')

model.fit(features_set, labels, epochs = 5, batch_size = 64)

model.save('/content/drive/MyDrive/mtech/project/lstm_sst_2/code/functional_api/timeandsst/model/sst_anomaly_l4_comb_epoch5_batch_64_v9.hdf5')