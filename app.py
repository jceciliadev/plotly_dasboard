import base64
import datetime
import io
import plotly.express as px
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table

import pandas as pd


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets,title='Dashboard_file')

app.layout = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'SUBA SU FICHERO ',
            html.A('Select Files')
        ]),
        style={
            'width': '50%',
            'height': '30px',
            'lineHeight': '30px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Div(id='output-data-upload'),
    #lo nueevo
    html.P("Names:"),
    dcc.Dropdown(
        id='upload-names' , 
        value='desc_finalidad', 
        options=[{'value': x, 'label': x} 
                 for x in ['RECUP. SUBASTA;', 'GARANTIA HIPOTECARIA', 'RET. CIRCULAR BDE VMER', 'CIRCULAR BDE']],
        clearable=False
    ),
    html.P("Values:"),
    dcc.Dropdown(
        id='upload-values',
        value='cod_finalidad', 
        options=[{'value': x, 'label': x} 
                 for x in [15, 17, 1,19]],
        clearable=False
    ),
    dcc.Graph(id='output-pie-chart-upload',
              
        )
])


def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')),sep=';')
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        dash_table.DataTable(
            #id= 'table',
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in  df.columns],
            fixed_rows={ 'headers': True, 'data': 0 },
            style_cell=dict( whiteSpace='normal',
                             line_color='darkslategray',
                            #line_color= df.Color, fill_color=df.Color),
                             fill_color='lightcyan'),
                            
            style_header=dict(backgroundColor="paleturquoise",
                              line_color='darkslategray',
                              fill_color='royalblue',
                              align=['left','center'],
                              font=dict(color='white', size=12),),
            style_data=dict(backgroundColor="lavender")
                         
        ),

        html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])


@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))

def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return  children 


df = update_output(Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified')) 


@app.callback( Output('output-pie-chart-upload', "figure"), 
               
               Input('upload-names', 'value'),
               Input('upload-values', 'value'))
    

def generate_chart(names, values):
    fig = px.pie( df,values=values, names=names)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True,port='8005')
