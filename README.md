# sqlalchemy-challenge


# Instructions
You are going on a long holiday to Honolulu, Hawaii.
To help with planning your trip, you want to analyze the climate for the area.

# Part 1
To start this project you will use Python and SQLAlchemy to do a basic climate analysis of the climate database.
You will need to connect to your SQLite database and reflect your tables into classes.

In the Precipitation Analysis you will need to find the most recent date in the dataset. After you get that date, you will need to grab the previous 12 moths of precipitation data. 
Once you get the 12 month summary, select only the "date" and "prcp" values. Then you will need to load the query results into a Pandas DataFrame and plot the results.

The Station Analysis requires you to design a query to calculate the total number of stations in the dataset and find the most-active stations. Similar to the Precipitation Analasis, you will be using the previous 12 months and plot the results of the calculations.

# Part 2
Now that the initial analysis is complete, you are tasked wiht designing a Flask API based on the queries you just developed.

To start you will need to list all of the available routes.

After the available routes are listed you then will work on th precipitation route. This will convert the query results from your precipitation analysis.

The next route you will work on is the stations route. You will need to return a JSON list of stations from the dataset.

The next route is the tobs route. In this route, you will query the dates and temperatire observations of the most-active station for the previous year of data.

The final routes you will do are the start and end routes. In this section you will need to find the min, avg, and max for the specified start and end dates.
