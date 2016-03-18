# A ModBus Controller for the Love 16B PID Controller
##### Created with Python 2.7PyQT4, guiqwt plotting library, and modbus_tk
<img src="https://raw.githubusercontent.com/robertguyser/PyQT4_Love16B_Controller/master/love16bscreenshot.PNG" alt="Love16B Controller Screenshot" width="233" height="217">
Software to allow the control, recording and analysis of Love 16B PID controllers

###### Features
* Communicates with the Love 16B PID temperature controller box, and likely other controllers
* Plotting and sampling interval settings
* Recording of control data with date stamps and statistical metadata
* Configurable ModBus ports for potential use with other PID boxes
* Monitor tab shows SV and PV in large LCD displays
* Save DAQ data as CSV file
* Export plot in PDF and SVG vector image formats
* Print plot diagrams
* Load DAQ data for printing or analysis

###### To Add
* Ramp and dwell control 
* Program saving, editing, display and loading
* Rate of change DAQ collection
* Love 16B pattern reading and writing
* Error and rate of change plotting
* Additional setting controls
* Farenheit Mode
* Profile based PID controller abstraction to allow easy hardware integration
* Clean up the messiness