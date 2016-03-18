import numpy as np
import datetime
import logging
from StringIO import StringIO
from PyQt4 import QtGui
from PyQt4.Qt import QString

class SequenceClass(object):
    def __init__(self, sequence_length=0):
        self.sequenceLength = sequence_length
        self.stepTemperatures = []
        self.stepTimesInSeconds = []
        self.steps = [self.stepTemperatures, self.stepTimesInSeconds]
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def add_step(self, temperature=0, time_in_seconds=0):
        self.logger.debug("add_step(temperature=%s, time_in_seconds=%s)" % (temperature, time_in_seconds))
        self.sequenceLength += 1
        self.stepTemperatures.append(float(temperature))
        self.stepTimesInSeconds.append(float(time_in_seconds))
        self.steps = [self.stepTemperatures, self.stepTimesInSeconds]

    def remove_step(self, step_to_remove):
        self.logger.debug("remove_step(%s)" % step_to_remove)
        try:
            self.stepTimesInSeconds.pop(step_to_remove)
            self.stepTemperatures.pop(step_to_remove)
            self.steps = [self.stepTemperatures, self.stepTimesInSeconds]
            self.sequenceLength -= 1
        except IndexError, e:
            error_msg = "Index Exception in removeStep(self, step=%s)= " % step_to_remove + str(e)
            self.logger.error(error_msg)
            return error_msg

    def sequence_length_seconds(self):
        seconds = float(sum(self.stepTimesInSeconds))
        return seconds

    def sequence_length_minutes(self):
        minutes = float(self.sequence_length_seconds() / 60)
        return minutes

    def sequence_length_hours(self):
        hours = float(self.sequence_length_minutes() / 60)
        return hours

    def sequence_length_formated(self):
        m, s = divmod(self.sequence_length_seconds(), 60)
        h, m = divmod(m, 60)
        return "%d:%02d:%02d" % (h, m, s)

    def length(self):
        return self.sequenceLength

    def get_step_temp(self, step):
        try:
            return self.stepTemperatures[step]
        except IndexError:
            error_msg = "Index Exception in getStepTemperature(self, step=%s)" % step
            self.logger.error(error_msg)
            return error_msg

    def get_step_time(self, step):
        try:
            return self.stepTimesInSeconds[step]
        except IndexError:
            error_msg = "Index Exception in getStepTime(self, step=%s)" % step
            self.logger.error(error_msg)
            return error_msg

    def reset_sequence(self, qtable = None):
        self.stepTemperatures = []
        self.stepTimesInSeconds = []
        self.steps = [self.stepTemperatures, self.stepTimesInSeconds]
        self.sequenceLength = 0

        if qtable is not None:
            qtable.reset()
            qtable.setRowCount(0)

    def steps_roc(self, step1, step2):
        try:
            seconds = float(self.stepTimesInSeconds[step1] + self.stepTimesInSeconds[step2])
            minutes = float(seconds / 60)
            return (self.stepTemperatures[step2] - self.stepTemperatures[step1]) / minutes
        except IndexError, e:
            error_msg = "Index Exception in rateOfChange(self, step1, step1)" + str(e)
            self.logger.error(error_msg)
            return error_msg

    def save_sequence(self, filename="sequence.csv"):
        self.steps = [self.stepTemperatures, self.stepTimesInSeconds]
        np.savetxt(filename, (
            np.c_[self.stepTemperatures, self.stepTimesInSeconds]),
                   delimiter=",", fmt="%.1f, %.1f", header="Time, Temperature, Saved: %s" % datetime.datetime.now())

    def load_sequence(self, filename="sequence.csv"):
        try:
            self.reset_sequence()
            loaded_data = np.genfromtxt((filename), unpack=True, delimiter=",", dtype=str)
            self.logger.info( "loaded_data: " + str(loaded_data.tolist()))
            self.stepTimesInSeconds = loaded_data[1].tolist()
            self.logger.info(loaded_data.dtype)
            self.stepTimesInSeconds = [float(x) for x in self.stepTimesInSeconds]
            self.stepTemperatures = loaded_data[0].tolist()
            self.stepTemperatures = [float(x) for x in self.stepTemperatures]
            self.steps = [self.stepTemperatures, self.stepTimesInSeconds]
            self.sequenceLength = (len(self.stepTemperatures))
            self.logger.info("load_sequence() self.steps: " + str(self.steps))
        except (SystemExit, KeyboardInterrupt):
            raise
        except Exception, e:
            self.logger.error('Failed to open file', exc_info=True)


    def get_sequence_qtable_from_array(self, array, qtable, rowcount):
        qtable.setRowCount(rowcount)
        for row in range(rowcount):
            for column in range(0,2):
                item = QtGui.QTableWidgetItem(QString("%1").arg(str(array[column][row])))
                qtable.setItem(row,column, item)
        qtable.resizeColumnsToContents()
