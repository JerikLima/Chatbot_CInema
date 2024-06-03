import requests
class Cinema:
    @staticmethod
    def obter_nome_cinema_por_cidade(nome_cidade):
        url = "https://api-content.ingresso.com/v0/theaters?partnership="
        headers = { 
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
            else:
                print(f"Não foram encontrados cinemas em {nome_cidade}")
        else: 
            print("Não foi possível acessar a api")


    
    @staticmethod
    def obter_id_por_cidade(nome_cidade):
        url = "https://api-content.ingresso.com/v0/theaters?partnership="
        headers = { 
            "Content-Type": "application/json",
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            cinemas = response.json()
            for cinema in cinemas:
                if cinema['cityName'].lower() == nome_cidade.lower():
                    return cinema['cityId']
            print(f"Não foi encontrado cityId para a cidade {nome_cidade}")
        else:
            print("Não foi possível acessar a api")
        return None
    

    @staticmethod
    def obter_id_por_cinema(nome_cinema, city_id):
        url = f"https://api-content.ingresso.com/v0/theaters/city/{city_id}?partnership="
        headers = { 
            "Content-Type": "application/json",
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            teatros = response.json()
            for teatro in teatros:
                if teatro['name'].lower() == nome_cinema.lower():
                    return teatro['id']
        else:
            print("Não foi possivel acessar a api")
        return None
    


    @staticmethod
    def filmes_por_cinema(city_id, theather_id):
     url = f"https://api-content.ingresso.com/v0/sessions/city/{city_id}/theater/{theather_id}?partnership="
     headers = { 
        "Content-Type": "application/json",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
     }
     response = requests.get(url, headers=headers)

     if response.status_code == 200:
        data = response.json()  
        filmes = data[0]['movies']  # Acessar a chave "movies" primeiro
        titulos_filmes = [filme['title'] for filme in filmes] 

        if titulos_filmes:
            print("Filmes disponíveis no cinema escolhido:")
            for titulo in titulos_filmes:
                print(titulo)
        else:
            print("Não foram encontrados filmes disponíveis neste cinema.")
     else:
        print("Não foi possível obter os filmes do cinema.")
