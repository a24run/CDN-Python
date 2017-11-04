CDN Project

Implementation Details:

CLIENT:
The client uploads a file to the server using sockets. The file is base64 encoded and the communication with server happens in JSON format.
With file name, upload type, size and data as the keys. Data consists the encoded base64 value of the file. The client sends the data in chunks.

SERVER:
Server listens to a port which was binded through sockets. The server performs many tasks.
The server first listens to 1024 bytes of data. The server then decodes it into what kind of request it is. Such as 
	1. Client upload 
	2. Server Distribution 
	3. Post , Get requests for Price changes.
	4. Post , Get requests to change other Servers.

Client Upload:
	The server takes the chunks of data sent by the client and then mergers all the data. The server then reads the data in json format and saves the file with the name as the client sent and decodes base64 data sent from client.

Server Distribution:
	The server After receiving the data from the client sends the data to the remaining servers. This is done by "sendToAllServers" function. This function takes the decoded json format file sent from the client. The "sendToAllServers" function then sends the file to each server from obtaining the host and port numbers of remaining servers provided as an argument while starting the server using "sendToIndividualserver" function.

Other Servers API:
	We would Iterate through the request and find what kind of request it is. Depending upon keywords "GET" , "POST". The server has 2 urls through which the price update functionality can be performed. 
	-"getServerList" sends the server list. The data is sent in http format. This is implemented using sockets. 
	-"setServerList" is a post request which takes a json input. The json input should provide the remaining servers in json format.

Price API:
	The server would set a basic value for the price of all the other servers it knows. There is a "ServerPrices" class which has host,port and price as parameters. The server file would create "ServerPrices" objects of all the remaining servers it knows and itself.
These server objects would be stored in a list. The list would be used as a reference for further transactions. 
	-The get requests are handled by "priceInfo" url. Which sends the prices of all servers.
	-The post requests to update the prices of servers is handled by "setpriceInfo" url. It takes the input in json format and changes the price of servers.

PROXY::

There is a http proxy server which accepts a command line flag and measures nectwork according to the flag.
	price : Makes the measurements of price of the server. get the value by querying the server with "GET" request on "priceInfo" URL.
	network: Sends a packet of data to all the servers and finds the RTT(round trip time). The least round trip time is the fastest route.
	networkPrice: Adds the network and price and then calculates the fastest route.
Browser,or a command line tool Wget or curl sends a command to the server. The proxy decodes the url and gets the file name. The proxy then performs the network measurements and queries the fastest server. The response from the server is then sent to the client. 




