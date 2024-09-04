import requests
import pandas as pd
import time

class Parser:
    # Ссылка для получения списка книг (960 книг)
    link = 'https://api.litres.ru/foundation/api/genres/5272/arts/facets?is_for_pda=false&limit=960&o=popular&offset=0&show_unavailable=false'
    
    def __init__(self) -> None:
        pass
    
    def request(self):
        response = requests.get(self.link)
        
        if response.status_code == 200:
            data = response.json() 
            return data.get('payload', {}).get('data', [])
        else:
            print(f"Ошибка запроса: {response.status_code}")
            return []

    def fetch_art_info(self, art_id):
        # Запрашиваем основную информацию о книге по ее id
        art_url = f'https://api.litres.ru/foundation/api/arts/{art_id}'
        art_response = requests.get(art_url)
        
        if art_response.status_code == 200:
            art_data = art_response.json().get('payload', {}).get('data', {})
            reviews_count = art_data.get('reviews_count', 0)
            return reviews_count
        else:
            print(f"Ошибка при запросе информации о книге {art_id}: {art_response.status_code}")
            return 0

    def fetch_reviews(self, art_id, reviews_count):
        # Если есть отзывы, делаем запрос для получения самих отзывов с лимитом
        if reviews_count > 0:
            reviews_url = f'https://api.litres.ru/foundation/api/arts/{art_id}/reviews?limit={reviews_count}'
            review_response = requests.get(reviews_url)
            
            if review_response.status_code == 200:
                reviews_data = review_response.json().get('payload', {}).get('data', [])
                reviews = [review.get('text', '') for review in reviews_data]
                return reviews
            else:
                print(f"Ошибка при запросе отзывов для книги {art_id}: {review_response.status_code}")
                return []
        else:
            return []

    def parse(self):
        books = self.request()
        parsed_books = []

        for book in books:
            art_id = book.get('id')
            
            # Запрашиваем количество отзывов
            time.sleep(1)
            review_count = self.fetch_art_info(art_id)
            time.sleep(1)
            
            # Запрашиваем сами отзывы, если они есть
            reviews = self.fetch_reviews(art_id, review_count)

            book_data = {
                "name": book.get('title'),
                "author": self.get_author(book.get('persons', [])),
                "link": f"https://www.litres.ru{book.get('url')}",
                "rating": book.get('rating', {}).get('rated_avg', 0),
                "rating_count": book.get('rating', {}).get('rated_total_count', 0),
                "review_count": review_count,
                "pages_count": book.get('symbols_count'),
                "price": book.get('prices', {}).get('final_price', 0),
                "text_reviews": reviews,
                "age": book.get('min_age'),
                "year": book.get('date_written_at', '').split('-')[0] if book.get('date_written_at') else None
            }
            parsed_books.append(book_data)

        return parsed_books

    @staticmethod
    def get_author(persons):
        for person in persons:
            if person.get('role') == 'author':
                return person.get('full_name')
        return "Неизвестный автор"

# Использование парсера
parser = Parser()
books_data = parser.parse()

# Создание DataFrame и сохранение в CSV
books_df = pd.DataFrame(books_data)
csv_file_path = './litres_books_with_reviews.csv'
books_df.to_csv(csv_file_path, index=False)
