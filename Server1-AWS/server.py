import socket,os,sys,json,base64

from priceinfo import ServerPrices;
s=socket.socket();
port = 21610
host = socket.gethostname();                       
print host;
# send data to each server 
def sendToIndividualserver(host,port,JsonOfFile):
    try:
        new_socket=socket.socket();
        new_socket.connect((host,int(port)))
        JsonOfFile['Type']="ServerDistribute"
        serverCommunication={"Type":JsonOfFile['Type'],"Name":JsonOfFile['Name'],"size":JsonOfFile['size']}
        jsonServerhead=json.dumps(serverCommunication);
        new_socket.send(jsonServerhead)
        ServerData={"data":JsonOfFile['data']}
        jsonServerData=json.dumps(ServerData);
        new_socket.send(jsonServerData)
        print "Done Sending"
        new_socket.close();
    except Exception:
        print("Other Servers",host, port ,"Down")
# Send to ALL servers 
def sendToAllServers(JsonOfFile):
    list_ofServers=sys.argv[1];
    with open(sys.argv[1]) as i:
        data=json.load(i)
    for x in range(0,len(data['AllAddresses'][0])):
        sendToIndividualserver(data['AllAddresses'][x]['host'],data['AllAddresses'][x]['port'],JsonOfFile);
# Creating Server Objects And Storing in array 
def CreateServerObjects():
    ServerArray=[]
    with open(sys.argv[1]) as i:
        data_price=json.load(i)
    presentServer=ServerPrices('127.0.0.1',port);
    for x in range(0,len(data_price['AllAddresses'][0])):
        temp=ServerPrices(data_price['AllAddresses'][x]['host'],data_price['AllAddresses'][x]['port']);
        ServerArray.append(temp)
    ServerArray.append(presentServer);
    return ServerArray

try:
    s.bind((host, port))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
s.listen(5)


# Creating server Objects and assigning the Prices to server Obects 

list_of_servers_with_price=CreateServerObjects();
while True:
    filename=""
    c, addr = s.accept()     # Establish connection with client.
    print 'Got connection from', addr
    getting_data=""
    data=c.recv(1024)
    #print('inital data is '+data);
    if(data):
        curlRequest=data.split('\n')
        typeAndUrl=curlRequest[0]
        valueOfUrl=curlRequest[len(curlRequest)-1]
        methodAndUrl=typeAndUrl.split(' ')
        TypeOfRequest=methodAndUrl[0]
        Url=str(methodAndUrl[1])[1:]
    #print ("the Type of request is ",TypeOfRequest,"The Url which we want is ",Url," data in post request if any is ",valueOfUrl);
        if(data.find("ClientUpload")!=-1):
            print ("request from the client");
            while(data!=""):
                getting_data+=data
                data=c.recv(1024)
            #tempString=getting_data
            tempString=getting_data.replace("}{",",")
            #print(tempString);
            JsonData=json.loads(tempString)
            f = open(JsonData['Name'],'wb')
            f.write(base64.b64decode(JsonData['data']))
            f.close()
            print "Done Receiving"
            c.send('Thank you for connecting')
            c.close()
            sendToAllServers(JsonData);
        elif(data.find("ServerDistribute")!=-1):
            print ("request from the Server");
            while(data!=""):
                getting_data+=data
                data=c.recv(1024)
            tempString=getting_data.replace("}{",",")
            #print(tempString);
            JsonData=json.loads(tempString)
            f = open(JsonData['Name'],'wb')
            f.write(base64.b64decode(JsonData['data']))
            f.close()
            print "Done Receiving"
            c.send('Thank you for connecting')
            c.close()
        elif(data.find("RoundTrip")!=-1):
            print("RTT request")
            c.send(data)
            c.close();
        elif(TypeOfRequest=="GET" and Url=="getServerList"):
            c.send("HTTP/1.1 200 OK\nContent-Type: text/html\n\n");
            list_ofServers=sys.argv[1];
            with open(sys.argv[1]) as i:
                data=json.load(i)
            tempVariable=data['AllAddresses']
            Value_to_Send=''
            for x in range(0,len(tempVariable)):
                Value_to_Send+=("Host"+" :"+tempVariable[x]['host']+ "Port is  "+" :"+tempVariable[x]['port']+"\n");
            c.send(str(Value_to_Send));
            c.shutdown(socket.SHUT_RDWR);
            print("connection closed");
            c.close();
        elif(TypeOfRequest=="POST" and Url=="setServerList" ):
            print valueOfUrl;
            file=open(sys.argv[1], "w")
            file.write(valueOfUrl)
            file.close();
            c.send("'HTTP/1.1 200 OK\nContent-Type: text/html\n\n'");
            c.send(valueOfUrl);
            c.shutdown(socket.SHUT_RDWR);
            print("connection closed");
            c.close();
            list_of_servers_with_price=CreateServerObjects();
        elif(TypeOfRequest=="GET" and Url=="priceInfo" ):
            c.send("HTTP/1.1 200 OK\nContent-Type: text/html\n\n");
            Value_to_Send=''
            data_sending=[]
            for x in range(0,len(list_of_servers_with_price)):
                Value_to_Send+=("Host is :"+str(list_of_servers_with_price[x].host)+"port is :"+str(list_of_servers_with_price[x].port)+"price is :"+str(list_of_servers_with_price[x].price)+"\n");
                tempJsonData={"Host":list_of_servers_with_price[x].host,"Port":list_of_servers_with_price[x].port,"Price":list_of_servers_with_price[x].price}
                data_sending.append(tempJsonData)
            JsonPriceList={"serversWithPrice":data_sending}
            c.send(json.dumps(JsonPriceList));
            c.shutdown(socket.SHUT_RDWR);
            print("connection closed");
            c.close();
        elif(TypeOfRequest=="POST" and Url=="setpriceInfo" ):
            postRequestInput=json.loads(valueOfUrl)
            print('\n')
            c.send("'HTTP/1.1 200 OK\nContent-Type: text/html\n\n'");
            Value_to_Send='';
            for x in range(0,len(postRequestInput['changes'])):
                print(postRequestInput['changes'][x]['price'])
                for server in list_of_servers_with_price:
                    print("presentServer "+server.host , str(server.port),"check port ",str(postRequestInput['changes'][x]['port']),"presentprice" , server.price);
                    if(server.host==postRequestInput['changes'][x]['host']  and str(server.port) == postRequestInput['changes'][x]['port']):
                        server.price=postRequestInput['changes'][x]['price'] 
            for x in range(0,len(list_of_servers_with_price)):
                Value_to_Send+=("Host is :"+str(list_of_servers_with_price[x].host)+"port is :"+str(list_of_servers_with_price[x].port)+"price is :"+str(list_of_servers_with_price[x].price)+"\n");
            c.send(str(Value_to_Send));
            c.shutdown(socket.SHUT_RDWR);
            c.close();
            print("connection closed");
        else:
            c.send('HTTP/1.1 '+str(404)+' Not Found'+'\n\n')
            c.send('BAD URL')
            print("Bad Request");
            c.shutdown(socket.SHUT_RDWR);
            c.close();
    else:
        print("Data Not Received After Connection");
        c.shutdown(socket.SHUT_RDWR);
        c.close();
    