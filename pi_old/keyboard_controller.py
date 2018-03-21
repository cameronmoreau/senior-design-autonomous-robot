import tkinter as tk
import serial

def move(direction, speed):
    print("moving bot", direction, speed)
    s = 'm ' + str(direction) + ' ' + str(speed)
    comm.write(s.encode())

# UI
# Key to degree
KEYS = {
    113: 270, #left
    114: 90, # right
    111: 0, # up
    116: 180, # down
}

comm = serial.Serial('/dev/ttyACM0', 9600)
speed = 0
direction = 0


# Code
def keyup(e):
    pass
    #if e.keycode in KEYS:
        #move(0, 0) # stop moving

def keydown(e):
    print(e.keycode)
    if e.keycode in KEYS:
        direction = KEYS[e.keycode]
        move(direction, speed)

    if e.keycode == 65:
        speed = 0
        move(direction, speed)

def updateSpeed(e):
    speed = slider.get()
    move(direction, speed)


root = tk.Tk()
frame = tk.Frame(root, width=100, height=100)
frame.bind('<KeyPress>', keydown)
frame.bind('<KeyRelease>', keyup)

slider = tk.Scale(frame, from_=10, to=150, orient=tk.HORIZONTAL)
slider.bind('<ButtonRelease-1>', updateSpeed)
slider.pack()

frame.pack()
frame.focus_set()

root.mainloop()
