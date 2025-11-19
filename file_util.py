import os, sys, csv, time, re, json

class FileUtil():
    '''
    '''
    def __init__(self):
        pass

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
    def read_parquet(file):
        print(sys._getframe().f_code.co_name, file)
        df = pd.read_parquet(file, engine='fastparquet')
        print('df:', df.shape)
        print(df.columns)
        return df

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


        