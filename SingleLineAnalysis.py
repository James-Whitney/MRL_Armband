import sys
import time
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np

import pyqtgraph as pg
import serial

ser = serial.Serial('/dev/cu.usbmodem1411', 9600)

ser.flush()

plotLength = 400

a_LongRun = 512.0

a_Data = [512] * plotLength
a_LongRunPlot = [512] * plotLength
# a_fftPlot = [512] * plotLength
# b_Data = [512] * plotLength
# c_Data = [512] * plotLength
# d_Data = [512] * plotLength

ia_Data = [512] * plotLength
# ib_Data = [512] * plotLength
# ic_Data = [512] * plotLength
# id_Data = [512] * plotLength

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
      self.raw_lineplot.setYRange(420, 580, padding=0)
      self.a_raw = self.raw_lineplot.plot(pen='y')
      self.a_avg = self.raw_lineplot.plot(pen='r')
      # self.hb = self.raw_lineplot.plot(pen='r')
      # self.hc = self.raw_lineplot.plot(pen='g')
      # self.hd = self.raw_lineplot.plot(pen='m')

      self.active_lineplot = self.canvas.addPlot()
      self.ia = self.active_lineplot.plot(pen='y')
      # self.a_fft = self.active_lineplot.plot(pen='g')
      # self.ib = self.active_lineplot.plot(pen='r')
      # self.ic = self.active_lineplot.plot(pen='g')
      # self.id = self.active_lineplot.plot(pen='m')


      #### Set Data  #####################

      self.x = np.linspace(0,1000., num=100)
      self.X,self.Y = np.meshgrid(self.x,self.x)

      self.counter = 0
      self.fps = 0.
      self.lastupdate = time.time()

      #### Start  #####################
      self._update()

   def _update(self):
      global a_LongRun, a_LongRunPlot
      lineData = ser.readline()
      readData = lineData.split(' ')

      a_Data.append(float(readData[0]))
      a_Data.pop(0)
      # b_Data.append(float(readData[1]))
      # b_Data.pop(0)
      # c_Data.append(float(readData[2]))
      # c_Data.pop(0)
      # d_Data.append(float(readData[3]))
      # d_Data.pop(0)

      # a_Average = np.average(a_Data)
      # b_Average = np.average(b_Data)
      # c_Average = np.average(c_Data)
      # d_Average = np.average(d_Data)

      ia_Data.append(1.0 if a_Data[-1] > a_Average + 2.5 else (-1.0 if a_Data[-1] < a_Average - 2.5 else 0.0))
      # ib_Data.append(1.0 if b_Data[-1] > b_Average + 2.5 else (-1.0 if b_Data[-1] < b_Average - 2.5 else 0.0))
      # ic_Data.append(1.0 if c_Data[-1] > c_Average + 2.5 else (-1.0 if c_Data[-1] < c_Average - 2.5 else 0.0))
      # id_Data.append(1.0 if d_Data[-1] > d_Average + 2.5 else (-1.0 if d_Data[-1] < d_Average - 2.5 else 0.0))

      a_LongRun = ((99.0 * a_LongRun) + a_Data[-1]) / 100.0
      a_LongRunPlot.append(a_LongRun)
      a_LongRunPlot.pop(0)

      # ia_Data.pop(0)
      # ib_Data.pop(0)
      # ic_Data.pop(0)
      # id_Data.pop(0)
      a_DataNP = np.asarray(a_Data)
      # a_FFTNP = abs(np.fft.fft(a_DataNP))

      self.a_raw.setData(a_DataNP)
      self.a_avg.setData(np.asarray(a_LongRunPlot))
      # self.a_fft.setData(a_FFTNP)
      # self.hb.setData(np.asarray(b_Data))
      # self.hc.setData(np.asarray(c_Data))
      # self.hd.setData(np.asarray(d_Data))
      # self.ia.setData(np.asarray(ia_Data))
      # self.ib.setData(np.asarray(ib_Data))
      # self.ic.setData(np.asarray(ic_Data))
      # self.id.setData(np.asarray(id_Data))


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