import os
import seaborn
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("/Users/marcinic/american_messi/data/final_data.csv")
viz_dir = "/Users/marcinic/american_messi/visualizations"

ax = seaborn.residplot('income','num_players',data=data)
ax.set_title('Residuals of Income on Number of USYNT Players 2015-2018')
plt.savefig(os.path.join(viz_dir,'residplot.png'))
plt.close()

ax = seaborn.regplot('income','num_players',data=data)
ax.set_title('County-level Income on Number of USYNT Players 2015-2018')
plt.savefig(os.path.join(viz_dir,'regplot.png'))
