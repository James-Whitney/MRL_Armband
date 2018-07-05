import sys
import time
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import pyqtgraph as pg
import serial
import csv

from scipy.spatial.distance import euclidean
from fastdtw import fastdtw
from multiprocessing import Pool


import scipy.signal as signal

pool = Pool(3)

windowSize = 75
winYmin = 450
winYmax = 550

time_window = -8
active_high = 530
active_low = 512

cali_samples = 2
print('Begin calibration by pressing \'Space\'')

class App(QtGui.QMainWindow):
   def __init__(self, parent=None):
      super(App, self).__init__(parent)

      #### Change these lines to select the port ####
      self.ser = serial.Serial('/dev/cu.usbmodem1411', 115200, parity=serial.PARITY_EVEN)
    #   self.ser = serial.Serial('COM3', 115200, parity=serial.PARITY_EVEN)
      self.ser.flush()

      #### Initalize windows ####
      self.raw_channel_a  = [512.0] * windowSize
      self.raw_channel_b  = [512.0] * windowSize
      self.raw_channel_c  = [512.0] * windowSize

      self.active_check   = [512.0]   * windowSize

      self.avg_channel_a = 512
      self.avg_channel_b = 512
      self.avg_channel_c = 512

      self.state = 0
      self.cali_counter = 0
      self.dtw_samples = []

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
      self.raw_lineplot.setXRange(0, windowSize, padding=0)      
      self.raw_lineplot.setYRange(winYmin, winYmax, padding=0) 

      self.raw_0 = self.raw_lineplot.plot(pen='y')
      self.raw_1 = self.raw_lineplot.plot(pen='r')
      self.raw_2 = self.raw_lineplot.plot(pen='g')

      self.active = self.raw_lineplot.plot(pen='m')

      self.avg_0 = self.raw_lineplot.plot(pen='y')
      self.avg_1 = self.raw_lineplot.plot(pen='r')
      self.avg_2 = self.raw_lineplot.plot(pen='g')

      # First, design the Butterworth filter
      self.B_filter, self.A_filter = signal.butter(2, 0.2, output='ba')

      #### Set Data  #####################
      self.x = np.linspace(0,1000., num=100)
      self.X,self.Y = np.meshgrid(self.x,self.x)

      self.counter = 0
      self.fps = 0.
      self.lastupdate = time.time()

      #### Start  #####################
      self._update()

   def dtw_compare(self, sample):
      mins = []
      for i in range(5):
         min_ = 10000
         for j in range(i * cali_samples, i * cali_samples + cali_samples):
            distance_a, path_a = fastdtw(np.convolve(self.dtw_samples[j][0][1::2], [-1, 1]), np.convolve(sample[0][1::2], [-1, 1]), dist=euclidean)
            distance_b, path_b = fastdtw(np.convolve(self.dtw_samples[j][1][1::2], [-1, 1]), np.convolve(sample[1][1::2], [-1, 1]), dist=euclidean)
            distance_c, path_c = fastdtw(np.convolve(self.dtw_samples[j][2][1::2], [-1, 1]), np.convolve(sample[2][1::2], [-1, 1]), dist=euclidean)
            dis = distance_a + distance_b + distance_c
            if dis < min_:
               min_ = dis
         mins.append(min_)
      print(mins)
      min_val = np.asarray(mins).min()
      if min_val < 100:
         i = mins.index(min_val)
         if i == 0:
            print('Wave Left')
         elif i == 1:
            print('Wave Right')
         elif i == 2:
            print('Double-Tap')
         elif i == 3:
            print('Fist')
         elif i == 4:
            print('Finger-Spread')
         else:
            print('NULL')

   def save_active(self, i):
      start = 0
      while self.active_check[start] == active_low:
         start += 1
         if start == windowSize:
            print('NO ACTIVE ZONE')
            self.cali_counter -= 1
            return
      end = start
      while self.active_check[end] == active_high:
         end += 1
         if end == windowSize:
            print('NO ISOLATED ZONE')
            self.cali_counter -= 1
            return
      self.dtw_samples.append([signal.filtfilt(self.B_filter, self.A_filter, self.raw_channel_a)[start:end],
                               signal.filtfilt(self.B_filter, self.A_filter, self.raw_channel_b)[start:end],
                               signal.filtfilt(self.B_filter, self.A_filter, self.raw_channel_c)[start:end]])
      return

   def keyPressEvent(self, event):
      if type(event) == QtGui.QKeyEvent:
         # print("KEYPRESS: ", self.keypressCount)
         if self.state == 0:
            self.state += 1
            print('Perform \'Wave Left\'...')
         elif self.state == 1:
            self.save_active(self.state)
            self.cali_counter += 1
            if self.cali_counter < cali_samples:
               print('Perform \'Wave Left\'...')
            else:
               self.state += 1
               print('Perform \'Wave Right\'...')
               self.cali_counter = 0
         elif self.state == 2:
            self.save_active(self.state)
            self.cali_counter += 1
            if self.cali_counter < cali_samples:
               print('Perform \'Wave Right\'...')
            else:
               self.state += 1
               print('Perform \'Double-Tap\'...')
               self.cali_counter = 0
         elif self.state == 3:
            self.save_active(self.state)
            self.cali_counter += 1
            if self.cali_counter < cali_samples:
               print('Perform \'Double-Tap\'...')
            else:
               self.state += 1
               print('Perform \'Fist\'...')
               self.cali_counter = 0
         elif self.state == 4:
            self.save_active(self.state)
            self.cali_counter += 1
            if self.cali_counter < cali_samples:
               print('Perform \'Fist\'...')
            else:
               self.state += 1
               print('Perform \'Finger-Spread\'...')
               self.cali_counter = 0
         elif self.state == 5:
            self.save_active(self.state)
            self.cali_counter += 1
            if self.cali_counter < cali_samples:
               print('Perform \'Finger-Spread\'...')
            else:
               self.state += 1
               print('Entering Live Mode:')
         else:
            print(len(self.dtw_samples))
            

   def _update(self):
      lineData = self.ser.readline()
      readData = lineData.split(' ')

      self.raw_channel_a.append(float(readData[0]))
      self.raw_channel_a.pop(0)

      self.raw_channel_b.append(float(readData[1]))
      self.raw_channel_b.pop(0)

      self.raw_channel_c.append(float(readData[2]))
      self.raw_channel_c.pop(0)

      std_0 = np.std(self.raw_channel_a[time_window:])
      std_1 = np.std(self.raw_channel_b[time_window:])
      std_2 = np.std(self.raw_channel_c[time_window:])

      if std_0 + std_1 + std_2 > 5.0:
         for i in range(time_window, -1,):
            self.active_check[i] = active_high
         self.active_check.append(active_high)
      else:
         self.avg_channel_a = np.average(self.raw_channel_a[time_window:])
         self.avg_channel_b = np.average(self.raw_channel_b[time_window:])
         self.avg_channel_c = np.average(self.raw_channel_c[time_window:])
         self.active_check.append(active_low)
      self.active_check.pop(0)


      if self.state > 5:
         if self.active_check[time_window - 1] > self.active_check[time_window]:
            start = time_window - 1
            while(self.active_check[start] == active_high):
               start -= 1
               if start == -1 * windowSize:
                  start = time_window - 1
                  break
            if (time_window - 1) - start > 5:
               self.dtw_compare([signal.filtfilt(self.B_filter, self.A_filter, self.raw_channel_a)[start:(time_window - 1)], 
                                 signal.filtfilt(self.B_filter, self.A_filter, self.raw_channel_b)[start:(time_window - 1)],
                                 signal.filtfilt(self.B_filter, self.A_filter, self.raw_channel_c)[start:(time_window - 1)]])

      self.raw_0.setData(signal.filtfilt(self.B_filter, self.A_filter, self.raw_channel_a))
      self.raw_1.setData(signal.filtfilt(self.B_filter, self.A_filter, self.raw_channel_b))
      self.raw_2.setData(signal.filtfilt(self.B_filter, self.A_filter, self.raw_channel_c))

      self.avg_0.setData(np.full(windowSize, self.avg_channel_a))
      self.avg_1.setData(np.full(windowSize, self.avg_channel_b))
      self.avg_2.setData(np.full(windowSize, self.avg_channel_c))

      self.active.setData(np.asarray(self.active_check))

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