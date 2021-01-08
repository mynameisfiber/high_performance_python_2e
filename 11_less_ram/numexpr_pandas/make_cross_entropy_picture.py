import matplotlib.pyplot as plt

import pandas as pd
import numpy as np
#nbr_items = 200_000_000

nbr_items = 99
yp = np.linspace(0.01, 0.99, nbr_items)
yt = np.ones(nbr_items)
answer = -(yt * np.log(yp) + ((1-yt) * (np.log(1-yp))))

yt0 = np.zeros(nbr_items)
answer0 = -(yt0 * np.log(yp) + ((1-yt0) * (np.log(1-yp))))

df = pd.DataFrame({'yp': yp, 'yt': yt, 'cross_entropy': answer, 'cross_entropy0': answer0})

fig, axs = plt.subplots(ncols=2)
ax = axs[0]
df.plot(x='yp', y='cross_entropy', ax=ax, label='Error for yt==1')
df.plot(x='yp', y='cross_entropy0', ax=ax, label='Error for yt==0', linestyle='--')
ax.set_ylabel('Cross Entropy or Error (smaller is better)')
ax.set_xlabel('Predicted Probability (yp)')
ax.set_title('Cross Entropy error for targets yt 0 and 1')

ax = axs[1]
logs = np.log(yp)
df_log = pd.DataFrame({'yp': yp, 'log_yp': logs})
df_log.plot(x='yp', y='log_yp', ax=ax)
ax.set_title('Natural Log for x==[0, 1]')
ax.set_xlabel('Predicted Probability (yp)')

plt.tight_layout()
plt.savefig('cross_entropy.png')
