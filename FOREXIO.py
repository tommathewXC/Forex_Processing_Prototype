import urllib2;
import datetime;
import os;
import zipfile;
import pandas;
import matplotlib.pyplot as plt;
        
class GainCapitalDownloader(object):
    BaseUrl = str();       
    
    #Initialize location
    def __init__(self):           
        self.BaseUrl = 'http://ratedata.gaincapital.com';  
       
    #takes base variables, and generates the path for it. If
    #any child or parent directories don't exist, it will
    # create it
    def createPath(self, year, month, basecurr, targetcurr, week):     
        self.typeValidation(year,month,basecurr,targetcurr,week);
        stringmonth = str(datetime.date(1900, month, 1).strftime('%B'));
        stringyear = str(year);
        stringweek = str(week);
        currentdir = str(os.getcwd()).replace('\\','/');
        if (not os.path.isdir(currentdir)):            
            os.makedirs(currentdir); 
        currentdir = currentdir+ '/'+stringyear;
        if (not os.path.isdir(currentdir)):            
            os.makedirs(currentdir); 
        currentdir = currentdir+ '/'+stringmonth;
        if (not os.path.isdir(currentdir)):            
            os.makedirs(currentdir); 
        currentdir = currentdir+ '/'+basecurr;
        if (not os.path.isdir(currentdir)):            
            os.makedirs(currentdir); 
        currentdir = currentdir+ '/'+targetcurr;
        if (not os.path.isdir(currentdir)):            
            os.makedirs(currentdir); 
        currentdir = currentdir+ '/'+stringweek;
        if (not os.path.isdir(currentdir)):            
            os.makedirs(currentdir);         
        return currentdir;    
        
    #takes the base variables and creates the URL location
    def createURL(self, year, month, basecurr, targetcurr, week):        
        self.typeValidation(year,month,basecurr,targetcurr,week);
        u = str();
        u = self.BaseUrl + '/'+str(year);
        monthint = str();
        if (month<10):
            monthint = '0'+str(month);
        else:
            monthint = str(month);
        u = u+'/'+monthint+'%20';
        u = u+str(datetime.date(1900, month, 1).strftime('%B'));
        u = u +'/'+basecurr+'_'+targetcurr+'_Week'+str(week)+'.zip';
        return u;
        
    def typeValidation(self, year, month, basecurr, targetcurr, week):
        if not isinstance(year, basestring):
            raise ValueError('Year must be string');
        if not isinstance(month, int):
            raise ValueError('Month must be int');
        else:
            if month < 1 or month > 12:
                raise ValueError('Month must be between 1 and 12');
        if not isinstance(basecurr, basestring):
            raise ValueError('Base currency must be expressed as String');
        if not isinstance(targetcurr, basestring):
            raise ValueError('Target currency must be expressed as String');
        if not isinstance(week, int):
            raise ValueError('Week must be expressed as int');            
        else:
            if week < 1 or week > 7:
                raise ValueError('Week must be between 1 and 7');    
    
    # creates the zip file name in the last directory
    def createFile(self, basecurr, targetcurr, week):
        return str(basecurr)+'_'+str(targetcurr)+'_Week'+str(week)+'.zip';
        
    # downloads the correct zip to the correct path using base variables
    # retunrs the name of the zip file        
    def downLoadZipToDirectory(self, year, month, basecurr, targetcurr, week):
        path = self.createPath(year, month, basecurr, targetcurr, week);
        ur = self.createURL(year, month, basecurr, targetcurr, week);
        path = path + '/'+self.createFile(basecurr,targetcurr, week);
        if(not os.path.isfile(path)):
            try:
                print 'Downloading to ', path;
                tempurl = urllib2.urlopen(ur);
                DATA = tempurl.read();
                with open(path, "wb") as C:
                    C.write(DATA);
            except:
                path = 'x';
                raise IOError('Could not download URL ' + ur);
        else:
            print 'Extracting ', path;                
        return path;      
        
    def downLoadCsvToDirectory(self, year, month, basecurr, targetcurr, week):
        csvfile = self.createCsvName(year, month, basecurr, targetcurr, week);
        outname = csvfile;
        if not os.path.isfile(csvfile):
            zippedfile = self.downLoadZipToDirectory(year, month, basecurr, targetcurr, week);
            if not zippedfile == 'x':
                f = open(zippedfile, 'rb');
                z = zipfile.ZipFile(f);
                for name in z.namelist():
                    u = self.createPath(year, month, basecurr, targetcurr, week);
                    z.extract(name, u);
                f.close();
                os.remove(zippedfile);
            else:
                print self.createFile(basecurr,targetcurr,week)+ ' not downloaded correctly'; 
        else:
            outname = csvfile;             
        print outname;
        return outname;
    
    #creates file namee of CSV in last directory.
    def createCsvName(self, year, month, basecurr, targetcurr, week):
        return self.createPath(year, month, basecurr, targetcurr, week)+'/' +self.createFile(basecurr, targetcurr,week).replace('.zip','.csv');
        
    def createTable(self, year, month, basecurr, targetcurr, week,ratetype):
        n1 = self.createCsvName(year, month, basecurr,targetcurr,week);
        n2 = n1.replace('.csv','_Table'+ratetype+'.csv');
        print n2;
        return n2;
        

class ForexWeeklyData(object):
    y = str();
    m = int();
    b = str();
    t = str();
    w = int();
    filename = str();
    askrate = pandas.core.series;
    bidrate = pandas.core.series;
    plot_height = int();
    plot_width  = int();
    
    def __init__(self, year, month, basecurr, targetcurr, week, load = True):
        self.y = year;
        self.m = month;
        self.b = basecurr;
        self.t = targetcurr;
        self.w = week;            
        G = GainCapitalDownloader();
        try:
            self.filename = G.downLoadCsvToDirectory(self.y, self.m, self.b, self.t, self.w); 
            if(load):                    
                filedata = pandas.read_csv(self.filename);
                self.askrate = [filedata['RateDateTime'], filedata['RateAsk']] ; 
                self.bidrate = [filedata['RateDateTime'], filedata['RateBid']];
            self.plot_height = 10;
            self.plot_width  = 10;
            filedata = [];
        except IOError as e:
            print e.message;
        except:
            print 'Could not open csv. Retry file download fcor '+ self.filename.replace('.csv','.zip');
            
        
    
    def getRate(self, ratetype):
        asktype = 'Ask';
        bidtype = 'Bid';
        if type(ratetype) is str:
            if(ratetype.lower() == asktype.lower()):
                return self.askrate;
            else:
                if(ratetype.lower() == bidtype.lower()):
                    return self.bidrate;
                else:
                    raise ValueError('ratetype must be "ask" or "bid"');
        else:
            raise ValueError('ratetype must be str');   
        
    
    def getDay(self, timestring):
        day = timestring.split(':')[0].split(' ')[0].split('-');
        year = int(day[0]);
        month = int(day[1]);
        d = int(day[2]);
        return datetime.date(year, month, d).weekday();
    
    def getDate(self, timestring):
        return timestring.split()[0].split('-')[2];
    
    def getHour(self, timestring):
        return timestring.split(' ')[1].split(':')[0];
    
    def getMinute(self, timestring):
        return timestring.split(' ')[1].split(':')[1];
    
    def plotData(self, x, label = ''):
        if (type(x) is list and type(x[0]) is pandas.core.series.Series and type(x[1]) is pandas.core.series.Series):
            plt.figure(figsize=(self.plot_height,self.plot_width));
            plt.plot(range(1, len(x[1]) + 1 ), x[1], color = 'g');
            _pc = plt.gca();
            _pc.axes.set_xticks([]);
            _pc.axes.set_xlabel('Price of '+self.b +' in '+self.t+' '+label);
            plt.grid();
        else:
#            raise ValueError('x should be a list of two pandas core series of the same size');
            print("Cannot plot data");
            
    def scatterData(self,x, timestring = True, label = ''):
        try:
            days = x[0].apply(self.getDay);
            plt.figure(figsize=(self.plot_height,self.plot_width));
            plt.scatter(range(1, len(x[1])+1), x[1], c= days, linewidth = '0');
            cb = plt.colorbar();
            cb.set_ticks([0,1, 2, 3, 4, 5 ,6]);
            cb.ax.set_yticklabels(['Monday','Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday' , 'Sunday']);
            _pca = plt.gca();
            _pca.axes.set_xlabel(label);
            _pca.axes.get_xaxis().set_visible(False);
            plt.grid();
            plt.show();
        except:
            print("Could not generate scatter plot");
        
    def combineData(self, x, y):
        q = x[0];
        a = y[0];
        w = x[1];
        s = y[1];
        g = pandas.concat([q, a]);
        h = pandas.concat([w, s]);
        final = [g, h];
        return final;
    def MonthData(self, ratetype, month, num_weeks = 4):
        asktype = 'Ask';
        bidtype = 'Bid';
        colname = '';
        week = int();
        if type(ratetype) is str:
            if(ratetype.lower() == asktype.lower()):
                colname = 'RateAsk';
            else:
                if(ratetype.lower() == bidtype.lower()):
                    colname = 'RateBid';
                else:
                    raise ValueError('ratetype must be "ask" or "bid"');
        else:
            raise ValueError('ratetype must be str'); 
        week = 1;
        try:
            G = GainCapitalDownloader();
            fn = G.downLoadCsvToDirectory(self.y, month, self.b, self.t, 1);
            data = pandas.read_csv(fn);
            x = [data['RateDateTime'], data[colname]];
            for i in range(1, num_weeks+1):
                week = i;
                G = GainCapitalDownloader();
                fn = G.downLoadCsvToDirectory(self.y, month, self.b, self.t, i); 
                data = pandas.read_csv(fn);
                v = [data['RateDateTime'], data[colname]];
                x = self.combineData(x, v);
            return x;
        except IOError:
            print 'Could not open CSV file for ', str(self.y) ,  '/'+ str(self.m) , ' for week no. ' ,str( week ), '. Re-attempting';
    
    def TabulateData(self, R, filename = ''):
        if not os.path.isfile(filename):
            print filename + ' does not exist.';
            s = R[0].apply(self.getDay);
            dates = R[0].apply(self.getDate);
            hours = R[0].apply(self.getHour);
            minutes = R[0].apply(self.getMinute);
            DF = pandas.DataFrame(R).transpose();
            DF = pandas.DataFrame([minutes, hours, dates, s,DF['RateDateTime'], DF['RateAsk']]).transpose();
            DF.columns = ['Minutes','Hours','Dates','Day','RateDateTime','RateAsk'];
            DF = pandas.DataFrame(DF);   
            DF[['Minutes', 'Hours',  'Dates', 'Day']] = DF[['Minutes', 'Hours',  'Dates', 'Day']].astype(int);            
            if not filename == '':
                DF.to_csv(filename);
            return DF;
        else:
            print filename + ' already exists.';
            try:
                X = pandas.read_csv(filename);
                del X['Unnamed: 0'];
                return pandas.DataFrame( X);
            except:
                print "Could not get pandas frame";
                return pandas.DataFrame;

class DataAggregator:
    YEAR = int();
    MONTH = int();
    WEEK = int();
    CURRENCY_FROM = str();
    CURRENCY_TO   = str();
    RATE_TYPE = str();
    WEEKS_IN_MONTH = 4;
    FXD = ForexWeeklyData;
    
    def getMonth(self):
        if(self.YEAR < 2000 or self.YEAR > 2015 or self.MONTH < 1 or self.MONTH > 12 ):
            print "Set correct year and month";
        else:
            try:                
                self.FXD = ForexWeeklyData(str(self.YEAR), self.MONTH,   self.CURRENCY_TO,  self.CURRENCY_FROM,  1, True);
                return self.FXD.MonthData(self.RATE_TYPE, self.MONTH, self.WEEKS_IN_MONTH);                
            except Exception,e:
                print e.message;
                return [];
    def plot(self):
        try:
            x = self.getMonth();
            self.FXD.plotData(x);
        except Exception,e:
            print e.message;
    def scatter(self):
        try:
            x = self.getMonth();
            self.FXD.scatterData(x);
        except Exception,e:
            print e.message;
                
                
        

#'C:/Users/Mathew/Documents/Python Scripts/Forex/2015/October/GBP/USD/1/GBP_USD_Week1_Table.csv'