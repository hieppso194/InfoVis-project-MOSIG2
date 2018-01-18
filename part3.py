import plotly
from plotly import tools
import plotly.graph_objs as go
import plotly.figure_factory as ff
import csv

def readData(filename):
    dst = [[] for i in range(11)]
    with open(filename) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=';')
        for index,row in enumerate(readCSV):
            for i in range(1, 12):
                row[i] = row[i].replace(" ","")
            for i in range(12,23):
                try:
                    if (index > 0) and (row[i] != ' None'):
                        row[i] = float(row[i])
                        if row[i]>=0 and row[i] <= 1:
                            dst[i-12].append(row[i])
                except ValueError,e:
                    print  "error",e

    return dst

dst1 = readData('data/VT1.csv')
dst2 = readData('data/VT2.csv')
dst3 = readData('data/VT3.csv')
candidates = ['NDA','MLP', 'EM','BH', 'NA', 'PP', 'JC', 'JL', 'JLM', 'FA', 'FF']

dst = [[] for i in range(11)]
for i in range(11):
    for j in range(len(dst1[i])):
        dst[i].append(dst1[i][j])
    for k in range(len(dst2[i])):
        dst[i].append(dst2[i][k])
    for m in range(len(dst3[i])):
        dst[i].append(dst3[i][m])
# print(len(dst[1]), len(dst1[1]+dst2[1]+dst3[1]))
# print (type(dst1[1][1]))


fig_dst0 = ff.create_distplot(dst,candidates,bin_size=.05,show_hist=False)
fig_dst1 = ff.create_distplot(dst1,candidates,bin_size=.05,show_hist=False)
fig_dst2 = ff.create_distplot(dst2,candidates,bin_size=.05,show_hist=False)
fig_dst3 = ff.create_distplot(dst3,candidates,bin_size=.05,show_hist=False)

fig_dst0['layout'].update(title='Score distribution in the evaluative voting in all VTs')
fig_dst1['layout'].update(title='Score distribution in the evaluative voting in VT1')
fig_dst2['layout'].update(title='Score distribution in the evaluative voting in VT2')
fig_dst3['layout'].update(title='Score distribution in the evaluative voting in VT3')

plotly.offline.plot(fig_dst0, filename='html/Score_distributionAllVTs.html')
# plotly.offline.plot(fig_dst1, filename='html/Score_distributionVT1.html')
# plotly.offline.plot(fig_dst2, filename='html/Score_distributionVT2.html')
# plotly.offline.plot(fig_dst3, filename='html/Score_distributionVT3.html')


