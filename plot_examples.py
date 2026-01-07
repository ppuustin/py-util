import os, json, random

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def get_id(what, index):
    _max = index.setdefault('MAX',-1)
    if what not in index:
        index['MAX'] = _max+1
        index[what] = index['MAX']
    return index
        
def count_stat(what, stats):
    cnt = stats.setdefault(what,0)
    stats[what] = cnt+1
    return stats

def count():
    lines = []    
    fa2id = 'a2id.json'
    a2id = {}
    f = 'file.csv'
    df = pd.read_csv(f)
    for row in zip(*df.to_dict("list").values()):         
        a, b = row[0], row[1]
        a2id = self.get_id(a, a2id)
        lines.append('{0},{1}'.format(a2id[a],b2id[b]))
    save_stat(fa2id, a2id)
    write_lines(fmap, lines, 'w')
    json_to_parquet(fa2id)
    self.csv_to_parquet(fmap)
        
# -----------------------------------------------------

def plot_barh(N=3):
    data =  '{"a" : 7, "b" : 3, "c" : 9, "d" : 5, "e" : 2}'
    data = json.loads(data)

    #data = {k: v for k, v in data.items() if re.match('.*(?=.*somestring.*)(?=.*someother.*).*',k)}        
    data = dict(sorted(data.items(), key=lambda item: item[1], reverse=True)[:N])
    data = {k: v for k, v in sorted(data.items(), key=lambda item: item[1])}
    '''
    for k, v in reversed(data.items()): if 'zzz' in k: print(k, v)
    '''
    fig = plt.figure(figsize=(5,4)) # w,h

    #plt.rcParams.update({'font.size': 10})
    #plt.rc('font', **{'size': 10})
    plt.rc('xtick', labelsize=8) 
    plt.rc('ytick', labelsize=8) 

    names, values = list(data.keys()), list(data.values())
    plt.barh(range(len(data)), values, tick_label=names)
    #pd.DataFrame(data.items(), columns=['x', 'count']).plot(kind='barh', figsize=(10,8), tick_label=names)
    plt.title('top-{0}'.format(N))
    #plt.xlabel('x')
    #plt.ylabel('y')
    #plt.xticks(rotation = 45)
    #plt.gca().invert_yaxis()
    plt.grid()
    plt.tight_layout() 
    plt.show()
    plt.close()

def plot_barh2(N=3):
    file = 'somefile.json'
    data =  '{"a" : {"acc": 0.8, "f1": 0.89}, "b" : {"acc": 0.7, "f1": 0.6}, "c" : {"acc": 0.5, "f1": 0.5} }'
    data = json.loads(data)

    metrics = ['acc', 'f1'] #'acc' 'accr' 'f1' 'f1r'

    #plt.rcParams.update({'font.size': 10})
    #plt.rc('font', **{'size': 10})
    #plt.rc('xtick', labelsize=8) 
    #plt.rc('ytick', labelsize=8) 

    width, multiplier = 0.3, 0
    fig, ax = plt.subplots(figsize=(7,4)) #wh
    #fig.subplots_adjust(hspace=.5, top=1)
    fig.subplots_adjust(left=0.2) 

    c = ['blue', 'orange']
    x = np.arange(len(data)) 
    z = 1
    for i, metric in enumerate(metrics):
        offset = width * multiplier
        names, values = list(data.keys()), [data[k][metric] for k in data] #list(data.values())         
        #ax.barh(range(len(data)), values, tick_label=names, label=metric, color=c[i])
        ax.barh(x + offset, values, width, tick_label=names, label=metric, color=c[i])
        
        for i, value in enumerate(values): ax.text(value + 0.01, i- 0.2*z, str(round(value, 2)))

        xmin, xmax = ax.get_xlim()
        ax.set_xlim(xmin, 1.1*xmax)
        multiplier += 1
        z = z*-1

    plt.legend(metrics) 
    plt.title('{0}: {1}'.format(metric, file))
    #plt.xlabel('')
    #plt.ylabel('')
    #plt.xticks(rotation = 45)
    #plt.gca().invert_yaxis()
    plt.grid()
    plt.tight_layout()
    plt.show()
    plt.close()

def dist():
    random.seed(0)
    how_many = 100
    values = [ random.random()*100 for _ in range(how_many)]

    what = 'random'
    tot = len(values)
    avg = (sum(values) / len(values))
    avg = round(avg, 2)

    fig, ax = plt.subplots(figsize=(5,3)) #wh
    plt.hist(values, bins=100) # color='lightgreen', ec='black', 
    plt.axvline(x = avg, color = 'r', label = 'mean')
    plt.title('{0}, tot: {1}, avg: {2}'.format(what, tot, avg)) 
    plt.xlabel('val')    
    #plt.ylim(0, 100)
    plt.xlim(0, 150)
    plt.grid()
    plt.tight_layout()
    plt.show()
    plt.close()

def table(fs=(5,2), fname='table.png', dpi=300):
    dict_ = {'key 1': 1, 'key 2': 2,}
    df = pd.DataFrame([dict_])

    fig, ax = plt.subplots(1,1, figsize=fs)
    t = ax.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc='center')#, colWidths=[.1,.1,.8])
    t.auto_set_font_size(False)
    t.set_fontsize(10)
    t.auto_set_column_width(col=list(range(len(df.columns))))

    plt.gca().axis('off')
    plt.tight_layout()
    plt.savefig(fname, dpi=dpi)
    plt.show()
    plt.close()

def main():
    table()

# ------------------------------------------

if __name__ == '__main__':
    main()

'''
try:


except Exception as e:
    print('error:', e)
'''