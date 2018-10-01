import pandas as pd
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output

#pojedynczy instrument. Wykres - wybor okresu (date range), instrumentu (dropdown), rodzaju wykresu (Radio - candle vs line),
#dodac wolumen jako Area
#czy model i jeśli tak to jaki (ARMA), jakie okno dla, ile opoźnien dla AR (input ze sliderami)
#wybor instrumentu z bazy (nie z CSV)
#update dzienny online

app = dash.Dash()


#pzu = pd.read_csv('pzu_d.csv')
#pko = pd.read_csv('pko_d.csv')
#pkn = pd.read_csv('pkn_d.csv')
#wig = pd.read_csv('wig_d.csv')

instrumenty = ['pzu','pko','pkn','wig']
instrumenty_lbl = ['Pzu','PKO BP','PKN Orlen','Indeks WIG']
dane= {i:pd.read_csv(i+'_d.csv') for i in instrumenty}


#x_values0 = wig['Data']
#y_values0 = wig['Zamkniecie']
#x_values1 = pko['Data']
#y_values1 = pko['Zamkniecie']

#trace0 = go.Scatter(x=x_values0, y=y_values0, mode='lines',name='WIG')
#trace1 = go.Scatter(x=x_values1, y=y_values1, mode='lines',name='PKO')

#data = [trace0]
#layout = go.Layout(title = 'WIG')


app.layout = html.Div(children = [html.H1('Modelowanie pojedynczego elementu'),
                                  html.Label('Wybierz okres'),
                                  html.Div([html.Label('Wybierz instrument'),
                                           dcc.Dropdown(id='instrument',
                                           options=[{'label': instrumenty_lbl[i], 'value': instrumenty[i]} for i in range(len(instrumenty))],
                                           value='wig'
                                           )],style={'width':'15%'}),
                                  dcc.Graph(id='g1')])

@app.callback(Output('g1','figure'),[Input('instrument','value')])
def update_g1(value):
    return {'data':[go.Scatter(x=dane[value]['Data'], y=dane[value]['Zamkniecie'], mode='lines')],
           'layout':go.Layout(title = instrumenty_lbl[instrumenty.index(value)]) }


if __name__ == '__main__':
    app.run_server()
