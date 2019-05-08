# coding: utf-8

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import numpy as np
from components import Header, make_dash_table, print_button
import dash_table
import pandas as pd


app = dash.Dash(__name__, instance_relative_config=True,csrf_protect=False)
server = app.server
# read data for tables (one df per table)
#####used year data
lifepath = './data/life_time_data.csv'
prodpath='./data/app_data.csv'
yeartable = pd.read_csv(lifepath)
producttable = pd.read_csv(prodpath)
#####used_year distribution
df=pd.merge(yeartable,producttable,how='inner',left_on='id',right_on='life_data_id')
mgr_options = df['type'].unique()
df = df[['id_x', 'type','used_year', 'next_maintenance_date']]
df.rename(columns={'id_x':'产品ID','type':'产品型号','used_year':'使用年限','next_maintenance_date':'下次维护日期'},inplace=True)
df['使用年限']=np.round(df['使用年限'])
mgr_options = df['产品型号'].unique()
#df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')
df=df.dropna()
#l=['I','II']
#df['框架']=np.random.choice(l,size=len(df.index))
N=len(df['产品型号'].unique())
c= ['hsl('+str(h)+',50%'+',50%)' for h in np.linspace(0, 180, N)]
dff = pd.pivot_table(
        df,
        index=["使用年限"],
        columns=['产品型号'],
        values=['产品ID'],
        aggfunc='count',
        fill_value=0)

########oped data
opedpath = './data/ID_DATA_SEAL.csv'
opedtable = pd.read_csv(opedpath)
#####used_year distribution
df2 = pd.merge(opedtable,producttable,how='inner',left_on='MLFB',right_on='mlfb')
df2 = df2[['id', 'type', 'OPENING_TIME_NOM', 'CLOSING_TIME_NOM','standard_open_time','standard_close_time']]
df2.rename(columns={'id':'产品ID','type':'产品型号','OPENING_TIME_NOM':'分闸时间','CLOSING_TIME_NOM':'合闸时间','standard_close_time':'标准合闸时间', 'standard_open_time':'标准开闸时间'},inplace=True)
#df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')
l=['I','II']
df2['框架']=np.random.choice(l,size=len(df2.index))
df2=df2.dropna()
N=len(df2['产品型号'].unique())
c2= ['hsl('+str(h)+',50%'+',50%)' for h in np.linspace(100, 250, N)]



#####temprature increase
currentpath = './data/health_data_1.csv'
currenttable = pd.read_csv(currentpath)
#####used_year distribution
df3 = pd.merge(currenttable,producttable,how='inner',left_on='id',right_on='health_data1_id')
#df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')
df3 = df3[['id_x','type', 'i1', 'i2', 't0','t1', 't2','tempu']]
#l=['I','II']
#df3['框架']=np.random.choice(l,size=len(df3.index))
df3.rename(columns={'id_x':'产品ID','i1':'实测运行电流','i2':'预期最大电流','tempu':'柜外环境温度','t0':'柜内温度','t1':'断路器桩头温度','type':'产品型号'},inplace=True)
df3=df3.dropna()
N=len(df3['产品型号'].unique())
c3= ['hsl('+str(h)+',50%'+',50%)' for h in np.linspace(0, 180, N)]
####temprature increase data

#####country map
locpath = './data/app_location.csv'
prodpath = './data/app_data.csv'
locationtable = pd.read_csv(locpath)
producttable = pd.read_csv(prodpath)
mergedtable = pd.merge(locationtable, producttable, how='inner', left_on='id', right_on='loc_id')
citydata=mergedtable.groupby(['admin_area','parent_city']).agg({'id_x':'count','lat':'mean','lon':'mean'})
citydata=citydata.reset_index(level=['admin_area','parent_city'])
citydata['location']='----'+citydata['parent_city']+'市'
citydata['admin_area']=citydata.admin_area+np.where(citydata.admin_area.isin(['上海','北京','重庆','天津']),'市',np.where(citydata.admin_area.isin(['宁夏','新疆','内蒙古','广西','西藏']),'自治区','省'))
provincedata=mergedtable.groupby(['admin_area']).agg({'id_x':'count','lat':'mean','lon':'mean'})
provincedata['lat']-=0.01
provincedata['lon']-=0.01
provincedata.reset_index(inplace=True)
provincedata['admin_area']=provincedata.admin_area+np.where(provincedata.admin_area.isin(['上海','北京','重庆','天津']),'市',np.where(provincedata.admin_area.isin(['宁夏','新疆','内蒙古','广西','西藏']),'自治区','省'))
provincedata['location']=provincedata['admin_area']
alldata=provincedata.append(citydata,sort=False).sort_values(['admin_area','location'],ascending=False)
df4 = alldata
mapbox_access_token = "pk.eyJ1IjoiaGl6aG9uZ2thaSIsImEiOiJjanV3dHR1cjYwMW03M3lwaWRnZWxlZWh5In0.1ox9WAyfyuQ6aN9986WdAg"

#########with load or not
ltipath = './data/life_time_input_data.csv'
prodpath='./data/app_data.csv'
ltitable = pd.read_csv(ltipath)
producttable = pd.read_csv(prodpath)
mergedtable=pd.merge(ltitable,producttable,how='inner',left_on='id',right_on='life_data_input_id')
#secmegedtable=pd.merge(mergedtable,hd2table,how='inner',left_on='health_data2_id',right_on='id')
if(any(mergedtable.opt_year>1000)):
          mergedtable.opt_year=round(mergedtable.opt_year/365).astype(int)
mergedtablegroup=mergedtable.groupby(['type','opt_year','with_load']).agg({'count_number':'mean'})
mergedtablegroup.count_number=mergedtablegroup.count_number.astype(int)
mergedtablegroup=mergedtablegroup.reset_index(level=['type','opt_year','with_load'])
mergedtablegroup.sort_values(by=['type','opt_year','with_load'],inplace=True)
df5 = mergedtablegroup





## Page layouts
loadornot = html.Div([  # page 1

        print_button(),
        html.Div([
            Header(),
            # Row 4
                 html.Div([
                  html.H6('电寿命分布柱状图'),
                     ],className='gs-header',style={'background-color':'lightblue','margin-bottom':10}),
            html.Div([
                html.Li("筛选条件为是否带负载，产品型号（各个产品系列以及所有产品），统计出与操作年数时间相对应的已操作次数。"),
            ], className='row'),
            # Row 5
            html.Div([
                dcc.Dropdown(id="load-selected",
                             options=[{'label': '带载操作' if i == 1 else '不带载操作', 'value': i} for i in
                                      df5.with_load.unique()],
                             multi=False,
                             #value=df5.with_load.unique()[0],
                             placeholder="请选择是否带负载",
                             style={
                                 "display": "block",
                                 "margin-left": "auto",
                                 "margin-right": "auto",
                                 "width": "50%"
                             }
                             ),
                dcc.Dropdown(id="mlfb-selected",
                             options=[{'label': '型号' + i, 'value': i} for i in df5.type.unique()],
                             multi=False,
                             #value=df5.type.unique()[0],
                             placeholder="请选择产品型号",
                             style={
                                 "display": "block",
                                 "margin-left": "auto",
                                 "margin-right": "auto",
                                 "width": "50%"
                             }
                             ),
                  html.Div(dcc.Graph(id="datatable-interactivity-container5"))
            ],className='row')
        ], className="subpage")
    ], className="page")





Temperature_Inc = html.Div([  # page 5

        print_button(),

        html.Div([

            Header(),

            # Row 1
            # Row 2
            html.Div([
                 html.Div([
                html.H6(['断路器实测最大电流和实测最大温升'], className="gs-header",style={'background-color':'lightblue','margin-bottom':10})],className="six columns"),
                 html.Div([
                html.H6(['断路器预期最大电流和预期最大温升'], className="gs-header",style={'background-color':'lightblue','margin-bottom':10})],className="six columns"),
                html.Div(id='datatable-interactivity-container3')
            ], className="row"),
            # Row 3

            html.Div([
                html.H6(['断路器电流和温升数据'],
                        className="gs-header",style={'background-color':'lightblue','margin-top':10}),
                dash_table.DataTable(
                    id='datatable-interactivity3',
                    columns=[
                        {"name": i, "id": i, "deletable": False} for i in df3.columns
                    ],
                    data=df3.to_dict("rows"),
                    editable=False,
                    filtering=True,
                    sorting=True,
                    sorting_type="multi",
                    row_selectable=False,
                    row_deletable=False,
                    selected_rows=[],
                    pagination_mode="fe",
                    style_cell={
                        'minWidth': '0px', 'maxWidth': '180px',
                        'whiteSpace': 'normal'
                    },
                    style_cell_conditional=[{
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(248, 248, 248)'
                                           }],
                    pagination_settings={
                        "displayed_pages": 1,
                        "current_page": 0,
                        "page_size": 5,
                    },
                    navigation="page",
                )
            ], className="row")

        ], className="subpage")

    ], className="page")


Used_Year = html.Div([  # page 1

        print_button(),
        html.Div([
            Header(),
            # Row 4
             html.Div([
                html.H6(['断路器使用年限柱状图'],
                         className="gs-header",style={'background-color':'lightblue','margin-bottom':10}),
                html.Div(id='datatable-interactivity-container1'),
                 ], className="row"),
            # Row 5

            html.Div([
                html.H6(['断路器使用年限数据'],
                         className="gs-header",style={'background-color':'lightblue','margin-top':10}),
                dash_table.DataTable(
                    id='datatable-interactivity1',
                    columns=[
                        {"name": i, "id": i, "deletable": True} for i in df.columns
                    ],
                    data=df.to_dict("rows"),
                    editable=True,
                    filtering=True,
                    sorting=True,
                    sorting_type="multi",
                    row_selectable="multi",
                    style_cell={
                        'minWidth': '0px', 'maxWidth': '180px',
                        'whiteSpace': 'normal'
                    },
                    style_cell_conditional=[{
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(248, 248, 248)'
                                           }],
                    row_deletable=True,
                    selected_rows=[],
                    pagination_mode="fe",
                    pagination_settings={
                        "displayed_pages": 1,
                        "current_page": 0,
                        "page_size": 5,
                    },
                    navigation="page",
                )
            ], className="row")

        ], className="subpage")

    ], className="page")



Open_and_Closing_Time = html.Div([  # page 5

        print_button(),

        html.Div([

            Header(),

            # Row 1
            # Row 2

            html.Div([
                html.H6(['断路器合分闸时间统计'],className="gs-header",style={'background-color':'lightblue','margin-bottom':10}),
                html.Div(id='datatable-interactivity-container2')
            ]),

            # Row 3

            html.Div([
                html.H6(['断路器合分闸时间数据'],
                        className="gs-header",style={'background-color':'lightblue','margin-top':10}),
                dash_table.DataTable(
                    id='datatable-interactivity2',
                    columns=[
                        {"name": i, "id": i, "deletable": False} for i in df2.columns
                    ],
                    data=df2.to_dict("rows"),
                    editable=False,
                    filtering=True,
                    sorting=True,
                    style_cell={
                        'minWidth': '0px', 'maxWidth': '180px',
                        'whiteSpace': 'normal'
                    },
                    style_cell_conditional=[{
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(248, 248, 248)'
                                           }],
                    sorting_type="multi",
                    row_deletable=False,
                    selected_rows=[],
                    pagination_mode="fe",
                    pagination_settings={
                        "displayed_pages": 1,
                        "current_page": 0,
                        "page_size": 15,
                    },
                    navigation="page",
                )
            ], className="row")

        ], className="subpage")

    ], className="page")


acbdistribution = html.Div([  # page 5

        print_button(),

        html.Div([

            Header(),

            # Row 1
            # Row 2
            html.Div([
                html.H6(['断路器全国分布'],className="gs-header",style={'background-color':'lightblue','margin-bottom':10}),
                 html.Li("\
                筛选条件为全国范围内的省、直辖市或者自治区。"),
            ], className='row'),
            # Row 3

            html.Div([
                    html.Div([
                    dcc.Dropdown(id="state-selected",
                                 options=[{'label': i, 'value': i} for i in
                                          df4[df4.parent_city.isnull()].location.unique()],
                                 multi=True,
                                 value='全国',
                                 placeholder="选择省份",
                                 style={
                                     "display": "block",
                                     "margin-left": "auto",
                                     "margin-right": "auto",
                                     "width": "50%"

                                 }
                                 )
                ]),
                html.Div(dcc.Graph(id="datatable-interactivity-container4"))

            ], className="row")

        ], className="subpage")

    ], className="page")

## Page layouts
noPage = html.Div([  # 404

    html.P(["404 Page not found"])

    ], className="no-page")

# Describe the layout, or the UI, of the app
app.config['suppress_callback_exceptions']=True
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# Update page
# # # # # # # # #
# detail in depth what the callback below is doing
# # # # # # # # #
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/dash-siemens-report' or pathname == '/dash-siemens-report/acbdistribution':
        return acbdistribution
    elif pathname == '/dash-siemens-report/Used_Year':
        return Used_Year
    elif pathname == '/dash-siemens-report/Temperature_Inc':
        return Temperature_Inc
    elif pathname == '/dash-siemens-report/loadornot':
        return loadornot
    elif pathname == '/dash-siemens-report/Open_and_Closing_Time':
        return Open_and_Closing_Time
    elif pathname == '/dash-siemens-report/full-view':
        return  acbdistribution, Temperature_Inc, Used_Year, loadornot, Open_and_Closing_Time
    else:
        return noPage




@app.callback(
    Output('datatable-interactivity-container1', "children"),
    [Input('datatable-interactivity1', "derived_virtual_data"),
     Input('datatable-interactivity1', "derived_virtual_selected_rows")])
def update_graph(rows, derived_virtual_selected_rows):
    # When the table is first rendered, `derived_virtual_data` and
    # `derived_virtual_selected_rows` will be `None`. This is due to an
    # idiosyncracy in Dash (unsupplied properties are always None and Dash
    # calls the dependent callbacks when the component is first rendered).
    # So, if `rows` is `None`, then the component was just rendered
    # and its value will be the same as the component's dataframe.
    # Instead of setting `None` in here, you could also set
    # `derived_virtual_data=df.to_rows('dict')` when you initialize
    # the component.
    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []

    if rows is None:
        dff = df
    else:
        dff = pd.DataFrame(rows)
    dff = pd.pivot_table(
            dff,
            index=["使用年限"],
            columns=['产品型号'],
            values=['产品ID'],
            aggfunc='count',
            fill_value=0)
    colors = []
    for i in range(len(dff)):
        if i in derived_virtual_selected_rows:
            colors.append("#7FDBFF")
        else:
            colors.append("#0074D9")

    return html.Div(
        [
            dcc.Graph(
                id='left-graph',
                figure={
                    "data": [
                go.Bar(x=dff.index, y=dff[('产品ID', mgr_options[i])], name='型号'+mgr_options[i])
                        for i in np.arange(0,len(mgr_options))
            # {
            #    "x": dff["country"],
            #    # check if column exists - user may have deleted it
            #    # If `column.deletable=False`, then you don't
            #    # need to do this check.
            #    "y": dff[column] if column in dff else [],
            #    "type": "bar",
            #    "marker": {"color": colors},
            # }
                          ],
                    "layout":
                        go.Layout(
                              autosize=False,
                              legend=dict(
                                traceorder='normal',
                                font=dict(
                                    family='sans-serif',
                                    size=11
                                )
                            ),
                                  xaxis={
                                      'title': "使用年限",
                                      'titlefont': {
                                          'color': 'black',
                                          'size': 12},
                                      'tickfont': {
                                          'size': 12,
                                          'color': 'black'

                                      }
                                  },
                                  yaxis={
                                      'title': "断路器数量",
                                      'titlefont': {
                                          'color': 'black',
                                          'size': 12,

                                      },

                                      'tickfont': {
                                          'color': 'black'

                                      }
                                  },
                            height=400,
                            width=700,
                            margin={
                                "r": 0,
                                "t": 11,
                                "b": 28,
                                "l": 40
                            },
                            barmode='stack')
                }
            )
    ])


@app.callback(
    Output('datatable-interactivity-container2', "children"),
    [Input('datatable-interactivity2', "derived_virtual_data"),
     Input('datatable-interactivity2', "derived_virtual_selected_rows")])
def update_graph(rows, derived_virtual_selected_rows):
    # When the table is first rendered, `derived_virtual_data` and
    # `derived_virtual_selected_rows` will be `None`. This is due to an
    # idiosyncracy in Dash (unsupplied properties are always None and Dash
    # calls the dependent callbacks when the component is first rendered).
    # So, if `rows` is `None`, then the component was just rendered
    # and its value will be the same as the component's dataframe.
    # Instead of setting `None` in here, you could also set
    # `derived_virtual_data=df.to_rows('dict')` when you initialize
    # the component.
    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []

    if rows is None:
        dff2 = df2
    else:
        dff2 = pd.DataFrame(rows)

    colors = []
    for i in range(len(dff2)):
        if i in derived_virtual_selected_rows:
            colors.append("#7FDBFF")
        else:
            colors.append("#0074D9")
#if __name__ == '__main__':
#    app.run_server(debug=False,
#            host='127.0.0.1',
#            port=8050
#            )
    return  html.Div([
        html.Div([
        dcc.Graph(
            id="graph-1",
            figure={
                'data': [
                go.Box(
                y=dff2[dff2['产品型号'] == dff2['产品型号'].unique()[i]]['分闸时间'],
                name='产品型号:'+dff2['产品型号'].unique()[i],
                marker=dict(
                        color=c2[i],
                           ),
                boxmean=True
                )  for i in np.arange(0,len(dff2['产品型号'].unique()))
                          ],
                'layout': go.Layout(
                    title='分闸时间箱型图',
                    autosize=False,
                    bargap=0.35,
                    font={
                        'family': "Franklin Gothic",
                        "size": 10,
                        'color': '#7f7f7f'
                    },
                    height=350,
                    width=350,
                    clickmode='event+select',
                    dragmode= 'zoom',
                    hovermode="closest",
                    margin={
                        'l': 15, 'r': 5, 'b': 15, 't': 30
                    },
                    xaxis={
                        "autorange": True,
                        "showline": True,
                        "title": "",
                        "type": "category"
                    },
                    yaxis={
                        "autorange": True,
                        "showgrid": True,
                        "showline": True,
                        "title": "",
                        "type": "linear",
                        "zeroline": False
                    }
                )
            },
            config={
                'displayModeBar': False
            }
        )
    ], className="six columns"),

    html.Div([
        dcc.Graph(
            id="graph-2",
            figure={
                'data': [
                go.Box(
                y=dff2[dff2['产品型号'] == dff2['产品型号'].unique()[i]]['合闸时间'],
                name='产品型号:'+dff2['产品型号'].unique()[i],
                marker=dict(
                        color=c2[i],
                           ),
                boxmean=True
                )  for i in np.arange(0,len(dff2['产品型号'].unique()))
                          ],
                'layout': go.Layout(
                    title='合闸时间箱型图',
                    autosize=False,
                    bargap=0.35,
                    font={
                        'family': "Franklin Gothic",
                        "size": 10,
                        'color': '#7f7f7f'
                    },
                    height=350,
                    width=350,
                    clickmode='event+select',
                    dragmode= 'zoom',
                    hovermode="closest",
                    margin={
                        'l': 15, 'r': 5, 'b': 15, 't': 30
                    },
                    xaxis={
                        "autorange": True,
                        "showline": True,
                        "title": "",
                        "type": "category"
                    },
                    yaxis={
                        "autorange": True,
                        "showgrid": True,
                        "showline": True,
                        "title": "",
                        "type": "linear",
                        "zeroline": False
                    }
                )
            },
            config={
                'displayModeBar': False
            }
        )
    ], className="six columns"),

], className="row ")




@app.callback(
    Output('datatable-interactivity-container3', "children"),
    [Input('datatable-interactivity3', "derived_virtual_data"),
     Input('datatable-interactivity3', "derived_virtual_selected_rows")])
def update_graph(rows, derived_virtual_selected_rows):
    # When the table is first rendered, `derived_virtual_data` and
    # `derived_virtual_selected_rows` will be `None`. This is due to an
    # idiosyncracy in Dash (unsupplied properties are always None and Dash
    # calls the dependent callbacks when the component is first rendered).
    # So, if `rows` is `None`, then the component was just rendered
    # and its value will be the same as the component's dataframe.
    # Instead of setting `None` in here, you could also set
    # `derived_virtual_data=df.to_rows('dict')` when you initialize
    # the component.
    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []

    if rows is None:
        dff3 = df3
    else:
        dff3 = pd.DataFrame(rows)

    colors = []
    for i in range(len(dff3)):
        if i in derived_virtual_selected_rows:
            colors.append("#7FDBFF")
        else:
            colors.append("#0074D9")

    return html.Div(
        [
          html.Div([
            dcc.Graph(
                id='left-graph',
                figure={
                    "data": [
                go.Scatter(
                x=dff3[dff3['产品型号'] == dff3['产品型号'].unique()[i]]['实测运行电流'],
                y=(dff3[dff3['产品型号'] == dff3['产品型号'].unique()[i]]['柜内温度'] -
                   dff3[dff3['产品型号'] == dff3['产品型号'].unique()[i]]['柜外环境温度']),
                #name=dff['产品型号'].unique()[i],
                mode='markers',
                text='产品ID:' + dff3[dff3['产品型号'] == dff3['产品型号'].unique()[i]]['产品型号'],
                    marker=dict(size=14,
                            line={'width': 0.5, 'color': 'white'},
                            color=c3[i],
                            opacity=0.7
                            )
                    )  for i in np.arange(0,len(dff3['产品型号'].unique()))
            # {
            #    "x": dff["country"],
            #    # check if column exists - user may have deleted it
            #    # If `column.deletable=False`, then you don't
            #    # need to do this check.
            #    "y": dff[column] if column in dff else [],
            #    "type": "bar",
            #    "marker": {"color": colors},
            # }
                          ],
                    "layout":
                        go.Layout(
                            title='实测最大电流与实测最大温升',
                            autosize=False,
                            bargap=0.35,
                            font={
                                'family': "Franklin Gothic",
                                "size": 10,
                                'color': '#7f7f7f'
                            },
                            height=350,
                            width=350,
                            clickmode='event+select',
                            dragmode='zoom',
                            showlegend=False,
                            hovermode="closest",
                            margin={
                                'l': 35, 'r': 0, 'b': 30, 't': 40
                            },
                            xaxis={
                                "title": "实测最大电流"
                            },
                            yaxis={
                                "title": "实测最大温升"
                            }
                        )
                },
                config={
                    'displayModeBar':  False
                }
            )
            ], className="six columns"),
            html.Div([
            dcc.Graph(
                id='right-graph',
                figure={
                    "data": [
                        go.Scatter(
                            x=dff3[dff3['产品型号'] == dff3['产品型号'].unique()[i]]['预期最大电流'],
                            y=(dff3[dff3['产品型号'] == dff3['产品型号'].unique()[i]]['断路器桩头温度'] -
                               dff3[dff3['产品型号'] == dff3['产品型号'].unique()[i]]['柜外环境温度']),
                            #name=dff['产品型号'].unique()[i],
                            mode='markers',
                            text='产品ID:' + dff3[dff3['产品型号'] == dff3['产品型号'].unique()[i]]['产品型号'],
                            marker=dict(size=14,
                                        line={'width': 0.5, 'color': 'white'},
                                        color=c3[i],
                                        opacity=0.7
                                        )
                        ) for i in np.arange(0,len(dff3['产品型号'].unique()))
                        # {
                        #    "x": dff["country"],
                        #    # check if column exists - user may have deleted it
                        #    # If `column.deletable=False`, then you don't
                        #    # need to do this check.
                        #    "y": dff[column] if column in dff else [],
                        #    "type": "bar",
                        #    "marker": {"color": colors},
                        # }
                    ],
                    "layout":go.Layout(
                    title='预期最大电流与预期最大温升',
                    autosize=False,
                    bargap=0.35,
                    font={
                        'family': "Franklin Gothic",
                        "size": 10,
                        'color': '#7f7f7f'
                    },
                    height=350,
                    width=350,
                    clickmode='event+select',
                    dragmode= 'zoom',
                    showlegend= False,
                    hovermode="closest",
                    margin={
                        'l': 35, 'r': 0, 'b': 30, 't': 40
                    },
                    xaxis={
                        "title": '预期最大电流'
                    },
                    yaxis={
                        "title": '预期最大温升'
                    }
                )
            },
            config={
                'displayModeBar': False
            }
        )
    ], className="six columns"),
], className="row ")




@app.callback(
    dash.dependencies.Output("datatable-interactivity-container4", "figure"),
    [dash.dependencies.Input("state-selected", "value")]
)
def update_figure(selected):
    if (selected=='全国') or selected == []:
        trace = []
        df4['mode']=np.where(df4['parent_city'].isnull(),'star','marker')
        df4['size']=np.where(df4['parent_city'].isnull(),12,8)
        dff=df4
        trace.append(go.Scattermapbox(
            lat=dff["lat"],
            lon=dff["lon"],
            mode='markers+text',
            marker={'symbol':dff['mode'], 'size': dff['size']},
            text=dff['location'].apply(lambda x:x.replace('-',''))+':'+dff['id_x'].apply(lambda x:str(x)),
            textposition='bottom center',
            hoverinfo='text',
            name='全国'
        ))
        latc = trace[0]['lat'].mean()
        lonc = trace[0]['lon'].mean()
        return {
            "data": trace,
            "layout": go.Layout(
                autosize=True,
                margin=dict(
                    l=0,
                    r=0,
                    b=0,
                    t=10
                ),
                hovermode='closest',
                showlegend=False,
                height=600,
                mapbox={'accesstoken': mapbox_access_token,
                        'bearing': 0,
                        'center': {'lat': latc, 'lon': lonc},
                        'pitch': 30, 'zoom': 3,
                        "style": 'mapbox://styles/mapbox/light-v9'},
            )
        }
    else:
        trace = []
        latc = []
        lonc = []
        for i,state in enumerate(selected):
                   dff = df4[(df4["admin_area"] == state) & (~df4["parent_city"].isnull())]
                   trace.append(go.Scattermapbox(
                     lat=dff["lat"],
                     lon=dff["lon"],
                     mode='markers+text',
                     marker={'symbol': 'marker', 'size': 11},
                     text=dff['location'].apply(lambda x:x.replace('-',''))+':'+dff['id_x'].apply(lambda x:str(x)),
                     textposition='bottom center',
                     hoverinfo='text',
                     name=state
                    ))
                   latc.append(trace[i]['lat'])
                   lonc.append(trace[i]['lon'])
        latc=np.concatenate(latc).ravel().mean()
        lonc=np.concatenate(lonc).ravel().mean()
        zoomvalue=5.5 if len(list(selected))==1 else 4.5 if len(list(selected))<=3 else 3.5
        return {
            "data": trace,
            "layout": go.Layout(
                autosize=True,
                margin=dict(
                    l=0,
                    r=0,
                    b=0,
                    t=10
                ),
                hovermode='closest',
                showlegend=False,
                height=600,
                mapbox={'accesstoken': mapbox_access_token,
                        'bearing': 0,
                        'center': {'lat': latc, 'lon': lonc},
                        'pitch': 30, 'zoom': zoomvalue,
                        "style": 'mapbox://styles/mapbox/light-v9'},
                )
           }



@app.callback(
    dash.dependencies.Output("datatable-interactivity-container5", "figure"),
    [dash.dependencies.Input("load-selected", "value"),
     dash.dependencies.Input("mlfb-selected", "value")]
)
def update_figure(selected1,selected2):
    dff=df5[(df5.with_load==selected1) & (df5.type==selected2)].sort_values(by='count_number')
    N = len(mergedtablegroup.count_number.unique())
    c4 = ['hsl(' + str(h) + ',50%' + ',50%)' for h in np.linspace(0, 300, N)]
    trace = go.Bar(x=dff.opt_year, y=dff.count_number,
                   name=(('带载操作:' if selected1==1 else '不带载操作:')+'<br>'+'产品型号:'+selected2))
    return {
            "data": [trace],
            "layout": go.Layout(xaxis={
                                      'title': "使用年限",
                                      'titlefont': {
                                          'color': 'black',
                                          'size': 14},
                                      'tickfont': {
                                          'size': 12,
                                          'color': 'black'

                                      }
                                  },
                                  yaxis={
                                      'title': "操作次数",
                                      'titlefont': {
                                          'color': 'black',
                                          'size': 14,

                                      },

                                      'tickfont': {
                                          'color': 'black'

                                      }
                                  },
                                  barmode='stack')
           }
# # # # # # # # #
#detail the way that external_css and external_js work and link to alternative method locally hosted
external_css = ["https://cdnjs.cloudflare.com/ajax/libs/normalize/7.0.0/normalize.min.css",
                "https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
                "//fonts.googleapis.com/css?family=Raleway:400,300,600",
                "https://codepen.io/bcd/pen/KQrXdb.css",
                "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css"]

for css in external_css:
    app.css.append_css({"external_url": css})

external_js = ["https://code.jquery.com/jquery-3.2.1.min.js",
               "https://codepen.io/bcd/pen/YaXojL.js"]

for js in external_js:
    app.scripts.append_script({"external_url": js})


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8080, debug=False)
