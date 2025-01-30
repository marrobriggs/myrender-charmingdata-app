# Fetch the data using wbdata for Poverty Rate (SI.POV.NAHC)
df_poverty = wb.data.DataFrame('SI.POV.NAHC', 
                               mrnev=1, 
                               columns='time', 
                               numericTimeKeys=True)
df_poverty = df_poverty.transpose()

# 1. Visual for GDP per Capita (Brazil, Argentina, Colombia)
df_gdp_brazil = wb.data.DataFrame('NY.GDP.PCAP.CD', 
                                  economy=['BRA', 'ARG', 'COL'],
                                  time=range(2000, 2020), 
                                  index='time')

# Convert to Plotly
fig_gdp_brazil = px.line(df_gdp_brazil, 
                          title="GDP per Capita (Brazil, Argentina, Colombia)", 
                          labels={'value': 'GDP per Capita (USD)', 'time': 'Year', 'variable': 'Country'},
                          markers=True)

# 2. Visual for Distribution of Poverty Rate (Bar Graph)
# Use the "df_poverty" data frame for the bar chart
poverty_counts = df_poverty.count(axis=1)
fig_poverty = px.bar(x=poverty_counts.index, 
                     y=poverty_counts, 
                     title="Distribution of Poverty Rate MRVs", 
                     labels={'x': 'Year', 'y': 'Poverty Rate (%)'})

# 3. Visual for Population Estimates Over Time
# Example data for demonstration purposes, replace with actual data
years = np.arange(2000, 2020)
population_data = np.random.random(20) * 100000000  # Random data for demonstration

# Plot as line chart
fig_population = px.line(x=years, 
                         y=population_data, 
                         title="Population Estimates Over Time", 
                         labels={'x': 'Year', 'y': 'Population'})

# Initialize the Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])

# Define Navbar
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/home", active="exact")),
        dbc.NavItem(dbc.NavLink("About Me", href="/about", active="exact")),
    ],
    brand="Global Development Dashboard",
    brand_href="/home",
    color="primary",
    dark=True,
    className="mb-4"
)

# Home Layout
home_layout = html.Div([
    # Main Panel for Home Layout with the 3 tabs
    html.Div([
        dcc.Tabs([
            dcc.Tab(label='GDP per Capita (Brazil, Argentina, Colombia)', children=[
                html.Div([
                    dcc.Graph(id='gdp-brazil-graph', figure=fig_gdp_brazil),
                ]),
            ]),
            dcc.Tab(label='Poverty Rate Distribution', children=[
                html.Div([
                    dcc.Graph(id='poverty-graph', figure=fig_poverty),
                ]),
            ]),
            dcc.Tab(label='Population Estimates', children=[
                html.Div([
                    dcc.Graph(id='population-graph', figure=fig_population),
                ]),
            ]),
        ])
    ], style={'padding': '20px'})
])

# About Layout
about_layout = html.Div([
    html.H1("About This Dashboard"),
    html.P("""
        This dashboard provides an interactive way to explore key development indicators
        such as GDP per capita, poverty rate distribution, and population estimates over time.
        The visualizations offer insights into these metrics for various countries and regions,
        helping to understand global development trends.
    """),
    html.P("""
        Built with Python, Dash, Plotly, and Bootstrap, this dashboard is designed to allow
        users to interact with and analyze data, offering a dynamic and engaging user experience.
    """)
])

# Main Layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),  # URL handling for routing
    navbar,
    html.Div(id='page-content', style={'padding': '20px'})
])

# Callbacks for handling page routing and updating content
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/about':
        return about_layout
    # Default to home layout
    return home_layout

# Run the app
if __name__ == "__main__":
    app.run(debug=True)

