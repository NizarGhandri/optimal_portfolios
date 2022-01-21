import os
import pandas as pd













class MarketWeighted():


    def __init__(self, cfg):  
        self.cfg = cfg  
        self.data = self.load_data()


    def load_data(self):
        return self.preprocess(pd.concat([pd.read_parquet(os.path.join(self.cfg.data_dir, f))["Close"] for f in os.listdir(self.cfg.data_dir)]))

    def preprocess(self, x, percent0=0.7, percent1=0.2):
        tmp = x.dropna(thresh=int(percent0*x.shape[1])).dropna(axis=1, thresh=int(percent1*x.shape[0])).fillna(method="ffill")
        dropped = set(x.columns) - set(tmp.columns) 
        logging.info("Preprocessing dropped the following stocks %s ".format(["-".join(list(dropped))]))
        return tmp
        #return x

    def __call__(self):
        #self.data = dataframe.from_pandas(self.data, npartitions=os.cpu_count())
        return ((self.data.diff()/self.data) + 1).tail(-1).cumprod()#.mean(axis=1)


     

