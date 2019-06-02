from flask import Flask
from flask import request
from flask import jsonify
from flask_pymongo import PyMongo
import RPi.GPIO as GPIO
import time
import datetime
#from picamera import PiCamera

#camera = PiCamera()

app = Flask(__name__)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(26, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
app.config['MONGO_DBNAME'] = 'pigate'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/feedmypet'

result26 = False
result6 = False
result13 = False
mongo = PyMongo(app)

# @app.route('/rgbcolour', methods=['POST'])
# def rgbcolour():
#     rgb.setColour(redvalue,greenvalue,bluevalue)
#     return "Colour set"


@app.route('/feed')
def test():
    global result26
    if result26 == False:
        result26 = True
        print("Feeding...")
        GPIO.output(26, GPIO.HIGH)
        time.sleep(3)
        GPIO.output(26, GPIO.LOW)
        print("Done feeding this scrub!")
        result26 = False
        feedmypet = mongo.db.status
        feedmypet.update_one({'id': '12345'}, {
                             '$set': {'last_fed': datetime.datetime.now(), 'level_perc': 45}})
        output = []
        for s in feedmypet.find():
            output.append(
                {'id': s['id'], 'last_fed': s['last_fed'], 'level': s['level']})
        return jsonify({'result': output})
    else:
        return "Sorry, still busy feeding the scrub!"

# Disabling this route for now as my camera does not want to pla along, potentiall a hardware error
# @app.route('/camera')
# def cameraPhoto():
#     camera.start_preview()
#     sleep(5)
#     camera.capture('/home/pi/Desktop/image.jpg')
#     camera.stop_preview()
#     camera.close()


@app.route('/history')
def testdb():
    feedmypet = mongo.db.history
    output = []
    for s in feedmypet.find():
        output.append({'id': s['id'], 'gate_closed': s['gate_closed']})
    return jsonify({'result': output})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=1234)
