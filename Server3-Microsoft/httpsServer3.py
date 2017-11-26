import socket,os,sys,json,base64,requests,threading,time, ssl
#from priceinfo import ServerPrices;
#creating Folder
cwd=os.getcwd();
filesFolder=cwd+"/files"
if (os.path.isdir(filesFolder) is False):
    os.mkdir("files")
while(1):
    try:
        print("in https only ")
        s=socket.socket();
        port = 6666
        host = socket.gethostname();
        try:
            s.bind((host, port))
        except socket.error , msg:
            print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            sys.exit()
        s.listen(5)
        while True:
            filename=""
            c, fromaddr = s.accept()
            connstream = ssl.wrap_socket(c,server_side=True,certfile="selfsigned.crt",keyfile="selfsigned.key")    # Establish connection with client.
            #print 'Got connection from', addr
            total_data=""
            while True:
                data=connstream.recv(1024)
                #print("yoyoyoyoyoyoy",data);
                if(data!=""):
                    total_data+=data;
                    if("\n\n" in data  or "\r\n\r\n" in data):
                        #print("in here ",total_data)
                        #print("\n\n" in total_data)
                        #print("\r\n\r\n" in total_data)
                        total_data.replace("\n\n","")
                        break;
                else:
                    break;
            #print('HTTP' in total_data)    
            if('HTTP' in total_data):
                total_data_json=""
                curlRequest=total_data.split('\n')
                print(curlRequest)
                typeAndUrl=curlRequest[0]
                valueOfUrl=curlRequest[len(curlRequest)-1]
                methodAndUrl=typeAndUrl.split(' ')
                TypeOfRequest=methodAndUrl[0]
                Url=str(methodAndUrl[1])[1:]
                print(Url)
            else:
                Url=""
                #print("data is ",total_data);
                total_data_json=json.loads(total_data)
                #print('inital data is ',total_data_json);
            if('ServerCommunication' in total_data_json):
                if(total_data_json['ServerCommunication']=='ServerStartupRequest'):
                    objToSend=json.dumps({"listOfFiles":os.listdir(filesFolder)});
                    #print("obj to send ",objToSend);
                    print("obj to send ",objToSend)
                    connstream.send(objToSend);
                    connstream.send("\n\n")
                    print("conn stream closing")
                    connstream.close();
                    print("conn stream closed")
                elif(total_data_json['ServerCommunication']=='ServerStartup/files'):
                    #print("value of url is",valueOfUrl);
                    #postRequestInput=json.loads(valueOfUrl);
                    #print(postRequestInput['listOfFiles'][0],postRequestInput['listOfFiles'][1])
                    #c.send("HTTP/1.1 200 OK\nContent-Type: text/html\n\n");
                    SendingDataArray=[]
                    print(len(total_data_json['listOfFiles']))
                    for x in range(0,len(total_data_json['listOfFiles'])):
                        with open(filesFolder+'/'+total_data_json['listOfFiles'][x], "rb") as imageFile:
                            b64Data = base64.b64encode(imageFile.read())
                            SendingDataArray.append({"Type":"StartupFileSave","Name":total_data_json['listOfFiles'][x],"data":b64Data})
                    #print(json.dumps({"Files":SendingDataArray}))
                    connstream.send(json.dumps({"Files":SendingDataArray})) 
                    connstream.send("\n\n")
                    #c.shutdown(socket.SHUT_RDWR);  
                    connstream.close();
                    print("data Sent");
            else:
                connstream.send('HTTP/1.1 '+str(404)+' Not Found'+'\n\n')
                connstream.send('BAD URL')
                print("Bad Request");
                connstream.shutdown(socket.SHUT_RDWR);
                connstream.close();
    except KeyboardInterrupt:
        s.close()
        print "\n User requested an Interruption"
        print "\n exciting Application"
        sys.exit()
