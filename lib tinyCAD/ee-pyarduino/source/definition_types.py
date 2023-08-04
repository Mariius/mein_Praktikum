# definition types
# see: https://rohmann.atlassian.net/wiki/spaces/HEL/pages/143425552/Data+Structure+Definition+for+Rohmann+SensorBus+Data

# own library
from source.library import mysql_lib  

# one init speed up load time
temp_lib = mysql_lib()

# enums defined in mysql database
eDeviceType     = temp_lib.get_enum('eDeviceType')
eTriggerType    = temp_lib.get_enum('eTriggerType')
eEncoderType    = temp_lib.get_enum('eEncoderType')
eInputType      = temp_lib.get_enum('eInputType')
eOutputType     = temp_lib.get_enum('eOutputType')
eCoilType       = temp_lib.get_enum('eCoilType')
fBusType        = temp_lib.get_enum('fBusType')

#temp_lib.close()