import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import plotly.express as px

x = ['Starting Median Salary',
     'Mid-Career 10th Percentile Salary',
     'Mid-Career 25th Percentile Salary',
     'Mid-Career Median Salary',
     'Mid-Career 75th Percentile Salary',
     'Mid-Career 90th Percentile Salary']


def get_all_salary_graph():
    print("read")
    df = pd.read_csv('lab3-datasets/college-salaries/degrees-that-pay-back.csv')
    for i in range(len(df.columns)):
        if df.columns[i] != 'Undergraduate Major':
            df[df.columns[i:]] = df[df.columns[i:]].replace('[\$,]', '', regex=True).astype(float)
    group = df.groupby('Undergraduate Major').mean()  # type: pd.DataFrame
    data = []
    idx = [0, 3, 4, 1, 5, 6]
    # print((group.iloc[0].name))
    for i in range(len(group)):
        trace = go.Scatter(x=x, y=group.iloc[i][idx],
                           name=group.iloc[i].name,
                           showlegend=True)
        data.append(trace)
    layout = dict(title='Average salaries of different stages of career by degree major')

    # 将data与layout组合为一个图像
    fig = dict(data=data, layout=layout)
    return fig


def get_salary_graph_by_region():
    df = pd.read_csv('lab3-datasets/college-salaries/salaries-by-region.csv')
    for i in range(len(df.columns)):
        if df.columns[i] != 'School Name' and df.columns[i] != 'Region':
            df[df.columns[i:]] = df[df.columns[i:]].replace('[\$,]', '', regex=True).astype(float)

    group = df.groupby('Region').mean()
    data = []

    idx = [0, 2, 3, 1, 4, 5]
    for i in range(len(group)):
        trace = go.Scatter(x=x, y=group.iloc[i][idx],
                           name=group.iloc[i].name,
                           showlegend=True)
        data.append(trace)
    layout = dict(title='Average salaries of different stages of career by region')

    # 将data与layout组合为一个图像
    fig = dict(data=data, layout=layout)
    return fig


def get_salary_plot_by_school_type():
    df = pd.read_csv('lab3-datasets/college-salaries/salaries-by-college-type.csv')
    for i in range(len(df.columns)):
        if df.columns[i] != 'School Name' and df.columns[i] != 'School Type':
            df[df.columns[i:]] = df[df.columns[i:]].replace('[\$,]', '', regex=True).astype(float)

    group = df.groupby('School Type').mean()  # type: pd.DataFrame
    data = []
    idx = [0, 2, 3, 1, 4, 5]
    # print((group.iloc[0].name))
    for i in range(len(group)):
        trace = go.Scatter(x=x, y=group.iloc[i][idx],
                           name=group.iloc[i].name,
                           showlegend=True)
        data.append(trace)
    layout = dict(title='Average salaries of different stages of career by school type')

    # 将data与layout组合为一个图像
    fig = dict(data=data, layout=layout)
    return fig


app = dash.Dash()

app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='type_filter',
                options=[{'label': i, 'value': i} for i in ['Undergraduate Major', 'Region', 'School Type']],
                value='Undergraduate Major',
                style={'width': '80%','margin-left': '5%'}

            ),
            dcc.Graph(id='avg_salary', figure=get_all_salary_graph()),
            html.Br(),
        ],style={'width': '40%','display': 'inline-block'}),
        #
        html.Div([
            dcc.Dropdown(
                id='stage_filter',
                options=[{'label': i, 'value': i} for i in ['Starting Median Salary',
                                                            'Mid-Career 10th Percentile Salary',
                                                            'Mid-Career 25th Percentile Salary',
                                                            'Mid-Career Median Salary',
                                                            'Mid-Career 75th Percentile Salary',
                                                            'Mid-Career 90th Percentile Salary']],
                value='Starting Median Salary',
                style={'width': '80%', 'margin-left': '5%'}
            ),
            dcc.Graph(id='stage_avg_salary')
        ], style={'width': '40%','display': 'inline-block'}),

        html.Div([
            'Sunbrast figure of Mid-Career Median Salary',
            dcc.Graph(id='sunbrast')
        ], style={'width': '50%','text-align':'center','padding':'10px'})
    ])
])



@app.callback(
    dash.dependencies.Output('stage_avg_salary', 'figure'),
    [dash.dependencies.Input('stage_filter', 'value'),
     dash.dependencies.Input('type_filter', 'value')]
)
def update_stage_avg_fig(stage, type):
    # print(filter.options)
    df = None
    if type == 'Region':
        print("Region")
        df = pd.read_csv('lab3-datasets/college-salaries/salaries-by-region.csv')
    elif type == 'School Type':
        print("School Type")
        df = pd.read_csv('lab3-datasets/college-salaries/salaries-by-college-type.csv')
    else:
        df = pd.read_csv('lab3-datasets/college-salaries/degrees-that-pay-back.csv')
    # 获得stage
    for i in range(len(df.columns)):
        if df.columns[i] != 'School Name' and df.columns[i] != type and df.columns[i] != 'Undergraduate Major':
            df[df.columns[i:]] = df[df.columns[i:]].replace('[\$,]', '', regex=True).astype(float)
    data = []
    group = df.groupby(type)
    for idx, item in group:
        trace = go.Box(y=item[stage], name=idx)
        data.append(trace)
    layout = dict(title='Salary of ' + stage + ' by ' + type)
    fig = dict(data=data, layout=layout)
    return fig

@app.callback(
    dash.dependencies.Output('avg_salary', 'figure'),
    dash.dependencies.Input('type_filter', 'value')
)
def update_avg_fig(type):
    if type  == 'Region':
        return get_salary_graph_by_region()
    elif type == 'School Type':
        return get_salary_plot_by_school_type()
    return get_all_salary_graph()

@app.callback(
    dash.dependencies.Output('sunbrast', 'figure'),
    dash.dependencies.Input('type_filter', 'value')
)
def get_sunbrast(type):
    if type == 'Region':
        df = pd.read_csv('lab3-datasets/college-salaries/salaries-by-region.csv')
        for i in range(len(df.columns)):
            if df.columns[i] != 'School Name' and df.columns[i] != 'Region':
                df[df.columns[i:]] = df[df.columns[i:]].replace('[\$,]', '', regex=True).astype(float)

        fig = px.sunburst(df, path=['Region', 'School Name'], values='Mid-Career Median Salary',
                          color='Mid-Career Median Salary',
                          color_continuous_scale='RdBu'
                          )
        return fig
    elif type == 'School Type':
        df = pd.read_csv('lab3-datasets/college-salaries/salaries-by-college-type.csv')
        for i in range(len(df.columns)):
            if df.columns[i] != 'School Name' and df.columns[i] != 'School Type':
                df[df.columns[i:]] = df[df.columns[i:]].replace('[\$,]', '', regex=True).astype(float)

        fig = px.sunburst(df, path=['School Type', 'School Name'], values='Mid-Career Median Salary',
                          color='Mid-Career Median Salary',
                          color_continuous_scale='RdBu'
                          )

        return fig
    else:
        fig = px.sunburst([], path=[], values=[],
                          color='',
                          color_continuous_scale='RdBu'
                          )
        return fig

app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

if __name__ == '__main__':
    app.run_server()
