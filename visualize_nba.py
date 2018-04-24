import pandas as pd
from pandas.plotting import scatter_matrix
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("clean_nba_data")
def scatter_nba(df):
    matplotlib.rc('figure', figsize=(10, 5))
    # scatter_matrix(df, alpha=0.2, figsize=(6, 6), diagonal='kde')
    scatter_matrix = scatter_matrix(
        df,
        figsize  = [20, 20],
        marker   = ".",
        s        = 0.6,
        diagonal = "kde"
    )

    for ax in scatter_matrix.ravel():
        ax.set_xlabel(ax.get_xlabel(), fontsize = 20, rotation = 90)
        ax.set_ylabel(ax.get_ylabel(), fontsize = 20, rotation = 0)

    plt.savefig("nba-data-scattermatrix.png")
def pairwise_nba(df):
    
    # Pair-wise Scatter Plots
    cols = ['pts','fgm','fga','fg%','3pm','3pa' ,'3p%','ftm','fta','ft%', 'oreb','dreb','reb','ast','stl','blk','tov','eff']
    pp = sns.pairplot(df[cols], size=1.8, aspect=1.8, diag_kind="kde")

    fig = pp.fig 
    fig.subplots_adjust(top=0.93, wspace=0.3)
    t = fig.suptitle('NBA Attributes Pairwise Plots', fontsize=14)
    fig.savefig("pairwise_nba.png")
def correlation_heat_map_nba(df):

# Correlation Matrix Heatmap
    f, ax = plt.subplots(figsize=(10, 6))
    corr = df.corr()
    hm = sns.heatmap(round(corr,2), annot=True, ax=ax, cmap="coolwarm",fmt='.2f',
                    linewidths=.05)
    f.subplots_adjust(top=0.93)
    t= f.suptitle('NBA Attributes Correlation Heatmap', fontsize=14)
    f.savefig("heatmap_nba.png")
# scatter_matrix(df)    
# pairwise_nba(df)  
# correlation_heat_map_nba(df)

df.plot()
plt.show()

