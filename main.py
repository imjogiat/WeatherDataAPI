import os
from flask import Flask, render_template
import pandas as pd
import glob


app = Flask(__name__)
#For the initial project, at this stage, the user will be expected to enter
#the station number, then the API URL will display the station, date and 
#temperature

variable = "abc"
station_data = pd.read_csv(r"data_small\stations.txt", skiprows=17)
station_data = station_data[["STAID","STANAME                                 "]]

#The home URL to display the format of the API URL and an example, as well
#as the table listing all station IDs, names and other labels
@app.route("/")
def home():
    return render_template("home.html", data=station_data.to_html())


#This URL will display the required API information as JSON data. 
#Therefore, for a requested station id, store the csv file data in DataFrame 
#then extract the temperature for a specific date.
@app.route("/api/v1/<station>/<date>")
def about(station, date):
    stationstr = str(station).zfill(6)
    filename = fr"data_small\TG_STAID{stationstr}.txt"
    
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    temperature = df.loc[df["    DATE"] == date]["   TG"].squeeze() / 10
    #return a view of the json file data
    return{"station:": station, 
           "date:": date,
           "temperature:": temperature}


#The URL below will display all annual/years data at a specific station
#example- for Dusseldorf station, all years from 1850 to 2025, 
# display temperature data
@app.route("/api/v1/<station>")
def station_all(station):
    stationstr = str(station).zfill(6)
    filename = fr"data_small\TG_STAID{stationstr}.txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    df_dict = df.to_dict(orient= "records")

    return df_dict
    

#The URL will display all station data during a provided year, rather 
# than full date
#example- temperature data during 1990 at all stations
@app.route("/api/v1/yearly/<station>/<year>")
def stations_yearly(station, year):
    stationstr = str(station).zfill(6)
    filename = fr"data_small\TG_STAID{stationstr}.txt"
    df = pd.read_csv(filename, skiprows=20)
    df["    DATE"] = df["    DATE"].astype(str)

    #accesses the column "date" then filters the column by string mehtod starts with
    #then use this column as a DF column string to access the filtered column
    #df[xyzabc] - xyzabc is a dataframe query 
    #filters a column and displays the resulting dataframe
    result = df[df["    DATE"].str.startswith(str(year))]
    results_dict = result.to_dict(orient="records")

    return results_dict


if __name__ == "__main__":
    app.run(debug=True)