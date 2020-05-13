from twilio.rest import Client

def send_request(ac_sid, auth_token, to, from_):
    client = Client(ac_sid, auth_token)
    body = "This is a test twilio message"
    client.messages.create(
        to=to, 
        from_=from_,
        body=body    
    )