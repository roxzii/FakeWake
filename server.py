from flask import Flask, render_template, jsonify, Response, request, redirect, url_for
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import subprocess
import RPi.GPIO as GPIO
import time

app = Flask(__name__)
auth = HTTPBasicAuth()
global status
status = "Unknown"

users = {
    "roxzii": generate_password_hash("hejgsiy8"),
    "eve": generate_password_hash("sakura")
}

@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username

@app.route('/')
@auth.login_required
def index():
    return render_template("index.html", status=status)

@app.route('/start', methods=['GET'])
def start():
	# Define the GPIO pin for the relay
	PinPower = 23

	# Setup GPIO
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(PinPower, GPIO.OUT)

	# Activate the relay for 0.1 seconds
	GPIO.output(PinPower, GPIO.HIGH)
	time.sleep(0.1)
	GPIO.output(PinPower, GPIO.LOW)

	# Clean up GPIO settings
	GPIO.cleanup()

	print("Pressed!")

	return "Ok"

@app.route('/reset', methods=['GET'])
def reset():
        # Define the GPIO pin for the relay
        PinPower = 23

        # Setup GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PinPower, GPIO.OUT)

        # Activate the relay for 4.5 seconds
        GPIO.output(PinPower, GPIO.HIGH)
        time.sleep(4.5)
        GPIO.output(PinPower, GPIO.LOW)

        # Clean up GPIO settings
        GPIO.cleanup()

        print("Reset!")

        return "Ok"

@app.route('/state', methods=['GET'])
def state():
	# Define the GPIO pin for the status
        LedState = 24

       # Setup GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(LedState, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        #Define the state
        if GPIO.input(LedState):
               status = "On"
       	else:
               status = "Off"

	# Clean up GPIO settings
        GPIO.cleanup()

        return jsonify(status)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80)
