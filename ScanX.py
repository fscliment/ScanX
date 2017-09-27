# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 23:12:21 2017

@author: fscliment
"""

import os
import quandl
global data
global val
global vals

os.environ['PYQTGRAPH_QT_LIB']='PyQt5'
import pyqtgraph as pg
from PyQt5 import QtCore, QtGui

class CandlestickItem(pg.GraphicsObject):
    def __init__(self, data):
        pg.GraphicsObject.__init__(self)
        self.data = data  ## data must have fields: time, open, close, min, max
        self.generatePicture()
    
    def generatePicture(self):
        self.picture = QtGui.QPicture()
        p = QtGui.QPainter(self.picture)
        p.setPen(pg.mkPen('w'))
        w = (self.data.index[1].value - self.data.index[0].value) / 3.
        for (self.data.index, self.data.Open, self.data.Close, self.data.High, self.data.Low) in self.data:
            p.drawLine(QtCore.QPointF(t, min), QtCore.QPointF(t, max))
            if open > close:
                p.setBrush(pg.mkBrush('r'))
            else:
                p.setBrush(pg.mkBrush('g'))
            p.drawRect(QtCore.QRectF(t-w, open, w*2, close-open))
        p.end()
    
    def paint(self, p, *args):
        p.drawPicture(0, 0, self.picture)
    
    def boundingRect(self):
        return QtCore.QRectF(self.picture.boundingRect())
        
def download_quandl_contract(contract):
   data = quandl.get(contract)
   global prices
   return data

data = [  ## fields are (time, open, close, min, max).
    (1., 10, 13, 5, 15),
    (2., 13, 17, 9, 20),
    (3., 17, 14, 11, 23),
    (4., 14, 15, 5, 19),
    (5., 15, 9, 8, 22),
    (6., 9, 15, 8, 16),
]

if __name__ == '__main__':
    
    repo = 'CHRIS'    
    code = ['CME_UL2']
    quandl.ApiConfig.api_key = 'cTPr7xF4zKL_F73aGjyi'
    for val in code:
    
        contract = repo + "/" + val
        print(contract)
        prices = download_quandl_contract(contract)
        prices=prices.drop(prices.columns[[5,6,7]], axis=1)
        #prices.to_csv("./"+ val,sep=' ', Index=True)
        item = CandlestickItem(prices)
        plt = pg.plot()
        plt.addItem(item)
        
        QtGui.QApplication.exec_()
