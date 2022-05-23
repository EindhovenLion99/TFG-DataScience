# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# %%
results = pd.read_csv('CSV/Segunda-20-21-Estadios.csv')

# %%
results.head()

# %%
results.info()

# %%
results.describe()

# %%
results['Goles1'].plot(kind = 'box', vert=False)

# %%
ax = results['Goles1'].plot(kind = 'density', figsize=(14, 6))
ax.axvline(results['Goles1'].mean(), color = 'red')
ax.axvline(results['Goles1'].median(), color = 'green')


# %%
ax = results['Goles2'].plot(kind = 'density', figsize=(14, 6))
ax.axvline(results['Goles2'].mean(), color = 'red')
ax.axvline(results['Goles2'].median(), color = 'green')

# %%
ax = results['Goles1'].plot(kind = 'hist', figsize=(14, 6))
ax.set_ylabel('Partidos')
ax.set_xlabel('Goles')

# %%
results['Goles1'].value_counts()
# %%
results['Goles1'].value_counts().plot(kind = 'pie')

# %%
ax = results['Goles1'].plot(kind = 'bar', figsize=(14, 6))
ax.set_ylabel('Partidos')
# %%
corr = results.corr()
corr
# %%
fig = plt.figure(figsize=(8,8))
plt.matshow(corr, cmap='RdBu', fignum=fig.number)
plt.xticks(range(len(corr.columns)), corr.columns, rotation='vertical')
plt.yticks(range(len(corr.columns)), corr.columns)
# %%
results.plot(kind='scatter', x='Goles1', y='Goles2', figsize=(6,6))
# %%
results.loc[results['Goles1'] >= 3, 'Goles2'].mean()

# %%
