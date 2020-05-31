from enum import Enum

class Mode(Enum):
  AUTO = 'auto'
  COOL = 'cool'
  DRY = 'dry'
  FAN = 'fan_only'
  OFF = 'off'

class FanMode(Enum):
  AUTO = 'auto'
  HIGH = 'high'
  MEDIUM = 'medium'
  LOW = 'low'
  QUIET = 'quiet'

def mode_to_int(mode, mode_class):
  modes = [i.value for i in mode_class]
  return modes.index(mode)

def fan_mode_to_int(mode):
  modes = [i.value for i in FanMode]
  return modes.index(mode)

class FujiAC:

  def __init__(self):
    self.reset()

  def reset(self):
    self.temperature = 22
    self.previous_mode = Mode.OFF
    self.mode = Mode.OFF
    self.fan_mode = FanMode.AUTO
    self.swing = False
    self.air_clean = False

  def set_temperature(self, temperature):
    self.previous_mode = self.mode
    self.temperature = temperature

  def set_mode(self, mode):
    self.previous_mode = self.mode
    self.mode = Mode(mode)

  def set_fan_mode(self, mode):
    self.previous_mode = self.mode
    self.fan_mode = FanMode(mode)

  def toggle_swing(self):
    self.swing = not self.swing

  def toggle_airclean(self):
    self.air_clean = not self.air_clean

  def get_state(self, key=None):
    result = {
      'temperature': self.temperature,
      'mode': self.mode.value,
      'fan_mode': self.fan_mode.value,
      'swing': 'on' if self.swing else 'off',
      'air_clean': self.air_clean
    }
    return result[key] if key else result

  def get_rf_code(self):
    if self.mode == Mode.OFF:
      return 15001
    else:
      flag_on = int(self.previous_mode == Mode.OFF and self.mode != Mode.OFF)
      return int(f'{self.temperature}{mode_to_int(self.mode.value, Mode)}{mode_to_int(self.fan_mode.value, FanMode)}{flag_on}')
