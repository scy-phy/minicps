#logger
from datetime import datetime

# It is hard to debug scripts running in mininet. We were not able to read
# stdout from them so we made them to log into a file by this function.
def hlog(message):
    f = open("/home/ubuntu/minicps/scripts/honeypot/hlog.txt", "a")
    #dateTimeObj = datetime.now()
    now = datetime.now()
    date_time = now.strftime(" %m/%d%Y , %H:%M:%S")
    f.write(message + date_time + "\n")
    f.close()

