#!bin/python3
from flask import Flask, jsonify, abort, request, make_response, url_for
from flask.ext.httpauth import HTTPBasicAuth

app = Flask(__name__, static_url_path = "")
auth = HTTPBasicAuth()

# -----------------
# 1 = open door
# 0 = close door
# -----------------

# -----------------
# The main functions
# -----------------

def get_door_state():
    # Send a signal to get the door state.
    return 1

def door_state(state):
    # Ask to open the door
    if state == 1:
        # If the door is already open, then return true.
        if get_door_state() == 1:
            return True
        else:
            # Open the door with GPIO
            pass

    # Ask to close the door
    elif state == 0:
        # If the door is already closed, return True.
        if get_door_state() == 0:
            return True
        else:
            # Close the door with GPIO
            pass

    elif state == "switch":
        if get_door_state() == 0:
            # Open the door
            pass
        elif get_door_state() == 1:
            # Close the door
            pass

    elif state == "lockdown":
        # Close the door
        pass
    elif state == "emergency":
        # message the owners and open the door.
        pass
    else:
        return False

@auth.get_password
def get_password(username):
    if username == 'miguel':
        return 'python'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify( { 'error': 'Unauthorized access' } ), 403)
    # return 403 instead of 401 to prevent browsers from displaying the default auth dialog

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

@app.route('/PyDoor/open', methods = ['GET'])
@auth.login_required
def open_door():
    # send a signal to open the door.
    if door_state(1) == 1:
        return make_response(jsonify( { 'OK': 'The door opened' } ), 200)
    else:
        return make_response(jsonify( { 'ERROR': 'A error occured' } ), 520)

@app.route('/PyDoor/close', methods = ['GET'])
@auth.login_required
def close_door():
    # send a signal to close the door.
    if door_state(0) == 1:
        return make_response(jsonify( { 'OK': 'The door closed' } ), 200)
    else:
        return make_response(jsonify( { 'ERROR': 'A error occured' } ), 520)

@app.route('/PyDoor/switch', methods = ['GET'])
@auth.login_required
def switch_door():
    # send a signal to switch the door state.
    if door_state("switch") == 1:
        return make_response(jsonify( { 'OK': 'The door state has switched' } ), 200)
    else:
        return make_response(jsonify( { 'ERROR': 'A error occured' } ), 520)

@app.route('/PyDoor/lockdown', methods = ['GET'])
@auth.login_required
def lockdown_house():
    # send a signal to close the door and refuse all other requests until a manual unlock of the door has been done.
    return make_response(jsonify( { 'OK': 'The door has been closed and the server will refuse all other requests until the door has been opened manually.' } ), 200)

@app.route('/PyDoor/emergency', methods = ['GET'])
@auth.login_required
def emergency():
    # send a telegram message to the people concerned and open the door.
    return make_response(jsonify( { 'OK': 'The door has been opened and the owners notified' } ), 200)

@app.route('/PyDoor/5pm', methods=['GET'])
def tea_time():
    return make_response(jsonify( { 'OK': 'I\'m a teapot.' } ), 418)


if __name__ == '__main__':
    app.run(debug = True,
            host="192.168.0.46",
            port=4000)
