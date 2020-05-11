from flask import Flask,render_template,url_for,request,redirect, make_response
import random
import json
from time import time
from random import random
import glob
import matplotlib.pyplot as plt
import numpy as np
import shutil
import os
app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def main():
    # xs = np.arange(1000)
    # ys = np.cos(xs/10)
    filters =[]
    d = request.form.to_dict()
    state = bool(d)

    print ('---------')
    print (d)
    print ('---------')

    # Remove last graph from folder for bypassing cached images in browser 
    [os.remove(file) for file in glob.glob('static/*_cosqm_graph*.png')]

    
    if state:
        year = request.form['date'][:4]
        month = request.form['date'][5:7]
        day = request.form['date'][8:10]
        station_name = request.form['station_name']

        #make timestamp string to make new file every reload of a page
        timestamp = str(time())
        timestamp_no_dot = timestamp[:10]+timestamp[11:]
        filename = year + month + day + '_cosqm_graph' + timestamp_no_dot + '.png'

        #get file from Martin Aube copy server
        path = 'http://dome.obsand.org:2080/DATA/CoSQM-Network/' + station_name + '/data/'+ year + '/' + month + '/' + year+ '-' + month + '-' + day + '.txt'
        
        #make plot for figure
        data = np.genfromtxt(path)
        xs = np.arange(data.shape[0])
        fig,ax = plt.subplots(1, 1, dpi=140, figsize=(8,4))

        #Select filter colors to show on plot
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
        
        ax.set_title(path[-14:-4])
        ax.set_xlabel('data point (#)')
        ax.set_ylabel('Magnitudes ($Mag/arcsec^2$)')
        plt.savefig('static/' + filename)
        plt.close()

    else:
        d = {'date':'2020-01-01', 'station_name':'Santa-Cruz_Tenerife'}
        filename = ''

    # Remove cosqm data from OBSAND server
    path_rm = 'dome.obsand.org:2080/'
    if os.path.exists(path_rm):
        shutil.rmtree(path_rm)

    return render_template('index.html', date=d['date'], filename=filename, station_name=d['station_name'], filters=filters)

if __name__ == "__main__":
    #app.run(debug=True, host='192.168.2.10', port=8080)
    app.run(debug=True)
