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
    error = ''
    success = ''

    if request.method == 'POST':
        try:
            username = request.form.get('username', '')
            password = request.form.get('password', '')
            recipient = request.form.get('recipient', '')
            message = request.form.get('message', '')

            sk = Skype(username, password)
            ch = sk.chats[recipient]
            ch.sendMsg(message)

            success = "The message has been sent to {}".format(recipient)
        except SkypeAuthException:
            error = "Login skype failed"
        except Exception as e:
            error = f"An unknown error: {str(e)}"
    return render_template('index.html', error=error, success=success)


@app.route('/info')
def info():
    resp = {
        'Resutl': 'OK',
        'Message': 'Success'
    }

    return jsonify(resp)


@app.route('/health-check')
def healthCheck():
    return 'OK'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
