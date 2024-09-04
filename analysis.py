import pandas as pd
import matplotlib.pyplot as plt

# Загрузка данных из файла CSV после обновленного парсинга
csv_file_path = './litres_books_with_reviews.csv'

# Чтение данных из CSV
df = pd.read_csv(csv_file_path)

# Первые 5 строк датасета и размер датасета
first_five_rows = df.head(5)
dataset_shape = df.shape
print("Первые 5 строчек:", first_five_rows)
print("Размер датасета:", dataset_shape)

# Проверка пропусков в данных
missing_data = df.isnull().sum()
print("Пропуски в данных:", missing_data)

# Проверка типов данных
data_types = df.dtypes
print("Типы данных:", data_types)

# Описательная статистика
median_price = df['price'].median()
most_common_age = df['age'].mode()[0]
average_reviews = df['review_count'].mean()
books_below_425 = df[df['rating'] < 4.25].shape[0]
most_common_year = df['year'].mode()[0]
print("Медианная цена книг:", median_price)
print("Чаще всего встречающееся возрастное ограничение:", most_common_age)
print("Среднее число отзывов в книге:", average_reviews)
print("Книг с рейтингом ниже 4.25:", books_below_425)
print("Год, в котором было написано больше всего книг:", most_common_year)

# Добавление нового поля 'is_popular': 1 если рейтинг >= 4.6 и >= 5 отзывов
df['is_popular'] = ((df['rating'] >= 4.6) & (df['rating_count'] >= 5)).astype(int)

# Среднее количество страниц среди популярных и непопулярных книг
popular_books_avg_pages = df[df['is_popular'] == 1]['pages_count'].mean()
non_popular_books_avg_pages = df[df['is_popular'] == 0]['pages_count'].mean()
print(f"Среднее число страниц среди популярных книг: {popular_books_avg_pages}")
print(f"Среднее число страниц среди непопулярных книг: {non_popular_books_avg_pages}")

# Топ-10 книг по числу отзывов
top_10_books_by_reviews = df.nlargest(10, 'review_count')[['name', 'author', 'review_count']]
print("Топ-10 книг по числу отзывов:", top_10_books_by_reviews)

# Средняя длина отзыва (в символах)
df['avg_review_length'] = df['text_reviews'].apply(lambda x: sum([len(str(review)) for review in eval(x)]) / len(eval(x)) if x and eval(x) else 0)
average_review_length = df['avg_review_length'].mean()
print("Средняя длина отзыва (в символах):", average_review_length)

# Таблица корреляций числовых переменных
correlation_table = df.corr(numeric_only=True)
print("Таблица корреляций числовых переменных:", correlation_table)

# Построение диаграммы рассеяния количества страниц и количества отзывов
plt.figure(figsize=(10, 6))
plt.scatter(df['pages_count'], df['rating_count'], alpha=0.5)
plt.title('Количество страниц vs Количество отзывов')
plt.xlabel('Количество страниц')
plt.ylabel('Количество отзывов')
plt.grid(True)
scatterplot_path = './диаграмма_рассеяния_страницы_отзывы.png'
plt.savefig(scatterplot_path)
plt.show()

# Линейный график количества книг по годам
books_per_year = df.groupby('year').size()
plt.figure(figsize=(10, 6))
books_per_year.plot(kind='line')
plt.title('Количество книг по годам')
plt.xlabel('Год')
plt.ylabel('Количество книг')
plt.grid(True)
lineplot_years_path = './линейный_график_книги_годы.png'
plt.savefig(lineplot_years_path)
plt.show()

# Гистограмма распределения рейтингов книг
plt.figure(figsize=(10, 6))
plt.hist(df['rating'], bins=20, color='blue', alpha=0.7)
plt.title('Распределение рейтингов книг')
plt.xlabel('Рейтинг')
plt.ylabel('Частота')
plt.grid(True)
hist_rating_path = './гистограмма_рейтинги.png'
plt.savefig(hist_rating_path)
plt.show()

# Гистограмма распределения цен книг
plt.figure(figsize=(10, 6))
plt.hist(df['price'].dropna(), bins=20, color='green', alpha=0.7)
plt.title('Распределение цен книг')
plt.xlabel('Цена (RUB)')
plt.ylabel('Частота')
plt.grid(True)
hist_price_path = './гистограмма_цены.png'
plt.savefig(hist_price_path)
plt.show()
