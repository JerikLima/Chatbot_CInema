import json
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from typing import Any, Text, Dict, List

class ActionSaveCity(Action):

    def name(self) -> Text:
        return "action_save_city"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Captura a entidade cidade
        city_entity = next(tracker.get_latest_entity_values("cidade"), None)
        
        if city_entity:
            dispatcher.utter_message(text=f"Você quer cinema de {city_entity}, correto?")
            # Salva a cidade em uma variável (slot)
            return [SlotSet("cidade", city_entity)]
        else:
            dispatcher.utter_message(text="Desculpe, não consegui identificar a cidade mencionada.")
            return []

class ActionProcurarCidade(Action):

    def name(self) -> Text:
        return "action_procurar_cidade"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        city = tracker.get_slot('cidade')
        
        if not city:
            dispatcher.utter_message(text="Por favor, mencione uma cidade.")
            return []

        with open('data/cities.json', 'r', encoding='utf-8') as f:
            cities_data = json.load(f)
        
        cities = [entry['city'].lower() for entry in cities_data]

        if city.lower() in cities:
            dispatcher.utter_message(text=f"A cidade {city} foi encontrada.")
        else:
            dispatcher.utter_message(text="Desculpe, não reconhecemos essa cidade. Você pode tentar outra cidade?")
        
        return []
