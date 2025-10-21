import cv2
import mediapipe as mp
import pyautogui
import util
from pynput.mouse import Button, Controller

mouse = Controller()
screen_width, screen_height = pyautogui.size()

mpHands = mp.solutions.hands
hands = mpHands.Hands(
    static_image_mode=False,
    model_complexity=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
    max_num_hands=1
)

is_scrolling = False
is_dragging = False

def find_finger_tip(processed):
    if processed.multi_hand_landmarks:
        hand_landmarks = processed.multi_hand_landmarks[0]
        index_finger_tip = hand_landmarks.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP]
        return index_finger_tip, processed.multi_handedness[0].classification[0].label
    return None, None

def move_mouse(index_finger_tip):
    if index_finger_tip is not None:
        x = int(index_finger_tip.x * screen_width)
        y = int(index_finger_tip.y / 2 * screen_height)
        pyautogui.moveTo(x, y)

def is_left_click(landmark_list, thumb_index_dist):
    return (
        util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) < 50 and
        util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12]) > 90 and
        thumb_index_dist > 50
    )

def is_right_click(landmark_list, thumb_index_dist):
    return (
        util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12]) < 50 and
        util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) > 90 and
        thumb_index_dist > 50
    )

def is_double_click(landmark_list, thumb_index_dist):
    return (
        util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) < 50 and
        util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12]) < 50 and
        thumb_index_dist > 50
    )

def is_scrolling_gesture(landmark_list, thumb_index_dist):
    return (
        thumb_index_dist < 50
    )

def is_dragging_gesture(landmark_list, thumb_index_dist):
    return (
        thumb_index_dist < 50 and
        util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) < 50
    )

def is_volume_gesture(landmark_list, thumb_pinky_dist):
    return (
        thumb_pinky_dist < 50
    )

def detect_gesture(frame, landmark_list, processed):
    global is_scrolling, is_dragging

    if len(landmark_list) >= 21:
        index_finger_tip, handedness = find_finger_tip(processed)

        if handedness == 'Right':
            thumb_index_dist = util.get_distance([landmark_list[4], landmark_list[5]])
            thumb_pinky_dist = util.get_distance([landmark_list[4], landmark_list[20]])

            # Volume control based on thumb-pinky distance and pinky vertical position change
            # We'll track pinky tip y compared to pinky pip joint y for up/down detection
            pinky_tip_y = landmark_list[20][1]
            pinky_pip_y = landmark_list[18][1]

            if is_volume_gesture(landmark_list, thumb_pinky_dist):
                if pinky_tip_y < pinky_pip_y:
                    pyautogui.press('volumeup')
                    cv2.putText(frame, "Volume Up", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                elif pinky_tip_y > pinky_pip_y:
                    pyautogui.press('volumedown')
                    cv2.putText(frame, "Volume Down", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

            if is_scrolling_gesture(landmark_list, thumb_index_dist):
                if index_finger_tip.y < landmark_list[6][1]:
                    pyautogui.scroll(10)
                    cv2.putText(frame, "Scrolling Up", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
                elif index_finger_tip.y > landmark_list[6][1]:
                    pyautogui.scroll(-10)
                    cv2.putText(frame, "Scrolling Down", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

            if is_dragging_gesture(landmark_list, thumb_index_dist):
                if not is_dragging:
                    mouse.press(Button.left)
                    is_dragging = True
                move_mouse(index_finger_tip)
            else:
                if is_dragging:
                    mouse.release(Button.left)
                    is_dragging = False

            if thumb_index_dist < 50 and util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) > 90:
                move_mouse(index_finger_tip)
            elif is_left_click(landmark_list, thumb_index_dist):
                mouse.press(Button.left)
                mouse.release(Button.left)
                cv2.putText(frame, "Left Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            elif is_right_click(landmark_list, thumb_index_dist):
                mouse.press(Button.right)
                mouse.release(Button.right)
                cv2.putText(frame, "Right Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            elif is_double_click(landmark_list, thumb_index_dist):
                pyautogui.doubleClick()
                cv2.putText(frame, "Double Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

def main():
    draw = mp.solutions.drawing_utils
    cap = cv2.VideoCapture(0)

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.flip(frame, 1)
            frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            processed = hands.process(frameRGB)

            landmark_list = []
            if processed.multi_hand_landmarks:
                hand_landmarks = processed.multi_hand_landmarks[0]
                draw.draw_landmarks(frame, hand_landmarks, mpHands.HAND_CONNECTIONS)
                for lm in hand_landmarks.landmark:
                    landmark_list.append((lm.x, lm.y))

            detect_gesture(frame, landmark_list, processed)

            cv2.imshow('Frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()

