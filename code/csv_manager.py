import pandas as pd

class CscManager:
    counter = 0
    list_of_writing = [0,1,2,3,4,5,7,10,15,20,25,30,35,40,50,60,70,80,90,100,110,120,140,160,180,200,220,250,275,300,325,350,375,400,450,500,550,600,650,700,750,800,850,900,950,1000]
    def __init__(self, name = 0):
        self.name = "code/result/name{}.csv".format(name)
        self.data = pd.DataFrame()
        self.read()

    def read(self):
        try: self.data = pd.read_csv(self.name)
        except: self.data = pd.DataFrame()
        return self.data

    def write_sometimes(self):
        if CscManager.counter < 1000:
            if CscManager.counter in CscManager.list_of_writing:
                self.write()
        else:
            if CscManager.counter % 100 == 0:
                self.write()
        CscManager.counter+=1
    def write(self):
        if not self.data.empty:
            self.data.to_csv(self.name, index=False)

    def set_data_from_list(self, two_dimension_list = [[1,2,3],[4,5,6]], columns = ["C1","C2","C3"]):
        self.set_data(pd.DataFrame(data = two_dimension_list, columns=columns))
    def set_data(self, df: pd.DataFrame):
        self.data = df
    def set_data_by_dicts(self, data):
        self.data = pd.DataFrame(data)

    def extend_row(self, to_add = {"C1":[5, 5], "C4":[5, 7]}):
        df = pd.DataFrame(to_add)
        self.data = self.data.append(df, ignore_index=True)
    def extend_column(self, name = "C7", value = [5,9]):
        self.data[name] = value

    def extend_row_by_dicts(self, *args, **kwargs):
        big_dict = {}
        for a in args:
            big_dict.update(**a)
        for k in kwargs:
            big_dict.update(**kwargs[k])
        self.extend_row(big_dict)