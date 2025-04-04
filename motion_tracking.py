import cv2, time, serial, threading
import numpy as np

# Capturing video - remove 2nd parameter if you're experiencing low FPS
video = cv2.VideoCapture(1, cv2.CAP_DSHOW)

frame_width = 1920
frame_height = 1080

xy_list = []
bounding_list = []
contour_list = []

prev_frame_time = 0
new_frame_time = 0
second = 0
totalFrame = 0
prev_contour = 0
lastCoordinate = 0
staticFrame = 0

# Tracking Sensitivity (lower = more sensitive)
sensitivity = 60

isArduinoAvailable = True

def reset():
    if isArduinoAvailable:
        arduino.write(("960 1000").encode())
        time.sleep(0.1)
        arduino.write(("960 540").encode())

def toggle():
    if isArduinoAvailable:
        arduino.write("9999 9999".encode())

def turn_off():
    if isArduinoAvailable:
        arduino.write("9998 9998".encode())

def turn_on():
    if isArduinoAvailable:
        arduino.write("9998 9999".encode())

def reset_position():
    global second
    while True:
        second += 1
        if second == 20:
            reset()
        time.sleep(0.5)
        if second < 0:
            break

try:
    arduino = serial.Serial(port='COM3', baudrate=2000000, timeout=10)
    time.sleep(0.001)
    turn_on()
except serial.serialutil.SerialException:
    print("Failed to communicate with Arduino board\nPossible solutions:\n"
          "1. Close Arduino serial monitor\n"
          "2. Change serial port\n"
          "3. Reset Arduino board\n")
    isArduinoAvailable = False

motion_list = [None, None]
static_back = None
font = cv2.QT_FONT_NORMAL

if isArduinoAvailable:
    threading.Thread(target=reset_position).start()

while True:
    totalFrame += 1
    
    check, frame = video.read()
    
    try:
        frame = cv2.resize(frame, (frame_width, frame_height))
        motion = 0
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    except:
        reset()
        time.sleep(0.001)
        turn_off()
        second = -1
        break

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    gray = cv2.blur(gray, (5, 5))

    if static_back is None:
        static_back = gray
        continue
    
    # Motion detection
    diff_frame = cv2.absdiff(static_back, gray)
    thresh_frame = cv2.threshold(diff_frame, sensitivity, 255, cv2.THRESH_BINARY)[1]
    thresh_frame = cv2.dilate(thresh_frame, np.ones([10, 10]), iterations=8)

    # Find contours
    cnts, _ = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in cnts:
        if cv2.contourArea(contour) > 20000:
            motion = 1
            contour_list.append(cv2.contourArea(contour))
            (x, y, w, h) = cv2.boundingRect(contour)
            bounding_list.append([x, y, w, h])
            xy_list.append(int((x+(w/2))*(y+(h/2))))

    if len(contour_list) != 0:
        prev_contour = min(xy_list, key=lambda a: abs(a-prev_contour))
        (x, y, w, h) = bounding_list[xy_list.index(prev_contour)]
        cv2.putText(frame, str(w*h), (x+20, y+30), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), thickness=3)
    
    # Calculate FPS
    new_frame_time = time.time()
    fps = int(1 / (new_frame_time - prev_frame_time))
    prev_frame_time = new_frame_time

    color = (0, 255, 0) if fps > 20 else (0, 255, 255) if fps >= 10 else (0, 0, 255)
    cv2.putText(frame, f"{fps}/{len(xy_list)}", (5, 20), font, 0.5, color, 1, cv2.LINE_AA)

    cv2.imshow("Threshold Frame", thresh_frame)
    cv2.imshow("Color Frame", frame)

    if len(xy_list) != 0 and isArduinoAvailable:
        try:
            arduino.write((str(int(1920 - (x + (w/2)) * (1920/frame_width))) + " " +
                           str(int(1080 - (y + (h/2)) * (1080/frame_height)))).encode())
            second = 0
        except NameError:
            pass
        x, y = 0, 0
        contour_list.clear()
        bounding_list.clear()
        xy_list.clear()

    static_back = gray

    key = cv2.waitKey(1)
    if key == ord('q'):
        video.release()
        reset()
        time.sleep(0.001)
        turn_off()
        second = -1
        break
    elif key == ord('l'):
        toggle()
    elif key == ord('r'):
        reset()
    elif key == ord('1'):
        turn_on()
    elif key == ord('2'):
        turn_off()

    # adds delay to filer out noise
    time.sleep(0.25)

cv2.destroyAllWindows()
