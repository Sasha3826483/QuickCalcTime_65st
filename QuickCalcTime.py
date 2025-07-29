import pyautogui as gui
import PIL as pil
import datetime
import os
import pytesseract as tess

# Убедитесь, что pytesseract настроен правильно
tess.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Сделаем скриншот заранее выделенной области экрана
screenshot = gui.screenshot(region=(870, 280, 1770, 330))
screenshot.save("screenshot.png")

# Преобразуем изображение в формат, который может быть обработан pytesseract
image = pil.Image.open("Screenshot.png") #("screenshot.png")

# Используем pytesseract для извлечения всех цифри и : из изображения
extracted_text = tess.image_to_string(image, config='--psm 6 -c tessedit_char_whitelist="0123456789:"')

# Разделим извлеченный текст на строки
lines = extracted_text.split('\n')

# Ищем строки, содержащие ровно два времени в формате MM:SS:FF
times = []
for line in lines:
    # Разделяем строку на части по пробелам
    parts = line.split()
    # Фильтруем части, оставляя только те, которые соответствуют формату MM:SS:FF
    valid_times = [part for part in parts if len(part) == 8 and part.count(':') == 2]
    for valid_time in valid_times:
        print("Valid time found:", valid_time)
    # Если нашли ровно два времени, добавляем их в список times
    if len(valid_times) == 2:
        times.extend(valid_times)

# Если найдено два времени, преобразуем их в timedelta
if len(times) == 2:
    time1_str, time2_str = times[0].strip(), times[1].strip()
    # Преобразуем строки времени в timedelta
    time1 = datetime.datetime.strptime(time1_str, '%M:%S:%f')
    time2 = datetime.datetime.strptime(time2_str, '%M:%S:%f')
    delta_time = time2 - time1
    print(f"Delta Time: {delta_time}")
else:
    print("Не удалось найти два времени в извлеченном тексте.")

# Удаляем временный файл скриншота
if os.path.exists("screenshot.png"):
    os.remove("screenshot.png")