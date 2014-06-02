from network import Listener, Handler, poll
import sys

handlers = {}  # map client handler to user name
MatchMakerMap = {} # map handlers to handlers
whoJustWent = None 
FirstRoundFlag = True;
 
class MyHandler(Handler):
     

    def on_open(self):
        pass
         
    def on_close(self):
        pass
     
    def on_msg(self, msg):
	global whoJustWent, FirstRoundFlag
        if 'join' in msg:
            print msg['join'] + " has joined."
            handlers[msg['join']] = self

	    #calculate how many handlers are in the map
	    print "map Length: " + str(len(handlers))
	    NumberOfHandlers = len(handlers)

	    if(NumberOfHandlers >= 2):
	        key1, valueHandler1 = handlers.popitem();
	        key2, valueHandler2 = handlers.popitem();

	        print "1User: " + key1
	        print "2User: " + key2


		MatchMakerMap[valueHandler1] = [valueHandler2,True]
		MatchMakerMap[valueHandler2] = [valueHandler1,False]

		msg = {'txt' : "Connected! Playing with: " +  key2}
		valueHandler1.do_send(msg)

		msg = {'txt' : "Connected! Playing with: " +  key1}
		valueHandler2.do_send(msg)

	    print "Handler Map Length: " + str(len(handlers))
	    print "MatchMaker Map Length: " + str(len(MatchMakerMap))
		
	        

            
            #need to figure out the type of what self is and need to delete the correct one
##            print handlers.keys()
        if 'txt' in msg:
            if msg['txt'] == 'quit':
                print msg['speak'] + " has left..."
                del handlers[msg['speak']]
##                print self.__class__.__name__
                Handler.do_close(self)

## handle broadcast clicking event
        if 'row_clicked' in msg:

	    #msg = {'txt' : "HelloooAfterClickFrom other player!!"}

	    #MatchMakerMap[self].do_send(msg)
	     
	    #if the same guy that just went clicked do not broadcast any change 
	    if(MatchMakerMap.has_key(self) and MatchMakerMap[self][1] == True):
	    	## broadcast to each client that has joined
	        msg = {'updateGameBoard': "", 'row_clicked': msg['row_clicked'] , 'col_clicked': msg['col_clicked']}

	        MatchMakerMap[self][0].do_send(msg)
	        MatchMakerMap[MatchMakerMap[self][0]][0].do_send(msg)

	        MatchMakerMap[self][1] = False
	        MatchMakerMap[MatchMakerMap[self][0]][1] = True 
	    elif(MatchMakerMap.has_key(self) == False):
	        msg = {'txt' : "Wait For Other Players To Automatically Connect When Avaiable"}
		self.do_send(msg)
	    else:
	        msg = {'txt' : "Not Your Turn"}
		self.do_send(msg)
 
port = 8887
server = Listener(port, MyHandler)
players = {}  # map a client handler to a player object 

while 1:
    try:
        poll(timeout=0.05) # in seconds
    except KeyboardInterrupt:
        print "Closing server, Bye: "
        for client in handlers:
            print client
            Handler.do_close(handlers[client])
        print handlers.keys()

        print "Server Shutdown Complete..."
        sys.exit()


