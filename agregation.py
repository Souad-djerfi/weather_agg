import app
from datetime import datetime, timedelta
from flask import jsonify
import statistics

def agre(type, start, end, data):
    
    #convertir les dates start et end ( UNIX) en  datetime
    data_final=[]
    start_dt=datetime.fromtimestamp(float(start))
    end_dt=datetime.fromtimestamp(float(end)) 

    # tester si l'interval entre start_dt et end_dt > 24 
    if (end_dt-start_dt).total_seconds()/3600 > 24:

    #calculer nombre d'internval de 2h
        nbr_interval=(end_dt - start_dt) // timedelta(hours=2)
        for i in range(nbr_interval) :
            interval_start = start_dt + i * timedelta(hours=2)
            interval_end = interval_start + timedelta(hours=2)
            tmp=[tmp["value"] for tmp in data if interval_start <= datetime.fromisoformat(tmp["ts"][:-1]) <interval_end] #liste de temperature dans l'intervale de 02h
            if not tmp :
                data_agr=0 # dans le cas ou y a pas eu de temperatures relevées dans lAPI meteo dans cette tranche j'ai proposé de donner 0 à l aggregation à revoir avec le responsable
            else : 
                if type=="max":
                    data_agr=max(tmp)
                elif type=="min":
                    data_agr=min(tmp)
                elif type=="avg":
                    data_agr=round(statistics.mean(tmp),2)
                
            data_final.append({
                  'value': data_agr,
                  'ts': app.formatdate(interval_start.isoformat())
                })
        return  data_final  