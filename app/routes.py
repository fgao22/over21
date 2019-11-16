from flask import json

from app import app
from pyfingerprint.pyfingerprint import PyFingerprint


@app.route('/')
@app.route('/health')
def index():
    try:
        f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

        if (f.verifyPassword() == False):
            raise ValueError('The given fingerprint sensor password is wrong!')

    except Exception as e:
        print('The fingerprint sensor could not be initialized!')
        print('Exception message: ' + str(e))
        return app.response_class(
            response=json.dumps(data),
            status=500,
            mimetype='application/json'
        )

    # Gets some sensor information
    print('Currently used templates: ' + str(f.getTemplateCount()) +
          '/' + str(f.getStorageCapacity()))

    # Tries to show a template index table page
    try:
        page = input(
            'Please enter the index page (0, 1, 2, 3) you want to see: ')
        page = int(page)

        tableIndex = f.getTemplateIndex(page)

        for i in range(0, len(tableIndex)):
            print('Template at position #' + str(i) +
                  ' is used: ' + str(tableIndex[i]))

    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        return app.response_class(
            response=json.dumps(data),
            status=501,
            mimetype='application/json'
        )
