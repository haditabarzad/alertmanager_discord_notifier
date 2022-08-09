from flask import Flask
from flask import request
import os
import sys
import requests
import json

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def hello():
    content_type = request.headers.get('Content-Type')
    discord_webhook_default = "https://discordapp.com/api/webhooks/1003629775698..._W_V7d"
    discord_webhook = os.environ.get('DISCORD_WEBHOOK', discord_webhook_default)
    if (content_type == 'application/json'):
        response_json = request.json
        for item in list(response_json['alerts']) :
            status = item['status']
            alertname = item['labels']['alertname']
            owner = item['labels']['owner']
            severity = item['labels']['severity']
            summary = item['annotations']['summary']
            startsAt = item['startsAt']
            action = item['annotations']['action']

            status_text = ""
            if status == "firing":
                status_text = ":fire: FIRING :fire:"
            elif status == "resolved":
                status_text = ":white_check_mark: RESOLVED :white_check_mark:"
            else:
                status_text = "UNKNOWN"
            
            severity_text = ""
            if severity == "critical":
                severity_text = ":red_square: critical :red_square:"
            elif severity == "information":
                severity_text = ":information_source: information :information_source:"
            elif severity == "warning":
                severity_text = ":yellow_square: warning :yellow_square:"
            else:
                severity_text = "no severity"

            discord_data = {
                "username": "Zi-tel DevOps",
                "avatar_url": "https://imgur.com/euhakCZ.png",
                "content": "Alerts from BSS Monitoring System"
                }
            discord_data["embeds"] = [
                    {
                        "author": {
                            "name": "Zitel Alerts",
                            "icon_url": "https://imgur.com/RGYh2ny.png"
                        },
                        "title": status_text,
                        "description": "** BSS Alert **",
                        "color": 15258703,
                        "fields": [
                        {
                            "name": "Severity",
                            "value": severity_text,
                        },
                        {
                            "name": "Alert Name",
                            "value": alertname,
                        },
                        {
                            "name": "Owner",
                            "value": owner,
                        },
                        {
                            "name": "Summary",
                            "value": summary
                        },
                        {
                            "name": "Action",
                            "value": action,
                        }
                    ]
                }
            ]
            response = requests.post(url = discord_webhook, json = discord_data)
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError as err:
                print(err, file=sys.stderr)
            else:
                print("Payload delivered successfully, code {}.".format(response.status_code), file=sys.stderr)
        return response_json
    else:
        return 'Content-Type not supported!'

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8088))
    app.run(debug=True, host='0.0.0.0', port=port)
