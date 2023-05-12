import os
from twilio.rest import Client
from includes import keys

client = Client(keys.twilio_account_sid, keys.twilio_auth_token)
def send_message(number, disease):
    message = client.messages.create(
                        body= disease + " has been identified in your plant.",
                        from_=keys.twilio_number,
                        to=number
                    )

    print(message.sid)

def make_call(mobile, animal):
    try:
        call = client.calls.create(
                    to=mobile,
                    from_=keys.twilio_number,
                    twiml=f"<Response><Say> {animal} entered into the field. I reapeat. An {animal} entered into the field. </Say></Response>"
                )
        print(call.sid)
        return True

    except Exception as e:
        print(e)
        return False