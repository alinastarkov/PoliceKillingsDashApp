import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config.supress_callback_exceptions = True

mapbox_access_token = 'pk.eyJ1IjoiaGF5bGVlbHV1IiwiYSI6ImNqdmR1ZTduYTA3MGQ0NHM3b3E1YThzczYifQ.Fu_BQlF0VnqAVpbWFNY_8A'

df = pd.read_csv('police_killings.csv')

layout_map = dict(
    autosize=True,
    font=dict(color="#191A1A"),
    titlefont=dict(color="#191A1A", size='14'),
    hovermode="closest",
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
    	 html.Div([
            dcc.Dropdown(
                id='columnNames',
                options=[{'label': i, 'value': i} for i in df.columns.values],
                #initial value of xaxis
            )
        ],
        style={'textAlign': 'center'})
    ]),
    html.Div([
            dcc.RadioItems(
                id='columnValues',
                labelStyle={'display': 'inline-block'},
            )
    ], style={'textAlign': 'center'}),
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
])

@app.callback(dash.dependencies.Output('columnValues', 'options'),
	[dash.dependencies.Input('columnNames', 'value')]
)
def update_columnValues(columnNames):
	return [{'label': i, 'value': i} for i in df[columnNames].unique()]

@app.callback(dash.dependencies.Output('map-graph', 'figure'),
	[dash.dependencies.Input('columnNames', 'value'), dash.dependencies.Input('columnValues', 'value')]
)
def update_graphBasedOnColumnNames(columnNames, columnValues):
	traces = []
	if (columnValues in df[columnNames].unique()): 
		traces.append(go.Scattermapbox(
				lat=df[df[columnNames] == columnValues]['latitude'],
				lon=df[df[columnNames] == columnValues]['longitude'],
				mode='markers',
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

