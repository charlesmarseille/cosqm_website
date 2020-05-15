from flask import Flask,render_template,url_for,request
from time import time
import glob
import matplotlib.pyplot as plt
from matplotlib import ticker
import numpy as np
import shutil
import os
import sys
import wget
import pandas as pd
from datetime import datetime as dt

#Download data beforehand from cosqm network server hosted by Martin Aube, creator of the instrument.
#where __init__.py lives, run following line in terminal to get all stations data:
#wget -r --no-parent --accept "*.txt" http://dome.obsand.org:2080/DATA/CoSQM-Network/




app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def main():
    filters =[]
    d = request.form.to_dict()
    state = bool(d)

    # Remove last graph from folder for bypassing cached images in browser and to remove unwanted temp graphs
    [os.remove(file) for file in glob.glob('/var/www/cosqm_website/cosqm_website/static/20*.png')]

    if state:

        print('#make timestamp string to make new file every reload of a page')
        timestamp = str(time())
        timestamp_no_dot = timestamp[:10]+timestamp[11:]
        station_name = request.form['station_name']
        year = request.form['date'][:4]
        month = request.form['date'][5:7]
        day = request.form['date'][8:10]
        filename = year + month + day + '_cosqm_graph' + timestamp_no_dot + '.png'
        filename1 = year + '-' + month + '-' + day + '.txt'
        print ('pre try-----')

        try:
            #filename_wget = wget.download(path)
            paths = sorted(glob.glob('/var/www/cosqm_website/cosqm_website/dome.obsand.org:2080/DATA/CoSQM-Network/'+ station_name 
                                + '/data/'+ year +'/' + month + '/' + filename1))
            datas = pd.read_csv(paths[0], sep=" ", header=None)
            data=np.array(datas)
            dates_plot = np.array([ dates+','+times for dates, times in data[:,0:2] ])
            xs = dates_plot
            fig,ax = plt.subplots(1, 1, dpi=140, figsize=(9,6))
            fig.subplots_adjust(bottom=0.20)
            xticks = ticker.MaxNLocator(8)
            ax.set_title(station_name + '-' + filename1[:-4])
            ax.tick_params('x',labelrotation=30)
            ax.xaxis.set_major_locator(xticks)

            if d['date2'] != '':
                try:
                    print('date2 not empty')
                    year2 = request.form['date2'][:4]
                    month2 = request.form['date2'][5:7]
                    day2 = request.form['date2'][8:10]
                    filename2 = year2 + '-' + month2 + '-' + day2 + '.txt'
                    print(year2, month2, day2)
                    paths = sorted(glob.glob('/var/www/cosqm_website/cosqm_website/dome.obsand.org:2080/DATA/CoSQM-Network/'+ station_name + '/data/*/*/*.txt'))
                    print (station_name)
                    datas = [pd.read_csv(path, delim_whitespace=True, header=None, error_bad_lines=False) for path in paths if os.path.getsize(path) >0]
                    data_all = np.concatenate(datas)
                    print (data_all.shape)
                    data = data_all[(data_all[:,0] >= filename1[:-4]) & (data_all[:,0] <= filename2[:-4])]
                    dates_plot = np.array([ dates+','+times for dates, times in data[:,0:2] ])
                    print ('dates_plot:', dates_plot)
                    xs = dates_plot
                    print (data.shape)
                    ax.set_title(station_name + '-' + filename1[:-4]+ ', ' + filename2[:-4])
                except:
                    print ('error 1 : date2 does not exist')
                    plt.close()
                    return render_template('index.php', d=d, date=d['date'], date2=d['date2'], filename='', station_name=d['station_name'], filters=filters, err='err2')



            print('#Select filter colors to show on plot')
            filters =[]
            if 'C' in d:
                Cs = data[:,7]
                filters.append('C')
                ax.scatter(xs, Cs, color='k', s=1)
            if 'R' in d:
                Rs = data[:,8]
                filters.append('R')
                ax.scatter(xs, Rs, color='r', s=1)
            if 'G' in d:
                Gs = data[:,9]
                filters.append('G')
                ax.scatter(xs, Gs, color='g', s=1)
            if 'B' in d:
                Bs = data[:,10]
                filters.append('B')
                ax.scatter(xs, Bs, color='b', s=1)
            if 'Y' in d:
                Ys = data[:,11]
                filters.append('Y')
                ax.scatter(xs, Ys, color='y', s=1)
            

            ax.set_xlabel('Date, Time (UTC)')
            ax.set_ylabel('Magnitudes ($Mag/arcsec^2$)')
            ax.set_ylim(np.min(data[:,7:12]))
            ax.grid(True)
            print('pre savefig')
            plt.savefig('static/'+filename)
            print('post savefig')
            plt.close()

            np.savetxt('/var/www/cosqm_website/cosqm_website/static/'+filename[:-4]+'.txt', data, fmt='%s')

        except Exception as e: 
            print(e)
            print ('error 1 : date1 does not exist')
            plt.close()
            return render_template('index.php', d=d, date=d['date'], date2=d['date2'], filename='', station_name=d['station_name'], filters=filters, err='err1')

    #When page is first loaded:
    else:
        d = {'date':'2020-01-01','date2':'2020-01-02', 'station_name':'Santa-Cruz_Tenerife', 'graph_state':0, 'C':1, 'R':1, 'G':1, 'B':1, 'Y':1}
        filename = ''  
    
    return render_template('index.php', d=d, date=d['date'], date2=d['date2'], filename=filename, station_name=d['station_name'], filters=filters)

if __name__ == "__main__":
    #app.run(debug=True, host='192.168.0.31', port=8080)
    app.run(debug=True)
