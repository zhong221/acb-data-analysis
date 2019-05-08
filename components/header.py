import dash_html_components as html
import dash_core_components as dcc

def Header():
    return html.Div([
        get_logo(),
        get_header(),
        html.Br([]),
        get_menu()
    ])

def get_logo():
    logo = html.Div([

        html.Div([
            html.Img(src='https://s3-eu-west-1.amazonaws.com/yousty-switzerland/content/lehrer/logos/Simens.png', height='40', width='160')
        ], className="ten columns padded"),

        html.Div([
            dcc.Link('Full View   ', href='/dash-siemens-report/full-view')
        ], className="two columns page-view no-print")

    ], className="row gs-header")
    return logo


def get_header():
    header = html.Div([

        html.Div([
            html.H5(
                '西门子空气断路器数字化增值服务')
        ], className="twelve columns padded",style={'background-color':'#2C9A87'})

    ], className="row gs-header gs-text-header")
    return header


def get_menu():
    menu = html.Div([

        dcc.Link('断路器地理位置分布      ', href='/dash-siemens-report/acbdistribution', className="tab first"),

        dcc.Link('断路器温升电流分析      ', href='/dash-siemens-report/Temperature_Inc', className="tab"),

        dcc.Link('断路器使用年限分析      ', href='/dash-siemens-report/Used_Year', className="tab"),

        dcc.Link('断路器电寿命分布分析      ', href='/dash-siemens-report/loadornot', className="tab"),

        dcc.Link('断路器合分闸时间分析      ', href='/dash-siemens-report/Open_and_Closing_Time', className="tab")

    ], className="row",style={'font-family': 'Times New Roman, Times, serif','display':'inline-block', 'font-weight': 'bold','margin-bottom':10})
    return menu
