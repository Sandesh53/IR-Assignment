/bin/sh
0 0 * * 0 cd /sandesh/Desktop/IR-Assignment/scraper && /usr/bin/scrapy crawl ycu_spider >> /var/log/cu_spider.log 2>&1


#The cron schedule 0 0 * * 0 means:
#
#0 → Minute 0 (at the start of the hour)
#0 → Hour 12 AM
#* → Every day of the month
#* → Every month
#1 → Sunday (0 represents Sunday)
#Execution Time:
#Your Scrapy spider will run every Monday at 12:00 AM


#>> /path/to/logfile.log 2>&1