#!/usr/bin/env python
import smtplib
import sys
#TODO:modify print messages
class EmailSender():
    def dbg(self,*something):
        if self.debug:
            print(*something)

    def __init__(self, _address, _password, _to_addrs, _cc_addrs=None,_bcc_addrs=None):
        self.ADDRESS = _address     #email address for sending 
        self.PASSWORD = _password   #password of the above address
        self.TO_ADDRS = _to_addrs   #To destination addresses
        self.CC_ADDRS = _cc_addrs   #Cc destination addresses
        self.BCC_ADDRS = _bcc_addrs #Bcc destination addresses
        self.FQDN = 'smtp.gmail.com'#domain name of SMTP server
        self.TLS_PORT = 587         #port number for STARTTLS
        self.SSL_PORT = 465         #port number for SMTP over SSL
        self.useTLS = True          #use STARTTLS or SMTP over SSL
        self.debug =  True
        self.dbg(_address,_password,_to_addrs,_cc_addrs,_bcc_addrs)

    def send(self, _subject, _body):
        success = False
        try:
            #when using STARTTLS
            if self.useTLS: 
                smtp_server = smtplib.SMTP(self.FQDN, self.TLS_PORT)
                smtp_server.ehlo() #TLS handshake
                if smtp_server.has_extn('STARTTLS'): #if it supports STARTTLS, use it
                    smtp_server.starttls()

            #when using SMTP over SSL
            else: 
                #when python 3.x
                if sys.version_info.major == 3:
                    import ssl
                    smtp_server = smtplib.SMTP_SSL(self.FQDN, self.SSL_PORT, context=ssl.create_default_context())
                #when python 2.x
                else:
                    from smtplib import SMTP_SSL
                    smtp_server = SMTP_SSL(self.FQDN, self.SSL_PORT)

            #login
            smtp_server.login(self.ADDRESS, self.PASSWORD)


            #compose a message according to RFC2822
            subject = 'Subject:' + _subject + '\r\n'
            if self.CC_ADDRS is None:
                cc = ''
            else:
                cc = 'Cc:' + ",".join(self.CC_ADDRS) + '\r\n'
            if self.BCC_ADDRS is None:
                bcc = ''
            else:
                bcc = 'Bcc:' + ",".join(self.BCC_ADDRS) + '\r\n'
            subject = 'Subject:' + _subject + '\r\n'
            msg =  cc + bcc + subject + '\r\n' + _body

            #send Email
            #this method returns a dictionary, with one entry for each recipient that was refused.
            retDict = smtp_server.sendmail(self.ADDRESS,",".join(self.TO_ADDRS),msg)
            if len(retDict.keys()) == 0:
                print('Email sent successfully')
                success = True
            else:
                raise Exception

        except Exception as e:
            print('An error has occurred')
            import traceback
            traceback.print_exc()
            print('can\'t send email')

        finally:
            if smtp_server in locals():
                #disconnect
                smtp_server.quit()
            return success

if __name__ == '__main__' :
    YourEmailAddress = ''
    PasswordForYourEmailAddress = ''
    DestEmailAddersses = ['']
    sender = EmailSender(YourEmailAddress, PasswordForYourEmailAddress, DestEmailAddersses)
    subject = 'testEmail'
    body = 'python version : ' + str(sys.version) + '\n' + 'use TLS : ' + str(sender.useTLS) + '\n' + 'use SSL : ' + str(sender.useTLS ^ True)
    sender.send(subject,body)
