import package.utilities.plotWidgetHelper
import models.ModbusWorkerClass
import models.ProcessClass
import models.DaqClass
import globals
from package.ui.modMonUI import Ui_MainWindow
from PyQt4 import QtCore, QtGui
import sys, logging, datetime
import qdarkstyle
import fancyqt.firefox
from PyQt4.QtCore import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LoveLogger(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)

        logger.info("LoveLogger() __Init__")
        self.setWindowTitle('Love 16B Data Logger')

        self.threadInstance = QThread() # no parent!
        self.modbusWorkerObject = models.ModbusWorkerClass.ModbusWorker() # no parent!
        self.modbusWorkerObject.moveToThread(self.threadInstance)
        self.threadInstance.start()

        self.connectButton.clicked.connect(self.openModbus)
        self.disconnectButton.clicked.connect(self.closeModbus)

        self.setSvButton.clicked.connect(self.setSV)
        self.getPvButton.clicked.connect(self.getThePV)
        self.getSvButton.clicked.connect(self.getTheSV)

        self.startButton.clicked.connect(self.startDaq)
        self.stopButton.clicked.connect(self.stopDaq)

        self.actionSave_Daq.triggered.connect(self.save_daq_file)
        #self.actionLoad_Daq.triggered.connect(self.load_daq_file)

        self.connect(self.modbusWorkerObject, SIGNAL("printPV(int)"), self.printPV)
        self.connect(self.modbusWorkerObject, SIGNAL("printSV(int)"), self.printSV)
        self.connect(self.modbusWorkerObject, SIGNAL("appendToDataText(QString)"), self.appendToDataText)
        self.connect(self.modbusWorkerObject, SIGNAL("fillPortList(QString)"), self.fillPortList)

        self.sampleIntervalDial.valueChanged[int].connect(self.sampleDialHandler)
        self.plottingIntervalDial.valueChanged[int].connect(self.plottingDialHandler)

        self.processObject = models.ProcessClass.processClass
        self.processObject.processSetValue = 0.0
        self.processObject.currentProcessValue = 0.0
        self.processObject.currentTime = 0

        self.svVerticalSlider.valueChanged[int].connect(self.svSliderHandler)

        # Instantiation of model classes
        self.myDAQ = models.DaqClass.DaqClass(0)

        self.sampleTimer = QtCore.QTimer(self)
        self.sampleTimer.timeout.connect(self.sampleTimerTimeout)

        self.plottingTimer = QtCore.QTimer(self)
        self.plottingTimer.timeout.connect(self.plotTimerTimeout)
        self.plottingTimer.stop()
        package.utilities.plotWidgetHelper.setupPlot(self)
        self.doStartup()

    def doStartup(self):
        QtCore.QMetaObject.invokeMethod(self.modbusWorkerObject, 'getComPorts', Qt.QueuedConnection,)
        self.plottingIntervalLabel.setText("Plotting Interval: " + str(self.plottingIntervalDial.value()))
        self.sampleIntervalLabel.setText("Sampling Interval: " + str(self.sampleIntervalDial.value()))
        self.DaqTableWidget.resizeColumnsToContents()
        self.pvLabel.setText("PV: 000.0")
        self.svLabel.setText("SV: 000.0")
        self.timeLabel.setText("Time: 0:0:0")
        self.actionSave_Daq.setEnabled(False)

    def sampleDialHandler(self):
        self.sampleTimer.setInterval(self.sampleIntervalDial.value())
        self.sampleIntervalLabel.setText("Sample Interval: " + str(self.sampleIntervalDial.value()))

    def plottingDialHandler(self):
        self.plottingTimer.setInterval(self.plottingIntervalDial.value())
        self.plottingIntervalLabel.setText("Plotting Interval: " + str(self.plottingIntervalDial.value()))

    def getThePV(self):
        QtCore.QMetaObject.invokeMethod(self.modbusWorkerObject, 'getPvFromWorker', Qt.QueuedConnection,)

    def getTheSV(self):
        QtCore.QMetaObject.invokeMethod(self.modbusWorkerObject, 'getSvFromWorker', Qt.QueuedConnection,)

    def fillPortList(self, portlist):
        self.portComboBox.addItem(portlist)
        logger.debug("fillPortList():" + portlist)

    def printPV(self, pv):
        self.processObject.currentProcessValue = pv
        self.dataTextEdit.append("<<<Got PV: " + str(float(self.processObject.currentProcessValue)/10))

    def printSV(self, sv):
        self.processObject.processSetValue = sv
        self.dataTextEdit.append("<<<Got SV: " + str(float(self.processObject.processSetValue)/10))

    def setSV(self):
        self.processObject.processSetValue = self.svVerticalSlider.value()
        SVdec = self.processObject.processSetValue
        QtCore.QMetaObject.invokeMethod(self.modbusWorkerObject, 'setSvAtWorker', Qt.QueuedConnection,
                                        QtCore.Q_ARG(float, self.processObject.processSetValue))
        self.appendToDataText(">>>Set SV: " + str(float(self.processObject.processSetValue)/10))

    def svSliderHandler(self):
        self.SvLcdNumber.display(float(self.svVerticalSlider.value())/10)

    def closeEvent(self, event):
        logger.info('closeEvent()')
        self.sampleTimer.stop()
        self.threadInstance.quit()
        self.threadInstance.wait()
        if self.modbusWorkerObject.ModBusPortState == True:
            self.modbusWorkerObject.closeModBusConnection()

    def openModbus(self):
        self.modbusWorkerObject.ModbusComPort = self.portComboBox.currentText()
        self.modbusWorkerObject.ModbusBaud = self.baudComboBox.currentText()
        self.modbusWorkerObject.ModbusBytesize = self.dataBitsComboBox.currentText()
        self.modbusWorkerObject.ModbusParity  = self.ParityComboBox.currentText()
        self.modbusWorkerObject.ModbusStopbits = self.stopBitsComboBox.currentText()
        self.modbusWorkerObject.ModbusTimeout = self.timoutDoubleSpinBox.value()
        try:
            QtCore.QMetaObject.invokeMethod(self.modbusWorkerObject, 'openModBusConnection', Qt.QueuedConnection,)
            self.sampleTimer.start(1000)
        except:
            logger.error("openModbus(): Error opening port")
        print self.modbusWorkerObject.ModbusComPort
        self.connectButton.setEnabled(False)
        self.disconnectButton.setEnabled(True)
        self.startButton.setEnabled(True)
        self.setSvButton.setEnabled(True)
        self.getSvButton.setEnabled(True)
        self.getPvButton.setEnabled(True)

    def appendToDataText(self, text):
        self.dataTextEdit.append(text)

    def sampleTimerTimeout(self):
        self.getThePV()
        self.getTheSV()
        the_temp = str(float(self.processObject.currentProcessValue)/10)
        the_sv = str(float(self.processObject.processSetValue)/10)
        self.pvLabel.setText("Pv: " + the_temp)
        self.svLabel.setText("Sv: " + the_sv)
        self.pvLcdNumber.display(the_temp)
        self.svLcdNumber.display(the_sv)

        if self.monitorScrollCheckBox.isChecked():
            self.dataTextEdit.moveCursor(QtGui.QTextCursor.End)

    def plotTimerTimeout(self):
        if globals.s < 59:
            globals.s += 1
        else:
            if globals.m < 59:
                globals.s = 0
                globals.m += 1
            elif globals.m == 59 and globals.h < 24:
                globals.h += 1
                globals.m = 0
                globals.s = 0
            else:
                self.plottingTimer.stop()
        time = "{0}:{1}:{2}".format(globals.h, globals.m, globals.s)

        self.timeLabel.setText("Time: " + time)
        self.daqSamplesTakenLabel.setText("# of Samples Taken: " + str(self.myDAQ.length()+1))
        logger.info("plotTimerTimeout(): Adding a Sample")
        self.dataTextEdit.append("plotTimerTimeout(): Adding a Sample")
        timer_ms = 100
        self.processObject.currentTime  += timer_ms
        elapsed_time = self.processObject.currentTime

        temp = (float(self.processObject.currentProcessValue)/10)
        setpoint = (float(self.processObject.processSetValue)/10)
        myDatetime = datetime.datetime.now()  # Gets the current Datetime
        self.myDAQ.add_sample(sample_temp=temp, sample_time_ms=elapsed_time, sample_datetime=myDatetime,
                              sample_setpoint=setpoint, sample_error=None)

        if self.daqScrollCheckBox.isChecked():
            self.DaqTableWidget.scrollToBottom()

        self.myDAQ.get_qtable_from_array(self.myDAQ.dataset, self.DaqTableWidget)


        tempYmax = max(self.myDAQ.sampleTemperatures)
        tempYmin = min(self.myDAQ.sampleTemperatures)
        timeXmax = max(self.myDAQ.sampleTimesInMs)
        timeXmin = min(self.myDAQ.sampleTimesInMs)
        maxSetPoint = max(self.myDAQ.sampleSetPoints)
        self.programCurveItem.set_data(self.myDAQ.sampleTimesInMs, self.myDAQ.sampleTemperatures)
        self.currentCurveItem.set_data(self.myDAQ.sampleTimesInMs, self.myDAQ.sampleSetPoints)
        self.curvewidget.plot.set_plot_limits(timeXmin,timeXmax+globals.chartTempYmargin, tempYmin,tempYmax+globals.chartTempYmargin)
        if (float(maxSetPoint) > tempYmax+globals.chartTempYmargin):
            self.curvewidget.plot.set_axis_limits(0,0,(maxSetPoint + globals.chartTempYmargin))
        self.programCurveItem.plot().replot()
        self.currentCurveItem.plot().replot()


    def startDaq(self):
        self.plottingTimer.setInterval(self.plottingIntervalDial.value())
        self.plottingTimer.start()
        running = self.plottingTimer.isActive()
        self.actionSave_Daq.setEnabled(True)
        if running:
            self.startButton.setEnabled(False)
            self.stopButton.setEnabled(True)

    def stopDaq(self):
        self.plottingTimer.stop()
        running = self.plottingTimer.isActive()
        if not running:
            self.startButton.setEnabled(True)
            self.stopButton.setEnabled(False)

    def closeModbus(self):
        self.sampleTimer.stop()
        self.stopDaq()
        self.modbusWorkerObject.closeModBusConnection()
        self.dataTextEdit.append("ModBus Connection Closed...")
        self.modbusWorkerObject.ModBusPortState = False
        self.connectButton.setEnabled(True)
        self.disconnectButton.setEnabled(False)
        self.startButton.setEnabled(False)
        self.setSvButton.setEnabled(False)
        self.getSvButton.setEnabled(False)
        self.getPvButton.setEnabled(False)
        logger.info("closeModbus(): Modbus is Closed")

    def save_daq_file(self):
        logger.info("save_daq_file()")
        self.statusbar.showMessage("Saving DAQ File...", 1500)
        self.myDAQ.save_daq_data()
        self.dataTextEdit.append("DAQ Data has been Saved...")

    def load_daq_file(self):
        logger.info("load_daq_file()")
        self.statusbar.showMessage("Loading DAQ File...", 1500)
        self.myDAQ.load_daq_data()
        self.myDAQ.get_qtable_from_array(self.myDAQ.dataset, self.daqTableWidget)
        self.dataTextEdit.append("DAQ Data has been Loaded...")


def run():
    app = QtGui.QApplication(sys.argv)
    # setup stylesheet
    if globals.darkUI:
        app.setStyleSheet(qdarkstyle.load_stylesheet(pyside=False))
    elif globals.fancyUI:
        app.setStyleSheet(fancyqt.firefox.style)
    form = LoveLogger()
    form.show()
    app.exec_()
    app.deleteLater()
    sys.exit(0)
