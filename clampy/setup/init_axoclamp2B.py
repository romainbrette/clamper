'''
Initializes data acquisition on the rig.
This is specific of the hardware configuration.
'''
from clampy import *
from clampy.devices.gains.axoclamp2b import gains
from clampy.setup.units import *

board = NI()

board.set_analog_input('Im', channel=0, gain=gains(0.1)['Im'])
board.set_analog_input('I2', channel=1, gain=gains(1)['I2'])
board.set_analog_input('V2', channel=2, gain=gains(1)['V2'])
board.set_analog_input('V1', channel=3, gain=gains(0.1)['10Vm'])  # Vm

board.set_analog_output('Ic1', channel=2, gain=gains(0.1)['ExtME1'])  # Current clamp command
board.set_analog_output('Ic2', channel=0, gain=gains(1)['ExtME2'])  # Current clamp command
board.set_analog_output('Vc', channel=1, gain=gains(1)['ExtVC']) # Voltage clamp command

board.set_aliases(I='Ic1', Ic='Ic1', I1='Ic1', I2='Ic2', V='V1', I_TEVC='I2')

dt = 0.1 * ms
board.sampling_rate = 1. / dt

#amplifier = board
