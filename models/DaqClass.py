import numpy as np
import datetime
import logging
from PyQt4 import QtGui
from PyQt4.Qt import QString

#  Sample Model:
#  Sample # | Time(H:M:S) | Datetime | Temperature | Set Point | Error
class DaqClass(object):
    def __init__(self, samples=0, sample_temps=[], sample_times_ms=[],
            sample_datetimes=[], sample_setpoints=[], sample_errors=[]):

        self.logger = logging.getLogger(__name__)
        self.samples = samples
        self.sampleTemperatures = sample_temps
        self.sampleTimesInMs = sample_times_ms
        self.sampleSetPoints = sample_setpoints
        self.sampleErrors = sample_errors
        self.sampleDateTimes = sample_datetimes
        self.dataset = [range(0, self.samples), self.sampleTimesInMs, self.sampleDateTimes, self.sampleTemperatures,
                        self.sampleSetPoints, self.sampleErrors]

        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def get_sample_time_seconds(self, sample):
        seconds = float(self.sampleTimesInMs[sample]/1000)
        return seconds

    def update_dataset(self):
        self.dataset = [range(0, self.samples), self.sampleTimesInMs, self.sampleDateTimes, self.sampleTemperatures,
                        self.sampleSetPoints, self.sampleErrors]

    # Adds a sample to the dataset
    def add_sample(self, sample_temp=0, sample_time_ms=0,
                   sample_datetime=None, sample_setpoint=0, sample_error=None):
        if sample_datetime is None:
            sample_datetime = datetime.datetime.now()
        if sample_error is None:
            abserror = float(abs(sample_setpoint - sample_temp))
            sample_error = (abserror / sample_setpoint)
            sample_error = format(sample_error, '.3f')
        self.logger.debug("add_sample(sample_temp=%s, sample_time_ms=%s, sample_datetime=%s, "
                          "sample_setpoint=%s, sample_error=%s)" %
                          (sample_temp, sample_time_ms, sample_datetime, sample_setpoint, sample_error))
        self.samples += 1
        self.sampleTemperatures.append(float(sample_temp))
        self.sampleTimesInMs.append(float(sample_time_ms))
        self.sampleDateTimes.append(sample_datetime)
        self.sampleSetPoints.append(float(sample_setpoint))
        self.sampleErrors.append(float(sample_error))
        self.update_dataset()

    def length(self):
        return self.samples

    def get_sample_temp(self, sample):
        try:
            return self.sampleTemperatures[sample]
        except IndexError:
            error_msg = "Index Exception in get_sample_temp(self, sample=%s)" % sample
            self.logger.error(error_msg)
            return error_msg

    def get_sample_setpoint(self, sample):
        try:
            return self.sampleSetPoints[sample]
        except IndexError:
            error_msg = "Index Exception in get_sample_setpoint(self, sample=%s)" % sample
            self.logger.error(error_msg)
            return error_msg

    def get_sample_error(self, sample):
        try:
            return self.sampleErrors[sample]
        except IndexError:
            error_msg = "Index Exception in get_sample_error(self, sample=%s)" % sample
            self.logger.error(error_msg)
            return error_msg

    # Returns the time a sample was recorded in Ms
    def get_sample_time_ms(self, sample):
        try:
            return self.sampleTimesInMs[sample]
        except IndexError:
            error_msg = "Index Exception in get_sample_time_ms(self, sample=%s)" % sample
            self.logger.error(error_msg)
            return error_msg

    # Returns a formated string (h, m, s, ms) from miliseconds input
    def format_time(self, time_ms):
        s, ms = divmod(time_ms, 1000)
        m, s = divmod(time_ms/1000, 60)
        h, m = divmod(m, 60)
        return "%d:%02d:%02d:%02d" % (h, m, s, ms)

    # Method to return formated string from format_time(time_in_ms)
    def get_sample_time_formated(self, sample):
        sample_time = self.format_time(self.sampleTimesInMs[sample])
        return sample_time

    # Takes in an array and a QTWidgetTable reference, and then modifies the referenced QTWidgetTable
    def get_qtable_from_array(self, array, qtable):
        qtable.setRowCount(self.length())
        for row in range(self.length()):
            for column in range(0,6):
                if column == 1:
                    # adds last time to current time so it accumilates in the chart
                    sampletime_ms = int(self.get_sample_time_ms(row))
                    sampletime = self.format_time(sampletime_ms)
                    item = QtGui.QTableWidgetItem(sampletime)
                else:
                    item = QtGui.QTableWidgetItem(QString("%1").arg(str(array[column][row])))
                qtable.setItem(row,column, item)
        qtable.resizeColumnsToContents()

    def reset_daq(self, qtable = None):
        self.logger.debug("reset_daq(self, qtable)")
        self.samples = 0
        self.sampleTemperatures, self.sampleTimesInMs, self.sampleSetPoints = [], [], []
        self.sampleErrors, self.sampleDateTimes = [], []
        self.update_dataset()

        if qtable is not None:
            qtable.reset()
            #qtable.clear()
            qtable.setRowCount(0)

    def save_daq_data(self, filename="daq-data.csv"):
        np.savetxt(filename, (
            np.c_[range(0, self.samples), self.sampleTimesInMs, self.sampleDateTimes, self.sampleTemperatures,
                        self.sampleSetPoints, self.sampleErrors]),
                   delimiter=",", fmt='%i,%i,%s,%.1f,%.1f,%.3f', header="Sample, Time H:M:S:ms, Datetime, Temperature, Set Point, Error, Saved: %s" % datetime.datetime.now())

    def load_daq_data(self, filename="daq-data.csv"):
        self.reset_daq()
        loaded_data = np.genfromtxt((filename), unpack=True, delimiter=",", dtype=str)

        self.sampleTimesInMs = loaded_data[1].tolist()
        self.sampleDateTimes = loaded_data[2].tolist()
        self.sampleTemperatures = loaded_data[3].tolist()
        self.sampleSetPoints = loaded_data[4].tolist()
        self.sampleErrors = loaded_data[5].tolist()
        self.samples = len(loaded_data[1])
        self.update_dataset()
        del(loaded_data)
