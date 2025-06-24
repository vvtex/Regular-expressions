import csv
import re


def format_phone(phone):
    """Приводит телефон к формату +7(999)999-99-99 с учётом добавочного номера"""
    if not phone:
        return ''

    phone = phone.strip()
    # Извлечение всех цифр из номера
    digits = re.sub(r'\D', '', phone)

    # Поиск добавочного номера
    ext_match = re.search(r'(?:доб|доб\.)\D*(\d+)', phone, re.IGNORECASE)
    ext = f" доб.{ext_match.group(1)}" if ext_match else ''

    # Обработка основного номера (10 или 11 цифр)
    if len(digits) == 11:
        digits = '7' + digits[1:]  # Нормализация 8XXX к 7XXX
    elif len(digits) == 10:
        digits = '7' + digits

    # Форматирование основного номера
    if len(digits) == 11:
        formatted = f"+7({digits[1:4]}){digits[4:7]}-{digits[7:9]}-{digits[9:11]}"
        return formatted + ext
    return phone  # Возврат исходного, если не удалось обработать


# Чтение исходных данных
with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

# Словарь для объединения записей (ключ: (lastname, firstname))
merged_dict = {}

# Обработка каждой записи (кроме заголовка)
for record in contacts_list[1:]:
    # Нормализация ФИО
    full_name = ' '.join(record[:3]).split()
    record[0] = full_name[0] if len(full_name) > 0 else ''
    record[1] = full_name[1] if len(full_name) > 1 else ''
    record[2] = full_name[2] if len(full_name) > 2 else ''

    # Форматирование телефона
    record[5] = format_phone(record[5])

    # Ключ для объединения: фамилия + имя
    key = (record[0], record[1])

    # Объединение дублирующихся записей
    if key in merged_dict:
        existing = merged_dict[key]
        for i in range(2, 7):  # Поля: surname, org, position, phone, email
            if not existing[i] and record[i]:
                existing[i] = record[i]
    else:
        merged_dict[key] = record

# Формирование итогового списка (включая заголовок)
result_list = [contacts_list[0]] + list(merged_dict.values())

# Запись результата в файл
with open("phonebook.csv", "w", encoding="utf-8") as f:
    writer = csv.writer(f, delimiter=',')
    writer.writerows(result_list)