import easyocr
import cv2
import re

reader = easyocr.Reader(['en']) # this needs to run only once to load the model into memory

FORBIDDEN_RE = re.compile(r'[!@#$%^&*()\[\]{};:\'\"<>,./?~\\|+\-=]')

for i in range(10):
    print(i+1)
    file = f'/home/tym/projects/test_task/sample_data/{i + 1}.jpeg'
    img = cv2.imread(file)
    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(grey, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    result = reader.readtext(binary)

    prob = 0.0
    for item in result:
        for word in item[1].split():
            if len(word) != 9:
                continue
            if not any(c.isdigit() for c in word):
                continue
            if word.isalpha():
                continue
            if any(c.islower() for c in word):
                continue
            if bool(FORBIDDEN_RE.search(word)):
                continue
            if item[2] > prob:
                prob = item[2]
                print(word, prob)

pass