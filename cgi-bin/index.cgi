#!/usr/bin/python
# -*- coding: UTF-8 -*-

# enable debugging
import cgitb
cgitb.enable()


import urllib
import xml.etree.ElementTree as ET
import json
import pprint
import urllib2
import cgi
import re
pp = pprint.PrettyPrinter(indent=4)
print "Content-Type: text/html;charset=utf-8"
print ""

currencies = {}
BTC = {}
# Currencies array = [ name, API URL, ,value in btc, amount, total in btc ]
currencies['SC'] = [ 'Solidcoin', ['MCXNOW'] ,0,0,0]
currencies['MNC'] = [ 'Mincoin', ['MCXNOW', 'CRYPTSY']  ,0,0,0]
currencies['WDC'] = [ 'Worldcoin', ['MCXNOW' ] ,0,0,0]
currencies['LTC'] = [ 'Litecoin', ['MCXNOW', 'BTCE', 'CRYPTSY'] ,0,0,0]
currencies['DVC'] = [ 'Devcoin', ['MCXNOW'] ,0,0,0]
currencies['BTC'] = [ 'Bitcoin', ['bitcurexEUR', 'virtexCAD', 'mtgoxUSD', 'bitstampUSD', 'mtgoxEUR', 'mtgoxAUD'] ,1.000,0,0]
currencies['NVC'] = [ 'Novacoin', ['BTCE', 'CRYPTSY'] ,0,0,0]
currencies['PPC'] = [ 'PPCoin', ['BTCE' ] ,0,0,0]
currencies['TRC'] = [ 'Terracoin', ['BTCE', 'CRYPTSY'] ,0,0,0]
currencies['NMC'] = [ 'Namecoin', ['BTCE', 'CRYPTSY'] ,0,0,0]
currencies['DOGE'] = [ 'Dogecoin', ['CRYPTSY'], 0,0,0]
currencies['DGC'] = [ 'Digitalcoin', ['CRYPTSY'], 0,0,0]
#currencies['MMC'] = [ 'Memorycoin', ['BTER'], 0,0,0]
currencies['XPM'] = [ 'Primecoin', ['CRYPTSY', 'BTCE'], 0,0,0]

form = cgi.FieldStorage()

source = {}
myholdings= {}
for currency in currencies:
	source[currency] = ""
	myholdings[currency] = float('0.0')

for i in form.list:
	if i.name in currencies.keys():
		myholdings[i.name] = float(i.value)


totalBTC = myholdings['BTC']
currencies['BTC'][3] = myholdings['BTC']
currencies['BTC'][4] = myholdings['BTC']


for currency in myholdings:
	for exchange in currencies[currency][1]:

		ticker = "%s.%s" %(currency, exchange)
       		url='http://graphite.internal/render?target=%s\&rawData=true\&format=json' %(ticker)
		exchangedata=json.loads(urllib.urlopen(url).read())

		lastprice=None
		n=len(exchangedata[0]['datapoints']) -1

        	while lastprice is None:
                	lastprice = exchangedata[0]['datapoints'][n][0]
                	n = n-1

		if currencies[currency][2] < lastprice:
			currencies[currency][2] = lastprice
			source[currency] = exchange
		if currency is 'BTC':
			BTC[exchange] = lastprice

for currency in source:
	if currency is not 'BTC':
		currencies[currency][3] = myholdings[currency]
		currencies[currency][4] = float(currencies[currency][2]) * float(currencies[currency][3])
		totalBTC += currencies[currency][4]

print "<html><head><title>Crypto-coin holdings calculator</title><meta http-equiv='refresh' content='120'></head>"
print "<body>"
print "<h2>Crypto coin currency holding value calculator</h2><br>"

print "<form name='input' action='/' method='get'>"
print "<table>"
print "<tr><th width=20%>Currency Name<th>Amount</th><th>Value in BTC</th><th width=15%>Rate</th><th width=10%>Source</th></tr>"

for currency in sorted(currencies, key=currencies.get):
	if currency is 'BTC':
		print "<tr><td align=right>%s</td><td align=right><input type='text' name='%s' value='%1.4f'></td><td>%10.4f</td><td align=right>%5.10f</td><td>%s</td></tr>" %(currencies[currency][0], currency, currencies[currency][3], currencies[currency][4], 1 ,"" )
	else:
		print "<tr><td align=right>%s</td><td align=right><input type='text' name='%s' value='%1.4f'></td><td>%10.4f</td><td align=right>%5.10f</td><td>%s</td></tr>" %(currencies[currency][0], currency, currencies[currency][3], currencies[currency][4], currencies[currency][2], source[currency])

#print "</table><br>"

print "<tr><td></td><td>Total (BTC)</td><td>%s</td></tr>" % totalBTC
print "<tr><td></td></tr>"

for exchange in sorted(BTC):
	lastprice = BTC[exchange]
	currency = ""
	for i in exchange:	
		if i.isupper():
			currency += i
	
	print "<tr><td></td><td>Total (%s)</td><td>%10.2f</td><td>%10.2f</td><td>%s</td></tr>" % (currency, float(totalBTC * lastprice), float(lastprice), exchange)


print "</table><br>"
#print "Total    %10.4f  BTC translates to %10.2f %s from %s<br>" %(totalBTC, totalBTC * lastprice, currency, exchange)
print "<input type='submit' value='Refresh'><Br>"
print "This uses last values, not calculating actual total earnings if all are sold at this price<br>"
print "Source is selected as the highest available price from available exchanges<br>"
print "Data updates every minute<br>"
print "</form>"

print "<script type='text/javascript'><!--"
print "google_ad_client = 'ca-pub-9636220328709354';"
print "/* BTC */"
print "google_ad_slot = '6157738668';"
print "google_ad_width = 728;"
print "google_ad_height = 90;"
print "//-->"
print "</script>"
print "<script type='text/javascript'"
print "src='http://pagead2.googlesyndication.com/pagead/show_ads.js'>"
print "</script>"

#print '<iframe scrolling="no" style="border: 0; width: 728px; height: 90px;" src="http://coinurl.com/get.php?id=13468"></iframe>'

print "<script>"
print "  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){"
print "  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),"
print "  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)"
print "  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');"
print "  ga('create', 'UA-41481753-1', 'cryptoholdings.com');"
print "  ga('send', 'pageview');"
print "</script>"

print "<br>"
print "Donations welcome:<br>"
print "BTC : 1GDbfzrpPiL86pCraxL16Lsr3k8K1EMV9X<br>"
print "LTC : LhdGw8SRewEqh8XUBhdDD8qhcaDpibSjMG<br>"
print "MNC : MQuYVGoncLcvERJVqDh6NCbTvYCFKD9byy<br>"

print "</body></html>"
