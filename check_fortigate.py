#!/usr/local/bin/python3
#check_juniper_srx

import sys, getopt, ipaddress, re
from pysnmp.hlapi import *
from pysnmp.entity.rfc3413.oneliner import cmdgen


exitmessage_d = { 0: "OK", 1: "WARNING", 2: "CRITICAL" }

def cpu_load(ipAddress_s=None, communityString_s=None, oidCurrent_d=None):
    percentage = -1
    cpuLoad_varBindTable = snmp_get(ipAddress_s, communityString_s, oidCurrent_d["oid"])
    if cpuLoad_varBindTable == -1:
        return unkown("snmp_get cpuLoad_varBindTable failed!")

    for varBindTableRow in cpuLoad_varBindTable:
        for name, val in varBindTableRow:
            percentage = int(val)

    perfdata_s = "cpu_load=%d;%d;%d;;100" % (percentage, oidCurrent_d["warning"], oidCurrent_d["critical"])

    if percentage != -1:
        if percentage < oidCurrent_d["warning"]:
            print ("%s - Everything is fine. | %s" % (exitmessage_d[0], perfdata_s))
            return 0
        elif percentage < oidCurrent_d["critical"]:
            print ("%s - CPU load is high! Verify: %s | %s" % (exitmessage_d[1], oidCurrent_d["cli"], perfdata_s))
            return 1
        elif percentage >= oidCurrent_d["critical"]:
            print ("%s - CPU load is too high! Verify: %s | %s" % (exitmessage_d[2], oidCurrent_d["cli"], perfdata_s))
            return 2
    else:
        return unkown("Something went wrong!")

def memory(ipAddress_s=None, communityString_s=None, oidCurrent_d=None, oidMax_d=None):
    memoryCurrent = -1
    memoryCurrent_varBindTable = snmp_get(ipAddress_s, communityString_s, oidCurrent_d["oid"])
    if memoryCurrent_varBindTable == -1:
        return unkown("snmp_get memoryCapacity_varBindTable failed!")

    for varBindTableRow in memoryCurrent_varBindTable:
        for name, val in varBindTableRow:
            memoryCurrent = val

    if  memoryCurrent == -1:
        return unkown ("memoryCapacity or memoryCurrent not set!")
    percentage = memoryCurrent

    perfdata_s = "memory=%s;%s;%s;;100" % (percentage, oidCurrent_d["warning"], oidCurrent_d["critical"])

    if percentage != -1:
        if percentage < oidCurrent_d["warning"]:
            print ("%s - Everything is fine. | %s" % (exitmessage_d[0],  perfdata_s))
            return 0
        elif percentage < oidCurrent_d["critical"]:
            print ("%s - Memory usage is high! Verify: %s | %s" % (exitmessage_d[1], oidCurrent_d["cli"], perfdata_s))
            return 1
        elif percentage >= oidCurrent_d["critical"]:
            print ("%s - Memory usage is too high! Verify: %s | %s" % (exitmessage_d[2], oidCurrent_d["cli"], perfdata_s))
            return 2
    else:
        return unkown("Something went wrong!")

def memory_low(ipAddress_s=None, communityString_s=None, oidCurrent_d=None, oidMax_d=None):
    memoryLowCurrent = -1
    percentage = -1
    memoryLowCurrent_varBindTable = snmp_get(ipAddress_s, communityString_s, oidCurrent_d["oid"])
    if memoryLowCurrent_varBindTable == -1:
        return unkown("snmp_get memoryLowCurrent_varBindTable failed!")

    for varBindTableRow in memoryLowCurrent_varBindTable:
        for name, val in varBindTableRow:
            memoryLowCurrent = int(val)

    if memoryLowCurrent == -1:
        return unkown ("memoryLowCapacity == -1 or memoryLowCurrent == -1")
    percentage = memoryLowCurrent

    perfdata_s = "memory_low=%s;%s;%s;;100" % (percentage, oidCurrent_d["warning"], oidCurrent_d["critical"])

    if percentage != -1:
        if percentage < oidCurrent_d["warning"]:
            print ("%s - Everything is fine. | %s" % (exitmessage_d[0], perfdata_s))
            return 0
        elif percentage < oidCurrent_d["critical"]:
            print ("%s - Low-Memory usage is high! | %s" % (exitmessage_d[1], perfdata_s))
            return 1
        elif percentage >= oidCurrent_d["critical"]:
            print ("%s - Low-Memory usage is too high! | %s" % (exitmessage_d[2], perfdata_s))
            return 2
    else:
        return unkown("Something went wrong!")


def disk(ipAddress_s=None, communityString_s=None, oidCurrent_d=None, oidMax_d=None):
    diskCurrent = -1
    diskCapacity = -1
    percentage = -1
    diskCurrent_varBindTable = snmp_get(ipAddress_s, communityString_s, oidCurrent_d["oid"])
    if diskCurrent_varBindTable == -1:
        return unkown("snmp_get diskCurrent_varBindTable failed!")

    for varBindTableRow in diskCurrent_varBindTable:
        for name, val in varBindTableRow:
            diskCurrent = val

    diskCapacity_varBindTable = snmp_get(ipAddress_s, communityString_s, oidMax_d["oid"])
    if diskCapacity_varBindTable == -1:
        return unkown("snmp_get diskCapacity_varBindTable failed!")

    for varBindTableRow in diskCapacity_varBindTable:
        for name, val in varBindTableRow:
            diskCapacity = val

    if diskCurrent == -1 or diskCapacity == -1:
        return unkown ("diskCurrent == -1 or diskCapacity == -1")
    percentage = int((diskCurrent / diskCapacity) * 100)

    perfdata_s = "disk=%s;%s;%s;;100" % (percentage, oidCurrent_d["warning"], oidCurrent_d["critical"])

    if percentage != -1:
        if percentage < oidCurrent_d["warning"]:
            print ("%s - Everything is fine. | %s" % (exitmessage_d[0], perfdata_s))
            return 0
        elif percentage < oidCurrent_d["critical"]:
            print ("%s - Disk usage is high! | %s" % (exitmessage_d[1], perfdata_s))
            return 1
        elif percentage >= oidCurrent_d["critical"]:
            print ("%s - Disk usage is too high! | %s" % (exitmessage_d[2], perfdata_s))
            return 2
    else:
        return unkown("Something went wrong!")


def session_four(ipAddress_s=None, communityString_s=None, oidCurrent_d=None):
    sessionFour_varBindTable = snmp_get(ipAddress_s, communityString_s, oidCurrent_d["oid"])
    if sessionFour_varBindTable == -1:
        return unkown("snmp_get failed!")

    for varBindTableRow in sessionFour_varBindTable:
        for name, val in varBindTableRow:
            perfdata_s = "sessioncount_four=%s;;;;" % str(val)
            print ("OK - IPv4 session count is %s | %s" % (str(val), perfdata_s))
            return 0

def session_six(ipAddress_s=None, communityString_s=None, oidCurrent_d=None):
    sessionSix_varBindTable = snmp_get(ipAddress_s, communityString_s, oidCurrent_d["oid"])
    if sessionSix_varBindTable == -1:
        return unkown("snmp_get sessionSix_varBindTable failed!")

    for varBindTableRow in sessionSix_varBindTable:
        for name, val in varBindTableRow:
            perfdata_s = "sessioncount_six=%s;;;;" % str(val)
            print ("OK - IPv6 session count is %s | %s" % (str(val), perfdata_s))
            return 0

def software_version(ipAddress_s=None, communityString_s=None, oidCurrent_d=None):
    version_varBindTable = snmp_get(ipAddress_s, communityString_s, oidCurrent_d["oid"])
    if version_varBindTable == -1:
        return unkown("snmp_get failed!")

    for varBindTableRow in version_varBindTable:
        for name, val in varBindTableRow:
            print ("OK - Version is %s" % (str(val)))
            return 0

def interface_list(ipAddress_s=None, communityString_s=None, oidCurrent_d=None):
    interfaces_varBindTable = snmp_get(ipAddress_s, communityString_s, oidCurrent_d["oid"])
    if interfaces_varBindTable == -1:
        return unkown("snmp_get failed!")

    for varBindTableRow in interfaces_varBindTable:
        for name, val in varBindTableRow:
            print ("Interface-ID: %s Interface-Name: %s" % (str(name).split('.')[10], val))

    return 0

def interface_status(ipAddress_s=None, communityString_s=None, oidCurrent_d=None, interfaceName_s=None):
    interfaces_varBindTable = snmp_get(ipAddress_s, communityString_s, oidCurrent_d["ifDescr"]["oid"])
    interfaceId_s = "-1"
    exitstatus_l = [0]
    critinfo_s = ""
    if interfaces_varBindTable == -1:
        return unkown("Interface-Name not found!")

    for varBindTableRow in interfaces_varBindTable:
        for name, val in varBindTableRow:
            if str(val) == str(interfaceName_s):
                interfaceId_s = str(name).split('.')[10]

    if interfaceId_s != "-1":
        ifAdminStatus = 0
        ifOperStatus = 0
        ifAdminStatus_table = snmp_get(ipAddress_s, communityString_s, oidCurrent_d["ifAdminStatus"]["oid"])
        for varBindTableRow in ifAdminStatus_table:
            for name, val in varBindTableRow:
                if str(name) == "%s.%s" % (oidCurrent_d["ifAdminStatus"]["oid"], interfaceId_s):
                    if int(val) == 2:
                        exitstatus_l.append(2)
                        critinfo_s = "%s Interface %s is administratively down!" % (critinfo_s, interfaceName_s)
                        ifAdminStatus = int(val)

        ifOperStatus_table = snmp_get(ipAddress_s, communityString_s, oidCurrent_d["ifOperStatus"]["oid"])
        for varBindTableRow in ifOperStatus_table:
            for name, val in varBindTableRow:
                if str(name) == "%s.%s" % (oidCurrent_d["ifOperStatus"]["oid"], interfaceId_s):
                    if int(val) == 2:
                        exitstatus_l.append(2)
                        critinfo_s = "%s Interface %s is down!" % (critinfo_s, interfaceName_s)
                    elif int(val) == 7:
                        exitstatus_l.append(2)
                        critinfo_s = "%s Interface %s is lowerLayerDown!" % (critinfo_s, interfaceName_s)
                    elif int(val) == 1:
                        exitstatus_l.append(0)
                        ifOperStatus = 0
                    else:
                        exitstatus_l.append(3)
                        critinfo_s = "%s Interface %s status is unkown!" % (critinfo_s, interfaceName_s)

        # Return-Data
        if max(exitstatus_l) == 0:
            print ("%s - Everything is fine | ifAdminStatus=%s;1;2;;2 ifOperStatus=%s;1;2;;2" %
                   (exitmessage_d[max(exitstatus_l)], ifAdminStatus, ifOperStatus))
        else:
            print ("%s %s | ifAdminStatus=%s;1;2;;2 ifOperStatus=%s;1;2;;2" %
                   (exitmessage_d[max(exitstatus_l)], critinfo_s, ifAdminStatus, ifOperStatus))
        return max(exitstatus_l)

def interface_status_detail(ipAddress_s=None, communityString_s=None, oidCurrent_d=None, interfaceName_s=None):
    interfaces_varBindTable = snmp_get(ipAddress_s, communityString_s, oidCurrent_d["ifDescr"]["oid"])
    interfaceId_s = "-1"
    exitstatus_l = [0]
    critinfo_s = ""
    ifAdminStatus = 0
    ifOperStatus = 0
    perfdata_s = ""
    if interfaces_varBindTable == -1:
        return unkown("Interface-Name not found!")

    for varBindTableRow in interfaces_varBindTable:
        for name, val in varBindTableRow:
            if str(val) == str(interfaceName_s):
                interfaceId_s = str(name).split('.')[10]

    if interfaceId_s != "-1":
        ifAdminStatus_table = snmp_get(ipAddress_s, communityString_s, oidCurrent_d["ifAdminStatus"]["oid"])
        for varBindTableRow in ifAdminStatus_table:
            for name, val in varBindTableRow:
                if str(name) == "%s.%s" % (oidCurrent_d["ifAdminStatus"]["oid"], interfaceId_s):
                    if int(val) == 2:
                        exitstatus_l.append(2)
                        critinfo_s = "%s Interface %s is administratively down!" % (critinfo_s, interfaceName_s)
                        ifAdminStatus = int(val)

        ifOperStatus_table = snmp_get(ipAddress_s, communityString_s, oidCurrent_d["ifOperStatus"]["oid"])
        for varBindTableRow in ifOperStatus_table:
            for name, val in varBindTableRow:
                if str(name) == "%s.%s" % (oidCurrent_d["ifOperStatus"]["oid"], interfaceId_s):
                    ifOperStatus = int(val)
                    if int(val) == 2:
                        exitstatus_l.append(2)
                        critinfo_s = "%s Interface %s is down!" % (critinfo_s, interfaceName_s)
                    elif int(val) == 7:
                        exitstatus_l.append(2)
                        critinfo_s = "%s Interface %s is lowerLayerDown!" % (critinfo_s, interfaceName_s)

        try:
            oidCurrent_d.pop("ifDescr", None)
            oidCurrent_d.pop("ifAdminStatus", None)
            oidCurrent_d.pop("ifOperStatus", None)
            oidCurrent_d.pop("ifType", None)
        except KeyError:
            return unkown("something went wrong!")

        for query in oidCurrent_d:
            query_table = snmp_get(ipAddress_s, communityString_s, oidCurrent_d[query]["oid"])
            for varBindTableRow in query_table:
                for name, val in varBindTableRow:
                    if str(name) == "%s.%s" % (oidCurrent_d[query]["oid"], interfaceId_s):
                        perfdata_s = "%s %s=%s;;;;" % (perfdata_s, query, str(val))

        # Return-Data
        if max(exitstatus_l) == 0:
            print ("%s - Everything is fine | ifAdminStatus=%s;1;2;;2 ifOperStatus=%s;1;2;;2 %s" %
                   (exitmessage_d[max(exitstatus_l)], ifAdminStatus, ifOperStatus, perfdata_s))
        else:
            print ("%s %s | ifAdminStatus=%s;1;2;;2 ifOperStatus=%s;1;2;;2 %s" %
                   (exitmessage_d[max(exitstatus_l)], critinfo_s, ifAdminStatus, ifOperStatus, perfdata_s))
        return max(exitstatus_l)
    else:
        return unkown("Interface-Name not found!")

def hardware_health(ipAddress_s=None, communityString_s=None, oidCurrent_d=None):
    alarmStatusIndexes_l = []
    criticalThings_l = []
    exitstring = ""
    fgHwSensorEntAlarmStatus_varBindTable = snmp_get(ipAddress_s, communityString_s, oidCurrent_d["fgHwSensorEntAlarmStatus"]["oid"])
    if fgHwSensorEntAlarmStatus_varBindTable == -1:
        return unkown("snmp_get fgGwSensorEntAlarmStatus failed!")

    for varBindTableRow in fgHwSensorEntAlarmStatus_varBindTable:
        for name, val in varBindTableRow:
            if val != 0:
                alarmStatusIndexes_l.append(str(name).split('.')[-1])

    if len(alarmStatusIndexes_l) == 0:
        print ("%s - Everything is fine." % exitmessage_d[0])
        return 0
    else:
        fgHwSensorEntName_varBindTable = snmp_get(ipAddress_s, communityString_s, oidCurrent_d["fgHwSensorEntName"]["oid"])
        fgHwSensorEntValue_varBindTable = snmp_get(ipAddress_s, communityString_s, oidCurrent_d["fgHwSensorEntValue"]["oid"])
        if fgHwSensorEntName_varBindTable == -1 or fgHwSensorEntValue_varBindTable == -1:
            return unkown ("snmp_get fgHwSensorEntName_varBindTable / fgHwSensorEntValue_varBindTable failed")

        exitstring = "%s -" % exitmessage_d[2]
        for index in alarmStatusIndexes_l:
            name = fgHwSensorEntName_varBindTable[int(index)-1][0][1]
            value = fgHwSensorEntValue_varBindTable[int(index)-1][0][1]
            exitstring = "%s %s is faulty (Value = %s), " % (exitstring, name, value)

        print (exitstring)
        return 2

def snmp_get (ipAddress_s, communityString_s, oid_s):
    cmdGen = cmdgen.CommandGenerator()

    errorIndication, errorStatus, errorIndex, varBindTable = cmdGen.nextCmd(
        cmdgen.CommunityData(communityString_s),
        cmdgen.UdpTransportTarget((ipAddress_s, 161)),
        oid_s,
        lookupNames=True,
        lookupValues=True
    )

    if errorIndication:
        print(errorIndication)
        return -1
    elif errorStatus:
        print("UNKOWN - %s at %s" % (
                errorStatus.prettyPrint(),
                errorIndex and varBinds[int(errorIndex)-1][0] or "?"
            )
        )
        return -1
    else:
        return varBindTable

def unkown (message_s=None):
    if not message_s:
        print ("UNKOWN - something went wrong!")
    else:
        print ("UNKOWN - %s" % message_s)
    return 3

def optError (err=None, mode_l=None):
    # Print Error Message
    if err:
        print (err)
    print ("check_juniper_srx -i <ipAddress> -c <communityString> -m <mode> [-n <interface-name>]")
    print ('available modes: ', mode_l)

def main (argv):
    # Globale Variablen
    exitstatus_l = [0]
    ipAddress_s = ""
    communityString_s = ""
    interfaceName_s = ""
    mode_s = ""
    mode_l = ["interface_status", "interface_status_detail", "interface_list",
              "software_version", "cpu_load", "memory", "memory_low",
              "disk", "session_four", "session_six", "hardware_health"]

    # OID Definition:

    FortiOSMib_d = {
        'fgSysVersion':         {'oid': '1.3.6.1.4.1.12356.101.4.1.1'},
        'fgSysMgmtVdom':        {'oid': '1.3.6.1.4.1.12356.101.4.1.2'},
        'fgSysCpuUsage': {
            'oid': '1.3.6.1.4.1.12356.101.4.1.3',
            'warning': 85,
            'critical': 95,
            'cli': "config global; get system performance status" #TODO: Add to output
        },
        'fgSysMemUsage': {
            'oid': '1.3.6.1.4.1.12356.101.4.1.4',
            'warning': 80,
            'critical': 95,
            'cli': "config global; get system performance status"  #TODO: Add to output
        },
        'fgSysMemCapacity':     {'oid': '1.3.6.1.4.1.12356.101.4.1.5'},
        'fgSysDiskUsage': {
            'oid': '1.3.6.1.4.1.12356.101.4.1.6',
            'warning': 75,
            'critical': 90
        },
        'fgSysDiskCapacity':    {'oid': '1.3.6.1.4.1.12356.101.4.1.7'},
        'fgSysSesCount':        {'oid': '1.3.6.1.4.1.12356.101.4.1.8'},
        'fgSysLowMemUsage':     {           # Get kernel memory
            'oid': '1.3.6.1.4.1.12356.101.4.1.9',
            'warning': 70,
            'critical': 80
        },
        'fgSysLowMemCapacity':  {
            'oid': '1.3.6.1.4.1.12356.101.4.1.10',
        },  # Get kernel memory
        'fgSysSes6Count':       {'oid': '1.3.6.1.4.1.12356.101.4.1.15'},
        'fgSysUpTime':          {'oid': '1.3.6.1.4.1.12356.101.4.1.20'}
    }

    ForiOSHardwareMib_d = {
        'fgHwSensorEntName':    {'oid': '1.3.6.1.4.1.12356.101.4.3.2.1.2'},
        'fgHwSensorEntValue':   {'oid': '1.3.6.1.4.1.12356.101.4.3.2.1.3'},
        'fgHwSensorEntAlarmStatus': {'oid': '1.3.6.1.4.1.12356.101.4.3.2.1.4'}
    }

    IfMib_d = {
        "ifDescr": {
            "oid": "1.3.6.1.2.1.2.2.1.2",
            "description": "Returns a list of all known interfaces"
        },
        "ifType": {
            "oid": "1.3.6.1.2.1.2.2.1.3",
            "description": "Returns a list of the interface Type"
        },
        "ifMtu": {
            "oid": "1.3.6.1.2.1.2.2.1.4",
            "description": "Returns a list of the Interface MTUs"
        },
        "ifSpeed": {
            "oid": "1.3.6.1.2.1.2.2.1.5",
            "description": "Returns a list of interface Speed"
        },
        "ifPhysAddress": {
            "oid": "1.3.6.1.2.1.2.2.1.6",
            "description": "Returns a list of interface Speed"
        },
        "ifAdminStatus": {
            "oid": "1.3.6.1.2.1.2.2.1.7",
            "description": "Returns a list of interface admin status"
        },
        "ifOperStatus": {
            "oid": "1.3.6.1.2.1.2.2.1.8",
            "description": "Returns a list of interface operational status"
        },
        "ifInDiscards": {
            "oid": "1.3.6.1.2.1.2.2.1.13",
            "description": "Input Discards"
        },
        "ifInErrors": {
            "oid": "1.3.6.1.2.1.2.2.1.14",
            "description": "Input Errors"
        },
        "ifOutDiscards": {
            "oid": "1.3.6.1.2.1.2.2.1.15",
            "description": "Output Discards"
        },
        "ifOutErrors": {
            "oid": "1.3.6.1.2.1.2.2.1.20",
            "description": "Output Errors"
        },
        "ifOutQLen": {
            "oid": "1.3.6.1.2.1.2.2.1.21",
            "description": "Output queue"
        },
    }

    if len(sys.argv) < 7:
        optError (err="Wrong parameter count: " + str(len(sys.argv)) + "Parameters: "+ str(sys.argv), mode_l=mode_l )
        sys.exit(3)


    try:
        opts, args = getopt.getopt(argv,
                                   "hi:c:m:n::",
                                   ["ipAddress_s=", "communityString_s=", "mode_s=", "interfaceName_s="]
                                   )
    except getopt.GetoptError as err:
        optError(err, mode_l) # call Error-Print-Function
        exitstatus_l.append(3)

    for opt, arg in opts:
        if opt == "-h":
            optError(None, mode_l)
            exitstatus_l.append(3)
        elif opt in ("-i", "--ipAddress"):
            try:
                ipAddress_s = ipaddress.ip_address(arg) # Test address if valid
                ipAddress_s = arg #save plain IP
            except ValueError:
                unkown("%s is not a valid IP-Address" % (arg))
                sys.exit(3)
        elif opt in ("-c", "--communityString"):
            communityString_s = arg
        elif opt in ("-m", "--mode"):
            if arg in mode_l:
                mode_s = arg
        elif opt in ("-n", "--interfaceName"):
            if opt:
                interfaceName_s = arg

    # Method dispatching + save exit status
    if mode_s == "interface_status":
        exitstatus_l.append(interface_status(ipAddress_s, communityString_s,
                                             oidCurrent_d=IfMib_d, interfaceName_s=interfaceName_s))
    elif mode_s == "interface_status_detail":
        exitstatus_l.append(interface_status_detail(ipAddress_s, communityString_s,
                                                    oidCurrent_d=IfMib_d, interfaceName_s=interfaceName_s))
    elif mode_s == "interface_list":
        exitstatus_l.append(interface_list(ipAddress_s, communityString_s,
                                           oidCurrent_d=IfMib_d["ifDescr"]))
    elif mode_s == "software_version":
        exitstatus_l.append(software_version(ipAddress_s, communityString_s,
                                             oidCurrent_d=FortiOSMib_d["fgSysVersion"]))
    elif mode_s == "cpu_load":
        exitstatus_l.append(cpu_load(ipAddress_s, communityString_s,
                                     oidCurrent_d=FortiOSMib_d["fgSysCpuUsage"]))
    elif mode_s == "memory":
        exitstatus_l.append(memory(ipAddress_s, communityString_s,
                                   oidCurrent_d=FortiOSMib_d["fgSysMemUsage"], oidMax_d=FortiOSMib_d["fgSysMemCapacity"]))
    elif mode_s == "memory_low":
        exitstatus_l.append(memory_low(ipAddress_s, communityString_s,
                                       oidCurrent_d=FortiOSMib_d["fgSysMemUsage"], oidMax_d=FortiOSMib_d["fgSysMemCapacity"]))
    elif mode_s == "disk":
        exitstatus_l.append(disk(ipAddress_s, communityString_s,
                                 oidCurrent_d=FortiOSMib_d["fgSysDiskUsage"], oidMax_d=FortiOSMib_d["fgSysDiskCapacity"]))
    elif mode_s == "session_four":
        exitstatus_l.append(session_four(ipAddress_s, communityString_s,
                                     oidCurrent_d=FortiOSMib_d["fgSysSesCount"]))
    elif mode_s == "session_six":
        exitstatus_l.append(session_six(ipAddress_s, communityString_s,
                                     oidCurrent_d=FortiOSMib_d["fgSysSes6Count"]))
    elif mode_s == "hardware_health":
        exitstatus_l.append(hardware_health(ipAddress_s, communityString_s, oidCurrent_d=ForiOSHardwareMib_d))
    else:
        optError (err="Wrong Mode! - Mode given was: " + mode_s, mode_l=mode_l)
        sys.exit(3)

    sys.exit (max(exitstatus_l))

# calling main function
if __name__ == "__main__":
    main(sys.argv[1:])
