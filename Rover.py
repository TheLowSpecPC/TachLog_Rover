import gpiozero as gp
from sshkeyboard import listen_keyboard
import time

en1 = gp.PWMLED(12)
m11 = gp.LED(27)
m12 = gp.LED(22)

en2 = gp.PWMLED(13)
m21 = gp.LED(9)
m22 = gp.LED(11)

def stop():
        m11.off()
        m12.off()
        en1.off()

        m21.off()
        m22.off()
        en2.off()
        print("Stop")

stop()

def forward(l, r):
        m11.on()
        m12.off()
        en1.value = r

        m21.off()
        m22.on()
        en2.value = l
        print("Forward: ", l, ",", r)

def backward(l, r):
        m11.off()
        m12.on()
        en1.value = r

        m21.on()
        m22.off()
        en2.value = l
        print("Backward: ", l, ",", r)

def press(key):
        if key == "up":
                forward(1, 1)
        elif key == "down":
                backward(1, 1)
        elif key == "left":
                forward(0.2, 1)
        elif key == "right":
                forward(1, 0.2)

def release(key):
        #print(f"Released {key}")
        stop()

#listen_keyboard(on_press=press, on_release=release)