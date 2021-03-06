import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.manifold import TSNE
from sklearn.decomposition import TruncatedSVD
from ggplot import *
import ggplot
import config as cfg

path = cfg.path
features_file = 'featuresFlowCapAnalysis2017.csv'
labels_file = 'labelsFlowCapAnalysis2017.csv'
save_fig_boxplot  ='boxplot_allsubjects1.eps'
save_fig_zscore_train = 'tsne_train_zscore.png'
save_fig_train_no_47 = 'tsne_train_no47.png'
save_fig_train_reduced = 'tsne_train_reduced.png'
save_fig_train_reduced_48 = 'tsne_train_reduced_48.png'

save_dataset1 = 'train_65.csv'
save_dataset2 = 'train_48.csv'

# loading training data
df_whole = pd.read_csv(path+features_file) #(359, 186)

features_train = df_whole.iloc[:179,:] 
labels_train = pd.read_csv(path+labels_file) 

features_test = df_whole.iloc[179:,:]

labels_train = pd.read_csv(path+labels_file) 
labels = np.asarray(labels_train)

# z-score transformation
## ---------------------------------------------------------------------------------

df = features_train

cols = list(df.columns)
for col in cols:
    col_zscore = col + '_zscore'
    df[col_zscore] = (df[col] - df[col].mean())/df[col].std(ddof=0)

df_z = df.iloc[:,186:]

# Plotting with z-score transformation

X_reduced = TruncatedSVD(n_components=70, random_state=42).fit_transform(df_z.values)

tsne = TSNE(n_components=2, verbose=0, perplexity=40, n_iter=1000, random_state=42)
tsne_results = tsne.fit_transform(X_reduced,labels_train)
df_tsne = pd.DataFrame(tsne_results,columns=['x-tsne','y-tsne'])
df_tsne['label']=np.asarray(labels_train)
chart = ggplot.ggplot(df_tsne, aes(x='x-tsne', y='y-tsne', color='label') ) + geom_point() + scale_color_brewer(type='diverging', palette=4)+ggtitle("tsne for dimensionality reduction on zscores (train set)")
chart.save(path+save_fig_zscore_train)
plt.close('all')

# plot with only most 65 informative features
## ----------------------------------------------------------------------------------------------------

df_z.columns = range(0,186)
leave_only = ['133', '10', '132', '122', '121', '125', '137', '183', '6', '40', '36', '7', '38', '8', '182', '91', '120', '181', '1', '136', '90', '2', '95', '123', '53', '48', '87', '94', '176', '14', '37', '3', '174', '134', '180', '167', '52', '178', '124', '89', '81', '4', '85', '162', '129', '166', '5', '0', '135', '79', '185', '141', '39', '83', '50', '99', '93', '26', '68', '49', '168', '27', '117', '16', '57']
leave_only_int = [int(n) for n in leave_only]
df1 = df_z[leave_only_int]



# Plotting with only important features

# X_reduced = TruncatedSVD(n_components=70, random_state=42).fit_transform(df_z.values)

tsne = TSNE(n_components=2, verbose=0, perplexity=40, n_iter=1000, random_state=42)
tsne_results = tsne.fit_transform(df1.values,labels_train)
df_tsne = pd.DataFrame(tsne_results,columns=['x-tsne','y-tsne'])
df_tsne['label']=np.asarray(labels_train)
chart = ggplot.ggplot(df_tsne, aes(x='x-tsne', y='y-tsne', color='label') ) + geom_point() + scale_color_brewer(type='diverging', palette=4)+ggtitle("tsne for dimensionality reduction on reduced features (train set)")
chart.save(path+save_fig_train_reduced)
plt.close('all')

# plot with only most 48 informative features
## ----------------------------------------------------------------------------------------------------

leave_only_int1 = leave_only_int[:48]
df2 = df_z[leave_only_int1]

# Plotting with only important features

tsne = TSNE(n_components=2, verbose=0, perplexity=40, n_iter=1000, random_state=42)
tsne_results = tsne.fit_transform(df2.values,labels_train)
df_tsne = pd.DataFrame(tsne_results,columns=['x-tsne','y-tsne'])
df_tsne['label']=np.asarray(labels_train)
chart = ggplot.ggplot(df_tsne, aes(x='x-tsne', y='y-tsne', color='label') ) + geom_point() + scale_color_brewer(type='diverging', palette=4)+ggtitle("tsne for dimensionality reduction on reduced features (train set)")
chart.save(path+save_fig_train_reduced_48)
plt.close('all')


#Save datasets

df1.to_csv(path+save_dataset1)
df2.to_csv(path+save_dataset2)

