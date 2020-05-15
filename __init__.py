from flask import Flask,render_template,url_for,request
from time import time
import glob
import matplotlib.pyplot as plt
import numpy as np
import shutil
import os
import sys
import wget

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def main():
    
    #print('os path: ', os.path.dirname(sys.executable))
    
    filters =[]
    d = request.form.to_dict()
    state = bool(d)

    print ('---------')
    print (d)
    print ('---------')

    # Remove last graph from folder for bypassing cached images in browser and to remove unwanted temp graphs
    [os.remove(file) for file in glob.glob('/var/www/cosqm_website/cosqm_website/20*.txt')]
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
        print('#get file from Martin Aube copy server')
        path = 'http://dome.obsand.org:2080/DATA/CoSQM-Network/' + station_name + '/data/'+ year + '/' + month + '/' + year+ '-' + month + '-' + day + '.txt'
        print('path:',path)

        try:
            filename_wget = wget.download(path)
            data = np.genfromtxt(filename_wget)
            #data = np.genfromtxt('/var/www/cosqm_website/cosqm_website/'+filename_wget)
            print(data)
            xs = np.arange(data.shape[0])
            fig,ax = plt.subplots(1, 1, dpi=140, figsize=(8,4))
            ax.set_title(path[-14:-4])
            filename1=filename

            if d['date2'] != '':
                try:
                    year2 = request.form['date2'][:4]
                    month2 = request.form['date2'][5:7]
                    day2 = request.form['date2'][8:10]
                    filename2 = year2 + month2 + day2 + '_cosqm_graph' + timestamp_no_dot + '.png'
                    path2 = 'http://dome.obsand.org:2080/DATA/CoSQM-Network/' + station_name + '/data/'+ year2 + '/' + month2 + '/' + year2+ '-' + month2 + '-' + day2 + '.txt'
                    filename_wget2 = wget.download(path2)
                    data2 = np.genfromtxt(filename_wget2)
                    datas = np.vstack((data,data2))
                    xs = np.arange(datas.shape[0])
                    data = datas
                    ax.set_title(path[-14:-4] + ', ' + path2[-14:-4])
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
            

            ax.set_xlabel('data point (#)')
            ax.set_ylabel('Magnitudes ($Mag/arcsec^2$)')
            ax.grid(True)
            print('pre savefig')
            plt.savefig('/var/www/cosqm_website/cosqm_website/static/'+filename)
            print('post savefig')
            plt.close()

        except Exception as e: 
            print(e)
            print ('error 1 : date1 does not exist')
            plt.close()
            return render_template('index.php', d=d, date=d['date'], date2=d['date2'], filename='', station_name=d['station_name'], filters=filters, err='err1')

    #When page is first loaded:
    else:
        d = {'date':'2020-01-01','date2':'2020-01-02', 'station_name':'Santa-Cruz_Tenerife', 'graph_state':0, 'C':1, 'R':1, 'G':1, 'B':1, 'Y':1}
        filename = ''

    # Remove cosqm data from OBSAND server
    path_rm = 'dome.obsand.org:2080/'
    if os.path.exists(path_rm):
        shutil.rmtree(path_rm)


    return render_template('index.php', d=d, date=d['date'], date2=d['date2'], filename=filename, station_name=d['station_name'], filters=filters)

if __name__ == "__main__":
    #app.run(debug=True, host='192.168.0.31', port=8080)
    app.run(debug=True)
