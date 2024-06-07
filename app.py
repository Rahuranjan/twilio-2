import datetime
import io
from flask import Flask, request
from pymongo import MongoClient
from twilio.twiml.messaging_response import MessagingResponse
import requests
from data import get_data
from media import media
from message import auth

# region
with io.open("vip.txt", "r") as f1:
    data_vip = f1.read()
    f1.close()

data_vip = data_vip.split("\n")
print(data_vip)

app = Flask(__name__)

client = MongoClient('mongodb+srv://rahuranjan3455:WuyQ95xxOWMyArfB@cluster0.yjbj6ol.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')

db = client.get_database('subdomain')
collection = db.get_collection('data')

if client is not None:
    print("Connected to MongoDB")


app.register_blueprint(auth)
app.register_blueprint(media)
@app.route('/sms', methods=["GET", "POST"])
def reply():
    num = request.form.get('From')
    num = num.replace("whatsapp:", "")
    msg_text = request.form.get('Body')
    x = collection.find_one({"Number": num})
    try:
        status = x["Status"]
    except:
        pass
    if(bool(x) == False):
        collection.insert_one({"Number": num, "Status": "First"})
        msg = MessagingResponse()
        resp = msg.message('''Hello , myself teetuu , a bot from total technology:
Utilize my services to get live status update on corona virus.
please select from below ,
*To get country specific data enter country name ,for example if you want to get update for australia please enter australia(not case sensitive)*''')
        return (str(msg))
    else:
        if(status == "First"):
            data = get_data(msg_text, num)
            msg = MessagingResponse()
            resp = msg.message(data)
            # collection.delete_one({"Number": num})
            collection.update_one({"NUMBER":num},{"$set":{"status":"done","last":datetime.datetime.now().timestamp()}})
            return (str(msg))
        
        if(status == "done"):
            t1 = x["last"]
            t2 = datetime.datetime.now().timestamp()
            if(num in data_vip):
           
                msg = MessagingResponse()
                collection.update_one({"NUMBER":num},{"$set":{"status":"First","last":datetime.datetime.now().timestamp()}})
                resp = msg.message('''Hello , myself teetuu , a bot from total technology:
Utilize my services to get live status update on corona virus.
please select from below ,
*To get country specific data enter country name ,for example if you want to get update for australia please enter australia(not case sensitive)*''')
                return (str(msg))
            
            else:
                if(t2-t1 >= 1800):
                    msg = MessagingResponse()
                    collection.update_one({"NUMBER":num},{"$set":{"status":"First","last":datetime.datetime.now().timestamp()}})
                    resp = msg.message('''Hello , myself teetuu , a bot from total technology:
Utilize my services to get live status update on corona virus.
please select from below ,
*To get country specific data enter country name ,for example if you want to get update for australia please enter australia(not case sensitive)*''')
                    return (str(msg))
            
                else:
                    diff = 1800 - (t2-t1)
                    diff = int(diff/60)
                    msg = MessagingResponse()
                    resp = msg.message('''You are not allowed to use the bot at this moment, please try again after '''+ str(diff) + ''' minutes. 
                                       \n*if you want to use vip access code please contact chatbot@gmail.com*''')
                    return (str(msg)) 



@app.route('/')
def hello_world():
    return 'Hello, World!'  

if __name__ == '__main__':
    app.run(debug=True)