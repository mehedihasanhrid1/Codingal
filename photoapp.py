import cv2
import numpy as np
import time

FILTERS = [None, 'GRAYSCALE', 'SEPIA', 'NEGATIVE', 'BLUR']
current_filter = 0

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Camera error")
    exit()

last_action_time = 0
DEBOUNCE_TIME = 1
capture_request = False

def apply_filter(frame, ftype):
    if ftype == 'GRAYSCALE':
        return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    elif ftype == 'SEPIA':
        sepia = np.array([[0.272, 0.534, 0.131],
                          [0.349, 0.686, 0.168],
                          [0.393, 0.769, 0.189]])
        return np.clip(cv2.transform(frame, sepia), 0, 255).astype(np.uint8)
    elif ftype == 'NEGATIVE':
        return cv2.bitwise_not(frame)
    elif ftype == 'BLUR':
        return cv2.GaussianBlur(frame, (15, 15), 0)
    return frame

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    roi = frame[100:400, 100:400]
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    lower_skin = np.array([0, 30, 60], dtype=np.uint8)
    upper_skin = np.array([20, 150, 255], dtype=np.uint8)
    mask = cv2.inRange(hsv, lower_skin, upper_skin)

    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.dilate(mask, kernel, iterations=2)
    mask = cv2.GaussianBlur(mask, (5, 5), 0)

    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        cnt = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(cnt)

        if area > 3000:
            hull = cv2.convexHull(cnt, returnPoints=False)
            defects = cv2.convexityDefects(cnt, hull)

            if defects is not None:
                pinch_like = False
                for i in range(defects.shape[0]):
                    s, e, f, d = defects[i, 0]
                    if d < 2000:
                        pinch_like = True
                        break

                now = time.time()

                if pinch_like and now - last_action_time > DEBOUNCE_TIME:
                    capture_request = True
                    last_action_time = now

            if area > 12000:
                now = time.time()
                if now - last_action_time > DEBOUNCE_TIME:
                    current_filter = (current_filter + 1) % len(FILTERS)
                    last_action_time = now

            cv2.drawContours(roi, [cnt], -1, (0, 255, 0), 2)

    filtered = apply_filter(frame, FILTERS[current_filter])
    display = cv2.cvtColor(filtered, cv2.COLOR_GRAY2BGR) if FILTERS[current_filter] == 'GRAYSCALE' else filtered

    if capture_request:
        ts = int(time.time())
        cv2.imwrite(f"picture_{ts}.jpg", display)
        cv2.putText(display, "Picture Captured!", (40, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        capture_request = False

    cv2.rectangle(display, (100, 100), (400, 400), (255, 0, 0), 2)
    cv2.putText(display, f"Filter: {FILTERS[current_filter] or 'None'}",
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    cv2.imshow("OpenCV Gesture Photo App", display)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
