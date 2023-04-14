from flask import Flask, request, jsonify
import requests 
import datetime

# créer une instance Flask
app = Flask(__name__) 

# endpoint temperature et humidity
@app.route('/api/v1/air/temperature')
@app.route('/api/v1/air/humidity')
def get_data():
    # Récupérez les paramètres query
    start = request.args.get('start')
    end = request.args.get('end') or datetime.datetime.utcnow().isoformat()
    longitude = request.args.get('longitude')
    latitude = request.args.get('latitude')
    agg = request.args.get('agg')
    
    if request.path == '/api/v1/air/temperature':
        # récupérer données météo avec une requête à stormglass.io
        url = f"https://api.stormglass.io/v2/weather/point?lat={latitude}&lng={longitude}&start={start}&end={end}&params=airTemperature"
        
    elif request.path == '/api/v1/air/humidity':   
        url = f"https://api.stormglass.io/v2/weather/point?lat={latitude}&lng={longitude}&start={start}&end={end}&params=humidity" 
        
    headers = {"Authorization": "2b64561c-da39-11ed-bc36-0242ac130002-2b6456c6-da39-11ed-bc36-0242ac130002"} #  clé API stormglass.io
    response = requests.get(url, headers=headers)
        
    print("coucoucoucoucocuo", response.json().keys())
    print("alllllllllllllllllllllllllllllllllaaa", response.json())
    
    # Transformez les données récupérées de stormglass.io en JSON 
    data = [{"ts": item["time"], "value": item["airTemperature"]["noaa"] } for item in response.json()["hours"]]
    
    #données à renvoyer
    data_final =[] 
    
    #agg =min
    if agg=="min" :
        temp_min=min([tmp["value"] for tmp in data]) # récupérer la température minimale 
        data_final=[val for val in data if val["value"]==temp_min]
        print(data_final)
        pass
    # agg=max
    elif agg=="max":
        temp_min=max([tmp["value"] for tmp in data]) # récupérer la température maximale 
        data_final=[val for val in data if val["value"]==temp_min]
        print(data_final)
        pass    
    # agg= avg
    elif agg=="avg":
        
        pass
    # erreur si agg n'est pas valide
    else:
        return jsonify({'error': 'Invalid agg value'}), 400
        
    return jsonify({"data": data_final})


if __name__ == '__main__':
    app.run(debug=True, port=5000)

