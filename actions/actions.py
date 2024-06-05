from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

# importação para SlotSet 
from rasa_sdk.events import SlotSet

class ActionSaveCity(Action):

    def name(self) -> Text:
        return "action_save_city"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Captura a entidade cidade
        city_entity = next(tracker.get_latest_entity_values("cidade"), None)
        
        if city_entity:
            # Salva a cidade em uma variável (slot)
            return [SlotSet("cidade", city_entity)]
        else:
            dispatcher.utter_message(text="Desculpe, não consegui identificar a cidade mencionada.")
            return []

