import os, sys, csv, time, re, json

class FileUtil():
    '''
    '''
    def __init__(self):
        pass

    @staticmethod
    def do_intersect(a, b):
        try:
            return [x for x in a if x in b]        
        except Exception as e:
            print('error:', e)

    @staticmethod
    def count_stat(what, stats):
        cnt = stats.setdefault(what,0)
        stats[what] = cnt+1
        return stats

    @staticmethod
    def get_id(what, index):
        _max = index.setdefault('MAX',-1)
        if what not in index:
            index['MAX'] = _max+1
            index[what] = index['MAX']
        return index

    @staticmethod
    def get_query(q_file):
        with open(q_file, 'r') as file:
            query = file.read()
        return query

    @staticmethod
    def do_stat(_dir, furls):
        from urllib.parse import urlparse
        stats = {}
        files = os.listdir(_dir)
        for i, f in enumerate(files):
            #if i > 2: break
            if '.csv.gz' in f:
                print(f)
                df = pd.read_csv(_dir + '/' + f)
                for row in zip(*df.to_dict("list").values()):         
                    pid, url = row[0], row[1]
                    parsed_url = urlparse(url)
                    #print(url)
                    if '_cat' in furls: url = parsed_url.netloc + '/' + parsed_url.path.split('/')[1]
                    elif '_all' in furls: url = url
                    else: url = parsed_url.scheme + '://' + parsed_url.netloc                
                    stats = count_stat(url, stats)
        FileUtil.save_stat(furls, stats)

    @staticmethod
    def index_urls(_dir, fpid2id, furl2id, fmap):
        from urllib.parse import urlparse
        stats = {}
        pid2id, url2id = {}, {}
        lines = []
        lines.append('pid,ind')
        files = os.listdir(_dir)
        for f in files:
            if '.csv.gz' in f:
                print(f)
                df = pd.read_csv(_dir + '/' + f)
                for row in zip(*df.to_dict("list").values()):         
                    pid, url = row[0], row[1]
                    pid2id = FileUtil.get_id(pid, pid2id)
                    url2id = FileUtil.get_id(url, url2id)
                    lines.append('{0},{1}'.format(pid2id[pid],url2id[url]))

        FileUtil.save_stat(fpid2id, pid2id)
        FileUtil.save_stat(furl2id, url2id)
        FileUtil.write_lines(fmap, lines, 'w')

    # ------------------------------------


    @staticmethod
    def atoi(text):
        return int(text) if text.isdigit() else text

    @staticmethod
    def natural_keys(text):
        '''
        alist.sort(key=natural_keys) sorts in human order
        http://nedbatchelder.com/blog/200712/human_sorting.html
        (See Toothy's implementation in the comments)
        '''
        return [ FileUtil.atoi(c) for c in re.split(r'(\d+)', text) ]

    @staticmethod
    def list_and_sort(fdir):
        paths = [os.path.join(fdir, fn) for fn in next(os.walk(fdir))[2]]
        paths.sort(key=FileUtil.natural_keys)
        return paths

    # ------------------------------------

    @staticmethod
    def mk_dirs(dirs):
        if not os.path.isdir(dirs): os.makedirs(dirs)

    @staticmethod
    def write_lines(file, lines, params, encoding='utf-8'): # "utf-8" "latin-1"
        print(f'writing {len(lines)} lines to {file}')
        FileUtil.mk_dirs(os.path.dirname(file)) 

        idx = 0
        with open(file, params, encoding=encoding) as f:
            for line in lines:
                f.write(line)
                f.write('\n')
                idx += 1
        return idx

    # ------------------------------------------------------------            

    @staticmethod
    def del_file(file):
        if os.path.isfile(file):
            os.remove(file)
    
    # ------------------------------------

    @staticmethod   
    def get_file_rows(file):
        print('read:', file, end=', ')    
        rows = []    
        with open(file, encoding="latin-1") as f:
            for line in f: rows.append(line.strip())
        print('rows:', len(rows))
        return rows	

    @staticmethod     
    def get_csv_rows(file, delim=','):            
        rows = []    
        with open(file, encoding="latin-1") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=delim)
            for row in csv_reader:
                rows.append(row)
        return rows

    @staticmethod  
    def to_csv(df, f, fmt='%Y-%m-%d', dcol='date'):
        df.to_csv(final_file, compression='gzip', index=False)
        #df.fillna(0.0).to_csv(f, header=True, index=False, encoding='utf-8')

    @staticmethod  
    def get_csv(f, fmt='%Y-%m-%d', dcol='date'):
        df = pd.read_csv(f)
        df[dcol] = pd.to_datetime(df[dcol], format=fmt)
        df = df.sort_values(by=dcol)
        return df.set_index(dcol)

    @staticmethod   
    def read_csv(file, sep=','):
        print(sys._getframe().f_code.co_name, file)
        df = pd.read_csv(file, sep=sep, encoding='utf-8')
        print('df:', df.shape)
        print(df.columns)
        return df

    @staticmethod
    def csv_to_parquet(file):
        print(sys._getframe().f_code.co_name, file)
        df = pd.read_csv(file, sep=',', encoding='utf-8')    
        print('to..')
        df.to_parquet(file.replace('.csv', '.parquet.gzip'), engine='fastparquet', compression='gzip')  

    @staticmethod
    def read_parquet(file, fmt='%Y-%m-%d %H:%M:%S:', dcol=None): #'%Y-%m-%dT%H:%M:%S.000Z'
        print(sys._getframe().f_code.co_name, file)
        df = pd.read_parquet(file, engine='fastparquet') #auto
        print('df:', df.shape)
        print(df.columns)
        if dcol is not None:
            df[dcol] = pd.to_datetime(df[dcol], format=fmt)
            df = df.sort_values(by=dcol)
            df = df.set_index(dcol)
        return df

    def json_to_csv(file):
        js = read_json(file)
        df = pd.DataFrame(columns=['value','index'])
        for i, k in enumerate(js):
            print(i, len(js))
            if 'MAX' == k: continue
            df.loc[len(df)] = [k,js[k]]
            #df.iloc[len(df)] = [k,js[k]]
        
        df.to_parquet(file.replace('.json', '.parquet.gzip'), engine='fastparquet', compression='gzip')


    @staticmethod
    def json_to_parquet(file):
        print(sys._getframe().f_code.co_name, file)
        js = FileUtil.read_json(file)
        del js['MAX']
        print('df..')
        df = pd.DataFrame(js.items(), columns=['a','b'])    
        print('to..')
        df.to_parquet(file.replace('.json', '.parquet.gzip'), engine='fastparquet', compression='gzip')

    @staticmethod          
    def read_json(file):
        with open(file) as js:
            return json.load(js) 

    @staticmethod          
    def write_json(file):
        with open(file, 'w') as js:
            json.dump(data, js, indent=2) 

    @staticmethod  
    def save_stat(file, stat):
        print(sys._getframe().f_code.co_name, file)
        if not os.path.isdir(os.path.dirname(file)): os.makedirs(os.path.dirname(file))
        with open(file, 'w') as fp: json.dump(stat, fp, indent=2)

    @staticmethod  
    def parse_wiki():
        import mwxml
        import glob
        import wikitextparser

        f = 'enwiktionary-20250401-pages-meta-current.xml.bz2' #tot: 10061853
        paths = glob.glob(f)

        def process_dump(dump, path):
            for page in dump:
                for revision in page:
                    txt = revision.text
                    l = len(txt) if txt is not None else 0

                    if txt is not None:
                        txt = wikitextparser.parse(txt).plain_text()
                        #txt = re.sub(r'[d+]', '', txt)
                        print('---\n')
                        print(txt)
                                    
                    #print(page.title)
                    yield page.id, revision.id, revision.timestamp, l

        i = 0
        for page_id, rev_id, rev_timestamp, rev_textlength in mwxml.map(process_dump, paths):
            #print("\t".join(str(v) for v in [page_id, rev_id, rev_timestamp, rev_textlength]))
            i += 1
            if i % 10000 == 0: print(i)
        print('tot:', i)
        
'''
data = {k: v for k, v in data.items() if re.match('.*(?=.*bbb.*)(?=.*ccc.*)(?!.*ddd.*).*',k)}

n = re.search(r'es_(.*?)\.csv\.gz', f).group(1)
            
'''