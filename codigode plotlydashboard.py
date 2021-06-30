import base64
import io
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

PAGE_SIZE = 5
app.layout = html.Div([
    dcc.Upload(
        id='datatable-upload',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '50%', 'height': '30px', 'lineHeight': '30px',
            'borderWidth': '1px', 'borderStyle': 'dashed',
            'borderRadius': '5px', 'textAlign': 'center', 'margin': '10px'},
    ),
    dash_table.DataTable(id='datatable-upload-container',        
                        page_current=0,
                        page_size=PAGE_SIZE,
                        page_action='custom',
                        style_cell={
                                    'whiteSpace': 'normal',
                                    'height': 'auto',},
    ),
   
    dcc.Checklist(
        id='datatable-use-page-count',
        options=[
            {'label': 'Use page_count', 'value': 'True'}
        ],
        value=['True']
    ),
    'Page count: ',
    dcc.Input(
        id='datatable-page-count',
        type='number',
        min=1,
        max=29,
        value=20
    ),
    dcc.Graph(id='datatable-upload-graph')
    
])


def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    print(filename)
    if 'csv' in filename:
        # Assume that the user uploaded a CSV file
        return pd.read_csv(
            io.StringIO(decoded.decode('utf-8')))
    elif 'xls' in filename:
        # Assume that the user uploaded an excel file
        return pd.read_excel(io.BytesIO(decoded))


@app.callback(Output('datatable-upload', 'contents'),
              Input('datatable-upload', 'contents'),
              State('datatable-upload', 'filename')
              )
def update_output(contents, filename):
    if contents is None:
        return [{}], []
    df = parse_contents(contents, filename)

    return df


@app.callback(Output('datatable-upload-container', 'data'),
              Output('datatable-upload-container', 'columns'),
    Input('datatable-upload-container', "page_current"),
    Input('datatable-upload-container', "page_size"),
    Input('datatable-upload-container', 'sort_by'),
    Input('datatable-upload', 'filename'))



def update_table(page_current, page_size,filename,):
    df = pd.read_csv(filename)
    
    return df.iloc[page_current*page_size:(page_current+ 1)*page_size].to_dict('records')


@app.callback(Output('datatable-upload-graph', 'figure'),
              Input('datatable-upload-container', 'data'))



def display_graph(rows):
    df = pd.DataFrame(rows)
    page_current=0,
    page_size=PAGE_SIZE,
    page_action='custom'

    if (df.empty or len(df.columns) < 1):
        return {
            'data': [{
                'x': [],
                'y': [],
                'type': 'bar'
            }]
        }
    return {
        'data': [{
            'x': df[df.columns[0]],
            'y': df[df.columns[1]],
            'type': 'bar',
            
        }]
    }


if __name__ == '__main__':
    app.run_server(debug=True,port='8888')