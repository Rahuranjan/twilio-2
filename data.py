
import json
import requests
import pandas as pd
import matplotlib.pyplot as plt
from reportlab.lib.styles import LineStyle

def get_data(msg_text,num):
    url = "https://covid-193.p.rapidapi.com/statistics"
    headers = {
	"x-rapidapi-key": "fa31171c41msh20fad170b06dfe1p111d80jsn1e5dc24de978",
	"x-rapidapi-host": "covid-193.p.rapidapi.com"
}
  

    response = requests.request("GET", url, headers=headers)
    data=response.text
    data=json.loads(data)
    for i in range(len(data["response"])):
        x=data["response"][i]["country"]
        if(x.lower()==msg_text.lower()):
            total=data["response"][i]["cases"]["total"]
            active_cases=data["response"][i]["cases"]["active"]
            recovered=data["response"][i]["cases"]["recovered"]
            critical_cases=data["response"][i]["cases"]["critical"]
            new_cases=data["response"][i]["cases"]["new"]
            total_deaths=data["response"][i]["deaths"]["total"]
            new_deaths=data["response"][i]["deaths"]["new"]
            data_complete="Data of "+x+"\n"+"""total_infected: """+str(total)+"""
active_case: """+str(active_cases)+"""
recovered: """+str(recovered)+"""
critical_cases: """+str(critical_cases)+"""    
new_cases: """+str(new_cases)+"""
total_death: """+str(total_deaths)+"""
new_deaths: """+str(new_deaths)
        #print(data_complete)
            # dc={}
            # try:
            #     dc.update({"total_cases":int(total)})
            #     dc.update({"active_cases":int(active_cases)})
            #     dc.update({"recovered":int(recovered)})
            #     dc.update({"critical_cases":int(total)})
            #     dc.update({"new_cases":int(new_cases)})
            #     dc.update({"total_deaths":int(total_deaths)})
            #     dc.update({"new_deaths":int(new_deaths)})
            # except:
            #     pass
            # df=pd.DataFrame.from_dict(dc, orient="index",columns=["All Categories"])
            # # fig=plt.figure(figsize=(20,10))
            # plt.style.use("dark_background")
            # df["All Categories"].plot(kind="bar",color=["red","blue","green","yellow","brown","skyblue","purple"],fontsize=40)
            # plt.xlabel("ALL CATEGORIES",fontsize=50,color="red",fontweight="bold")
            # plt.grid(b=True,which="both",color="white",linestyle="-")
            # plt.title("Current Data Of corona Virus for: "+x,color="blue",fontsize=80)
            # plt.savefig(num+".png",bbox_inches="tight")
        
        
        
        
            return(data_complete)
            break
     
    return("country entered not found") 