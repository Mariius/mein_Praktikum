from enum import Enum, EnumMeta

class MyMeta(EnumMeta):
    def __contains__(self, other):
        enum_list = [x.upper() for x in self.list()]
        if isinstance(other, str):
            if other.upper() in enum_list:
                return True
            else:
                return False
        else:
            try:
                return isinstance(other, self)
            except:
                raise NotImplementedError("Type '{}' not implemented!".format(type(other)))
            
class ExtendedEnum(Enum, metaclass = MyMeta):

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))

    @classmethod
    def has_key(cls, key):
        ''' returns True if enum has the special key '''
        return key in cls.__members__

    @classmethod
    def keys(cls):
        ''' answer with the list of keys '''
        return list(cls.__members__.keys())

    # def equals(self, string):
    #     ''' returns True if the name of the enum matches '''
    #     return self.name == string

    def __str__(self):
        return str(self.value)

    def __eq__(self, other):
        if isinstance(other, str):
            return self.value == other or self.value.upper() == other.upper()
        else:
            return self.__class__ is other.__class__ and other.value == self.value or self.__class__ is other.__class__ and other.value.upper() == self.value.upper()

    def describe(self):
         # self is the member here
        return self.name, self.value

class ProjectName(ExtendedEnum):
    UNKNOWN     = 'unknown'
    MAXWELL     = 'maxwell'   # pl600
    CAMPBELL    = 'campbell'  # pl650
    FARADAY     = 'faraday'   # plxxx
    HELMHOLTZ   = 'helmholtz' # m6

class DeviceType(ExtendedEnum):
    UNKNOWN     = 'unknown'
    NA          = ''          # not applicable
    PL600       = 'pl600'     # maxwell
    PL650       = 'pl650'     # campbell

class DeviceVariant(ExtendedEnum):
    UNKNOWN     = 'unknown'
    NA          = ''          # not applicable
    R           = 'R'         # remote (without display)
    RC          = 'RC'        # remote (without display) and short version
    RC24V       = 'RC-24V'    # remote (without display) and short version with external power supply 24VDC

class ModuleType(ExtendedEnum):
    UNKNOWN     = 'unknown'
    MOTHERBOARD = 'motherboard'
    BACKPLANE   = 'backplane'
    EDDY        = 'a6'
    IO_FIELDBUS = 'io_fieldbus'
    IO_PARALLEL = 'io_parallel'
    IO_ANALOG   = 'io_analog'
    IO_RS485    = 'io_rs485'
    IO_EMDC     = 'io_emdc'
    IO_ETH      = 'io_ethernet'

class PackageType(ExtendedEnum):
    UNKNOWN     = 'unknown'
    FIRMWARE    = 'firmware'
    CLIENT      = 'client'
    CONFIGTOOL  = 'config-tool'
    UPDATETOOLS = 'update-tools'
    V6PCI       = 'v6pci'
    FPC         = 'fpc'

class LogicDeviceType(ExtendedEnum):
    UNKNOWN = 'unknown'
    FPGA    = 'FPGA'
    CPLD    = 'CPLD'

class ChainType(ExtendedEnum):
    FTDI   = 'ftdi'
    V6JTAG = 'v6jtag'
