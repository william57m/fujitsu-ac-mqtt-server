import codes
import syslog

from enum import Enum
from rpi_rf import RFDevice

class ExtendEnum(Enum):
  def to_int(self):
    items = [i.value for i in self.__class__]
    return items.index(self.value)

class Mode(ExtendEnum):
  AUTO = 'auto'
  COOL = 'cool'
  DRY = 'dry'
  FAN = 'fan_only'
  OFF = 'off'

class FanMode(ExtendEnum):
  AUTO = 'auto'
  HIGH = 'high'
  MEDIUM = 'medium'
  LOW = 'low'
  QUIET = 'quiet'


class FujiAC:

  def __init__(self, gpio=17):
    # Init AC state
    self.reset(False)

    # Init RF
    self.rfdevice = RFDevice(gpio)
    self.rfdevice.enable_tx()
    self.rfdevice.tx_repeat = 10

  def reset(self, commit=True):
    self.temperature = 22
    self.previous_mode = Mode.OFF
    self.mode = Mode.OFF
    self.fan_mode = FanMode.AUTO
    self.swing = False
    self.air_clean = False

    if commit:
      self.commit()

  def set_temperature(self, temperature):
    self.previous_mode = self.mode
    self.temperature = temperature
    if self.mode == Mode.OFF:
      self.set_mode(Mode.AUTO.value)
    self.commit()

  def set_mode(self, mode):
    self.previous_mode = self.mode
    self.mode = Mode(mode)
    self.commit()

  def set_fan_mode(self, mode):
    self.previous_mode = self.mode
    self.fan_mode = FanMode(mode)
    self.commit()

  def toggle_swing(self):
    self.swing = not self.swing
    self.commit(codes.CODE_TOGGLE_SWING)

  def toggle_airclean(self):
    self.air_clean = not self.air_clean
    self.commit(codes.CODE_TOGGLE_AIRCLEAN)

  def set_wing(self):
    self.commit(codes.CODE_SET_WING)

  def get_state(self, key=None):
    result = {
      'temperature': self.temperature,
      'mode': self.mode.value,
      'fan_mode': self.fan_mode.value,
      'swing': 'on' if self.swing else 'off',
      'air_clean': self.air_clean
    }
    return result[key] if key else result

  def __get_rf_code(self):
    if self.mode == Mode.OFF:
      return codes.CODE_TURN_OFF
    else:
      flag_on = int(self.previous_mode == Mode.OFF and self.mode != Mode.OFF)
      return int(f'{self.temperature}{self.mode.to_int()}{self.fan_mode.to_int()}{flag_on}')

  def commit(self, code=None):
    if code is None:
      code = self.__get_rf_code()
    print(f'SEND RF CODE: {code}')
    syslog.syslog(f'SEND RF CODE: {code}')
    self.rfdevice.tx_code(code)
