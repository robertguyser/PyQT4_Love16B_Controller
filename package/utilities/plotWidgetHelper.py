from guidata.qt.QtGui import QPushButton,QSlider,QGridLayout,QLabel,QFont
import package.globals as globals
from PyQt4 import QtGui
from guiqwt.builder import make
from guiqwt.plot import CurveDialog, CurveWidget, BasePlot, ImageWidget, ImageDialog

def setupPlot(self):
    self.toolbar = self.addToolBar("data")
    self.axisLabelfont = QFont()
    self.color = QtGui.QColor(212,123,123)
    self.alarmPointCursor = make.hcursor(100, label='alarm = %d')
    self.programCurveItem = make.curve([], [],"Temperature",color='b', linewidth=6)
    self.currentCurveItem = make.curve([], [],"Set Point",color='r', linewidth=6)
    self.alarmPointCursor = make.hcursor(globals.alarmSetPoint, label='alarm = %d')
    self.disp2 = make.label( "Max Temperature: ", "T", (-100, 10), "L",title="Max Temp")
    self.legend = make.legend("TR")
    self.alarmPointCursor.set_pos(10,globals.timeXmax+20)
    self.programCurveItem.set_data(globals.tempY, globals.timeX)
    self.axisLabelfont.setPointSize(14)
    self.axisLabelfont.setBold(True)
    #self.curvewidget.plot.set_plot_limits_synchronised(tempYmin,tempYmax+chartTempYmargin,timeXmin,timeXmax+chartTempYmargin)
    self.curvewidget.plot.set_axis_font("left", self.axisLabelfont)
    self.curvewidget.plot.set_axis_font("bottom", self.axisLabelfont)
    self.curvewidget.plot.set_axis_title(BasePlot.X_BOTTOM, globals.chartXlabel)
    self.curvewidget.plot.set_axis_title(BasePlot.Y_LEFT,globals.chartYlabel)
    self.curvewidget.add_toolbar(self.toolbar, "default")
    self.curvewidget.register_all_curve_tools()
    self.curvewidget.plot.add_item(self.alarmPointCursor)
    self.curvewidget.plot.add_item(self.currentCurveItem)
    self.curvewidget.plot.add_item(self.programCurveItem)
    self.curvewidget.plot.set_antialiasing(True)
    self.curvewidget.plot.add_item(self.legend)
    self.curvewidget.plot.add_item(self.disp2)
    self.curvewidget.get_itemlist_panel().show()
    self.programCurveItem.plot().replot()
    self.currentCurveItem.plot().replot()