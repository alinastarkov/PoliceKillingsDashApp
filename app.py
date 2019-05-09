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
    html.H1(id="abc", children="Map of police killings in the United States ", style={
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
                    "size": 8,
                    "opacity": 0.7
                }
        }],
        "layout": layout_map
        },
           style={'margin-top': '20'})
        ], className= 'twelve columns', id="graph-container"
    ), 
    html.Div([html.Button('Table to filter the map', id='tableButton', style={'text-align': 'center', 'margin-right': '5px'}),
    html.Button('Dropdown to filter the map', id='dropdownButton')],style={'text-align': 'center', 'margin-right': '5px'}),
    html.Div(children=[], style={'textAlign': 'center'}, id='buttons'),  
])
 
@app.callback(dash.dependencies.Output('buttons', 'children'), 
    [   dash.dependencies.Input('dropdownButton', 'n_clicks'), dash.dependencies.Input('tableButton', 'n_clicks'),
        dash.dependencies.Input('dropdownButton', 'n_clicks_timestamp'), dash.dependencies.Input('tableButton', 'n_clicks_timestamp')
    ])
def show_dropDowns(dropDownClick, tableClick, dropDownTS, tableTS):
    if (dropDownClick == None and tableClick == None):
        return []
    elif (dropDownClick != None and tableClick == None):
        content= [ dcc.Dropdown(
                id='columnNames',
                style={'width':'50%','margin':'auto', 'margin-top': '1%'},
                options=[{'label': i, 'value': i} for i in df.columns.values],
            ), 
            dcc.Dropdown(
                id='columnValues',
                style={'width':'50%','margin':'auto', 'margin-top': '0.5%'}
            ) ]
    elif (tableClick != None and dropDownClick == None):
        content = [ dash_table.DataTable(
             id='dataTable', 
            columns=[{"name": i, "id": i} for i in df.columns],
            row_selectable='multi',
            sorting_type='multi',
            selected_rows=[],
            filtering=True,
            row_deletable=True,
            sorting=True,
            n_fixed_rows=1,
            style_cell={'width': '150px'},
            style_table={
                'maxHeight': '300',
                'overflowY': 'scroll',
                'overflowX': 'scroll',
                'margin-top': '1%'

            },
            data=df.to_dict("rows")) ]
    elif (dropDownTS > tableTS):
        content= [ dcc.Dropdown(
                id='columnNames',
                options=[{'label': i, 'value': i} for i in df.columns.values],
                style={'width':'50%','margin':'auto', 'margin-top': '1%'}

            ), 
            dcc.Dropdown(
                id='columnValues',
                style={'width':'50%','margin':'auto', 'margin-top': '0.5%'}
            )]
    else:
        content= [ dash_table.DataTable(
            id='dataTable', 
            columns=[{"name": i, "id": i} for i in df.columns],
            row_selectable='multi',
            sorting_type='multi',
            selected_rows=[],
            filtering=True,
            row_deletable=True,
            sorting=True,
            n_fixed_rows=1,
            style_cell={'width': '150px'},
            style_table={
                'maxHeight': '300',
                'overflowY': 'scroll',
                'overflowX': 'scroll',
                'margin-top': '1%'
            },
            data=df.to_dict("rows")) ]
    return content

@app.callback(dash.dependencies.Output('columnValues', 'options'),
    [dash.dependencies.Input('columnNames', 'value')]
)
def update_columnValues(columnNames):
    if (columnNames == None):
        raise PreventUpdate
    else:
        return [{'label': i, 'value': i} for i in df[columnNames].unique()]

@app.callback(dash.dependencies.Output('map-graph', 'figure'),
    [dash.dependencies.Input('columnNames', 'value'), dash.dependencies.Input('columnValues', 'value'),
    ]
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

@app.callback(
    dash.dependencies.Output('graph-container', "children"),
    [dash.dependencies.Input('dataTable', "derived_virtual_data"), dash.dependencies.Input('dataTable', "derived_virtual_selected_rows")])
def update_graph(newData, derived_virtual_selected_rows):
    if newData is None:
        dff = df
    else:
        dff = pd.DataFrame(newData)
    latArray = []
    longArray = [] 
    if (derived_virtual_selected_rows != []):
        for i in derived_virtual_selected_rows:
            lon = dff.loc[i,'longitude']
            lat = dff.loc[i,'latitude']
            latArray.append(str(lat))
            longArray.append(str(lon))
    else:
        longArray = list(dff['longitude'])
        latArray = list(dff['latitude'])
    return [
        dcc.Graph(
            id='map-graph',
            config={
            'scrollZoom': True },
            figure={
        "data": [{
                "type": "scattermapbox",
                "lat": latArray,
                "lon": longArray,
                "mode": "markers",
                "marker": {
                    "size": 8,
                    "opacity": 0.7
                }
        }],
        "layout": layout_map
        },
           style={'margin-top': '20'})
        ]


if __name__ == '__main__':
    app.run_server(debug=True)

