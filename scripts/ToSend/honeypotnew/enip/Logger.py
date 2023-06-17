#logger
from datetime import datetime


def hlog(message):
    f = open("/home/ubuntu/minicps/scripts/honeypot/enip/hlog.txt", "a")
    #dateTimeObj = datetime.now()
    now = datetime.now()
    date_time = now.strftime(" %m/%d%Y , %H:%M:%S")
    f.write(message + date_time + "\n")
    f.close()

