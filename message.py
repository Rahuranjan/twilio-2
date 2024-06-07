from flask import Blueprint, request
from twilio.twiml.messaging_response import MessagingResponse
import io
import requests

auth = Blueprint('auth', __name__)

def read_file(file_name):
    # with io.open(file_name, "r", encoding= "utf-8") as f2:
    #     data = f2.read()
    #     f2.close()
    #     data_url = data.split(",")[1]
    file_data = requests.get(file_name)
    file_data = file_data.text.split("\n")[:100]
    with io.open("output.csv", "w", encoding="utf-8") as f3:
        for i in file_data:
            f3.write(i+ "\n")
        f3.close()


@auth.route('/validate', methods=["GET", "POST"])
def validate():
    print(request.form)
    num = request.form.get('From').replace("whatsapp:", "")
    msg_text = request.form.get('Body')
    count_file = request.form.get('NumMedia')
    type123 = request.form.get('MediaContentType0')
    print(count_file)
    print(type123)
    if(count_file == "1"):
        file_type = request.form.get('MediaContentType0').split('/')[1]
        if(file_type=="csv"):
            url_file = request.form.get('MediaUrl0')
            msg = MessagingResponse()
            resp = msg.message("valid attachment")
            resp = msg.message(f"you sent {msg_text} from {num},and you attached {file_type} file.File is available in {url_file} ")
            with io.open("file.csv", "w", encoding="utf-8") as f1:
                f1.write(num+ "," + url_file)
                f1.close()
            read_file(url_file)
            return (str(msg))
        else:
            msg = MessagingResponse()
            resp = msg.message("invalid attachment")
            resp = msg.message(f"you sent {msg_text} from {num},and you attached {file_type} file")
            return (str(msg))
        
    else:
        msg = MessagingResponse()
        resp = msg.message("invalid attachment")
        resp = msg.message(f"you sent {msg_text} from {num}")
        return (str(msg))
               