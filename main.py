import datetime

class User:
    def __init__(self, username, password):
        # Конструктор класу User, що ініціалізує нового користувача з ім'ям та паролем
        # Також створює порожній список бронювань для користувача
        self.username = username
        self.password = password
        self.bookings = []

    def add_booking(self, booking):
        # Метод для додавання нового бронювання до списку бронювань користувача
        self.bookings.append(booking)

    def cancel_booking(self, booking_id):
        # Метод для скасування бронювання на основі ID
        # Проходить по списку бронювань, шукає бронювання з заданим ID, і видаляє його
        for i, booking in enumerate(self.bookings):
            if booking.id == booking_id:
                del self.bookings[i]
                return True
        return False  # Якщо бронювання з таким ID не знайдено, повертає False

    def show_bookings(self):
        # Метод для виведення списку всіх бронювань користувача
        if not self.bookings:
            print("У вас немає заброньованих квитків.")  # Якщо список бронювань порожній
        else:
            for booking in self.bookings:
                print(booking)  # Виведення кожного бронювання

    def update_password(self, new_password):
        # Метод для оновлення пароля користувача
        self.password = new_password
        print("Пароль успішно оновлено.")  # Повідомлення про успішне оновлення пароля
class Booking:
    booking_id_counter = 1  # Статичний лічильник, який використовується для присвоєння унікальних ID кожному бронюванню

    def __init__(self, user, destination, date, time, coach, seat):
        # Конструктор класу Booking, який ініціалізує нове бронювання із вказаними параметрами
        self.id = Booking.booking_id_counter  # Ініціалізація ID бронювання з поточним значенням лічильника
        Booking.booking_id_counter += 1  # Інкремент лічильника ID для наступного бронювання
        self.user = user  # Зберігає об'єкт користувача, який здійснив бронювання
        self.destination = destination  # Зберігає напрямок поїздки
        self.date = date  # Зберігає дату поїздки
        self.time = time  # Зберігає час відправлення
        self.coach = coach  # Зберігає номер вагона
        self.seat = seat  # Зберігає номер місця у вагоні

    def __str__(self):
        # Метод для визначення строкового представлення об'єкта
        # Вивід інформації про бронювання у зрозумілій формі
        return f"Бронювання ID: {self.id}, Напрямок: {self.destination}, Дата: {self.date}, Час: {self.time}, Вагон: {self.coach}, Місце: {self.seat}"
class TicketSystem:
    def __init__(self):
        # Ініціалізація системи квитків
        self.users = {}  # Словник для зберігання користувачів системи, ключем є ім'я користувача
        self.available_tickets = {
            # Словник, що зберігає інформацію про доступні квитки на різні маршрути, дати та часи
            ('Київ', 'Одеса'): {
                '25.12.2021': {
                    '12:00': {'1': ['1A', '1B', '1C'], '2': ['2A', '2B', '2C']},
                    '18:00': {'1': ['1A', '1B'], '2': ['2A', '2B']}
                }
            },
            ('Львів', 'Київ'): {
                '25.12.2021': {
                    '10:00': {'1': ['1A', '1B', '1C'], '2': ['2A', '2B', '2C']},
                    '16:00': {'1': ['1A', '1B'], '2': ['2A', '2B']}
                }
            }
            # Додаткові маршрути можуть бути додані аналогічно
        }
        self.logs = []  # Список для зберігання логів дій в системі

    def register_user(self, username, password):
        # Реєстрація нового користувача в системі
        if username in self.users:
            print("Користувач з таким іменем вже існує.")
            return False  # Якщо користувач з таким іменем вже є, повертаємо False
        self.users[username] = User(username, password)  # Створення нового користувача та додавання його до словника
        print("Реєстрація успішна.")
        return True  # Успішна реєстрація користувача

    def login_user(self, username, password):
        # Перевірка входу користувача в систему
        if username in self.users and self.users[username].password == password:
            print("Вхід в систему успішний.")
            return self.users[username]  # Повертаємо об'єкт користувача при успішному вході
        print("Неправильне ім'я користувача або пароль.")
        return None  # Повертаємо None, якщо ім'я користувача або пароль не співпадають

    def check_availability(self, start, destination, date, time, coach, seat):
        # Метод для перевірки доступності місця для конкретного рейсу за заданими параметрами.
        if (start, destination) in self.available_tickets:
            # Перевірка чи існує такий маршрут в системі
            journey_data = self.available_tickets[(start, destination)]
            if date in journey_data:
                # Перевірка чи доступна задана дата для рейсу
                if time in journey_data[date]:
                    # Перевірка чи існує вказаний час виїзду в цю дату
                    if coach in journey_data[date][time]:
                        # Перевірка чи є доступний вказаний вагон
                        if seat in journey_data[date][time][coach]:
                            # Перевірка чи місце доступне для бронювання
                            return True  # Місце доступне для бронювання
        return False  # Місце не доступне

    def book_ticket(self, user, start, destination, date, time, coach, seat):
        # Метод для бронювання квитка, якщо він доступний
        if self.check_availability(start, destination, date, time, coach, seat):
            # Спочатку перевіряємо, чи доступне місце
            booking = Booking(user, destination, date, time, coach, seat)
            # Створюємо нове бронювання
            user.add_booking(booking)
            # Додаємо бронювання до списку бронювань користувача
            self.available_tickets[(start, destination)][date][time][coach].remove(seat)
            # Видаляємо місце з доступних, оскільки воно тепер заброньоване
            self.logs.append(f"Booked: {booking}")
            # Додаємо запис до логів про здійснене бронювання
            print(
                f"Квиток з {start} до {destination} на {date} о {time}, вагон {coach}, місце {seat} успішно заброньовано.")
            return booking
        else:
            print("На жаль, квиток на вказану дату, час, вагон або місце недоступний.")
            return None
            # Якщо місце не доступне, повідомляємо користувача про неможливість бронювання

    def cancel_ticket(self, user, booking_id):
        # Метод для скасування бронювання, якщо воно було зроблене
        if user.cancel_booking(booking_id):
            # Якщо скасування бронювання успішне, повідомляємо про це
            self.logs.append(f"Cancelled: Booking ID {booking_id}")
            # Додаємо запис до логів про скасування бронювання
            print(f"Бронювання ID {booking_id} відмінено.")
        else:
            print("Бронювання не знайдено.")
            # Якщо бронювання з вказаним ID не знайдено, повідомляємо про помилку

    def show_available_tickets(self):
        # Відображення списку усіх доступних квитків
        print("Доступні квитки:")
        for (start, destination), dates in self.available_tickets.items():
            # Прохід по всім маршрутам
            for date, times in dates.items():
                # Прохід по всім датам для кожного маршруту
                for time, coaches in times.items():
                    # Прохід по всіх часах відправлення для кожної дати
                    for coach, seats in coaches.items():
                        # Отримання інформації про доступні місця в кожному вагоні
                        print(
                            f"З {start} до {destination} дата {date} о {time} Вагон {coach}: Місця: {' '.join(seats)}")

    def find_routes_with_transfers(self, start, end, date):
        # Пошук маршрутів з пересадками
        results = []
        intermediate_stops = []
        # Збір інформації про доступні маршрути від початкової точки
        for (start_point, inter_point), schedules in self.available_tickets.items():
            if start_point == start and date in schedules:
                intermediate_stops.append(inter_point)
        # Перевірка можливості доїхати до кінцевої точки з проміжних зупинок
        for inter in intermediate_stops:
            for (inter_point, end_point), schedules in self.available_tickets.items():
                if inter_point == inter and end_point == end and date in schedules:
                    results.append((start, inter, end, date))
        return results

    def route_exists(self, start, end, date):
        # Перевіряє, чи існує маршрут між вказаними пунктами відправлення та прибуття на певну дату
        route_key = (start, end)
        return route_key in self.available_tickets and date in self.available_tickets[route_key]

    def show_segment_availability(self, start, destination, date):
        # Виводить інформацію про наявність місць для конкретного сегмента шляху на вказану дату
        route_key = (start, destination)
        if route_key in self.available_tickets and date in self.available_tickets[route_key]:
            print(f"Доступні місця з {start} до {destination} на {date}:")
            for time, coaches in self.available_tickets[route_key][date].items():
                for coach, seats in coaches.items():
                    print(f"О {time} Вагон {coach}: Місця: {' '.join(seats)}")
        else:
            print(f"Немає доступних рейсів з {start} до {destination} на {date}.")

    def book_multiple_segments(self, user, segments):
        # Бронювання декількох сегментів подорожі одразу
        for segment in segments:
            start, destination, date, time, coach, seat = segment
            if self.check_availability(start, destination, date, time, coach, seat):
                self.book_ticket(user, start, destination, date, time, coach, seat)
                # Бронює кожен сегмент, якщо він доступний
            else:
                print(f"Не вдалося забронювати місце на сегменті з {start} до {destination} на {date} о {time}.")
                return False
                # Якщо хоча б один сегмент неможливо забронювати, процес зупиняється
        print("Усі сегменти успішно заброньовані.")
        return True

    def parse_date(self, date_str):
        # Конвертує рядкове представлення дати у форматі "dd.mm.yyyy" в об'єкт datetime
        return datetime.datetime.strptime(date_str, "%d.%m.%Y")

    def format_date(self, date):
        # Форматує об'єкт datetime у рядок за шаблоном "dd.mm.yyyy"
        return date.strftime("%d.%m.%Y")

    def find_alternative_dates(self, start, destination, input_date, days_range=3):
        # Пошук альтернативних дат для поїздки в заданий інтервал днів від вказаної дати
        input_date_dt = self.parse_date(input_date)  # Перетворюємо рядок дати в об'єкт datetime
        alternatives = []

        # Перевіряємо дати в діапазоні +/- days_range днів від заданої дати
        for delta in range(-days_range, days_range + 1):
            if delta == 0:
                continue  # Пропускаємо вихідну дату
            new_date = input_date_dt + datetime.timedelta(days=delta)  # Визначаємо нову дату
            new_date_str = self.format_date(new_date)  # Форматуємо нову дату у рядковий формат
            if self.route_exists(start, destination, new_date_str):
                alternatives.append(new_date_str)  # Додаємо дату до списку альтернатив, якщо маршрут існує
        return alternatives

    def interactive_ticket_booking(self, user):
        # Інтерактивне бронювання квитків з виводом варіантів у випадку відсутності прямого маршруту
        print("Ласкаво просимо до системи бронювання квитків!")
        start = input("Звідки ви бажаєте виїхати? ")
        destination = input("Куди ви бажаєте поїхати? ")
        date = input("На яку дату? (формат: дд.мм.рррр) ")

        if not self.route_exists(start, destination, date):
            print("Прямі квитки з даного міста на дану дату недоступні.")
            possible_routes = self.find_routes_with_transfers(start, destination, date)
            if possible_routes:
                print("Можливі маршрути з пересадками:")
                for route in possible_routes:
                    print(f"Маршрут через {route[1]} з доступністю:")
                    self.show_segment_availability(route[0], route[1], date)
                    self.show_segment_availability(route[1], route[2], date)

                    response = input("Бажаєте забронювати цей маршрут? (так/ні) ")
                    if response.lower() == "так":
                        segments = []
                        for i in [0, 1]:  # Для кожного сегмента маршруту збираємо інформацію для бронювання
                            time = input(f"Введіть час відправлення для сегмента з {route[i]} до {route[i + 1]}: ")
                            coach = input(f"Введіть номер вагону: ")
                            seat = input(f"Введіть номер місця: ")
                            segments.append((route[i], route[i + 1], date, time, coach, seat))
                        self.book_multiple_segments(user, segments)
                # Якщо прямий маршрут відсутній, запитуємо користувача про бажання забронювати маршрут з пересадками
            else:
                print("Маршрути з пересадками також недоступні.")
                alternative_dates = self.find_alternative_dates(start, destination, date)
                if alternative_dates:
                    print("Альтернативні дати для вашого маршруту:")
                    for alt_date in alternative_dates:
                        print(alt_date)
                    alt_date_choice = input("Бажаєте забронювати квиток на одну з альтернативних дат? (так/ні) ")
                    if alt_date_choice.lower() == 'так':
                        alt_date_selected = input("Оберіть дату для бронювання (формат: дд.мм.рррр): ")
                        time = input("На який час? (формат: гг:хх) ")
                        coach = input("Введіть номер вагону: ")
                        seat = input("Введіть номер місця: ")
                        self.book_ticket(user, start, destination, alt_date_selected, time, coach, seat)
                    # Якщо маршрути з пересадками недоступні, надаємо користувачу інформацію про альтернативні дати
                else:
                    print("Немає доступних альтернативних дат.")
        else:
            time = input("На який час? (формат: гг:хх) ")  # Збираємо інформацію про час відправлення
            coach = input("Введіть номер вагону: ")  # Збираємо інформацію про номер вагону
            seat = input("Введіть номер місця: ")  # Збираємо інформацію про номер місця
            self.book_ticket(user, start, destination, date, time, coach, seat)  # Бронюємо квиток

def main():
    system = TicketSystem()
    while True:
        print("\n1. Реєстрація\n2. Вхід\n3. Вийти")
        choice = input("Оберіть опцію: ")
        if choice == '1':
            username = input("Введіть ім'я користувача: ")
            password = input("Введіть пароль: ")
            system.register_user(username, password)
        elif choice == '2':
            username = input("Введіть ім'я користувача: ")
            password = input("Введіть пароль: ")
            user = system.login_user(username, password)
            if user:
                while True:
                    print("\n1. Бронювання квитка\n2. Показати мої квитки\n3. Скасувати квиток\n4. Змінити пароль\n5. Показати доступні квитки\n6. Вихід")
                    user_choice = input("Оберіть опцію: ")
                    if user_choice == '1':
                        system.interactive_ticket_booking(user)
                    elif user_choice == '2':
                        user.show_bookings()
                    elif user_choice == '3':
                        booking_id = int(input("Введіть ID бронювання для скасування: "))
                        system.cancel_ticket(user, booking_id)
                    elif user_choice == '4':
                        new_password = input("Введіть новий пароль: ")
                        user.update_password(new_password)
                    elif user_choice == '5':
                        system.show_available_tickets()
                    elif user_choice == '6':
                        break
        elif choice == '3':
            break

if __name__ == "__main__":
    main()