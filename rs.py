# Install RsVisa
# https://scdn.rohde-schwarz.com/ur/pws/dl_downloads/dl_common_library/dl_manuals/gb_1/h/hmc804x/HMC804x_SCPI_ProgrammersManual_en_02.pdf
# https://scdn.rohde-schwarz.com/ur/pws/dl_downloads/dl_common_library/dl_manuals/gb_sg/nge/NGE100_User_Manual_en_04_Web.pdf

from RsInstrument import *

import serial.tools.list_ports

# Scope
# instr = RsInstrument('TCPIP::192.168.1.31::hislip0', id_query=True, reset=True)


class RsNGE103B:
  
  def __init__(self):

    self.comport = None
    ports = serial.tools.list_ports.comports()
    for port, desc, hwid in sorted(ports):
      if "ROHDE & SCHWARZ Device" in desc:
        self.comport = port[3:4]

    if (self.comport):
      self.instr = RsInstrument("ASRL" + str(self.comport) + "::INSTR")
      idn = self.instr.query_str('*IDN?')
      print('PSU found = ', idn)
   

  def set_voltage(self,v_ch,v_voltage):
    self.instr.write('INST OUT' + str(v_ch))
    self.instr.write('VOLT ' + str(v_voltage))  # Set volt

  def set_current_limmit(self,v_ch,v_current):
    self.instr.write('INST OUT' + str(v_ch))
    self.instr.write('CURR ' + str(v_current))  # Set current 

  def get_voltage(self,v_ch):
    self.instr.write('INST OUT' + str(v_ch))
    return round(float(self.instr.query_str('MEAS:VOLT?')),3)

  def get_current(self,v_ch):
    self.instr.write('INST OUT' + str(v_ch))
    return round(float(self.instr.query_str('MEAS:CURR?')),3)

  def set_output(self,v_state):
    self.instr.write('OUTP ' + str(v_state))

  def reset(self):
    self.instr.write('*RST')

  def close(self):
    self.instr.close()

psu = RsNGE103B()
try:

#  psu.reset()

  psu.set_voltage(1,24)
  psu.set_current_limmit(1,0.02)
  psu.set_output('ON')

  psu.set_voltage(2,23)
  psu.set_current_limmit(2,0.1)
  psu.set_output('OFF')

  psu.set_voltage(3,3.25)
  psu.set_output('OFF')




  print("Ch1 = ", psu.get_voltage(1), " V")
  print("Ch1 = ", psu.get_current(1), " A")

  print("Ch2 = ", psu.get_voltage(2), " V")
  print("Ch2 = ", psu.get_current(2), " A")

  print("Ch3 = ", psu.get_voltage(3), " V")
  print("Ch3 = ", psu.get_current(3), " A")


  psu.close()

except:
  print('ROHDE & SCHWARZ psu not found')






