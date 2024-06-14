import json
from rasa.shared.nlu.training_data.message import Message

# Carregar os dados do arquivo JSON
with open("data/cities.json", "r", encoding="utf-8") as file:
    cities_data = json.load(file)

# Criar exemplos de treinamento
training_examples = []

for city_data in cities_data:
    city = city_data["city"]
    message = Message(data={"text": city, "intent": "inform", "entities": [{"start": 0, "end": len(city), "value": city, "entity": "cidade"}]})
    training_examples.append(message)

# Salvar exemplos de treinamento no formato Rasa NLU
training_data = {"rasa_nlu_data": {"common_examples": [example.as_dict() for example in training_examples]}}

with open("data/training_data.json", "w", encoding="utf-8") as file:
    json.dump(training_data, file, ensure_ascii=False, indent=2)
