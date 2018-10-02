
import pandas as pd
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output
from datetime import datetime as dt

#pojedynczy instrument.
#dodac wolumen
#dodac pierwsze roznice
#modele i wskazniki
#styling
#date range - niewygodny
#wybor instrumentu z bazy danych (nie z CSV)
#update dzienny online
#portfel (oddzielna apka)


app = dash.Dash()

#pobranie i wstepna obróbka danych
instrumenty = ['pzu','pko','pkn','wig']
instrumenty_lbl = ['Pzu','PKO BP','PKN Orlen','Indeks WIG']
dane= {i:pd.read_csv(i+'_d.csv') for i in instrumenty}
for i in dane.keys():
    dane[i]['Zamkniecie_diff'] = dane[i]['Zamkniecie'] - dane[i]['Zamkniecie'].shift(1)



app.layout = html.Div(children = [html.H1('Modelowanie pojedynczego instrumentu'),
                                  html.Div([html.Label('Wybierz okres'),
                                      dcc.DatePickerRange(
                                      id='okres',
                                      min_date_allowed=dt(1991, 1, 1),
                                      max_date_allowed=dt.now(),
                                      start_date=dt(1991, 1, 1),
                                      end_date=dt.now()
                                    )]),
                                  html.Div([html.Label('Wybierz instrument'),
                                          dcc.Dropdown(id='instrument',
                                          options=[{'label': instrumenty_lbl[i], 'value': instrumenty[i]} for i in range(len(instrumenty))],
                                          value='wig'
                                          )],style={'width':'15%'}),
                                  html.Div([html.Label('Wybierz typ wykresu'),
                                          dcc.RadioItems(id='graph_type',
                                          options=[{'label': 'Wykres liniowy', 'value': 'line'},{'label': 'Wykres świecowy', 'value': 'candle'}],
                                          value='line',
                                          labelStyle={'display': 'inline-block'}
                                          )],style={'width':'15%'}),
                                  html.Div([dcc.Graph(id='g1'),dcc.Graph(id='g2')],id='wykresy',style={'width':'70%'})])

@app.callback(Output('g1','figure'),[Input('instrument','value'),Input('okres', 'start_date'),Input('okres', 'end_date'),Input('graph_type','value')])
def update_g1(value,poczatek,koniec,typ):
    szereg = dane[value][(pd.to_datetime(dane[value]['Data'],format='%Y-%m-%d')>=poczatek)&(pd.to_datetime(dane[value]['Data'],format='%Y-%m-%d')<=koniec)]
    #szereg = dane[value]
    if (typ=='line'):
            return {'data':[go.Scatter(x=szereg['Data'], y=szereg['Zamkniecie'], mode='lines'),
                            go.Bar(x=szereg['Data'], y=szereg['Wolumen'],yaxis='y2',marker=dict(color='rgb(149,174,219)'))],
                    'layout':go.Layout(title = instrumenty_lbl[instrumenty.index(value)],
                                       yaxis=dict(title='Cena'),
                                       yaxis2=dict(title='Wolumen',side='right',overlaying='y'),
                                       showlegend = False) }
    else:
            return {'data':[go.Candlestick(x=szereg['Data'], open=szereg['Otwarcie'], high=szereg['Najwyzszy'],low=szereg['Najnizszy'],close=szereg['Zamkniecie']),
                            go.Bar(x=szereg['Data'], y=szereg['Wolumen'],yaxis='y2',marker=dict(color='rgb(149,174,219)'))],
                    'layout':go.Layout(title = instrumenty_lbl[instrumenty.index(value)],
                                       yaxis=dict(title='Cena'),
                                       yaxis2=dict(title='Wolumen',side='right',overlaying='y'),
                                       xaxis = dict(rangeslider = dict(visible = False)),
                                       showlegend = False)
                   }

@app.callback(Output('g2','figure'),[Input('instrument','value'),Input('okres', 'start_date'),Input('okres', 'end_date')])
def update_g2(value,poczatek,koniec):
    szereg = dane[value][(pd.to_datetime(dane[value]['Data'],format='%Y-%m-%d')>=poczatek)&(pd.to_datetime(dane[value]['Data'],format='%Y-%m-%d')<=koniec)]
    return {'data':[go.Scatter(x=szereg['Data'], y=szereg['Zamkniecie_diff'], mode='lines')],
            'layout':go.Layout(title = 'Dzienna zmiana na zamknięciach',
                               showlegend = False) }



if __name__ == '__main__':
    app.run_server()
