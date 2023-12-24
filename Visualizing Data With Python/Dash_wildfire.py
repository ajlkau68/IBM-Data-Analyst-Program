import pandas as pd
import plotly.express as px
from dash import dash, dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import datetime as dt

# Create app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Clear the layout and do not display exception till callback gets executed
app.config.suppress_callback_exceptions = True

# Read the wildfire data into a dataframe
path = r'C:\Users\James\OneDrive\Documents\Jupyter Notebooks\IBM Data Analyst Course\Visualizing Data With Python\Historical_Wildfires.csv'
df = pd.read_csv(path)

# Extract year and month from the date column
# used for the names of the month
df['Month'] = pd.to_datetime(df['Date']).dt.month_name()
df['Year'] = pd.to_datetime(df['Date']).dt.year

# create a list of regions and years for the app widgets
regions = list(df.Region.unique())
years = list(df.Year.unique())

# Create layout of app
app.layout = html.Div(children=[
    # add title to the dashboard
    html.H1('Australia Wildfire Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': '26'}),

    # 1st Inner Div
    # add radioitems and dropdown
    html.Div([
        html.H2('Select Region', style={'margin-right': '2em'}),
        dcc.RadioItems(id='regions',
                       options=regions,
                       value='NSW',
                       inline=True
                       )
    ]),

    # 2nd Inner Div
    # add dropdown
    html.Div([
        html.H2('Select Year', style={'margin-right': '2em'}),
        dcc.Dropdown(
            id='years',
            options=years,
            value=2005
        )
    ]),

    # Outer Div
    html.Div([

        # Inner Divs for Graphs
        html.Div([], id='plot1'),
        html.Div([], id='plot2')
    ], style={'display': 'flex'})

])

# Add callback decorator


@app.callback([Output(component_id='plot1', component_property='children'),
               Output(component_id='plot2', component_property='children')],
              [Input(component_id='regions', component_property='value'),
               Input(component_id='years', component_property='value')])
def reg_year_display(input_region, input_year):
    # data
    region_data = df.query('Region == @input_region')
    yr_data = df.query('Year == @input_year')

    # Plot one (pie chart) - Monthly Average Estimated Fire Area
    est_data = region_data.groupby(
        'Month')['Estimated_fire_area'].mean().reset_index()

    pie_fig = px.pie(est_data, values='Estimated_fire_area', names='Month',
                     title="{} : Monthly Average Estimated Fire area in Year {}".format(input_region, input_year))

    # Plot two (bar chart) - Monthly Average Count of Pixels for Presumed Vegattion Fires
    veg_data = yr_data.groupby('Month')['Count'].mean().reset_index()
    bar_fig = px.bar(veg_data, x='Month', y='Count',
                     title="{} : Average Count of Pixels for Presumed Vegetation Fires in Year {}".format(input_region, input_year))

    return [dcc.Graph(figure=pie_fig), dcc.Graph(figure=bar_fig)]


if __name__ == '__main__':
    app.run_server()
