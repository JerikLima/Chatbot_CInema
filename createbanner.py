import concurrent.futures
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import requests
import base64

def fetch_image(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return Image.open(BytesIO(response.content))
        else:
            print(f"Failed to fetch image from {url}. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching image from {url}: {str(e)}")
        return None


def create_movies_image(movies):
    posters = []
    titles = []
    all_sessions = []

    # Baixar as imagens dos posters em paralelo
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_url = {executor.submit(fetch_image, movie['poster_url']): movie for movie in movies}
        for future in concurrent.futures.as_completed(future_to_url):
            movie = future_to_url[future]
            img = future.result()
            img = img.resize((1200, 1500))  # Redimensionar os posters
            posters.append(img)
            titles.append(movie['title'])
            all_sessions.append(" ".join(movie['sessions']))

    # Definir algumas configurações básicas
    num_movies = len(movies)
    poster_width, poster_height = posters[0].size

    # Espaçamentos configuráveis
    padding_left = 500  # Espaço à esquerda da imagem
    padding_top = 80   # Espaço acima do primeiro filme
    padding_between_poster = 1400  # Espaço entre os posters
    padding_between_row = 250   # Espaço entre as linhas de filmes
    padding_title_poster = -750   # Espaço vertical entre o título e o poster (ajustado)
    padding_session_poster = 150   # Espaço vertical entre os horários e o poster

    # Tamanhos das fontes
    font_size_title = 150
    font_size_session = 150

    # Carregar a fonte padrão uma vez
    font_title = ImageFont.truetype("fonts/ARIALBD.TTF", font_size_title)
    font_session = ImageFont.truetype("fonts/ARIALBI.TTF", font_size_session)

    # Calcular o tamanho da imagem final dinamicamente
    max_columns = 5
    rows = (num_movies - 1) // max_columns + 1
    total_width = (poster_width + padding_between_poster) * max_columns + 2 * padding_left
    total_height = padding_top + rows * (poster_height + font_size_title * 2 + padding_between_poster + font_size_session + padding_between_row)

    # Criar uma nova imagem
    final_image = Image.new('RGB', (total_width, total_height), color=(22, 2, 84))
    draw = ImageDraw.Draw(final_image)

    # Adicionar os posters, títulos e horários na imagem final
    x_offset = padding_left
    y_offset = padding_top
    for i in range(num_movies):
        # Adicionar título acima do poster
        title_bbox = draw.textbbox((0, 0), titles[i], font=font_title)
        title_width, title_height = title_bbox[2] - title_bbox[0], title_bbox[3] - title_bbox[1]
        title_x = x_offset + (poster_width - title_width) // 2  # Centralizar o título em relação ao pôster
        title_y = y_offset + poster_height + padding_title_poster  # Ajuste para alinhar próximo ao poster
        draw.text((title_x, title_y), titles[i], font=font_title, fill=(255, 255, 255))

        # Adicionar poster
        poster_y = y_offset + title_height + padding_between_poster
        final_image.paste(posters[i], (x_offset, poster_y))

        # Calcular a largura total dos horários
        total_sessions_width = sum(draw.textlength(session + " ", font=font_session) for session in all_sessions[i].split()) + 10 * (len(all_sessions[i].split()) - 1)

        # Adicionar horários abaixo do poster
        sessions_y = poster_y + poster_height + padding_session_poster  # Espaço entre os horários e o poster
        session_x = x_offset + (poster_width - total_sessions_width) // 2  # Centralizar os horários em relação ao pôster
        for session in all_sessions[i].split():
            session_text = session + " "
            draw.text((session_x, sessions_y), session_text, font=font_session, fill=(255, 255, 255))
            session_x += draw.textlength(session_text, font=font_session) + 10  # Espaçamento entre os horários

        # Atualizar x_offset e y_offset para o próximo filme
        x_offset += poster_width + padding_between_poster
        if (i + 1) % max_columns == 0:
            x_offset = padding_left
            y_offset += poster_height + font_size_title * 2 + padding_between_poster + font_size_session + padding_between_row

    # Converter a imagem para base64
    buffered = BytesIO()
    final_image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

    return img_str

