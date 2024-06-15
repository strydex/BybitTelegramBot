import matplotlib.pyplot as plt  # Импорт matplotlib для создания графиков
import io  # Импорт модуля io для работы с потоками данных

def create_chart(timestamps, prices, ticker):
   # Функция для создания графика цены.
    plt.figure(figsize=(10, 5))  # Создание новой фигуры для графика размером 10x5 дюймов
    plt.plot(timestamps, prices, label=ticker)  # Построение графика с заданными временными метками и ценами
    plt.title(f'Price chart for {ticker}')  # Установка заголовка графика
    plt.xlabel('Time')  # Установка подписи для оси X
    plt.ylabel('Price')  # Установка подписи для оси Y
    plt.legend()  # Добавление легенды на график
    plt.grid(True)  # Включение отображения сетки на графике

    buf = io.BytesIO()  # Создание буфера для хранения изображения в бинарном формате
    plt.savefig(buf, format='png')  # Сохранение графика в буфер в формате PNG
    buf.seek(0)  # Переход к началу буфера
    plt.close()  # Закрыть фигуру, чтобы освободить память
    return buf  # Возврат буфера с изображением