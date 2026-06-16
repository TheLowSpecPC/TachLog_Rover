#!/usr/bin/python
"""
We are using a small REST server to control our robot.
"""
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import math
import numpy as np
#import Rover.py
from multiprocessing import Process, Queue

_debug = True


# TODO: axis-mapping should be OOP and automatic!


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
CORS(app)
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on_error_default
def default_error_handler(e):
    pass
    #print("======================= ERROR")
    #print(e)


@socketio.on('control', namespace='/control')
def control(message):
    data = message["data"]
    if "left" in data.keys():
        x = data["left"][0]
        y = data["left"][1]
        #if _debug: print("[Server] Left: ", x, ",", y)

        x = max(-2, min(x, 2))
        y = max(-2, min(y, 2))
        x = np.interp(x, [-2, 2], [-1, 1])
        y = np.interp(-y, [-2, 2], [-1, 1])
        print("[Server] Left (mapped): ", x, ",", y)

    elif "right" in data.keys():
        x = data["right"][0]
        y = data["right"][1]
        #if _debug: print("[Server] Right: ", x, ",", y)

        x = max(-2, min(x, 2))
        y = max(-2, min(y, 2))
        x = np.interp(x, [-2, 2], [-1, 1])
        y = np.interp(-y, [-2, 2], [-1, 1])
        print("[Server] Right (mapped): ", x, ",", y)

        if y > 0:
            if x > 0:
                Rover.forward(y, y-(y*x))
            elif x < 0:
                Rover.forward(y-(y*-x), y)
            else:
                Rover.forward(y, y)
        elif y < 0:
            y = -y
            if x > 0:
                Rover.backward(y, y-(y*x))
            elif x < 0:
                Rover.backward(y-(y*-x), y)
            else:
                Rover.backward(y, y)
        else:
            Rover.stop()

    elif "A" in data.keys():
        if _debug: print("[Server] A")

    elif "B" in data.keys():

        if _debug: print("[Server] B")

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", debug=True, use_reloader=False)
