__author__ = 'jonathan_allen'

import platform
import urllib2
import cookielib
import urllib
import requests
import mechanize
import smtplib
import sys
from bs4 import BeautifulSoup
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def main():

    #declare var
    smtpurl = 'localhost'
    me = 'sender@email.com'
    you = 'reciever@email.com'
    if len(sys.argv) > 1:
        URL = sys.argv[1]
    else:
        URL = 'http://saltlakecity.craigslist.org/search/apa?postedToday=1&maxAsk=1000&bedrooms=2'
    errorCheck = 0
    baseURL = 'http://saltlakecity.craigslist.org'

    #init browser and open login URL
    browser = mechanize.Browser()
    htmlResponse = browser.open(URL)

    #if error (500) then it is down
    #try:
    #    htmlResponse = browser.open(URL + '/admin/users/new')
    #except urllib2.HTTPError, e:
    #    errorCheck = 0
    soup = BeautifulSoup(htmlResponse)
    rows = soup.findAll( 'time', attrs={ "datetime": True })
    links = soup.findAll( 'a', attrs={ "class" : 'hdrlnk' })

    s_rows = [ x["datetime"] for x in rows ]
    s_links = [ y["href"] for y in links ]
    #print the results
    r_rows = []
    for item in s_rows:
        datetime_obj = datetime.strptime(item, '%Y-%m-%d %H:%M')
        r_rows.append(datetime_obj)

    num = 0
    currTime = str(datetime.now())
    s_currTime = datetime.strptime(currTime, '%Y-%m-%d %H:%M:%S.%f')
    final_rows = []
    for item1 in r_rows:
        temp1 = s_currTime - item1
        diff_in_min = temp1.total_seconds()/60
        final_rows.append(diff_in_min)

    emailString = ''
    while num < len(rows):
        if final_rows[num] < 60:
            emailString = emailString + baseURL + s_links[num] + '\n'
        num = num + 1

    msg = MIMEMultipart('alternative')
    msg['Subject'] = "New Pads To Look At"
    msg['From'] = me
    msg['To'] = you

    part1 = MIMEText(emailString, 'plain')

    msg.attach(part1)

    s = smtplib.SMTP(smtpurl)
    s.sendmail(me, you, msg.as_string())
    s.quit()
    print "sent mail"

    browser.close()

if __name__ == "__main__":
    main()