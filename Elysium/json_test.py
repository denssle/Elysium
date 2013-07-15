import socket, json, time

class jsontest:
    def hosten(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        s.bind(("", 51000)) 
        s.listen(1)

        try: 
            while True: 
                komm, addr = s.accept() 
                while True: 
                    data = komm.recv(1024)
                    try:
                        data2 = json.loads(data)
                        print "JSON entpackt"
                    except:
                        print "kein Json!"
                    print data, type(data)
                    print data2["ktp"], type(data2)

        finally: 
            s.close()

    def einsteigen(self):
        ip = "127.0.0.1"
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        s.connect((ip, 51000))

        try: 
            while True: 
                nachricht = {"ktp": 10, "kit": 10}
                s.send(json.dumps(nachricht)) 
                time.sleep(2)
        finally: 
            s.close()
    
while True:
    entscheidung = raw_input("Host oder einsteigen?")
    if entscheidung == "h":
        jsontest().hosten()
    elif entscheidung == "e":
        jsontest().einsteigen()
    elif entscheidung == "q":
        break