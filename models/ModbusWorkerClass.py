import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus_rtu as modbus_rtu
from PyQt4 import QtCore
from PyQt4.QtCore import SIGNAL
import time, serial
from numpy import float
from package.utilities.serialUtils import full_port_name, enumerate_serial_ports


class ModbusWorker(QtCore.QObject):
    def __init__(self, ModbusComPort = "COM5", ModbusBaud= 38400, ModbusBytesize=8, ModbusParity="N", ModbusStopbits=1, ModbusTimeout=.1):
        super(ModbusWorker, self).__init__()
        self.ModbusComPort = ModbusComPort
        self.ModbusBaud = ModbusBaud
        self.ModbusBytesize = ModbusBytesize
        self.ModbusParity = ModbusParity
        self.ModbusStopbits = ModbusStopbits
        self.ModbusTimeout = ModbusTimeout


    finished = QtCore.pyqtSignal()
    logger = modbus_tk.utils.create_logger("console")

    @QtCore.pyqtSlot()
    def getPvFromWorker(self):
        print "Worker.getPvFromWorker()"
        try:
            #print ("thread: getPV(): try...")
            PV = (self.master.execute(1, cst.READ_HOLDING_REGISTERS , 4096, 1))
            print PV
            self.emit(SIGNAL('printPV(int)'), PV[0])
        except modbus_tk.modbus.ModbusError, e:
            self.logger.error("%s- Code=%d" % (e, e.get_exception_code()))
        time.sleep(0)
        self.finished.emit()

    @QtCore.pyqtSlot()
    def getSvFromWorker(self):
        print "Worker.getSvFromWorker()"
        try:
            #print ("thread: getSV(): try...")
            SVin = (self.master.execute(1, cst.READ_HOLDING_REGISTERS , 4097, 1))
            print SVin
            self.emit(SIGNAL('printSV(int)'), SVin[0])
        except modbus_tk.modbus.ModbusError, e:
            self.logger.error("%s- Code=%d" % (e, e.get_exception_code()))
        time.sleep(0)
        self.finished.emit()

    @QtCore.pyqtSlot(float)
    def setSvAtWorker(self, setValueIn):
        print "Worker.setSvAtWorker()" + str(setValueIn)
        try:
            self.logger.info(self.master.execute(1, cst.WRITE_SINGLE_REGISTER, 4097, output_value=(setValueIn)))
        except modbus_tk.modbus.ModbusError, e:
            self.logger.error("%s- Code=%d" % (e, e.get_exception_code()))
        time.sleep(0)
        self.finished.emit()

    @QtCore.pyqtSlot()
    def getComPorts(self):
        for portname in enumerate_serial_ports():
            portnames = portname
            self.emit(SIGNAL('fillPortList(QString)'), portname)
            #print "getComPorts(): " + portnames

    @QtCore.pyqtSlot()
    def openModBusConnection(self):
        self.sendToTextBox(self.ModbusComPort + " baud: " + str(self.ModbusBaud) + " bytesize: " + str(self.ModbusBytesize) + " parity: "+ str(self.ModbusParity[0]) + " timeout: " + str(self.ModbusTimeout))
        self.modSerial = serial.Serial(port=str(self.ModbusComPort), baudrate=self.ModbusBaud, bytesize=int(self.ModbusBytesize),
                                       parity=str(self.ModbusParity[0]),stopbits=int(self.ModbusStopbits), xonxoff=0, timeout=(self.ModbusTimeout))
        #modSerial.setDTR(0)
        #time.sleep(.5)
        self.master = modbus_rtu.RtuMaster(self.modSerial)
        self.master.set_timeout(.2)
        self.master.set_verbose(True)
        #print(self.master._is_opened)

    def sendToTextBox(self, text):
        self.emit(SIGNAL('appendToDataText(QString)'), text)