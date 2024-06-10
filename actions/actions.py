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
            dispatcher.utter_message(text=f"Aqui está a lista dos cinemas em {city}: \n", buttons=botoes)
        else:
            dispatcher.utter_message(text="Desculpe, não reconhecemos essa cidade. Você pode tentar outra cidade?")
        
        return [Cinema.obter_id_por_cidade(city)]
    

class ActionProcurarId(Action):

    def name(self) -> Text:
        return "action_salvar_ids"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        movie = tracker.get_slot('cinema')
        city  = tracker.get_slot('cidade')
        city_id = Cinema.obter_id_por_cidade(city)
        movie_id = Cinema.obter_id_por_cinema(movie, city_id)
        dispatcher.utter_message(text = f"Fala meu chapa, se liga nos filmes em cartaz no {movie}:\n")
        dispatcher.utter_message(text = f"{Cinema.filmes_por_cinema(city_id, movie_id)}")
        

    

