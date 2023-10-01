from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import sqlite3

app = Flask(__name__)

# Initialize database
conn = sqlite3.connect('reminders.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS reminders
             (id INTEGER PRIMARY KEY AUTOINCREMENT, phone_number TEXT, message TEXT, remind_at TEXT)''')
conn.commit()

# Initialize scheduler
scheduler = BackgroundScheduler()
scheduler.start()

def send_reminder(phone_number, message):
    response = MessagingResponse()
    response.message(message)
    return str(response)

@app.route('/webhook', methods=['POST'])
def webhook():
    incoming_msg = request.values.get('Body', '')
    phone_number = request.values.get('From', '').replace('whatsapp:', '')

    if incoming_msg.lower() == 'remindme':
        reply = "Sure! What would you like me to remind you about?"
        save_reminder(phone_number, reply)
    else:
        reply = "I'm sorry, I didn't understand. Type 'remindme' to set a reminder."

    return str(MessagingResponse().message(reply))

def save_reminder(phone_number, message):
    remind_at = datetime.now() + timedelta(minutes=1)  # Set a reminder after 1 minute
    conn = sqlite3.connect('reminders.db')
    c = conn.cursor()
    c.execute("INSERT INTO reminders (phone_number, message, remind_at) VALUES (?, ?, ?)",
              (phone_number, message, remind_at))
    conn.commit()

    # Schedule the reminder
    scheduler.add_job(send_reminder, trigger='date', run_date=remind_at,
                      args=[phone_number, message])

if __name__ == '__main__':
    app.run(debug=True)
