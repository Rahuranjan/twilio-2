

from flask import Flask, request, Blueprint
from twilio.twiml.messaging_response import MessagingResponse
import requests
import shutil

media = Blueprint('media', __name__)

#  Twilio credientials
account_sid = 'ACe45aa633376491968426bda66f570c15'
auth_token = '7af18507556799955ba8e3be7c1652b8'

@media.route('/media', methods=['POST', 'GET'])
def reply():
    num = request.form.get('From')
    num = num.replace("whatsapp:", "")
    msg_text = request.form.get('Body')
    media_url = request.form.get('MediaUrl0')
    file_type = request.form.get('MediaContentType0').split('/')[1]
    print(request.form)
    print(media_url)
    
    response = requests.get(media_url, auth=(account_sid, auth_token))
    print(response.status_code)
 
    if response.status_code != 200:
        print(f"Failed to fetch media file: {response.status_code}")
        return f"Failed to fetch media file: {response.status_code}", 400

    file_name = media_url.split("/")[-1]
    print(file_name)
    read_data = requests.get(media_url, stream=True)
    read_data.raw.decode_content = True
    
    with open(file_name+"."+file_type, 'wb') as f2:
        shutil.copyfileobj(read_data.raw, f2)
        f2.close()

    with open('received_media.txt', 'wb') as f:
        f.write(response.content)  
        
         
    msg = MessagingResponse()
    resp = msg.message("Image sent by "+num)
    print("response sent")
    resp.media(media_url)
    print("media sent")
    return (str(msg))

