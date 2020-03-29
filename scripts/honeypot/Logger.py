def hlog(message):
    f = open("/home/ubuntu/minicps/scripts/honeypot/hlog.txt", "a")
    f.write(message + "\n")
    f.close()
