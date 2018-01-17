import plotly
from plotly import tools
import plotly.graph_objs as go
import numpy as np
import csv

# Votes together
def readData(filename):
    cor = np.zeros((11, 11))
    males = np.zeros((1,11))
    females = np.zeros((1,11))
    ages = np.zeros((5,11))
    etude = np.zeros((3,11))
    a = 0
    with open(filename) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=';')
        for index,row in enumerate(readCSV):
            try:
                if(index>0) and (row[24]!=' NSPP'):
                    row[24] = row[24].replace(" ", "")
                    row[24] = int(row[24])
            except ValueError,e:
                print "error",e
            for i in range(1, 12):
                # together
                for j in range(1, 12):
                    if (row[i] == row[j] == ' 1'):
                        cor[i-1][j-1] += 1
                # sexe
                if (row[i] == ' 1') and (row[25]==' F'):
                    females[0][i-1]+=1
                if (row[i] == ' 1') and (row[25]==' M'):
                    males[0][i-1]+=1
                # ages
                if (17<row[24]<30) and (row[i]==' 1'):
                    ages[0][i-1]+=1
                elif(29<row[24]<40) and (row[i]==' 1'):
                    ages[1][i-1]+=1
                elif(39<row[24]<50) and (row[i]==' 1'):
                    ages[2][i-1]+=1
                elif(49<row[24]<60) and (row[i]==' 1'):
                    ages[3][i-1]+=1
                elif(row[24]>59) and (row[i]==' 1'):
                    ages[4][i-1]+=1
    #                 etude
                if (row[26]==' 1') and (row[i]==' 1'):
                    etude[0][i-1]+=1
                if (row[26]==' 2') and (row[i]==' 1'):
                    etude[1][i-1]+=1
                if (row[26]==' S') and (row[i]==' 1'):
                    etude[2][i-1]+=1


    return cor,males,females,ages,etude

cor1,males1,females1,ages1,etude1 = readData('data/VT1.csv')
cor2,males2,females2,ages2,etude2 = readData('data/VT2.csv')
cor3,males3,females3,ages3,etude3 = readData('data/VT3.csv')

males = []
females = []
m1 = []
m2=[]
m3=[]
f1=[]
f2=[]
f3=[]
cor = np.zeros((11,11))
ages = np.zeros((5,11))
etude = np.zeros((3,11))
for i in range(0,5):
    for j in range(0,11):
        ages[i][j]=ages1[i][j]+ages2[i][j]+ages3[i][j]
for i in range(0,3):
    for j in range(0,11):
        etude[i][j]=etude1[i][j]+etude2[i][j]+etude3[i][j]
for i in range(0,11):
    males.append(males1[0][i]+males2[0][i]+males3[0][i])
    females.append(females1[0][i]+females2[0][i]+females3[0][i])
    m1.append(males1[0][i])
    m2.append(males2[0][i])
    m3.append(males3[0][i])
    f1.append(females1[0][i])
    f2.append(females2[0][i])
    f3.append(females3[0][i])

    for j in range(0,11):
        cor[i][j] = cor1[i][j]+cor2[i][j]+cor3[i][j]

candidates = ['NDA','MLP', 'EM','BH', 'NA', 'PP', 'JC', 'JL', 'JLM', 'FA', 'FF']

trace0 = go.Heatmap(z=cor,x=candidates,y=candidates,colorbar=dict(x=0.47,y=0.81,len=0.4),colorscale='Viridis',name='All VTs')
trace1 = go.Heatmap(z=cor1,x=candidates,y=candidates, colorbar=dict(y=0.81,len=0.4),name='VT1')
trace2 = go.Heatmap(z=cor2,x=candidates,y=candidates, colorbar=dict(x=0.47,y=0.19,len=0.4),name='VT2')
trace3 = go.Heatmap(z=cor3,x=candidates,y=candidates, colorbar=dict(y=0.19,len=0.4), name='VT3')

fig = tools.make_subplots(rows=2, cols=2, subplot_titles=('All VTs','VT1','VT2','VT3'))
fig.append_trace(trace0,1,1)
fig.append_trace(trace1,1,2)
fig.append_trace(trace2,2,1)
fig.append_trace(trace3,2,2)

fig['layout'].update(title='Did the voters vote candidates together? ')

# -----------------------------------------------------------------------------------------------------------------------------
#Votes follow sexe
sexe = ['Male','Female']
traces0 = go.Heatmap(z=np.column_stack((males,females)),x=sexe,y=candidates,colorbar=dict(x=0.47,y=0.81,len=0.4),colorscale='Viridis',name='All VTs')
traces1 = go.Heatmap(z=np.column_stack((m1,f1)),x=sexe,y=candidates,colorbar=dict(y=0.81,len=0.4),name='VT1')
traces2 = go.Heatmap(z=np.column_stack((m2,f2)),x=sexe,y=candidates,colorbar=dict(x=0.47,y=0.19,len=0.4),name='VT2')
traces3 = go.Heatmap(z=np.column_stack((m3,f3)),x=sexe,y=candidates,colorbar=dict(y=0.19,len=0.4),name='VT3')


fig_sexe = tools.make_subplots(rows=2, cols=2, subplot_titles=('All VTs','VT1','VT2','VT3'))

fig_sexe.append_trace(traces0,1,1)
fig_sexe.append_trace(traces1,1,2)
fig_sexe.append_trace(traces2,2,1)
fig_sexe.append_trace(traces3,2,2)


fig_sexe['layout'].update(title='Vote follow sexe')

# ------------------------------------------------------------------------------------------------------------------------------
#Votes follow age
age_periods = ['18-29','30-39','40-49','50-59','60+']
tracea0 = go.Heatmap(z=ages,y=age_periods,x=candidates,colorbar=dict(x=0.47,y=0.81,len=0.4),colorscale='Viridis',name='All VTs')
tracea1 = go.Heatmap(z=ages1,y=age_periods,x=candidates,colorbar=dict(y=0.81,len=0.4),name='VT1')
tracea2 = go.Heatmap(z=ages2,y=age_periods,x=candidates,colorbar=dict(x=0.47,y=0.19,len=0.4),name='VT2')
tracea3 = go.Heatmap(z=ages3,y=age_periods,x=candidates,colorbar=dict(y=0.19,len=0.4),name='VT3')

fig_age = tools.make_subplots(rows=2, cols=2, subplot_titles=('All VTs','VT1','VT2','VT3'))

fig_age.append_trace(tracea0,1,1)
fig_age.append_trace(tracea1,1,2)
fig_age.append_trace(tracea2,2,1)
fig_age.append_trace(tracea3,2,2)


fig_age['layout'].update(title='Vote follow age')
# ------------------------------------------------------------------------------------------------------------------------------
# Vote follow by study
etude_levels = ['Primary','Second','Greduate']
tracee0 = go.Heatmap(z=etude,y=etude_levels,x=candidates,colorbar=dict(x=0.47,y=0.81,len=0.4),colorscale='Viridis',name='All VTs')
tracee1 = go.Heatmap(z=etude1,y=etude_levels,x=candidates,colorbar=dict(y=0.81,len=0.4),name='VT1')
tracee2 = go.Heatmap(z=etude2,y=etude_levels,x=candidates,colorbar=dict(x=0.47,y=0.19,len=0.4),name='VT2')
tracee3 = go.Heatmap(z=etude3,y=etude_levels,x=candidates,colorbar=dict(y=0.19,len=0.4),name='VT3')

fig_etude = tools.make_subplots(rows=2, cols=2, subplot_titles=('All VTs','VT1','VT2','VT3'))

fig_etude.append_trace(tracee0,1,1)
fig_etude.append_trace(tracee1,1,2)
fig_etude.append_trace(tracee2,2,1)
fig_etude.append_trace(tracee3,2,2)


fig_etude['layout'].update(title='Vote follow study level')

#------------------------------------------------------------------------------------------------------------------------------
plotly.offline.plot(fig, filename='html/Vote_together.html')
plotly.offline.plot(fig_sexe, filename='html/Vote_follow_sexe.html')
plotly.offline.plot(fig_age, filename='html/Vote_follow_age.html')
plotly.offline.plot(fig_etude, filename='html/Vote_follow_study_level.html')