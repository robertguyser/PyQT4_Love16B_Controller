import models.SequenceClass
import time
import logging
from guppy import hpy
import random

h = hpy()
h.setref()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mySequence = models.SequenceClass.SequenceClass(sequence_length=0)

logger.info("Adding a bunch of Dummy Steps")
for x in range(0,5):
    temp = random.randrange(0.0,200.0,1)
    rantime = random.randrange(0,2000,1)
    mySequence.add_step(temp, rantime)
#mySequence.add_step(100.0, 8000)
#mySequence.add_step(100.0, 6200)
#mySequence.add_step(372.0, 6000)
#mySequence.add_step(0.0, 6000)


def debug_object():
    print "-------------------------------------------"
    print "Temps: " + str(mySequence.stepTemperatures)
    print "Times: " + str(mySequence.stepTimesInSeconds)
    print "Step Length: %d" % (mySequence.length())
    print "steps: %s" % mySequence.steps
    print "Seconds: %s" % (mySequence.sequence_length_seconds())
    print "Minutes: %s" % (mySequence.sequence_length_minutes())
    print "Hours: %f" % (mySequence.sequence_length_hours())
    print "Rate of Change: %s degrees/minute" % (mySequence.steps_roc(0, 1))
    print "Formated Length: %s" % mySequence.sequence_length_formated()
    print "-------------------------------------------"
    time.sleep(0)


debug_object()

mySequence.save_sequence()

mySequence.reset_sequence()

mySequence.load_sequence()

debug_object()

#mySequence.remove_step(99)
print h.heap()
