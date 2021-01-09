from openpyxl import load_workbook
from openpyxl import Workbook

class ExcelManager:
    def __init__(self, name = "code/name(0).xlsx"):
        self.name = name
        self.open_book()

    def open_book(self):
        try:
            self.wb = load_workbook(filename = self.name, data_only=True)
        except:
            self.wb = Workbook()
            self.wb.save(filename = self.name)
            self.wb = load_workbook(filename=self.name, data_only=True)

        self.letter = self.wb["Sheet"]

    def read(self):
        i = 0
        last_row = []
        first = 0
        for row in self.letter.iter_rows(min_row = 1):
            i += 1
            last_row = []
            first = 0
            for j in range(len(row)):
                if j == 0:
                    first = row[j].value
                else:
                    last_row.append(row[j].value)
        return first, last_row

    def write_data2D(self, hight=1, weights=[[0,0], [1,1]]):
        new_mas = []
        for i in range(len(weights)):
            for j in range(len(weights[i])):
                new_mas += weights[i][j]
        self.write_data(hight, new_mas)
    def write_data(self, hight = 1, weights = [0]):
        data_to_end = [hight] + weights
        self.letter.append(data_to_end)
        self.save_data()
    def save_data(self):
        self.wb.save(self.name)
        self.open_book()