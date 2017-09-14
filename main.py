import serial
com_port = "COM4"
ENUM = 5111
RANGE = 5112
config_options = [
    (0,
     (ENUM,(0,'Do not generate $STALK sentence for each incoming SeaTalk datagram'),(1,'Send out every incoming seatalk telegram as $STALK to NMEA')),
    'Echo all incoming SeaTalk datagrams'),
    (1,
     (ENUM,(1,'300'),(2,'600'),(3,'1200'),(4,'2400'),(5,'4800'),(6,'9600'),(7,'19200'),(8,'38400'), ),
    'NMEA Baudrate'),
    (2,
     (RANGE,(65,90),(97,122),(48,57)),
    'First char in Talker id'),

    #Continue...

    (3,
     ((0,'0 - Do not generate $STALK sentence for each incoming SeaTalk datagram'),(1,'1 - Send out every incoming seatalk telegram as $STALK to NMEA')),
    'Echo all incoming SeaTalk datagrams'),
    (4,
     ((0,'0 - Do not generate $STALK sentence for each incoming SeaTalk datagram'),(1,'1 - Send out every incoming seatalk telegram as $STALK to NMEA')),
    'Echo all incoming SeaTalk datagrams'),

]
cur_config = []
def test_connection(comport):
    with serial.Serial(comport, 4800, timeout=1) as ser:
        ser.write(b'$xxx\n')
        # x = ser.read()          # read one byte
        # s = ser.read(10)        # read up to ten bytes (timeout)
        line = ser.readline()   # read a '\n' terminated line
        if b'$xxx' in line:
            return True
        return False

def extract_response(line):
    parts = str.split(str(line, "utf-8"), ',')
    if '-' in parts[2]:
        ret = parts[2].lstrip('- ')
        ret = '-' + ret
        return int(float(ret.rstrip('\\\r\n '))*1000)
    return int(float(parts[2].rstrip('\\\r\n ').lstrip())*1000)

def extract_address(line):
    parts = str.split(str(line, "utf-8"), ',')
    if '-' in parts[1]:
        ret = parts[1].lstrip('- ')
        ret = '-' + ret
        return int(float(ret.rstrip('\\\r\n ')))
    return int(float(parts[1].rstrip('\\\r\n ').lstrip()))

def get_conf_address(comport, address):
    with serial.Serial(comport, 4800, timeout=1) as ser:
        s = '$SNBSE,'+str(address)+'\n'
        ser.write(bytes(s,"utf-8"))
        line = ser.readline()   # read a '\n' terminated line
        return extract_response(line)

def check_response(ret, value):
    if ret==value:
        return True
    return False

def set_conf_address(comport, address, value):
    with serial.Serial(comport, 4800, timeout=1) as ser:
        s = '$SNBSE,'+str(address)+','+str(value) + '\n'
        ser.write(bytes(s,"utf-8"))

    res = get_conf_address(com_port, address)
    return check_response(res, value)

def trns_0(address,val):
    ret = str(address) + ": "
    if address is 0:
        ret +=  'Echo all incoming SeaTalk datagrams: '
        if val is 0:
            return ret+'0 - Do not generate $STALK sentence for each incoming SeaTalk datagram'
        elif val is 1:
            return ret+ '1 - Send out every incoming seatalk telegram as $STALK to NMEA'
        else:
            return ret+ 'Incorrect value'
    elif address is 1:
        ret +=  'NMEA port baudrate: '
        if val is 1:
            return ret+'300'
        elif val is 2:
            return ret+ '600'
        elif val is 3:
            return ret+ '1200'
        elif val is 4:
            return ret+ '2400'
        elif val is 5:
            return ret+ '4800'
        elif val is 6:
            return ret+ '9600'
        elif val is 7:
            return ret+ '19200'
        elif val is 8:
            return ret+ '38400'
        else:
            return ret+ 'Incorrect value'
    elif address is 2:
        ret +=  'First char in Talker id: '
        if (val >= 65 and val<=90) or (val >= 97 and val<=122):
            return ret + chr(val)
        else:
            return ret + 'Incorrect value'
    elif address is 3:
        ret +=  'Second char in Talker id: '
        if (val >= 65 and val <= 90) or (val >= 97 and val <= 122):
            return ret + chr(val)
        else:
            return ret + 'Incorrect value'
    elif address is 4:
        ret +=  'Echo all incoming NMEA messages: '
        if val is 0:
            return ret+'0 - False'
        elif val is 1:
            return ret+ '1 - True'
        else:
            return ret+ 'Incorrect value'
    elif address is 6:
        ret +=  'Send $IIVHW when new SeaTalk data arrive: '
        if val is 0:
            return ret+'0 - False'
        elif val is 1:
            return ret+ '1 - True'
        else:
            return ret+ 'Incorrect value'
    elif address is 7:
        ret +=  'Send $IIHDM when new SeaTalk data arrive: '
        if val is 0:
            return ret+'0 - False'
        elif val is 1:
            return ret+ '1 - True'
        else:
            return ret+ 'Incorrect value'
    elif address is 8:
        ret +=  'Send $IIMWV when new SeaTalk data arrive: '
        if val is 0:
            return ret+'0 - False'
        elif val is 1:
            return ret+ '1 - True'
        else:
            return ret+ 'Incorrect value'
    elif address is 9:
        ret +=  'Send $IIDBT when new SeaTalk data arrive: '
        if val is 0:
            return ret+'0 - False'
        elif val is 1:
            return ret+ '1 - True'
        else:
            return ret+ 'Incorrect value'
    elif address is 10:
        ret +=  'Send $IIMTW when new SeaTalk data arrive: '
        if val is 0:
            return ret+'0 - False'
        elif val is 1:
            return ret+ '1 - True'
        else:
            return ret+ 'Incorrect value'
    elif address is 11:
        ret +=  'Send $IIVLW when new SeaTalk data arrive: '
        if val is 0:
            return ret+'0 - False'
        elif val is 1:
            return ret+ '1 - True'
        else:
            return ret+ 'Incorrect value'
    elif address is 14:
        ret +=  'Send SOG and STW to SeaTalk when new NMEA SOG msg arrives: '
        if val is 0:
            return ret+'0 - SOG and STW'
        elif val is 1:
            return ret+ '1 - SOG only'
        else:
            return ret+ 'Incorrect value'
    if address is 15:
        ret +=  'Echo only interpreted incoming SeaTalk datagrams (dependes on address 0 as well): '
        if val is 0:
            return ret+'0 - Echo all datagrams'
        elif val is 1:
            return ret+ '1 - Echo interpreted datagrams only'
        else:
            return ret+ 'Incorrect value'
    elif address is 16:
        ret +=  'SeaTalk port read-only: '
        if val is 0:
            return ret+'0 - True'
        elif val is 1:
            return ret+ '1 - False'
        else:
            return ret+ 'Incorrect value'
    elif address is 17:
        ret +=  'Wind speed units: '
        if val is 0:
            return ret+'0 - Knots'
        elif val is 1:
            return ret+ '1 - m/s'
        else:
            return ret+ 'Incorrect value'
    elif address is 18:
        ret +=  'Send SOG to SeaTalk: '
        if val is 0:
            return ret+'0 - False'
        elif val is 1:
            return ret+ '1 - True'
        else:
            return ret+ 'Incorrect value'
    elif address is 19:
        ret +=  'Send position to SeaTalk: '
        if val is 0:
            return ret + '0 - False'
        elif val is 1:
            return ret + '1 - True'
        else:
            return ret+ 'Incorrect value'
    elif address is 20:
        ret +=  'Depth units: '
        if val is 0:
            return ret+'0 - feet'
        elif val is 1:
            return ret+ '1 - meters'
        else:
            return ret+ 'Incorrect value'
    elif address is 22:
        ret +=  'RMC and GLL messages for position: '
        if val is 0:
            return ret+'0 - RMC only'
        elif val is 1:
            return ret+ '1 - RMC and GLL'
        else:
            return ret+ 'Incorrect value'
    elif address is 24:
        ret +=  'Transducer depth offset: '
        return ret+ str(val) + 'Plus What is in address 23'
    elif address is 25:
        ret +=  'Translation of data available both on NMEA and Seatalk: '
        if val is 0:
            return ret + '0 - False'
        elif val is 1:
            return ret + '1 - True'
        else:
            return ret+ 'Incorrect value'
    elif address is 26:
        ret +=  'Send RSA message: '
        if val is 0:
            return ret + '0 - False'
        elif val is 1:
            return ret + '1 - True'
        else:
            return ret + 'Incorrect value'
    elif address is 28:
        ret +=  'Send waypoint autopilot data to SeaTalk: '
        if val is 0:
            return ret + '0 - False'
        elif val is 1:
            return ret + '1 - True'
        else:
            return ret + 'Incorrect value'
    else:
        return ret + 'Address unknown \ not in use'



print(test_connection(com_port))
# for i in range(0,29):
#     res = get_conf_address(com_port,i)
#     cur_config.append(tuple((i,res)))
#     print(trns_0(i,res))


print(set_conf_address(com_port,6,0))

for i in range(0,29):
    res = get_conf_address(com_port,i)
    cur_config.append(tuple((i,res)))
    print(trns_0(i,res))
#print(cur_config)


