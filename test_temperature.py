import unittest
import requests

"""créer une classe qui hérite de unittest.TestCase. 
       Cette classe contient des méthodes de test qui effectuent des assertions 
       pour vérifier que le comportement du code est conforme aux attentes
    """

class TestTemperatureAPI(unittest.TestCase):
    
    base_url = 'http://localhost:5000//api/v1/air/temperature'
    """_summary_
    """
    
    def test_temperature_with_valid_params(self):
        params = {
            'start': '1611400000',
            'end': '1618506400',
            'latitude': 48.8566,
            'longitude': 2.3522,
            'agg': 'avg'
        }
        response = requests.get(self.base_url, params=params) # envoyer une requete GET à notre API et récupérer la reponse
        self.assertEqual(response.status_code, 200) #vérifier que le code de statut de la réponse de l'API est égal à 200 (réponse HTTP réussie)
        self.assertTrue('data' in response.json()) #vérifier si la clé "data" existe dans le dictionnaire renvoyé par la requête en testant si elle est présente dans le contenu JSON de la réponse. Si la clé existe, le test réussit, sinon le test échoue.
        
    def test_temperature_with_invalid_params(self):
        params = {
            'start': 'invalid_date_format',
            'end': 'invalid_date_format',
            'latitude': 'invalid_latitude',
            'longitude': 'invalid_longitude',
            'agg': 'invalid_agg_type'
        }
        response = requests.get(self.base_url, params=params)
        self.assertEqual(response.status_code, 400)
        self.assertTrue('error' in response.json())
