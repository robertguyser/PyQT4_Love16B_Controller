import models.DaqClass
import datetime
import logging
import random
from guppy import hpy


h = hpy()
h.setref()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

myDAQ = models.DaqClass.DaqClass(0)


oneSecondInMs = 1000
oneHourInMs = 60 * (60 * 1000)  # One hour + 500ms in ms

aDatetime = datetime.datetime(2016, 3, 14, 2, 4, 47, 678000)

logger.info("Adding a few dummy Samples")
for x in range(0, 5):
    myDatetime = datetime.datetime.now()  # Gets the current Datetime
    temp = random.randrange(0.0, 200.0, 1)
    myDAQ.add_sample(sample_temp=temp, sample_time_ms=oneSecondInMs, sample_datetime=myDatetime,
                     sample_setpoint=150, sample_error=None)


def debug_object():
    print "-------------------------------------------"
    print "Temps: " + str(myDAQ.sampleTemperatures)
    print "Times (ms): " + str(myDAQ.sampleTimesInMs)
    print "Datetimes: " + str(myDAQ.sampleDateTimes)
    print "Set Points:" + str(myDAQ.sampleSetPoints)
    print "Errors (%): " + str(myDAQ.sampleErrors)
    print "Number of Samples: %d" % (myDAQ.length())
    print "dataset: %s" % myDAQ.dataset
    print "Sample 0 ms: %s" % (myDAQ.get_sample_time_ms(0))
    print "Sample 0 Temperature: %s" % (myDAQ.get_sample_temp(0))
    print "Sample 0 Set Point: %s" % (myDAQ.get_sample_setpoint(0))
    print "Sample 0 Error: %s" % (myDAQ.get_sample_error(0)*100) + '%'
    print "Sample 0 Formated Time: %s" % myDAQ.get_sample_time_formated(0)
    print "-------------------------------------------"


debug_object()

print str(myDAQ.sampleDateTimes[0])

print myDAQ.get_sample_time_seconds(0)
print myDAQ.get_sample_time_formated(0)

#print h.heap()