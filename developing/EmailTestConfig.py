import os
import sys
import json
emailJson = 'emailTestConfig.json'
if os.path.exists(emailJson):
    #confirm existing information
    with open(emailJson,'r') as f:
        conf = json.load(f)
        for k,i in conf.items():
            print(k,':',i)
else:
    #create json file
    conf = {}
    with open(emailJson,'w') as f:
        print('YourEmailAddress =')
        conf['YourEmailAddress'] = sys.stdin.readline().strip()
        print('PasswordForYourEmailAddress =')
        conf['PasswordForYourEmailAddress'] = sys.stdin.readline().strip()
        print('DestEmailAddersses = [')
        conf['DestEmailAddersses'] = []
        while True:
            tmp = sys.stdin.readline().strip()
            if len(tmp) == 0:
                break
            conf['DestEmailAddersses'].append(tmp)
        print(']')
        json.dump(conf,f)