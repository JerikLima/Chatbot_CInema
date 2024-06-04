from cinemapercity import Cinema

nome_cidade = input("Digite a cidade que você procura cinema: \n ")
Cinema.obter_nome_cinema_por_cidade(nome_cidade)
city_id = Cinema.obter_id_por_cidade(nome_cidade)
nome_cinema = input("Digite qual dos cinemas você gostaria de ir: \n")
theather_id = Cinema.obter_id_por_cinema(nome_cinema, city_id)
Cinema.filmes_por_cinema(city_id, theather_id)
