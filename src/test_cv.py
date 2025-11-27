import cv2


image = cv2.imread("/home/tym/projects/test_task/sample_data/6.jpeg")
image = cv2.imread("/home/tym/projects/test_task/sample_data/Examples-of-ID-cards-a-to-c-showcase-examples-of-bona-fide-generated-print.png")
grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

_, binary = cv2.threshold(grey, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

cv2.imwrite('tmp/grey.png', binary)