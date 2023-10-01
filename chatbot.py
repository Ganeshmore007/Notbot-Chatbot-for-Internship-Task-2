from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    incoming_msg = request.values.get('Body', '')
    resp = MessagingResponse()

    # Simple echo bot
    resp.message("You said: {}".format(incoming_msg))

    return str(resp)

if __name__ == '__main__':
    app.run(debug=True)
