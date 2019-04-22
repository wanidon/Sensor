#!/usr/bin/env python2
#-coding:utf8-#
import socket                                         
import select
from EmailSender import EmailSender
import time

HOST = None
PORT = 45988
sock0 = 0
#TODO:modify print messages


bufsize = 1024
def monitoringServer(interval,ADDRESS,TO_ADDR,PASSWORD):

        emailSender = EmailSender(ADDRESS,PASSWORD,TO_ADDR)
    
        print('\nserver:launch server\n')
        #IPv4を指定
        for res in socket.getaddrinfo(HOST, PORT, socket.AF_INET,
                                      socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
            af, socktype, proto, canonname, sa = res
            try:
                sock0 = socket.socket(af, socktype, proto)
            except socket.error as msg:
                sock0 = None
                print('server:'+msg)
                continue
            try:
                sock0.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                sock0.bind(sa)
                sock0.listen(5)
            except socket.error as e:
                print(e)
                sock0.close()
                print('server:socket error')
                sock0 = None
                continue
            break
        if sock0 is None:
            print('could not open socket')
            import sys
            sys.exit(1)



        finalconftime = {}  #addr -> time 辞書型配列
        deathflag = {}      #addr -> (0 or 1) 辞書型配列
        readfds = [sock0]
        print('server:runninng')
        try:
            while True:
                rready, wready, xready = select.select(readfds, [], [],1)
                for sock in rready:
                    if sock is sock0: #接続要求があった場合
                        conn, (address, port )= sock.accept()
                        # conn, address= sock.accept()
                        print(address)
                        print('server:connected from '+address)

                        #新たなクライアントと通信する場合
                        if address not in finalconftime:
                                print('server:confirmed new client')
                        elif deathflag[address] == 1:
                                print('server:a dead client has revived')
                                subject = 'monitoring info'
                                body = address + ' has revived'
                                if emailSender.send(subject,body):
                                    print('server:success to send email')
                                else:
                                    print('server:due to an error, cannot send email')
                                
                        finalconftime[address] = time.time()
        
                        deathflag[address] = 0
                        readfds.append(conn)
                    else:#データの送信があった場合
                        try:
                                msg = sock.recv(bufsize).decode()
                                
                                #EOF
                                if len(msg) == 0 or len(msg) == -1:
                                    sock.close()
                                    readfds.remove(sock)
                                #サーバー停止処理
                                elif msg == 'kill':
                                    print('server:received termination signal')
                                    return
                                #クライアントの離脱処理
                                elif msg == 'close':
                                    finalconftime.pop(address)#(addr:time)辞書型配列
                                    deathflag.pop(address)
                                #データを受け取った場合   
                                else:
                                    print('server:message received \"'+msg+'\"')
                                    sock.send(msg.encode())


                

                        except socket.timeout:
                                pass
                        except Exception as e:
                                print("server:an error occurred")
                                print("server:errror "+ str(e))
                                #print("server:message "+e.message)
                
                for addr,fct in finalconftime.items():
                    #基準時間以降応答がない場合応答なしの場合メール送信
                    if fct + interval < time.time() and deathflag[addr] == 0:  
                        print('server:death confirmed')
                        subject = 'monitoring info'
                        body = addr + ' is dead'
                        if emailSender.send(subject,body):
                            print('server:success to send email')
                        else:
                            print('server:due to an error, cannot send email')
                        print('server:success to send email')
                        deathflag[addr] = 1
                


                        

                        
        except KeyboardInterrupt:
                    print("server:KeyboardInterrupt")
                    pass
        finally:
                    for sock in readfds:
                        sock.close()
                    print('server:all socket closed')

if __name__ == '__main__':
        import threading
        INTERVAL = 5
        ADDRESS = "YourGmailAddress@gmail.com"
        PASSWORD = "YourGmail'sPassword"
        TO_ADDR = ["destinationEmailAddress"]


        th = threading.Thread(target=monitoringServer,args=(INTERVAL,ADDRESS,TO_ADDR,PASSWORD))
        th.start()
        print('\n this is main\n')
        
       
