import sys
import time
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import pyqtgraph as pg
import serial
import csv

windowSize = 50

# print(input_Raw_Data)
# np.asarray([[512], [512], [512], [512]] * windowSize

# ia_Data = [0] * windowSize
# ib_Data = [0] * windowSize
# ic_Data = [0] * windowSize
# id_Data = [0] * windowSize

class App(QtGui.QMainWindow):
   def __init__(self, parent=None):
      super(App, self).__init__(parent)

      #### Create Data Structures ####
      self.train_data_a = []
      self.train_data_b = []
      self.train_data_c = []

      self.train_labels = []
      self.keypressCount = 0
      self.currentLabel = 0
      self.ser = serial.Serial('/dev/cu.usbmodem1411', 9600)
      self.ser.flush()
      self.raw_channel_a  = [512.0] * windowSize
      self.raw_channel_b  = [512.0] * windowSize
      self.raw_channel_c  = [512.0] * windowSize
      # self.avg_channel_a  = [512.0] * windowSize
      # self.avg_channel_b  = [512.0] * windowSize
      # self.avg_channel_c  = [512.0] * windowSize
      # self.base_a         = 512.0
      # self.base_b         = 512.0
      # self.base_c         = 512.0

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
      self.raw_lineplot.setYRange(410, 590, padding=0)      
      self.raw_0 = self.raw_lineplot.plot(pen='y')
      self.raw_1 = self.raw_lineplot.plot(pen='r')
      self.raw_2 = self.raw_lineplot.plot(pen='g')
      # self.raw_3 = self.raw_lineplot.plot(pen='m')

      self.active_lineplot = self.canvas.addPlot()
      self.active_lineplot.setYRange(410, 590, padding=0)
      self.avg_0 = self.active_lineplot.plot(pen='y')
      self.avg_1 = self.active_lineplot.plot(pen='r')
      self.avg_2 = self.active_lineplot.plot(pen='g')
      # self.avg_3 = self.active_lineplot.plot(pen='m')


      #### Set Data  #####################

      self.x = np.linspace(0,1000., num=100)
      self.X,self.Y = np.meshgrid(self.x,self.x)

      self.counter = 0
      self.fps = 0.
      self.lastupdate = time.time()

      #### Start  #####################
      self._update()

   def keyPressEvent(self, event):
      if type(event) == QtGui.QKeyEvent:
         print("KEYPRESS: ", self.keypressCount)

         self.train_data_a += [self.raw_channel_a]
         self.train_data_b += [self.raw_channel_b]
         self.train_data_c += [self.raw_channel_c]

         train_label_temp = np.zeros(6, dtype=int)
         train_label_temp[self.currentLabel] = 1
         # print(self.train_labels)
         self.train_labels += [train_label_temp]
         # print('Keypress: {}'.format(self.keypressCount))

         self.keypressCount += 1
         if self.keypressCount % 100 == 0:
            print('GESTURE_CHANGE!')
            self.currentLabel += 1

         if self.keypressCount == 600:
            train_data = np.asarray([self.train_data_a, self.train_data_b, self.train_data_c])
            with open('DATA/train_data.dat', 'wb') as outputFile:
               np.save(outputFile, train_data)
            with open('DATA/train_labels.dat', 'wb') as outputFile:
               np.save(outputFile, self.train_labels)
            exit()
            

        

   def _update(self):
      lineData = self.ser.readline()
      readData = lineData.split(' ')

      # print("ReadData: ", readData)

      self.raw_channel_a.append(float(readData[0]))
      self.raw_channel_b.append(float(readData[1]))
      self.raw_channel_c.append(float(readData[2]))

      self.raw_channel_a.pop(0)
      self.raw_channel_b.pop(0)
      self.raw_channel_c.pop(0)


      # a_Average = np.average(a_Data)
      # b_Average = np.average(b_Data)
      # c_Average = np.average(c_Data)
      # d_Average = np.average(d_Data)

      # ia_Data.append(1.0 if a_Data[-1] > a_Average + 2.5 else (-1.0 if a_Data[-1] < a_Average - 2.5 else 0.0))
      # ib_Data.append(1.0 if b_Data[-1] > b_Average + 2.5 else (-1.0 if b_Data[-1] < b_Average - 2.5 else 0.0))
      # ic_Data.append(1.0 if c_Data[-1] > c_Average + 2.5 else (-1.0 if c_Data[-1] < c_Average - 2.5 else 0.0))
      # id_Data.append(1.0 if d_Data[-1] > d_Average + 2.5 else (-1.0 if d_Data[-1] < d_Average - 2.5 else 0.0))

      # ia_Data.pop(0)
      # ib_Data.pop(0)
      # ic_Data.pop(0)
      # id_Data.pop(0)

      self.raw_0.setData(np.asarray(self.raw_channel_a))
      self.raw_1.setData(np.asarray(self.raw_channel_b))
      self.raw_2.setData(np.asarray(self.raw_channel_c))
      # self.raw_3.setData(np.asarray(self.input_Raw_Data)[:,3])

      # self.avg_0.setData(np.asarray(self.avg_Data)[:,0])
      # self.avg_1.setData(np.asarray(self.avg_Data)[:,1])
      # self.avg_2.setData(np.asarray(self.avg_Data)[:,2])
      # self.avg_3.setData(np.asarray(self.avg_Data)[:,3])
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