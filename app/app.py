import logging
from flask import Flask
from flask import jsonify
from flask import request
from flask import render_template
from skpy import Skype
from skpy import SkypeAuthException

app = Flask(__name__)

log_handler = logging.FileHandler('app.log')
log_handler.setLevel(logging.INFO)
app.logger.addHandler(log_handler)


@app.route('/', methods=['GET', 'POST'])
def index():
    result = {
        'Message': '',
        'Result': '',
    }

    if request.method == 'POST':
        result = sendMessage()

    return render_template('index.html', result=result)

@app.route('/send', methods=['POST'])
def send():
    return jsonify(sendMessage())

def sendMessage():
    if request.method == 'POST':
        try:
            if request.is_json:
                input = request.get_json()
            else:
                input = {
                    'username': request.form.get('username', ''),
                    'password': request.form.get('password', ''),
                    'recipient': request.form.get('recipient', ''),
                    'message': request.form.get('message', ''),
                }

            sk = Skype(input['username'], input['password'])
            ch = sk.chats[input['recipient']]
            ch.sendMsg(input['message'], rich=True)

            result = {
                'Message': "The message has been sent to {}".format(input['recipient']),
                'Result': 'OK',
            }
        except SkypeAuthException:
            result = {
                'Message': 'Login skype failed',
                'Result': 'ERROR',
            }
        except Exception as e:
            result = {
                'Message': f"An unknown error: {str(e)}",
                'Result': 'ERROR',
            }
    else:
        result = {
            'Message': 'Method unsupported',
            'Result': 'ERROR',
        }
    return result


@app.route('/info')
def info():
    result = {
        'Result': 'OK',
        'Message': 'Success'
    }

    return jsonify(result)


@app.route('/health-check')
def healthCheck():
    return 'OK'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
