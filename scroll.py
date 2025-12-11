import cv2
import mediapipe as mp
import numpy as np
import pyautogui
import time

pyautogui.FAILSAFE = False

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.6, min_tracking_confidence=0.6)
mp_draw = mp.solutions.drawing_utils

SCROLL_BASE = 100
DEBOUNCE_FRAMES = 6
COOLDOWN_SECONDS = 0.15
MIN_AREA = 0.02

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
last_action_time = 0
stable_count = 0
last_count = None

def count_fingers(hand_landmarks, handedness_label):
    tips_ids = [4, 8, 12, 16, 20]
    fingers = []
    lm = hand_landmarks
    wrist_x = lm[0].x
    if handedness_label == 'Right':
        thumb_is_open = lm[tips_ids[0]].x < lm[tips_ids[0] - 1].x
    else:
        thumb_is_open = lm[tips_ids[0]].x > lm[tips_ids[0] - 1].x
    fingers.append(1 if thumb_is_open else 0)
    for id in range(1,5):
        tip_y = lm[tips_ids[id]].y
        pip_y = lm[tips_ids[id] - 2].y
        fingers.append(1 if tip_y < pip_y else 0)
    return sum(fingers), fingers

def normalized_area(landmarks):
    xs = [p.x for p in landmarks]
    ys = [p.y for p in landmarks]
    w = max(xs) - min(xs)
    h = max(ys) - min(ys)
    return w * h

print('Mediapipe Hand Scroll — Press q to quit')

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)
    gesture_text = 'No Hand'
    finger_count = 0
    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[0]
        hand_label = results.multi_handedness[0].classification[0].label
        lm = hand_landmarks.landmark
        area = normalized_area(lm)
        mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        finger_count, fingers_list = count_fingers(lm, hand_label)
        gesture_text = f'Fingers: {finger_count}'
        cv2.putText(frame, f'Hand: {hand_label}', (10, h-60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (200,200,200), 2)
        cv2.putText(frame, f'Area: {area:.3f}', (10, h-35), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200,200,200), 2)
        cv2.putText(frame, gesture_text, (10, h-90), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)
        if area > MIN_AREA:
            if last_count == finger_count:
                stable_count += 1
            else:
                stable_count = 1
            last_count = finger_count
            if stable_count >= DEBOUNCE_FRAMES:
                now = time.time()
                if now - last_action_time > COOLDOWN_SECONDS:
                    if finger_count == 5:
                        factor = min(max(area / 0.08, 0.5), 4.0)
                        amount = int(SCROLL_BASE * factor)
                        pyautogui.scroll(amount)
                        last_action_time = now
                        cv2.putText(frame, 'Scroll Up', (w-220,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 3)
                    elif finger_count <= 1:
                        factor = min(max(area / 0.08, 0.5), 4.0)
                        amount = int(SCROLL_BASE * factor)
                        pyautogui.scroll(-amount)
                        last_action_time = now
                        cv2.putText(frame, 'Scroll Down', (w-260,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
        else:
            stable_count = 0
            last_count = None
    else:
        stable_count = 0
        last_count = None
    overlay = np.zeros_like(frame)
    cv2.rectangle(overlay, (0,0), (w,40), (0,0,0), -1)
    alpha = 0.35
    frame = cv2.addWeighted(overlay, alpha, frame, 1-alpha, 0)
    cv2.putText(frame, 'Mediapipe Hand Scroll Controller', (10,28), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)
    cv2.imshow('Hand Scroll', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()