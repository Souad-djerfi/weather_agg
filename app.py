from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import requests
import agregation 

# créer une instance Flask
app = Flask(__name__) 

def formatdate (date):
    date_obj=datetime.fromisoformat(date)
    return date_obj.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
# endpoint temperature et humidity
@app.route('/api/v1/air/temperature')
@app.route('/api/v1/air/humidity')
def get_data():
    # Récupérez les paramètres query
    start = request.args.get('start')
    end = request.args.get('end') or datetime.datetime.utcnow().isoformat() # cas si "end" est ommit,on prend now comme date de fin.)
    longitude = request.args.get('longitude')
    latitude = request.args.get('latitude')
    agg = request.args.get('agg')
    #      
    param=''  
    
    if request.path == '/api/v1/air/temperature':
        param='airTemperature'
    elif request.path == '/api/v1/air/humidity':
        param='humidity'    
        
    # récupérer données météo avec une requête à stormglass.io
    url = f"https://api.stormglass.io/v2/weather/point?lat={latitude}&lng={longitude}&start={start}&end={end}&params={param}"
    # Transformez les données récupérées de stormglass.io en JSON
    headers = {"Authorization": "2b64561c-da39-11ed-bc36-0242ac130002-2b6456c6-da39-11ed-bc36-0242ac130002"} #  clé API stormglass.io
    response = requests.get(url, headers=headers) 
    #selectionner que les données dont on a besoin dans data
    data = [{"ts": formatdate(item["time"]), "value": item[param]["noaa"] } for item in response.json()["hours"]]
     
    # données que notre API renvoie       
    if agg in ("max","min","avg"):
        return jsonify({"data": agregation.agre(agg,start, end,data)})
    return jsonify({'error': 'Invalid agg value'}), 400 
        
  
if __name__ == '__main__':
    app.run(debug=True, port=5000)

