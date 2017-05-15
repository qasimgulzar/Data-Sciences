# import matplotlib
# import matplotlib.pyplot as plt
#

#
# curINR.plot(kind='line')
import matplotlib
import matplotlib.patches as mpatches
matplotlib.use('Qt4agg')
import pylab as p
import pandas

curINR = pandas.read_csv('data/CUR-INR.csv')

curINR['RATEDIFF']=curINR['RATE']-curINR['RATE'].shift(-1)
line_ratediff,=p.plot(pandas.to_datetime(curINR['DATE']), curINR['RATEDIFF'],label='difference')
line_rate,=p.plot(pandas.to_datetime(curINR['DATE']), curINR['RATE'],label='rate')
rolling_mean=pandas.rolling_mean(curINR['RATE'],window=1000,center=True)
line_rolling_mean,=p.plot(pandas.to_datetime(curINR['DATE']), rolling_mean,label='rolling mean')

# print(curINR.describe())
print(curINR.groupby('RATE').size().describe())
p.axhline(y=curINR['RATE'].mean(),color='r')
p.axhline(y=curINR['RATE'].median(),color='y')
p.axhline(y=curINR['RATE'].mode().max(),color='b')

p.legend([line_ratediff, line_rate,line_rolling_mean], ['Difference', 'Rate','Rolling Mean'])

p.show()
