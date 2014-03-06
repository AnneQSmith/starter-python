import os

from flask import Flask
from flask import Response
from flask import request
from flask import render_template
from twilio import twiml
from twilio.rest import TwilioRestClient

# Pull in configuration from system environment variables
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
TWILIO_NUMBER = os.environ.get('TWILIO_NUMBER')

# create an authenticated client that can make requests to Twilio for your
# account.
client = TwilioRestClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Create a Flask web app
app = Flask(__name__)

# Render the home page
@app.route('/')
def index():
    return render_template('index.html')

# Handle a POST request to send a text message. This is called via ajax
# on our web page
@app.route('/message', methods=['POST'])
def message():
    # Send a text message to the number provided
    message = client.sms.messages.create(to=request.form['to'],
                                         from_=TWILIO_NUMBER,
                                         body='Good luck on your Twilio quest!')

    # Return a message indicating the text message is enroute
    return 'Message on the way!'

# Handle a POST request to make an outbound call. This is called via ajax
# on our web page
@app.route('/call', methods=['POST'])
def call():
    # Make an outbound call to the provided number from your Twilio number
    call = client.calls.create(to=request.form['to'], from_=TWILIO_NUMBER, 
                               url='http://twimlets.com/message?Message%5B0%5D=http://demo.kevinwhinnery.com/audio/zelda.mp3')

    # Return a message indicating the call is coming
    return 'Call inbound!'

# Generate TwiML instructions for an outbound call
@app.route('/hello')
def hello():
    response = twiml.Response()
    response.say('Hello there! You have successfully configured a web hook.')
    response.say('Good luck on your Twilio quest!', voice='woman')
    return Response(str(response), mimetype='text/xml')

@app.route('/incoming/sms')
def incoming_sms():
    response = twiml.Response()
    response.sms("I just responded to a text message. Yeah!")
    return Response(str(response), mimetype='text/xml') 

# @app.route('/incoming/call')
# def incoming_call():
#     response = twiml.Response()
#     response.say("I just responded to a voice message Yeah!")
#     return Response(str(response), mimetype='text/xml') 

@app.route('/incoming/call', methods=['GET', 'POST'])
def incoming_call():
    response = twiml.Response()
    with response.gather(numDigits=1, action="/incoming/gatherHandler") as g:
        g.say("Please enter 1 for customer service, 2 for sales") 
    return Response(str(response), mimetype='text/xml')

@app.route('/incoming/gather', methods = ['GET', "POST"])
def response():
    response = twiml.Response()

    digit = int(request.form.get("Digits", request.args.get("Digits")))

    if digit == 1:
        response.say("Sorry our cusomer service is a joke")
    elif digit == 2:
        response.say("You can't afford our products")
    elif digit == 0:
         response.dial('6505347648')
    return Response(str(response), mimetype='text/xml')





if __name__ == '__main__':
    # Note that in production, you would want to disable debugging
    app.run(debug=True)