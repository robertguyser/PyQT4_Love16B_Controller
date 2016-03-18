class processClass(object):
   def __init( self, processSetValue=0.0, currentProcessValue=0.0):
      self.processSetValue = processSetValue
      self.currentProcessValue = currentProcessValue
      self.currentTime = 0
   def __del__(self):
      class_name = self.__class__.__name__
      print class_name, "processClass instance has been destroyed"
