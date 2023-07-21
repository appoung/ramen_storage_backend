from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)
CORS(app, methods=["GET", "POST"])
CORS(app, origins="http://localhost:3000")

DATA_FILE = "ramen_data.json"  # File to store the Ramen data

# Load Ramen data from file on server startup
try:
    with open(DATA_FILE, "r") as file:
        ramendata = json.load(file)
except FileNotFoundError:
    ramendata = []


@app.route('/api/ramens', methods=['GET', 'POST'])
def ramens():
    global ramendata

    if request.method == 'POST':
        data = request.get_json()
        for ramen in data["ramens"]:
            name = ramen['name']
            count = ramen['count']
            ramendata = [ramen for ramen in ramendata if ramen["name"] in [
                r["name"] for r in data["ramens"]]]
            existing_ramen = next(
                (item for item in ramendata if item["name"] == name), None)

            if existing_ramen:
                existing_ramen["count"] = count
            else:
                ramendata.append({"name": name, "count": count})

        # Save Ramen data to file
        with open(DATA_FILE, "w") as file:
            json.dump(ramendata, file)

        return jsonify({"ramens": ramendata})

    elif request.method == 'GET':
        return jsonify({"ramens": ramendata})


if __name__ == "__main__":
    app.run(debug=True)
