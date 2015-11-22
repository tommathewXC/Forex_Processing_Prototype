# -*- coding: utf-8 -*-
"""
Forex processing
"""
import FOREXIO as P

year = '2015';
month = 9;
curr_from = 'USD';
curr_to = 'GBP';
rate = 'ask';

rat = P.ForexWeeklyData(year, month,curr_to, curr_from,  1, True );
WEEK1 = rat.askrate;

rat = P.ForexWeeklyData(year, month,curr_to, curr_from,  2, True );
WEEK2 = rat.askrate;

rat = P.ForexWeeklyData(year, month,curr_to, curr_from,  3, True );
WEEK3 = rat.askrate;

rat = P.ForexWeeklyData(year, month,curr_to, curr_from,  4, True );
WEEK4 = rat.askrate;

print "Tabulated data";
G = P.GainCapitalDownloader();
fn = G.createTable(year, month, curr_from, curr_to, 4, rate);
V = rat.TabulateData(WEEK4, fn);

the25th =  V[V.Dates == 25];
fiveoclock = the25th[the25th.Hours == 16];
halfway = fiveoclock[fiveoclock.Minutes == 30];

print " ";
print "October 25th data";
q = [the25th['RateDateTime'], the25th['RateAsk']];
rat.plotData(q);
print "October 25th, 5PM - 6PM data";
q = [fiveoclock['RateDateTime'], fiveoclock['RateAsk']];
rat.plotData(q);
print "October 25th, 5:30 data";
q = [halfway['RateDateTime'], halfway['RateAsk']];
rat.plotData(q);