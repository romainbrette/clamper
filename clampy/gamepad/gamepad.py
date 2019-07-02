'''
Gamepad control
'''
import threading
import time
try:
    import inputs_gamepad as inputs
except ModuleNotFoundError: # I had to change the module name because of a conflict with Tensorflow
    import inputs

__all__ = ['GamepadReader', 'GamepadUpdater']

class GamepadReader(threading.Thread):
    '''
    Captures gamepad input and stores events and current state of buttons.
    This is necessary because reading is in blocking mode. (could this be changed?)
    '''
    def __init__(self, gamepad_number=0):
        self.event_container = []
        self.gamepad = inputs.devices.gamepads[gamepad_number]
        super(GamepadReader, self).__init__()
        self.terminated = False
        # Joystick 1
        self.X = 0.
        self.Y = 0.
        self.Z = 0.
        # Joystick 2
        self.RX = 0.
        self.RY = 0.
        self.RZ = 0.

    def run(self):
        while not self.terminated:
            event = self.gamepad.read()[0] # This blocks the thread
            if event.code == 'ABS_X':
                self.X = event.state/32768.
            elif event.code == 'ABS_Y':
                self.Y = event.state / 32768.
            elif event.code == 'ABS_Z':
                self.Z = event.state / 255.
            elif event.code == 'ABS_RX':
                self.RX = event.state/32768.
            elif event.code == 'ABS_RY':
                self.RY = event.state / 32768.
            elif event.code == 'ABS_RZ':
                self.RZ = event.state / 255.
            else:
                self.event_container.append(event)

    def stop(self):
        self.terminated = True

class GamepadUpdater(threading.Thread):
    '''
    Updates XYZ values modified by joysticks.
    Joystick position specifies the speed of change of variables.
    '''
    def __init__(self, gamepad_reader, rate=100.):
        '''
        Refresh rate in Hz.
        '''
        self.gamepad_reader = gamepad_reader
        self.period = 1./rate
        super(GamepadUpdater, self).__init__()
        self.terminated = False
        # Joystick 1
        self.X = 0.
        self.Y = 0.
        self.Z = 0.
        # Joystick 2
        self.RX = 0.
        self.RY = 0.
        self.RZ = 0.
        self.threshold = 0.1

    def run(self):
        while not self.terminated:
            if abs(self.gamepad_reader.X) > self.threshold:
                self.X += self.gamepad_reader.X
            elif abs(self.gamepad_reader.Y) > self.threshold:
                self.Y += self.gamepad_reader.Y
            elif abs(self.gamepad_reader.Z) > self.threshold:
                self.Z += self.gamepad_reader.Z
            elif abs(self.gamepad_reader.RX) > self.threshold:
                self.RX += self.gamepad_reader.RX
            elif abs(self.gamepad_reader.RY) > self.threshold:
                self.RY += self.gamepad_reader.RY
            elif abs(self.gamepad_reader.RZ) > self.threshold:
                self.RZ += self.gamepad_reader.RZ
            time.sleep(self.period)

    def stop(self):
        self.terminated = True
