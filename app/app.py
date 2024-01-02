import logging
import requests
from flask import Flask
from flask import jsonify
from flask import request
from flask import render_template
from skpy import Skype
from skpy import SkypeAuthException
from datetime import date

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

@app.route('/report', methods=['GET'])
def report():
    # GET API KEY: https://redmine.monotos.biz/my/account
    # YOUR API KEY
    api_key = request.args.get('key', '')
    
    if not api_key:
        return "The key parameter is required. Visit: https://redmine.monotos.biz/my/account to get api key"

    url = "https://redmine.monotos.biz/time_entries.json?limit=20"
    headers = {"X-Redmine-API-Key": api_key}

    try:
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return f"Requests error: {e}"

    data = response.json()

    if 'time_entries' not in data or not data['time_entries']:
        return 'No data or your API key is invalid.'

    result = {}
    spent_on = ''

    # Get spent times of the last day working
    for item in data['time_entries']:
        if spent_on and item['spent_on'] != spent_on:
            break

        project_name = item['project']['name']
        issue_id = item['issue']['id']

        result.setdefault(project_name, []).append(issue_id)
        spent_on = item['spent_on']

    now_date = date.today().strftime('%Y/%m/%d')
    report = f"Daily Report: {now_date}<br/>"
    report += "Hôm trước:<br/>"

    for project_name, issue_ids in result.items():
        report += f"&nbsp;&nbsp;&nbsp;&nbsp;{project_name}: #{', #'.join(map(str, issue_ids))}<br/>"

    report += "Hôm nay:<br/>"
    report += "&nbsp;&nbsp;&nbsp;&nbsp;Tiếp tục task<br/>"

    return report


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
