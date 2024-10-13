import cv2
import numpy as np

cam = cv2.VideoCapture(1)

cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

def nothing(x):
    pass

cv2.namedWindow('tirrek bar')

cv2.createTrackbar('Hue Min', 'tirrek bar', 0, 179, nothing)
cv2.createTrackbar('Hue Max', 'tirrek bar', 179, 179, nothing)
cv2.createTrackbar('Sat Min', 'tirrek bar', 0, 255, nothing)
cv2.createTrackbar('Sat Max', 'tirrek bar', 255, 255, nothing)
cv2.createTrackbar('Val Min', 'tirrek bar', 0, 255, nothing)
cv2.createTrackbar('Val Max', 'tirrek bar', 255, 255, nothing)

while True:
    ret, camView = cam.read()

    if not ret:
        print("Kamera görüntüsü alınamadı!")
        continue

    hsv_camView = cv2.cvtColor(camView, cv2.COLOR_BGR2HSV)

    # Trackbar değerlerini al
    h_min = cv2.getTrackbarPos('Hue Min', 'tirrek bar')
    h_max = cv2.getTrackbarPos('Hue Max', 'tirrek bar')
    s_min = cv2.getTrackbarPos('Sat Min', 'tirrek bar')
    s_max = cv2.getTrackbarPos('Sat Max', 'tirrek bar')
    v_min = cv2.getTrackbarPos('Val Min', 'tirrek bar')
    v_max = cv2.getTrackbarPos('Val Max', 'tirrek bar')

    lower_bound = np.array([h_min, s_min, v_min])
    upper_bound = np.array([h_max, s_max, v_max])
    mask = cv2.inRange(hsv_camView, lower_bound, upper_bound)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) > 0:
        coordinates = []  # Tespit edilen koordinatları saklamak için
        for contour in contours:
            area = cv2.contourArea(contour)

            if area > 3000:  # Eğer alan 3000'den büyükse
                x, y, w, h = cv2.boundingRect(contour)
                center_x = x + w // 2
                center_y = y + h // 2
                coordinates.append((center_x, center_y))

                # Kontur etrafında bir dikdörtgen çiz
                cv2.rectangle(camView, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Yeşil dikdörtgen
                cv2.circle(camView, (center_x, center_y), 5, (255, 0, 0), -1)  # Mavi nokta

        # Koordinatları yazdırma mantığı
        if len(coordinates) < 2:
            # Y ekseni değeri daha fazla olan nesnenin koordinatını yazdır
            max_y_coordinate = max(coordinates, key=lambda coord: coord[1])
            print(f"Y ekseni en yüksek olan: X: {max_y_coordinate[0]}, Y: {max_y_coordinate[1]}")
        else:
            # X ekseni değeri daha fazla olan nesnenin koordinatını yazdır
            max_x_coordinate = max(coordinates, key=lambda coord: coord[0])
            print(f"X ekseni en yüksek olan: X: {max_x_coordinate[0]}, Y: {max_x_coordinate[1]}")

    # Sonuçları göster
    cv2.imshow("KUPA KIZI", camView)

    if cv2.waitKey(50) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()

