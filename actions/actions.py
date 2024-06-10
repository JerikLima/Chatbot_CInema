import json
import unidecode
from cinemapercity import Cinema
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from typing import Any, Text, Dict, List


class ActionProcurarCidade(Action):

    def name(self) -> Text:
        return "action_procurar_cidade"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        city = tracker.get_slot('cidade')
        if not city:
            dispatcher.utter_message(text="Não foram encontrados cinemas nesse local")
            return []

        with open('data/cities.json', 'r', encoding='utf-8') as f:
            cities_data = json.load(f)
        cities = [unidecode.unidecode(entry['city'].lower()) for entry in cities_data]
        if unidecode.unidecode(city).lower() in cities:
            cinemas = Cinema.obter_nome_cinema_por_cidade(city)
            botoes = [{"title": cinema, "payload": f"/escolher_cinema{{\"cinema\":\"{cinema}\"}}"} for cinema in cinemas]
            dispatcher.utter_message(text=f"Os cinemas em {city} são:", buttons=botoes)
        else:
            dispatcher.utter_message(text="Desculpe, não reconhecemos essa cidade. Você pode tentar outra cidade?")
        
        return []
    

