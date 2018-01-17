import plotly
from plotly import tools
import plotly.graph_objs as go
import numpy as np
import csv


def readData(filename):
    number_votes = np.zeros((1,11))
    means = np.zeros((1,11))
    counts = np.zeros((1,11))
    sums = np.zeros((1,11))
    with open(filename) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=';')
        for index,row in enumerate(readCSV):
            for i in range(1, 12):
                row[i] = row[i].replace(" ","")
                if row[i]=='1':
                    number_votes[0][i-1] += 1
            for i in range(12,23):
                try:
                    if (index > 0) and (row[i] != ' None'):
                        row[i] = float(row[i])
                        if row[i]>=0 and row[i] <= 1:
                            counts[0][i-12] +=1
                            sums[0][i-12] += row[i]
                except ValueError,e:
                    print  "error",e

    # print(sums,counts)
    for i in range(0,11):
        means[0][i] = sums[0][i]*100/counts[0][i]
    return number_votes,means,sums,counts

VT1_votes, VT1_means, VT1_sums, VT1_counts = readData('data/VT1.csv')
VT2_votes, VT2_means, VT2_sums, VT2_counts = readData('data/VT2.csv')
VT3_votes, VT3_means, VT3_sums, VT3_counts = readData('data/VT3.csv')

VT_votes = np.zeros((1,11))
VT_means = np.zeros((1,11))

for i in range(0,11):
    VT_votes[0][i] = VT1_votes[0][i] + VT2_votes[0][i] + VT3_votes[0][i]
    VT_means[0][i] = (VT1_sums[0][i] + VT2_sums[0][i] + VT3_sums[0][i])*100/(VT1_counts[0][i] + VT2_counts[0][i] + VT3_counts[0][i])

candidates = ['NDA','MLP', 'EM','BH', 'NA', 'PP', 'JC', 'JL', 'JLM', 'FA', 'FF']
data = []
# For Both
trace0 = go.Bar(
    x = candidates,
    y = VT_votes[0,:],
    name = 'Number of votes in all'
)

trace01 = go.Scatter(
    x = candidates,
    y = VT_means[0,:],
    name = 'Mean of vote score in all'
)

#VT1
trace1 = go.Bar(
    x = candidates,
    y = VT1_votes[0,:],
    name = 'Number of votes in VT1'
)

trace2 = go.Scatter(
    x = candidates,
    y = VT1_means[0,:],
    name = 'Mean of vote score in VT1'
)

#VT2
trace3 = go.Bar(
    x = candidates,
    y = VT2_votes[0,:],
    name = 'Number of votes in VT2'
)

trace4 = go.Scatter(
    x = candidates,
    y = VT2_means[0,:],
    name = 'Mean of vote score in VT2'
)
#VT3
trace5 = go.Bar(
    x = candidates,
    y = VT3_votes[0,:],
    name = 'Number of votes in VT3'
)

trace6 = go.Scatter(
    x = candidates,
    y = VT3_means[0,:],
    name = 'Mean of vote score in VT3'
)

fig = tools.make_subplots(rows=2, cols=2, subplot_titles=('All VTs','VT1','VT2','VT3'))

fig.append_trace(trace0, 1, 1)
fig.append_trace(trace01, 1, 1)
fig.append_trace(trace1, 1, 2)
fig.append_trace(trace2, 1, 2)
fig.append_trace(trace3, 2, 1)
fig.append_trace(trace4, 2, 1)
fig.append_trace(trace5, 2, 2)
fig.append_trace(trace6, 2, 2)

layout = go.Layout(
    title = 'Who won the French election?',
    xaxis = dict(
        title = 'Candidate',
        titlefont=dict(
            size=16,
            color='rgb(107,107,107)'
        ),
        tickfont=dict(
            size=14,
            color='rgb(107,107,107)'
        )
    ),
    yaxis = dict(
        titlefont=dict(
            size=16,
            color='rgb(107,107,107)'
        ),
        tickfont=dict(
            size=14,
            color='rgb(107,107,107)'
        )
    ),
    legend=dict(
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    )
)
fig['layout'].update(title='Who won the French presidental election?')

plotly.offline.plot(fig, filename='html/Who_won_the_election.html')
#--------------------------------------------------------------------------------------------------------------------------
# Visualize from left to right
def append(arr1,arr2):
    n = len(arr1)
    a = [list for i in range(0,n)]
    for i in range(0,n):
        a[i] = [arr1[i],arr2[0][i]]
    return a

def getKey(item):
    return item[1]

VT_LR = sorted(append(candidates,VT_votes),key=getKey)
VT1_LR = sorted(append(candidates,VT1_votes),key=getKey)
VT2_LR = sorted(append(candidates,VT2_votes),key=getKey)
VT3_LR = sorted(append(candidates,VT3_votes),key=getKey)

def get(arr,option):
    sorted_candidates = []
    sorted_votes = []
    for i in range(len(arr)):
        sorted_candidates.append(arr[i][0])
        if option == 0:
            sorted_votes.append(arr[i][1]/4)
        else:
            sorted_votes.append(arr[i][1]/2)

    return sorted_candidates,sorted_votes

sorted_candidates, sorted_votes = get(VT_LR,0)
sorted_candidates1, sorted_votes1 = get(VT1_LR,1)
sorted_candidates2, sorted_votes2 = get(VT2_LR,1)
sorted_candidates3, sorted_votes3 = get(VT3_LR,1)

# sorted_votes = sorted_votes/4
print (sorted_votes)
y = np.zeros(len(sorted_votes))
trace1D = go.Scatter(
        x=sorted_candidates,
        y=y,
        name='All VTs',
        mode='markers',
        marker=dict(
            size= sorted_votes,
        )
    )

trace1D1 = go.Scatter(
        x=sorted_candidates1,
        y=y,
        name='VT1',
        mode='markers',
        marker=dict(
            size= sorted_votes1,
        )
    )

trace1D2 = go.Scatter(
        x=sorted_candidates2,
        y=y,
        name = 'VT2',
        mode='markers',
        marker=dict(
            size= sorted_votes2,
        )
    )

trace1D3 = go.Scatter(
        x=sorted_candidates3,
        y=y,
        name='VT3',
        mode='markers',
        marker=dict(
            size= sorted_votes3,
        )
    )
fig_1D = tools.make_subplots(rows=2, cols=2, subplot_titles=('All VTs','VT1','VT2','VT3'))

fig_1D.append_trace(trace1D,1,1)
fig_1D.append_trace(trace1D1,1,2)
fig_1D.append_trace(trace1D2,2,1)
fig_1D.append_trace(trace1D3,2,2)

fig_1D['layout'].update(title='Can we order the candidate along a 1D axis (left-right)?')
plotly.offline.plot(fig_1D, filename='html/LeftToRight.html')