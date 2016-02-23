#  %matplotlib inline
import subprocess
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import scipy.stats as st
from sklearn.cluster import KMeans
from progress.bar import Bar
from itertools import *


# Get the data
myCommand = 'pypy pypy-graph-alloc-removal.py 2>/dev/null | tail -n2 | head -n1'
nRuns = 7
rawData = dict()
bar = Bar('Running ...', max=nRuns+1)
bar.start()
# for ii in range(7):
#     rawData['run{0:02d}'.format(ii)] = eval(
#         subprocess.check_output(myCommand, shell=True))
#     bar.next()
# data = pd.DataFrame.from_dict(rawData)
data = pd.DataFrame.from_csv('foo.csv')

data['gg'] = data.index / 5

xx = data.groupby('gg').mean()
yy = data.groupby('gg').std()

fig, ax = plt.subplots(ncols=1)
yy = data['run00'].groupby('gg').mean().get_values()

ax.plot(range(100), )
plt.show()

## reshape the data to use seaborn
#N, K = data.shape
#unpivotedDataDict = {'duration': data.values.ravel('F'),
#                     'runId': np.asarray(data.columns).repeat(N),
#                     'executionId': np.tile(np.asarray(data.index), K)}
#
#data = pd.DataFrame.from_dict(unpivotedDataDict)
#bar.finish()
#
#print data
#sns.tsplot(data, "executionId", "runId", None, "duration")
#sns.plt.show()

## Show the data
#fig1, ax = plt.subplots(ncols=1, nrows=1)
#for ll, currentColor in zip((l1, l2, l3, l4, l5, l6, l7),
#                            sns.color_palette("hls",  7)):
#    ax.scatter(range(samplesPerRun), ll, c=currentColor)
#fig1.show()
#
## Try how well the data fits some distributions
#data = l1
#distributions = [st.laplace, st.norm, st.gamma]
#mles = []
#
#fig2, ax = plt.subplots(ncols=len(distributions), nrows=1)
#for index, distribution in enumerate(distributions):
#    pars = distribution.fit(data)
#    mle = distribution.nnlf(pars, data)
#    mles.append(mle)
#    x = range(samplesPerRun)
#    ax[index].scatter(x, ll)  # , c=currentColor[index])
#    #yy = 
#    #ax[index].plot(x, distribution.pdf(x, pars), 'r-')
#fig2.show()
#
#results = [(distribution.name, mle) for distribution, mle in zip(distributions, mles)]
#best_fit = sorted(zip(distributions, mles), key=lambda d: d[1])[0]
#print 'Best fit reached using {}, MLE value: {}'.format(best_fit[0].name, best_fit[1])
#
#plt.show()
#
## data = np.hstack((np.array(l1), np.array(l2), np.array(l3), np.array(l4),
##                   np.array(l5), np.array(l6), np.array(l7)))
## someColors = sns.color_palette("hls", 7)
## 
## runLabel = []
## for c in someColors[:7]:
##     runLabel = runLabel+[c, ]*500
## 
## # Try to cluster it in order to see if it follows any pattern
## kmeans_model = KMeans(n_clusters=5, random_state=1).fit(data.reshape(-1, 1))
## clusterLabels = [someColors[kk] for kk in kmeans_model.labels_]
## # to use the generative for like [ foo[kk] (or default value) for kk in K ]
## # but properly maybe you find hints here:
## # http://stackoverflow.com/questions/6981717/pythonic-way-to-combine-for-loop-and-if-statement
## # meanwhile just run this
## previousClusterLabel = [(0, 0, 0)] + clusterLabels[:-2]
## nextClusterLabel = clusterLabels[1:] + [(0, 0, 0)]
## 
## 
## # Show stuff and see what happens
## xSamples = samplesPerRun*nRuns
## fig, ax = plt.subplots(ncols=2, nrows=2)
## for ax0indx, ax1indx, colorMap in ((0, 0, runLabel),
##                                    (0, 1, clusterLabels),
##                                    (1, 0, previousClusterLabel),
##                                    (1, 1, nextClusterLabel)):
##     ax[ax0indx][ax1indx].scatter(range(xSamples), data, c=colorMap)
## plt.show()
## 
## print """ DONE
##       """
