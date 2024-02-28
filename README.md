# sqlalchemy-challenge
Part 1: Analyze and Explore the Climate Data - Honolulu, Hawaii

Python and SQLAlchemy is used to do a basic climate analysis and data exploration of the climate database. Specifically, used SQLAlchemy ORM queries, Pandas, and Matplotlib.

. Used the provided files (climate_starter.ipynb and hawaii.sqlite) to complete climate analysis and data exploration.

. Used the SQLAlchemy create_engine() function to connect to the SQLite database.

. Used SQLAlchemy automap_base() function to reflect the tables into classes, and then saved references to the classes named station and measurement.

. Linked Python to the database by creating a SQLAlchemy session.

Performed a precipitation analysis and station analysis.

Precipitation Analysis:

. Determined the most recent date in the dataset.

. Using that date, the previous 12 months of precipitation data is obtained by querying the previous 12 months of data.

. The query results are loaded into a Pandas DataFrame. Explicitly set the column names.

. Sorted the DataFrame values by "date".

. The results are then plotted.

. Used Pandas to print the summary statistics for the precipitation data.

Station Analysis:

. Designed a query to calculate the total number of stations in the dataset.

. Designed a query to find the most-active stations (that is, the stations that have the most rows- greatest number of observations) by listing the stations and observation counts in descending order.

. A query is written to calculate the lowest, highest, and average temperatures that filters on the most-active station id found in the previous query.

. Designed a query to get the previous 12 months of temperature observation (TOBS) data by filtering the station that has the greatest number of observations.

. Queried the previous 12 months of TOBS data for that station and results are plotted as a Histogram and closed the session.

Part 2: Design Your Climate App
To design a Flask API based on the queries that was just developed. To do so, used Flask to create the routes as follows:

1. / Started at the homepage.

   Listed all the available routes.

2. /api/v1.0/precipitation

  Converted the query results from the precipitation analysis (i.e. retrieved only the last 12 months of data) to a 
  dictionary using date as the key and prcp as the value. Returned the JSON representation of the dictionary. (Used the 
  Flask jsonify function to convert your API data to a valid JSON response object)

3. /api/v1.0/stations

   Returned a JSON list of stations from the dataset.
   
5. /api/v1.0/tobs

  Queried the dates and temperature observations of the most-active station for the previous year of data. Returned a JSON 
  list of temperature observations for the previous year.

6. /api/v1.0/<start> and /api/v1.0/<start>/<end>

  Returned a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified 
  start or start-end range.
  
  For a specified start, calculated TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.

  For a specified start date and end date, calculated TMIN, TAVG, and TMAX for the dates from the start date to the end 
  date, inclusive.



