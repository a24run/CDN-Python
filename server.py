import socket
import sys
import os
s=socket.socket();
port = 21606
host = socket.gethostname()
print host;
# Next bind to the port
# we have not typed any ip in the ip field
# instead we have inputted an empty string
# this makes the server listen to requests 
# coming from other computers on the network
def sendToRemainingServers(filename):
    #ssh -p 6774 a24run@host scp -rp -P 21604 /media/a24run/New Volume/Ubuntu data /codeing stuff /LearningSockets/ hi  a24run@host:
    os.system("scp hi USER@SERVER:PATH")

#start socket
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

    # size = c.recv(1024)
    # filesize=""
    # for i in range(0,1024):
    #     if (size[i].isdigit()):
    #         filesize+=size[i]
    #     else:
    #         break   
    # print filesize
    # filename= size[i:1024]
    # for i in range(1024,int(filesize)):
    #     temp=c.recv(1);
    #     if temp.isdigit():
    #         temp=0
    #     else:
    #         filename += c.recv(1)
    # print filename  
    # f = open(filename,'wb')
    # l = c.recv(1024)
    # while (l):
    #     print "Receiving..."
    #     f.write(l)
    #     l = c.recv(1024)
    # f.close()
    # print "Done Receiving"
    c.send('Thank you for connecting')
    c.close()  