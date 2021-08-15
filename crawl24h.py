import time
import datetime
import os
os.chdir('tutorial')
while True:
    os.system("scrapy crawl theNewKisssub")
    time.sleep(datetime.timedelta(days=1).total_seconds())
