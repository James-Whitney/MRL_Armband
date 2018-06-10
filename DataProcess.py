import sys
import time
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import pyqtgraph as pg
import serial
import csv

a_Data = []
b_Data = []
c_Data = []
d_Data = []

ia_Data = []
ib_Data = []
ic_Data = []
id_Data = []

with open(sys.argv[1], 'r') as inputFile:
   fileReader = csv.reader(inputFile, delimiter=',')
   fileReader.next()
   for i, line in enumerate(fileReader):
      a_Data.append(float(line[1]))
      b_Data.append(float(line[3]))
      c_Data.append(float(line[5]))
      d_Data.append(float(line[7]))

   a_Data = np.asarray(a_Data)
   b_Data = np.asarray(b_Data)
   c_Data = np.asarray(c_Data)
   d_Data = np.asarray(d_Data)

   a_Average = np.average(a_Data)
   b_Average = np.average(b_Data)
   c_Average = np.average(c_Data)
   d_Average = np.average(d_Data)

   for i in range(0, len(a_Data)):
      ia_Data.append(1.0 if a_Data[i] > a_Average + 2.5 else (-1.0 if a_Data[i] < a_Average - 2.5 else 0.0))
      ib_Data.append(1.0 if b_Data[i] > b_Average + 2.5 else (-1.0 if b_Data[i] < b_Average - 2.5 else 0.0))
      ic_Data.append(1.0 if c_Data[i] > c_Average + 2.5 else (-1.0 if c_Data[i] < c_Average - 2.5 else 0.0))
      id_Data.append(1.0 if d_Data[i] > d_Average + 2.5 else (-1.0 if d_Data[i] < d_Average - 2.5 else 0.0))

class App(QtGui.QMainWindow):
   def __init__(self, parent=None):
      super(App, self).__init__(parent)

      #### Create Gui Elements ###########
      self.mainbox = QtGui.QWidget()
      self.setCentralWidget(self.mainbox)
      self.mainbox.setLayout(QtGui.QVBoxLayout())

      self.canvas = pg.GraphicsLayoutWidget()
      self.mainbox.layout().addWidget(self.canvas)

      self.label = QtGui.QLabel()
      self.mainbox.layout().addWidget(self.label)

      #  line plot
      self.raw_lineplot = self.canvas.addPlot()
      self.ha = self.raw_lineplot.plot(pen='y')
      self.hb = self.raw_lineplot.plot(pen='r')
      self.hc = self.raw_lineplot.plot(pen='g')
      self.hd = self.raw_lineplot.plot(pen='m')

      self.active_lineplot = self.canvas.addPlot()
      self.ia = self.active_lineplot.plot(pen='y')
      self.ib = self.active_lineplot.plot(pen='r')
      self.ic = self.active_lineplot.plot(pen='g')
      self.id = self.active_lineplot.plot(pen='m')


      #### Set Data  #####################

      self.x = np.linspace(0,1000., num=100)
      self.X,self.Y = np.meshgrid(self.x,self.x)

      self.counter = 0
      self.fps = 0.
      self.lastupdate = time.time()

      #### Start  #####################
      self._update()

   def _update(self):
      
      self.ha.setData(np.asarray(a_Data))
      self.hb.setData(np.asarray(b_Data))
      self.hc.setData(np.asarray(c_Data))
      self.hd.setData(np.asarray(d_Data))
      self.ia.setData(np.asarray(ia_Data))
      self.ib.setData(np.asarray(ib_Data))
      self.ic.setData(np.asarray(ic_Data))
      self.id.setData(np.asarray(id_Data))

      now = time.time()
      dt = (now-self.lastupdate)
      if dt <= 0:
         dt = 0.000000000001
      fps2 = 1.0 / dt
      self.lastupdate = now
      self.fps = self.fps * 0.9 + fps2 * 0.1
      tx = 'Mean Frame Rate:  {fps:.3f} FPS'.format(fps=self.fps )
      self.label.setText(tx)
      QtCore.QTimer.singleShot(1, self._update)
      self.counter += 1


if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    thisapp = App()
    thisapp.show()
    sys.exit(app.exec_())