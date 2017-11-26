import socket,os,sys,json,base64,requests,threading,time
from PriceClass import PriceInfoClass;

s=socket.socket();
port = 21612
host = socket.gethostname();                       
print host;
try:
    s.bind((host, port))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
s.listen(5)
with open(sys.argv[1]) as i:
    Server_data=json.load(i)
list_ofServers=Server_data['AllAddresses'];
print(list_ofServers)
# Generate Server Objects
PriceServer_objects_list=[]
for i in range (0,len(list_ofServers)):
    PriceServer_objects_list.append(PriceInfoClass(list_ofServers[i]['provider'],list_ofServers[i]['network hourly cost'],list_ofServers[i]['server hourly cost']))
#print Server Objects 
for i in range(0,len(PriceServer_objects_list)):
    print(PriceServer_objects_list[i].provider);

def AddServerObjectsToListOfServers():
    Value=[]
    for i in range(0,len(PriceServer_objects_list)):
        Value.append({"provider" : PriceServer_objects_list[i].provider,"network hourly cost": PriceServer_objects_list[i].network_hourly_cost,"server hourly cost": PriceServer_objects_list[i].server_hourly_cost})
    JsonFinalValue={"AllAddresses":Value}
    file=open(sys.argv[1], "w") 
    json.dump(JsonFinalValue, file)
    file.close();
while True:
    c, addr = s.accept()     # Establish connection with client.
    print 'Got connection from', addr
    try:
        total_data=""
        while True:
            data=c.recv(1024)
            #print("receving",data);
            #print("yoyoyoyoyoyoy",data);
            if(data!=""):
                total_data+=data;
                if("\n\n" in total_data or "\r\n\r\n"):
                    #print("in here ",total_data)
                    total_data.replace("\n\n","")
                    break;
            else:
                break;
        if('HTTP' in total_data):
            total_data_json=""
            curlRequest=total_data.split('\n')
            print(curlRequest)
            typeAndUrl=curlRequest[0]
            valueOfUrl=curlRequest[len(curlRequest)-1]
            methodAndUrl=typeAndUrl.split(' ')
            TypeOfRequest=methodAndUrl[0]
            combinedURL=(str(methodAndUrl[1])[1:]).split('/')
            Url=combinedURL[0]
            specific="";
            try:
                specific=combinedURL[1]
            except:
                print("no specific")
            print(combinedURL, specific)
        else:
            Url=""
            #print("data is ",total_data);
            total_data_json=json.loads(total_data)
            #print('inital data is ',total_data_json);
        if(methodAndUrl[0]=="GET"):
            if(Url=="cost" and specific=="get"):
                c.send("HTTP/1.1 200 OK\nContent-Type: text/html\n\n");
                Value_to_Send=''
                data_sending=[]
                #print(list_ofServers);
                # for x in range (0,len(list_ofServers)):
                #     print(list_ofServers[x])
                for x in range(0,len(list_ofServers)):
                    #Value_to_Send+=("Host is :"+str(list_ofServers[x]['host'])+"port is :"+str(list_ofServers[x]['port'])+"price is :"+str(list_ofServers[x]['price'])+"\n");
                    tempJsonData={"provider":list_ofServers[x]['provider'],"network hourly cost":list_ofServers[x]['network hourly cost'],"server hourly cost":list_ofServers[x]['server hourly cost']}
                    data_sending.append(tempJsonData)
                JsonPriceList={"serversWithPrice":data_sending}
                c.send(json.dumps(data_sending));
                c.shutdown(socket.SHUT_RDWR);
                print("connection closed");
                c.close();
            elif(Url=="cost" and specific!=""):
                print("specific",specific)
                count=0
                for i in range(0,len(PriceServer_objects_list)):
                    count+=1
                    if(specific==PriceServer_objects_list[i].provider):
                        tempJsonData={"provider":list_ofServers[i]['provider'],"network hourly cost":list_ofServers[i]['network hourly cost'],"server hourly cost":list_ofServers[i]['server hourly cost']}
                        c.send(json.dumps(tempJsonData))
                        c.shutdown(socket.SHUT_RDWR);
                        c.close();
                if(count==len(PriceServer_objects_list)):
                    print("here");
                    c.send("Improper URl");
                    c.close();
        elif(methodAndUrl[0]=="POST"):
            if(Url=="addCost"):
                postRequestInput=json.loads(valueOfUrl)
                print('\n')
                c.send("'HTTP/1.1 200 OK\nContent-Type: text/html\n\n'");
                Value_to_Send='';
                print("valueOfUrl",valueOfUrl)
                data_of_post=json.loads(valueOfUrl)
                obj =PriceInfoClass(data_of_post['provider'],data_of_post['network hourly cost'],data_of_post['server hourly cost'])
                print(obj.provider)
                PriceServer_objects_list.append(obj)
                AddServerObjectsToListOfServers();
                c.shutdown(socket.SHUT_RDWR);
                c.close();
                print("connection closed");
        elif(methodAndUrl[0]=="PUT"):
            if(Url=="costs" and specific!=""):
                print("specific",specific)
                count=0
                data_of_put=json.loads(valueOfUrl)
                for i in range(0,len(PriceServer_objects_list)):
                    count+=1
                    if(specific==PriceServer_objects_list[i].provider):
                        PriceServer_objects_list[i].network_hourly_cost=data_of_put['network hourly cost']
                        PriceServer_objects_list[i].server_hourly_cost=data_of_put['server hourly cost']
                        AddServerObjectsToListOfServers();
                        c.send("Updated")
                        c.shutdown(socket.SHUT_RDWR);
                        c.close();
                if(count==len(PriceServer_objects_list)):
                    print("here");
                    c.send("Improper URl");
                    c.close();
            else:
                c.send("Improper URl");
                c.close();
        elif(methodAndUrl[0]=="DELETE"):
            if(Url=="costs" and specific!=""):
                print("specific",specific)
                count=0
                data_of_put=json.loads(valueOfUrl)
                for i in range(0,len(PriceServer_objects_list)):
                    count+=1
                    if(specific==PriceServer_objects_list[i].provider):
                        del PriceServer_objects_list[i]
                        AddServerObjectsToListOfServers();
                        c.send("DELETED")
                        c.shutdown(socket.SHUT_RDWR);
                        c.close();
                        break;
                if(count==len(PriceServer_objects_list)):
                    print("here");
                    c.send("Improper URl");
                    c.close();
            else:
                c.send("Improper URl");
                c.close();
    except KeyboardInterrupt:
        print("exiting");
        s.close();
        sys.exit();
