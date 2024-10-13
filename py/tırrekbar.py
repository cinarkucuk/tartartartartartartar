import cv2
import numpy as np

# Gerekli fonksiyon
def nothing(x):
    pass

# VideoCapture nesnesi ile kamerayı başlat
cap = cv2.VideoCapture(0)

# Pencere oluştur
cv2.namedWindow('Camera Feed')

# Trackbar oluştur (Hue, Saturation, Value için)
cv2.createTrackbar('Hue Min', 'Camera Feed', 0, 179, nothing)
cv2.createTrackbar('Hue Max', 'Camera Feed', 179, 179, nothing)
cv2.createTrackbar('Sat Min', 'Camera Feed', 0, 255, nothing)
cv2.createTrackbar('Sat Max', 'Camera Feed', 255, 255, nothing)
cv2.createTrackbar('Val Min', 'Camera Feed', 0, 255, nothing)
cv2.createTrackbar('Val Max', 'Camera Feed', 255, 255, nothing)

while True:
    # Kameradan bir çerçeve al
    ret, frame = cap.read()
    if not ret:
        print("Kameradan görüntü alınamadı.")
        break

    # BGR görüntüsünü HSV formatına çevir
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Trackbar değerlerini al
    h_min = cv2.getTrackbarPos('Hue Min', 'Camera Feed')
    h_max = cv2.getTrackbarPos('Hue Max', 'Camera Feed')
    s_min = cv2.getTrackbarPos('Sat Min', 'Camera Feed')
    s_max = cv2.getTrackbarPos('Sat Max', 'Camera Feed')
    v_min = cv2.getTrackbarPos('Val Min', 'Camera Feed')
    v_max = cv2.getTrackbarPos('Val Max', 'Camera Feed')

    # HSV aralığına göre mask oluştur
    lower_bound = np.array([h_min, s_min, v_min])
    upper_bound = np.array([h_max, s_max, v_max])
    mask = cv2.inRange(hsv_frame, lower_bound, upper_bound)

    # Maskeyi uygulayarak sonucu göster
    result = cv2.bitwise_and(frame, frame, mask=mask)

    # Sonuçları göster
    cv2.imshow('Camera Feed', result)

    # Çıkış için 'q' tuşuna bas
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Kaynağı serbest bırak ve pencereleri kapat
cap.release()
cv2.destroyAllWindows()
