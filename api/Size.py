import pandas as pd
import requests


class Size():
    def __init__(self, url, match=False):
        self.url = url
        self.match = match

    def getSizeTable(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        response = requests.get(self.url, headers=headers).text.encode('utf-8')

        if self.match:
            table = pd.read_html(response, header=0,
                                 encoding='utf-8', match=self.match)[0]
        else:
            table = pd.read_html(response, header=0,
                                 encoding='utf-8', match=self.match)[0]

        df = table.to_dict('records')

        return df

    def run(self):
        result = self.getSizeTable()
        return result


class Musinsa(Size):
    def __init__(self, url, match):
        super().__init__(url=url, match=match)

    def removeNaN(self, df):
        for item in df:
            for i in item:
                if str(item[i]) == 'nan' or str(item[i]) == 'NaN':
                    item[i] = ''
        return df

    def optimizeMusinsa(self, df):
        df = df[1:]
        for item in df:
            currentItem = list(item)
            for i in currentItem:
                if 'Unnamed:' in i:
                    del item[i]
        return df

    def run(self):
        df = self.getSizeTable()
        df = self.removeNaN(df)
        result = self.optimizeMusinsa(df)
        return result
