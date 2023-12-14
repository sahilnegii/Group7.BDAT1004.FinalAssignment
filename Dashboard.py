# Importing the libraries to create connection with mongoDB atlas and displaying graph with dash.
import dash
from dash import html, dcc, dash_table
import pandas as pd
import urllib.parse
from pymongo import MongoClient

# ---------------------------------------------------------------------------------
# providing the username and password to url. Here we have used parse to give ID and pass because
# it was giving us error when we gave the arguments directy.
username = urllib.parse.quote_plus('RajPatel')
password = urllib.parse.quote_plus("Rp4formongodb@@4")

# URL to connect to the MongoDB atlas. Here we have used the balldontlie api to fetch the
# player's average season statistics.
client = MongoClient(
    "mongodb+srv://{}:{}@nbaplayers.6fc3bea.mongodb.net/Results?retryWrites=true&w=majority".format(username, password))

# Creating a new database and collection instant and data_from mongo will fetch all the available data from our database
db = client["Results"]
collection = db["Info"]
data_from_mongo = list(collection.find({}))

# Now our data is stored in a database into the json format here we are converting our
# original data to pandas dataframe. this will make it easy for visualization and exploration.
df = pd.DataFrame([record['data'][0] for record in data_from_mongo])

# Data Dictionary Information
data_dict_info = """
**Data Dictionary:**

- games_played: Number of games played
- player_id: Player number
- season: Year played
- min: Played minutes
- fgm: Field goals made
- fga: Field goal attempts
- fg3m: 3-point field goals made
- fg3a: 3-point field goal attempts
- ftm: Free throws made
- fta: Free throw attempts
- oreb: Offensive rebounds
- dreb: Defensive rebounds
- reb: Total rebounds
- ast: Assists
- stl: Steals
- blk: Blocks per game
- turnover: Turnovers per game
- pts: Points made per game
- fg_pct: Field goal percentage
- fg3_pct: 3-point field goal percentage
- ft_pct: Free throw percentage
"""

app = dash.Dash(__name__)

# Here we are defining the layout for the webpage and using Dash DataTable to display
# our stored data into a table format on the web.
app.layout = html.Div([

    #Header
    html.H1("NBA Player's Statistical Analysis", style={'textAlign':'center', 'background-color':'green'}),

    # Data Dictionary
    dcc.Markdown(data_dict_info, style={'padding': '10px', 'border': '1px solid #ccc','background-image':'url("https://images.pexels.com/photos/41433/pexels-photo-41433.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2")'}),

    html.H1("Data Table from our cloud database", style={'textAlign':'center', 'background-color':'green'}),
    dash_table.DataTable(
        id='table',
        columns=[{'name': col, 'id': col} for col in df.columns],
        data=df.to_dict('records'),  # Here we are converting our dataframe to the list of the dictionaries.
        style_table={'color': '#010127'},  # Giving a style by specifying color.
    ),

    html.H1("Our Analysis", style={'textAlign':'center', 'background-color':'green'}),

    html.H3("Note: Hover over each charts to reveal more information", style={'textAlign':'center','font-family': 'italic', 'background-color':'red'}),

    html.H2("Research question 1 : Relationship between the number of games played by individual players and the total points they have scored?"),
    
    # In dash, we use dcc.Graph to make interactive graph and charts.
    dcc.Graph(
        id='bar-chart', # specifying the id of graph.
        figure={
            'data': [
                {
                    'x': df['games_played'],  # X-axis data to be displayed
                    'y': df['pts'],           # y-axis data to be displayed
                    'type': 'bar',    # With the help of the type we are describing which type of chart we want to make.
                    'text': df['player_id'],  # Adding player_id from our data as data labels
                    'name': 'Points',
                    'marker': {'color': '#FFA07A'},  # Setting marker color
                },
            ],
            # defining the layout of the graph.
            'layout': {
                'title': 'Games Played vs Points (Bar Graph)',
                'xaxis': {'title': 'Games Played'},
                'yaxis': {'title': 'Points'},
                'plot_bgcolor': '#f0f0f0',
            }
        }
    ),
    html.H3("Research question 1 - Insights:"),
    html.P("When we hover our cursor over any data point on the above graph, we gain insights into the number of games a player participated in and their corresponding points scored. For instance, examining the first bar of the graph reveals that it corresponds to player ID 54, who has played 4 games and achieved an average score of 17.5 points."),


    html.H2("Research question 2: Based on the number of steals and rebounds, which player demonstrates better defensive skills?"),
    
    # Now we are creating the Dash Scatter Plot for finding out who is better defensive player from the data.
    dcc.Graph(
        id='defense-scatter-plot',
        figure={
            'data': [
                {
                    'x': df['reb'],
                    'y': df['stl'],
                    'mode': 'markers',
                    'marker': {'color': '#FFA07A'},
                    'text': df['player_id'],  # Add player_id as text labels
                    'name': 'Rebounds vs Steals',
                },
            ],

            'layout': {
                'title': 'Defensive Performance of the Player',
                'xaxis': {'title': 'Rebounds'},
                'yaxis': {'title': 'Steals'},
                'plot_bgcolor': '#f0f0f0',  # Setting plot background color to light grey
            }
        }
    ),
    html.H3("Research question 2 - Insights:"),
    html.P("When hovering over any data point, we can readily access the player's identification (ID) along with the respective statistics for rebounds and steals. This graphical representation allows us to make a clear observation: among the data points in the scatter plot, player ID 4, situated at the farthest end, stands out as the superior defensive player according to the specified criteria."),

    html.H2("Research question 3: Identify the most efficient three-point shooter from the provided data."),
    # Dash Bar Chart for finding out 3 point Efficiency
    dcc.Graph(
        id='efficiency-bar-chart',
        figure={
            'data': [
                {
                    'x': df['player_id'],
                    'y': df['fg3m'] / df['fg3a'],  # Here we are finding out the Efficiency ratio of 3 point shooting.
                                            # Efficiency ratio: 3-point field goals made/3-point field goal attempts
                    'type': 'bar', # type of the chart
                    'marker': {'color': '#FFA07A'},
                    'text': df['player_id'],  # Adding player_id as text labels
                    'name': '3-Point Efficiency',
                },
            ],
            'layout': {
                'title': 'Bar Chart for 3-Point Efficiency of Players',
                'xaxis': {'title': 'Player ID'},
                'yaxis': {'title': 'Efficiency Ratio'},
                'plot_bgcolor': '#f0f0f0',
            }
        }
    ),
    html.H3("Research question 3 - Insights:"),
    html.P("By calculating the efficiency ratio as the division of made three-point field goals by attempted three-point field goals, we've derived a meaningful metric. Based on this calculation, it becomes evident that player ID 38, with a remarkable shooting percentage of approximately 46.3%, emerges as the most proficient shooter within the dataset.")

])

if __name__ == '__main__':
    app.run_server(debug=False)