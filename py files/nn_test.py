import numpy as np
import pandas as pd
import os
from matplotlib import pyplot as plt

f_name = 'NGA_West2_finitefault.csv'

pd.set_option('display.max_columns', None)


df = pd.read_csv(f_name)
df.replace(np.nan, 0)
df.replace('',0, regex=True)
df.columns

from sklearn import metrics
x_set_values = df[['Hypocenter Depth (km)', 'Total Fault Length (km)', 'Total Fault Width (km)','Strike (deg)',
'Dip  (deg)']].values

y_set_values = df['Moment Magnitude'].values

from sklearn.model_selection import train_test_split

x_train25, x_test25, y_train25, y_test25 = train_test_split(x_set_values, 
y_set_values, test_size = 0.25, random_state=1)

print(y_train25, type(y_train25))

# Scaled values using standard scaling
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

sc = StandardScaler()
x_train25 = sc.fit_transform(x_train25)
x_test25 = sc.transform(x_test25)


from sklearn.neural_network import MLPRegressor as mlp 

clf = mlp(solver = 'lbfgs',
alpha = 1e-5,
hidden_layer_sizes = (100,6),
random_state=1)

clf.fit(x_train25, y_train25)

y_pred_nn = clf.predict(x_test25)

residuals = y_test25 - y_pred_nn 


## PLOTTING PREDICTED AND ACTUAL MOMENT MAGNITUDE
df_temp = pd.DataFrame(
    {'Actual': y_test25,
    'Predicted': y_pred_nn}
)
df_temp = df_temp.head(30)
df_temp.plot(kind='bar',figsize=(10,6))
plt.grid(which='major', linestyle='-', linewidth='0.5', color='green')
plt.grid(which='minor', linestyle=':', linewidth='0.5', color='black')



plt.title('Actual Moment and Predicted Moment', fontsize=20)
plt.xlabel('Moment', fontsize=18)
plt.ylabel('Moment magnitude', fontsize=16)
fig.savefig('Moments predicted.jpg')

plt.show()

## PLOTTING RESIDUALS 
fig, ax = plt.subplots(figsize = (10,10))

ax.plot(y_test25, residuals, 'ro')

ax.set_xlabel('True moment magnitude')
ax.set_ylabel('Residuals')

plt.title('True moment and residuals from neural network')

plt.grid(which='both', axis = 'both')
plt.show()