# vendor ids
# see: https://rohmann.atlassian.net/wiki/spaces/HEL/pages/143425552/Data+Structure+Definition+for+Rohmann+SensorBus+Data

# own library
from source.library import mysql_lib  

# one init speed up load time
temp_lib = mysql_lib()

# enums defined in mysql database
eVendorId = temp_lib.get_vendor_id()

#temp_lib.close()