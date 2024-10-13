import cv2
import numpy as np

cam = cv2.VideoCapture(1)

cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Gerekli fonksiyon
def nothing(x):
    pass

#lower_red_1 = np.array([0, 120, 70])
#upper_red_1 = np.array([10, 255, 255])
#lower_red_2 = np.array([170, 120, 70])
#upper_red_2 = np.array([180, 255, 255])

cv2.namedWindow('tirrek bar')


cv2.createTrackbar('Hue Min', 'tirrek bar', 0, 179, nothing)
cv2.createTrackbar('Hue Max', 'tirrek bar', 179, 179, nothing)
cv2.createTrackbar('Sat Min', 'tirrek bar', 0, 255, nothing)
cv2.createTrackbar('Sat Max', 'tirrek bar', 255, 255, nothing)
cv2.createTrackbar('Val Min', 'tirrek bar', 0, 255, nothing)
cv2.createTrackbar('Val Max', 'tirrek bar', 255, 255, nothing)



while (True):
    ret, camWiew = cam.read()
    hsv_camWiew = cv2.cvtColor(camWiew, cv2.COLOR_BGR2HSV)

        # Trackbar değerlerini al
    h_min = cv2.getTrackbarPos('Hue Min', 'tirrek bar')
    h_max = cv2.getTrackbarPos('Hue Max', 'tirrek bar')
    s_min = cv2.getTrackbarPos('Sat Min', 'tirrek bar')
    s_max = cv2.getTrackbarPos('Sat Max', 'tirrek bar')
    v_min = cv2.getTrackbarPos('Val Min', 'tirrek bar')
    v_max = cv2.getTrackbarPos('Val Max', 'tirrek bar')

    lower_bound = np.array([h_min, s_min, v_min])
    upper_bound = np.array([h_max, s_max, v_max])
    mask = cv2.inRange(hsv_camWiew, lower_bound, upper_bound)
    

    #mask1 = cv2.inRange(hsv_camWiew, lower_red_1, upper_red_1)
    #mask2 = cv2.inRange(hsv_camWiew, lower_red_2, upper_red_2)

    #mask = mask1 | mask2

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    num_contours = len(contours)

    
    for contour in contours:
        area = cv2.contourArea(contour)  # Kontur alanını hesapla

        if area > 3000:  # Eğer alan 1300'den büyükse
            # Kontur etrafında bir dikdörtgen çiz
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(camWiew, (x, y), (x + w, y + h), (0, 255, 0), 15)  # Yeşil dikdörtgen
            # Dikdörtgenin merkezini hesapla
            center_x = x + w // 2
            center_y = y + h // 2
            
            # Merkeze mavi bir nokta koy
            cv2.circle(camWiew, (center_x, center_y), 5, (255, 0, 0), 10)  # Mavi nokta
            koordinatlar = f"X: {center_x}, Y: {center_y}"
            print(koordinatlar)  # Konsola yazdır
            cv2.putText(camWiew, koordinatlar, (center_x + 10, center_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)  




    result = cv2.bitwise_and(camWiew, camWiew, mask=mask)


    cv2.imshow("KUPA KIZI", camWiew)
    cv2.imshow("SINEK VALESI", result)




    if cv2.waitKey(50) & 0xFF == ord('q'):
        break


cam.release()
cv2.destroyAllWindows()