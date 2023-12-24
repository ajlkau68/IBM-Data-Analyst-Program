import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import dash_bootstrap_components as dbc

# Load the data using pandas
path = r'C:\Users\James\OneDrive\Documents\Jupyter Notebooks\IBM Data Analyst Course\Visualizing Data With Python\historical_automobile_sales.csv'
df = pd.read_csv(path)

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# ---------------------------------------------------------------------------------
#  Create app widgets
items = [{'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
         {'label': 'Recession Period Statistics', 'value': 'Recession Statistics'}]
# Dropdown
report_dropdown = html.Div(
    dcc.Dropdown(
        id='dropdown-report', options=items, placeholder='Select report type', clearable=True
    )
)
# Year Slider
year_slider = html.Div(
    dcc.Slider(
        id='year-slider',
        min=df['Year'].min(),
        max=df['Year'].max(),
        step=1,
        marks={str(year): str(year) for year in range(1980, 2024, 2)},
        value=df['Year'].min()
    )
)

# Create app layout
app.layout = dbc.Container([
    dbc.Row([
        # Logo and Title
        dbc.Col([
            # Logo
            dbc.Card([
                dbc.CardImg(src="/assets/xyz_logo.png")
            ], className='mb-2')

        ], width=2),
        dbc.Col([
            # Title
            dbc.Card([
                dbc.CardBody([
                    html.H1('Sales Statistics Dashboard',
                            style={'textAlign': 'center', 'color': '#88001B', 'font-size': 35})
                ])
            ])

        ])
    ], className='mb-2 mt-2 ml-2 mr-2'),
    # Dropdown and Year Slider
    dbc.Row([
        dbc.Col([
            # Dropdown
            dbc.Card([
                dbc.CardHeader(
                    html.H6('Report Type'), style={'textAlign': 'center'}),
                dbc.CardBody([
                    html.Div(report_dropdown)
                ])
            ])

        ], width=3),
        dbc.Col([
            # Year slider
            dbc.Card([
                dbc.CardHeader(
                    html.H6('Years'), style={'textAlign': 'center'}),
                dbc.CardBody([
                    year_slider
                ])
            ])

        ])
    ], className='mb-2 mt-2'),
    # Text visuals
    dbc.Row([
        dbc.Col([
            # Total Sales
            dbc.Card([
                dbc.CardBody([
                    html.H6('TOTAL SALES'),
                    html.H2(id='content-sales', children='000')
                ], style={'textAlign': 'center'})
            ])

        ]),
        dbc.Col([
            # Average price
            dbc.Card([
                dbc.CardBody([
                    html.H6('AVERAGE PRICE ($)'),
                    html.H2(id='content-price', children='000')
                ], style={'textAlign': 'center'})
            ])

        ]),
        dbc.Col([
            # No. of Vehicle Types
            dbc.Card([
                dbc.CardBody([
                    html.H6('VEHICLE TYPES'),
                    html.H2(id='content-vehicle', children='000')
                ], style={'textAlign': 'center'})
            ])

        ]),
        dbc.Col([
            # Unemployment rate
            dbc.Card([
                dbc.CardBody([
                    html.H6('AVERAGE UNEMPLOYMENT RATE (%)'),
                    html.H2(id='content-unemployment', children='000')
                ], style={'textAlign': 'center'})
            ])

        ])
    ], className='mb-2'),

    # Graphs
    dbc.Row([
        dbc.Col([
            # Total Sales by Year Line graph
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='chart1', figure={})
                ])
            ])

        ]),
        dbc.Col([
            # Total Monthly Sales by year (line chart)
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='chart2', figure={})
                ])
            ])

        ]),
    ], className='mb-2'),
    # More graphs
    dbc.Row([
        dbc.Col([
            # Average monthly Sales per vehicle (bar chart)
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='chart3', figure={})
                ])
            ])

        ]),
        dbc.Col([
            # Total Advert Expenditure per vehicle (horizontal bar chart)
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='chart4', figure={})
                ])
            ])

        ])
    ], className='mb-2')

], fluid=True)

# Create 1st callback for report type


@app.callback(Output(component_id='dropdown-report', component_property='value'),
              Input(component_id='year-slider', component_property='disabled'))
def update_input_container(selected_statistics):
    if (selected_statistics == 'Yearly Statistics') or (selected_statistics == 'Recession Statistics'):
        return False
    else:
        return True

# Create 2nd callback to update small cards


@app.callback([Output(component_id='content-sales', component_property='children'),
               Output(component_id='content-price',
                      component_property='children'),
               Output(component_id='content-vehicle',
                      component_property='children'),
               Output(component_id='content-unemployment', component_property='children')],
              [Input(component_id='dropdown-report', component_property='value'),
               Input(component_id='year-slider', component_property='value')])
def update_small_cards(selected_statistics, input_year):
    if selected_statistics == 'Recession Statistics':
        recession_data = df.query('Recession == 1 and Year == @input_year')
        # Update total sales card
        total_sales = round(recession_data['Automobile_Sales'].sum())

        # Update average price card
        avg_price = round(recession_data['Price'].mean(), 2)

        # Update vehicle type card
        num_vehicle = len(recession_data['Vehicle_Type'].unique())

        # Update average unemployment card
        avg_unemp_rate = round(recession_data['unemployment_rate'].mean(), 2)

        return [total_sales, avg_price, num_vehicle, avg_unemp_rate]

    elif (selected_statistics == 'Yearly Statistics' and input_year):
        yearly_data = df.query('Year == @input_year')

        # Update total sales card
        total_sales = round(yearly_data['Automobile_Sales'].sum())

        # Update average price card
        avg_price = round(yearly_data['Price'].mean(), 2)

        # Update vehicle type card
        num_vehicle = len(yearly_data['Vehicle_Type'].unique())

        # Update average unemployment card
        avg_unemp_rate = round(yearly_data['unemployment_rate'].mean(), 2)

        return [total_sales, avg_price, num_vehicle, avg_unemp_rate]

# Create 3rd callback to update charts


@app.callback([Output(component_id='chart1', component_property='figure'),
               Output(component_id='chart2', component_property='figure'),
               Output(component_id='chart3', component_property='figure'),
               Output(component_id='chart4', component_property='figure')],
              [Input(component_id='dropdown-report', component_property='value'),
               Input(component_id='year-slider', component_property='value')])
def update_graphs(selected_statistics, input_year):
    if selected_statistics == 'Recession Statistics':
        # Filter data for recession period
        recession_data = df.query('Recession == 1 and Year == @input_year')
        # Update chart 1 (line chart)
        monthly_sales = recession_data.groupby(
            'Month')['Automobile_Sales'].sum().reset_index()
        Rchart1 = px.line(monthly_sales, x='Month', y='Automobile_Sales',
                          title=f'Monthly Automobile Sales for {input_year}')

        # Update chart 2 (bar chart - average monthly sales by vehicle)
        vehicle_sales = recession_data.groupby(['Month', 'Vehicle_Type'])[
            'Automobile_Sales'].mean().reset_index()
        Rchart2 = px.bar(vehicle_sales, x='Month', y='Automobile_Sales',
                         color='Vehicle_Type', title=f'Average Monthly Sales by Vehicle for {input_year}')

        # Update chart 3 (hbar chart - advert expenditure)
        advert_exp = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum(
        ).reset_index().sort_values(by='Advertising_Expenditure', ascending=True)
        Rchart3 = px.bar(advert_exp, x='Advertising_Expenditure', y='Vehicle_Type',
                         orientation='h', title=f'Advertisement Expenditure per Vehicle for {input_year}')

        # Update chart 4 (bar chart - unemployment)
        unemployment_rate = recession_data.groupby(['unemployment_rate', 'Vehicle_Type'])[
            'Automobile_Sales'].sum().reset_index()
        Rchart4 = px.bar(unemployment_rate, x='unemployment_rate', y='Automobile_Sales',
                         color='Vehicle_Type', title=f'Effect of Unemployment on Vehicle Type Sales for {input_year}')

        return [Rchart1, Rchart2, Rchart3, Rchart4]

    elif (selected_statistics == 'Yearly Statistics' and input_year):
        # Filter data for years
        yearly_data = df.query('Year == @input_year')
        # Update chart 1 (line chart - monthly sales)
        monthly_sales = yearly_data.groupby(
            'Month')['Automobile_Sales'].sum().reset_index()
        Ychart1 = px.line(monthly_sales, x='Month', y='Automobile_Sales',
                          title=f'Monthly Automobile Sales for {input_year}')

        # Update chart 3 (bar chart - month sales by vehicle)
        vehicle_sales = yearly_data.groupby(['Month', 'Vehicle_Type'])[
            'Automobile_Sales'].mean().reset_index()
        Ychart2 = px.bar(vehicle_sales, x='Month', y='Automobile_Sales',
                         color='Vehicle_Type', title=f'Average Monthly Sales by Vehicle for {input_year}')

        # Update chart 4 (hbar chart - advert expenditure)
        advert_exp = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum(
        ).reset_index().sort_values(by='Advertising_Expenditure', ascending=True)
        Ychart3 = px.bar(advert_exp, x='Advertising_Expenditure', y='Vehicle_Type',
                         orientation='h', title=f'Advertisement Expenditure per Vehicle for {input_year}')

        # Update chart 2 (bar chart - unemployment rate sales)
        unemployment_rate = yearly_data.groupby(['unemployment_rate', 'Vehicle_Type'])[
            'Automobile_Sales'].sum().reset_index()
        Ychart4 = px.bar(unemployment_rate, x='unemployment_rate', y='Automobile_Sales',
                         color='Vehicle_Type', title=f'Monthly Automobile Sales for {input_year}')

        return [Ychart1, Ychart2, Ychart3, Ychart4]


# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
