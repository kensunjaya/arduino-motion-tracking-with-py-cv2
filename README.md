# arduino-motion-tracking-with-py-cv2
Simple arduino motion tracking with python OpenCV via serial communication

To run the python script, install all required libraries including:
1. opencv-python
2. pyserial
3. numpy

What you'll need for the project:
1. Dual axis micro servo bracket - (1)
2. SG90 / MG90s (optional) - (2)
3. KY-008 laser diode - (1)
4. Arduino UNO / Nano / Mega (optional) - (1)
5. Jumper wires (male - female & male - male)
6. 1080p webcam - (1)
7. Transparent box - (1)
8. Small breadboard - (1)
9. Breadboard power supply - (1)
10. 9V or 12V step up USB cable - (1)

https://www.youtube.com/shorts/dnyTHZVyEF8

Schematic :
![alt text](https://i.imgur.com/qoc0ZfX.png)

To adjust the servo base position, you can change this code :
```
//change 55 and 10
angle_x = map(x_data, 0, 1920, 55, 1920/sensitivity_x + 55);
angle_y = map(y_data, 0, 1080, 10, 1080/sensitivity_y + 10);
```

If you are using different camera model, you might need to adjust these variables (as the camera might have a different field of view) :
```
int sensitivity_x = 25; //Lower value = more sensitive
int sensitivity_y = 25; //Lower value = more sensitive
```

![alt text](https://i.imgur.com/mmzHCyZ.png)


