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
        multiple=True
    ),
    dash_table.DataTable(id='datatable-upload-container',
                         
                         page_current=0,
                         page_size=PAGE_SIZE,
                         page_action='custom',
                         style_cell={
                             'whiteSpace': 'normal',
                             'height': 'auto', },
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
    try:
       if 'csv' in filename:
        # Assume that the user uploaded a CSV file
          df=pd.read_csv(
            io.StringIO(decoded.decode('utf-8')))
       elif 'xls' in filename:
        # Assume that the user uploaded an excel file
          df=pd.read_excel(io.BytesIO(decoded))

    except Exception as e:
        print(e)
        return None
        

    return df
    

@app.callback(Output('datatable-upload-container', 'data'),
             Output('datatable-upload-container', 'columns'),
             Input('datatable-upload', 'contents'),
              Input('datatable-upload', 'filename'),)

def update_output( contents, filename,):
    start_table_df = pd.DataFrame(columns=['Start Column'])  ####### inserted line
    if contents and filename:
        df_nuevo = parse_contents(contents, filename,)
        data=start_table_df.to_dict('records')
        columns=[{"name": i, "id": i} for i in  sorted(df_nuevo.columns)]
        
        print(df_nuevo.head())
    return data,columns
    #else:
 
        #return start_table_df.to_dict('records'), [{'id': '', 'name': ''}]

        


@app.callback(
    Output('datatable-upload-container', 'page_count'),
    Input('datatable-use-page-count', 'value'),
    Input('datatable-page-count', 'value'))
def update_output(use_page_count, page_count_value):
    if len(use_page_count) == 0 or page_count_value is None:
        return None
    return page_count_value


@app.callback(Output('datatable-upload-graph', 'figure'),
              Input('datatable-upload-container', 'data'))
def display_graph(rows):
    df = pd.DataFrame(rows)
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
    app.run_server(debug=True, port='8888')
