import os
from flask import Flask, render_template
import pandas as pd
import glob


app = Flask(__name__)
#For the initial project, at this stage, the user will be expected to enter
#the station number, then the API URL will display the station, date and 
#temperature

@app.route("/")
def home():
    return render_template("home.html")

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
    

if __name__ == "__main__":
    app.run(debug=True)