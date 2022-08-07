import cv2, time, serial, threading
import numpy as np

prev_contour = 0

xy_list = []
bounding_list = []
contour_list = []

prev_frame_time = 0
new_frame_time = 0

# Sensitivity variable (lower = more sensitive)
sensitivity = 10
second = 0

isArduinoAvailable = True

try:
    # Make sure to set the baudrate to 2000000 in your arduino IDE
    # Lower baudrate = more data loss
    arduino = serial.Serial(port='COM5', baudrate=2000000, timeout=2)
except serial.serialutil.SerialException:
    print("Failed to communicate with arduino board\nPossible solutions :\n1. Close arduino serial monitor\n2. Change serial port\n3. Reset arduino board\n")
    isArduinoAvailable = False



# List when any moving object appear
motion_list = [None, None]
static_back = None

# Capturing video - remove 2nd parameter if you're experiencing low FPS
video = cv2.VideoCapture(0, cv2.CAP_DSHOW) 

video.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
video.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

font = cv2.QT_FONT_NORMAL

def reset():
    arduino.write(("960" + " " + "1000").encode())
    time.sleep(0.1)
    arduino.write(("960" + " " + "540").encode())

def turn_off():
    if isArduinoAvailable:
        arduino.write("o".encode())


def reset_position():
    global second
    while True:
        second += 1
        if second == 20:
            reset()
        time.sleep(0.5)
        if second < 0:
            break

if isArduinoAvailable:
    (threading.Thread(target=reset_position)).start()
    
        


while True:
    
    check, frame = video.read()
    try:
        # Remove unwanted shadows from the image (also reduce frame rate)
        img_hsv: np.ndarray = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(src=img_hsv, lowerb=np.array([0, 64, 133]), upperb=np.array([255, 255, 255]))
        img_hsv_modify: np.ndarray = cv2.bitwise_and(frame, frame, mask=mask)


        # Initializing motion = 0 (no motion)
        motion = 0
    
        gray = cv2.cvtColor(img_hsv_modify, cv2.COLOR_BGR2GRAY)
    except:
        second = -1
        break

    # Converting gray scale image to GaussianBlur
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # Assign value of static_back for the first time
    if static_back is None:
        static_back = gray
        continue
    

    # Difference between static background
    # and current frame(which is GaussianBlur)
    diff_frame = cv2.absdiff(static_back, gray) 

    # If change in between static background and
    # current frame is greater than (sensitivity var) it will show white color(255)
    thresh_frame = cv2.threshold(diff_frame, sensitivity, 255, cv2.THRESH_BINARY)[1]
    thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)

    # Finding contour of moving object
    cnts, _ = cv2.findContours(thresh_frame.copy(),
                               cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for contour in cnts:
        if (cv2.contourArea(contour) > 10000):
            motion = 1
            contour_list.append(cv2.contourArea(contour))
            (x, y, w, h) = cv2.boundingRect(contour)
            bounding_list.append([x, y, w, h])
            xy_list.append((x+(w/2))*(y+(h/2)))

        else:
            continue

        # making green rectangle around the moving object
   

    if len(contour_list) != 0:

        # Finding the closest contour compared to previous x and y contour's coordinate
        prev_contour = min(xy_list, key=lambda a:abs(a-prev_contour))
        

        # Display all contours
        # for bounding in bounding_list:
        #    (x, y, w, h) = (bounding)
        #    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 2)
            

        (x, y, w, h) = (bounding_list[xy_list.index(prev_contour)])
        cv2.putText(frame, str(w*h), (x+20, y+30), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        print(f"Area({len(xy_list)}) : " + str(xy_list))
        print(f"x : {x} | y : {y}\n")

        


    # Calculating the fps
    new_frame_time = time.time()
    fps = 1/(new_frame_time - prev_frame_time)
    prev_frame_time = new_frame_time
    fps = int(fps)

    if fps > 20:
        cv2.putText(frame, str(fps) + "/" + str(len(xy_list)), (5, 20), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    elif (fps <= 20) & (fps >= 10):
        cv2.putText(frame, str(fps) + "/" + str(len(xy_list)), (5, 20), font, 0.5, (0, 255, 255), 1, cv2.LINE_AA)
    else:
        cv2.putText(frame, str(fps) + "/" + str(len(xy_list)), (5, 20), font, 0.5, (0, 0, 255), 1, cv2.LINE_AA)


    # cv2.imshow("Gray Frame", gray)

    # cv2.imshow("Difference Frame", diff_frame)
    # cv2.imshow("HSV frame", img_hsv)
    
    cv2.imshow("Threshold Frame", thresh_frame)
    cv2.imshow("Color Frame", frame)

    
    if len(xy_list) != 0:
        try:
            if x != 0:
                #print("X = " + str(x+(w/2)) + " | Y = " + str(y+(h/2)))
                if (isArduinoAvailable):
                    arduino.write((str(int(1920-(x+(w/2)))) + " " + str(int(1080-(y+(h/2))))).encode())
                    second = 0

                    # Use the code below to configure servo's sensitivity
                    # arduino.write(("960" + " " + "540").encode())
        
        except NameError:
            pass
        x,y = 0,0
        contour_list.clear()
        bounding_list.clear()
        xy_list.clear()

    static_back = gray

    key = cv2.waitKey(1)
    # if q entered whole process will stop
    if key == ord('q'):
        turn_off()
        second = -1
        break
    if key == ord('l'):
        turn_off()
    if key == ord('r'):
        reset()

    continue
    
    

video.release()

cv2.destroyAllWindows()