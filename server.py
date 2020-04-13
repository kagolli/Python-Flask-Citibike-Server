import json
import requests
from flask import *
from math import sin, cos, sqrt, atan2, radians, floor

app = Flask(__name__)

# test route to see if server works
@app.route("/api", methods=['GET'])
def api():
    return "hello world"

# displays bike data with analysis
@app.route("/", methods=['GET'])
def home():
    with open('db.json', 'r') as db_read:
        data = json.load(db_read)
    map = {}
    for i in range(0, len(data)):
        curr = data[i]["start_station"]
        if curr in map:
            count = map[curr]
            map[curr] += 1
        else:
            map[curr] = 1

    sorted_map = sorted(map.items(), key=lambda kv: kv[1], reverse = True)

    map = {}
    count = 0
    for key, value in sorted_map:
        if count < 10:
            map[key] = value
            count += 1
    
    R = 6373.0

    # initialize empty array and distance ranges
    arr = [0,0,0,0,0,0,0,0,0,0]
    labels = ["0-299", "300-599","600-899","900-1199","1200-1499","1500-1799","1800-2099","2100-2399","2400-2699","2700-2999"]
    average = 0
    for i in range(0, len(data)):

        # checks if the entry has no data
        if data[i]["start_lat"] != "" and data[i]["start_lon"] != "" and data[i]["end_lat"] != "" and data[i]["end_lon"] != "":
            lat1 = radians(data[i]["start_lat"])
            lon1 = radians(data[i]["start_lon"])
            lat2 = radians(data[i]["end_lat"])
            lon2 = radians(data[i]["end_lon"])

            dlon = lon2 - lon1
            dlat = lat2 - lat1

            a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))

            distance = R * c * 1000

            # finds the respective index
            index = floor(distance / 300)

            # if the distance is within one of the given ranges, include that distance
            if distance > 0 and index < 10:
                average += distance
                arr[index] += 1
                count += 1

    average = str(round(average / (count - 10), 2))
    distances = {}

    # places data in dictionary
    for i in range(len(labels)):
        distances[labels[i]] = arr[i]
    return render_template("home.html", result = map, labels = distances, avg = average)

#CitiBike Data
@app.route("/bikes", methods=['GET'])
def bike():
    #requests the API
    req = requests.get("https://gbfs.citibikenyc.com/gbfs/es/station_status.json")
    req = req.json()
    sumAvailable = 0
    sumEAvailable = 0
    sumDisabled = 0
    sumDocsAvailable = 0
    sumDocsDisabled = 0
    sumStationsInstalled = 0

    #updates the live sum of each data point
    for i in range(0, len(req["data"]["stations"])):
        sumAvailable += req["data"]["stations"][i]["num_bikes_available"]
        sumEAvailable += req["data"]["stations"][i]["num_ebikes_available"]
        sumDisabled += req["data"]["stations"][i]["num_bikes_disabled"]
        sumDocsAvailable += req["data"]["stations"][i]["num_docks_available"]
        sumDocsDisabled += req["data"]["stations"][i]["num_docks_disabled"]
        sumStationsInstalled += req["data"]["stations"][i]["is_installed"]

    #transfer over to HTML
    return render_template("numbers.html", sumAvailable = sumAvailable, sumEAvailable = sumEAvailable,
            sumDisabled = sumDisabled, sumDocsAvailable = sumDocsAvailable, sumDocsDisabled = sumDocsDisabled,
            sumStationsInstalled = sumStationsInstalled)

if __name__ == "__main__":
    app.run(port=5000, debug=True)