import cv2
import numpy as np

# Kamera açma
cam = cv2.VideoCapture(1)  # Kamerayı başlat

# Gerekli kontrol
if not cam.isOpened():
    print("Kamera açılamadı!")
    exit()

# Kamera çözünürlüğü ayarlama
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Gerekli fonksiyon
def nothing(x):
    pass

cv2.namedWindow('tirrek bar')

# Trackbar oluşturma
cv2.createTrackbar('Hue Min', 'tirrek bar', 0, 179, nothing)
cv2.createTrackbar('Hue Max', 'tirrek bar', 179, 179, nothing)
cv2.createTrackbar('Sat Min', 'tirrek bar', 0, 255, nothing)
cv2.createTrackbar('Sat Max', 'tirrek bar', 255, 255, nothing)
cv2.createTrackbar('Val Min', 'tirrek bar', 0, 255, nothing)
cv2.createTrackbar('Val Max', 'tirrek bar', 255, 255, nothing)

while True:
    ret, camWiew = cam.read()

    # Kamera görüntüsü alınamadıysa döngüyü kır
    if not ret:
        print("Kamera görüntüsü alınamadı!")
        break

    # Görüntüyü HSV formatına çevirme
    hsv_camWiew = cv2.cvtColor(camWiew, cv2.COLOR_BGR2HSV)

    # Trackbar değerlerini alma
    h_min = cv2.getTrackbarPos('Hue Min', 'tirrek bar')
    h_max = cv2.getTrackbarPos('Hue Max', 'tirrek bar')
    s_min = cv2.getTrackbarPos('Sat Min', 'tirrek bar')
    s_max = cv2.getTrackbarPos('Sat Max', 'tirrek bar')
    v_min = cv2.getTrackbarPos('Val Min', 'tirrek bar')
    v_max = cv2.getTrackbarPos('Val Max', 'tirrek bar')

    lower_bound = np.array([h_min, s_min, v_min])
    upper_bound = np.array([h_max, s_max, v_max])
    mask = cv2.inRange(hsv_camWiew, lower_bound, upper_bound)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    coordinates = []  # Koordinatları saklamak için liste

    for contour in contours:
        area = cv2.contourArea(contour)  # Kontur alanını hesapla

        if area > 3000:  # Eğer alan 3000'den büyükse
            # Kontur etrafında bir dikdörtgen çiz
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(camWiew, (x, y), (x + w, y + h), (0, 255, 0), 15)  # Yeşil dikdörtgen

            # Dikdörtgenin merkezini hesapla
            center_x = x + w // 2
            center_y = y + h // 2
            
            # Merkeze mavi bir nokta koy
            cv2.circle(camWiew, (center_x, center_y), 5, (255, 0, 0), 10)  # Mavi nokta
            
            # Koordinatları listeye ekle
            coordinates.append((center_x, center_y))

            koordinatlar = f"X: {center_x}, Y: {center_y}"
            print(koordinatlar)  # Konsola yazdır
            cv2.putText(camWiew, koordinatlar, (center_x + 10, center_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2) 

    # Koordinatları yazdırma mantığı
    if len(coordinates) <= 2:
        if coordinates:  # Liste boş değilse
            max_y_coordinate = max(coordinates, key=lambda coord: coord[1])
            print(f"Y ekseni en yüksek olan: X: {max_y_coordinate[0]}, Y: {max_y_coordinate[1]}")
    else:
        if coordinates:  # Liste boş değilse
            max_x_coordinate = max(coordinates, key=lambda coord: coord[0])
            print(f"X ekseni en yüksek olan: X: {max_x_coordinate[0]}, Y: {max_x_coordinate[1]}")             

    result = cv2.bitwise_and(camWiew, camWiew, mask=mask)

    cv2.imshow("KUPA KIZI", camWiew)
    cv2.imshow("SINEK VALESI", result)
    cv2.imshow("a", contours)

    if cv2.waitKey(50) & 0xFF == ord('q'):
        break

# Kaynağı serbest bırak
cam.release()
cv2.destroyAllWindows()
