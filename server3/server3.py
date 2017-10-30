import socket,os,sys,json,base64
    
# send data to each server 
def sendToIndividualserver(host,port,JsonOfFile):
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
# Send to ALL servers 
def sendToAllServers(JsonOfFile):
    list_ofServers=sys.argv[1];
    with open(sys.argv[1]) as i:
        data=json.load(i)
    for x in range(0,len(data['AllAddresses'][0])):
        print("sending to ",data['AllAddresses'][x]['host'],data['AllAddresses'][x]['port'])
        sendToIndividualserver(data['AllAddresses'][x]['host'],data['AllAddresses'][x]['port'],JsonOfFile);
s=socket.socket();
port = 21611
host = socket.gethostname();                       
print host;
try:
    s.bind((host, port))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
s.listen(5)

while True:
    filename=""
    c, addr = s.accept()     # Establish connection with client.
    print 'Got connection from', addr
    getting_data=""
    data=c.recv(1024)
    #print('inital data is '+data);
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
        c.send("'HTTP/1.1 200 OK\nContent-Type: text/html\n\n'");
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
    else:
        print("request from admin");
    