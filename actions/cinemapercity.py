import requests

class Cinema:

 def obter_nome_cinema_por_cidade(nome_cidade):
     url = "https://api-content.ingresso.com/v0/theaters?partnership="
     headers={ 
        "Content-Type": "application/json",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
     response = requests.get(url, headers=headers)
     print(response)

     if response.status_code == 200:
        cinemas = response.json()
        cinemas_da_cidade = [cinema['name'] for cinema in cinemas if cinema['cityName'].lower() == nome_cidade.lower()]

        if cinemas_da_cidade:
            print(f"cinemas em {nome_cidade}:")
            for cinema in cinemas_da_cidade:
                print(cinema)
        else: print(f"Não foram encontrados cinemas em {nome_cidade}")
     else: 
        print("Não foi possível acessar a api")

 nome_cidade = input("Digite a cidade que você procura cinema:")
 obter_nome_cinema_por_cidade(nome_cidade)
 