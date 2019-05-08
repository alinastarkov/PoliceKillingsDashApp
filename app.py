import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.exceptions import PreventUpdate


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config.supress_callback_exceptions = True #find a different -> prevent update 

mapbox_access_token = 'pk.eyJ1IjoiaGF5bGVlbHV1IiwiYSI6ImNqdmR1ZTduYTA3MGQ0NHM3b3E1YThzczYifQ.Fu_BQlF0VnqAVpbWFNY_8A'

df = pd.read_csv('police_killings.csv')

layout_map = dict(
    autosize=True,
    font=dict(color="#191A1A"),
    titlefont=dict(color="#191A1A", size='14'),
    hovermode="closest",
    height='600',
    plot_bgcolor='#fffcfc',
    paper_bgcolor='#fffcfc',
    legend=dict(font=dict(size=10), orientation='h'),
    title='Police Killings Map ',
    mapbox=dict(
        accesstoken=mapbox_access_token,
        style="light",
        center=dict(
           lat=38,
           lon=-94
        ),
        zoom=3
    )
)

app.layout = html.Div(style={'backgroundColor': 'white'}, children=[
    html.H1(children="Map of police killings in the United States ", style={
            'font-weight': 'bold',
            'font-family': 'helvetica',
            'textAlign': 'center',
            'color': '#1B1B1C'
        }),
    html.Div([
        dcc.Graph(
            id='map-graph',
            config={
            'scrollZoom': True },
            figure={
        "data": [{
                "type": "scattermapbox",
                "lat": list(df['latitude']),
                "lon": list(df['longitude']),
                "mode": "markers",
                "hoverinfo": "text",
                "hovertext": [["Name: {} <br>Cause: {}".format(i,j)]
                                for i,j in zip(df['name'], df['cause'])],
                "name": list(df['name']),
                "marker": {
                    "size": 6,
                    "opacity": 0.7
                }
        }],
        "layout": layout_map
        },
           style={'margin-top': '20'})
        ], className= 'twelve columns'
    ), 
    html.Button('Table to filter the map', id='tableButton'),
    html.Button('Dropdown to filter the map', id='dropdownButton'),
    html.Div([
            dcc.Dropdown(
                id='columnNames',
                options=[{'label': i, 'value': i} for i in df.columns.values],
            ), 
            dcc.Dropdown(
                id='columnValues',
            )
    ], style={'textAlign': 'center', 'display': 'none'}, id='buttons'),  
])
 
@app.callback(dash.dependencies.Output('buttons', 'style'), 
    [dash.dependencies.Input('dropdownButton', 'n_clicks')]
)
def show_dropDowns(n_clicks):
    if (n_clicks == None):
        return {'display': 'none'}
    else:
        return {'display': 'block'}


@app.callback(dash.dependencies.Output('columnValues', 'options'),
    [dash.dependencies.Input('columnNames', 'value')]
)
def update_columnValues(columnNames):
    if (columnNames == None):
        raise PreventUpdate
    else:
        return [{'label': i, 'value': i} for i in df[columnNames].unique()]

@app.callback(dash.dependencies.Output('map-graph', 'figure'),
    [dash.dependencies.Input('columnNames', 'value'), dash.dependencies.Input('columnValues', 'value')]
)
def update_graphBasedOnColumnNames(columnNames, columnValues):
    traces = []
    if (columnNames == None):
        raise PreventUpdate
    elif (columnValues in df[columnNames].unique()): 
        traces.append(go.Scattermapbox(
                lat=df[df[columnNames] == columnValues]['latitude'],
                lon=df[df[columnNames] == columnValues]['longitude'],
                mode='markers',
                name=columnValues,
                marker=go.scattermapbox.Marker(
                    size=8,
                    opacity=1
                )))    
    else: 
        for i in df[columnNames].unique():
            traces.append(go.Scattermapbox(
                lat=df[df[columnNames] == i]['latitude'],
                lon=df[df[columnNames] == i]['longitude'],
                name=i,
                mode='markers',
                marker=go.scattermapbox.Marker(
                    size=8,
                    opacity=1
                )    
        ))
    return {
    "data": traces,
    "layout": layout_map
    }



if __name__ == '__main__':
    app.run_server(debug=True)
