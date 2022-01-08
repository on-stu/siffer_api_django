import pandas as pd
import requests
import re


class Size():
    def __init__(self, url, match=False, encoding='utf-8'):
        self.url = url
        self.match = match
        self.encoding = encoding

    def getSizeTable(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        data = requests.get(self.url, headers=headers)
        data.raise_for_status()
        data.encoding = self.encoding

        response = data.text
        print(response)
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
    def __init__(self, url, match, encoding):
        super().__init__(url=url, match=match, encoding=encoding)

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


class Xexymix(Size):
    def __init__(self, url, match=False, encoding='utf-8'):
        super().__init__(url, match=match, encoding=encoding)

    def injectNewUrl(self):
        index = re.search(r'\b(branduid=)\b', self.url)
        end = index.end()
        productCode = self.url[end:]
        for i in range(0, len(productCode)):
            if(productCode[i] == '&'):
                productCode = productCode[:i]
                break
        return productCode

    def run(self):
        productCode = self.injectNewUrl()
        self.url = 'https://fit4.cre.ma/xexymix.com/fit/products/{0}/combined_fit_product?nonmember_token='.format(
            productCode)
        result = self.getSizeTable()
        return result


class Leelin(Xexymix):
    def __init__(self, url, match=False, encoding='utf-8'):
        super().__init__(url, match=match, encoding=encoding)

    def run(self):
        productCode = self.injectNewUrl()
        self.url = 'https://fit3.cre.ma/leelin.co.kr/fit/products/{0}/size_detail'.format(
            productCode)
        result = self.getSizeTable()
        return result
