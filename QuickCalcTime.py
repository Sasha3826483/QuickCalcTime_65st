import pyautogui as gui
import PIL as pil
import datetime
import os
import pytesseract as tess
import cv2
import mss

# Убедитесь, что pytesseract настроен правильно
tess.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Удаляем файл result.txt, если он существует
if os.path.exists("result.txt"):
    os.remove("result.txt")

# Сделаем скриншот заранее выделенной области экрана
screenshot = gui.screenshot(region=(770, 280, 980, 30))
screenshot.save("screenshot.png")

print("PWD:", os.getcwd())

# С помощью OpenCV Увеличим изображение и преобразуем его в оттенки серого
image = cv2.imread("screenshot.png")
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Увеличим изображение для лучшего распознавания c применением бикубической интерполяции (медленная, но качественная)
image = cv2.resize(image, None, fx=4, fy=4, interpolation=cv2.INTER_CUBIC)

# Сохраним измененное изображение для отладки
#cv2.imwrite("screenshot_resized.png", image)

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
    # Запишем delta_time в файл rusult.txt
    with open("result.txt", "w") as file:
        file.write(f"Time 1: {time1_str}\n")
        file.write(f"Time 2: {time2_str}\n")
        file.write(f"Delta Time: {delta_time}\n")
else:
    print("ERROR: Couldn't find two times")
    with open("result.txt", "w") as file:
        file.write("ERROR: Couldn't find two times")

# Удаляем временный файл скриншота и resized скриншота
if os.path.exists("screenshot.png"):
    os.remove("screenshot.png")
#if os.path.exists("screenshot_resized.png"):
#    os.remove("screenshot_resized.png")
    
#input("Press Enter to exit...")