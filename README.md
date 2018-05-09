# check_fortigate

`check_fortigate` is a check for Nagios or Icinga in order to check the health of your Fortigate firewall and to get performance data from it. It uses Python 3.

# Setup

Just download the `.py` file from this repository and save it to a folder where your monitoring system can access it.

## Requirements

The script uses the following Python 3 Modules:
* `sys`
* `getopt`
* `ipaddress`
* `re`
* `pysnmp`

# Usage

Simply call the Python-Script:

```
check_fortigate -i <ipv4Address> -c <communityString> -m <mode> [-n <interface-name>]
```

## Available Modes:

* `interface_status`
* `interface_status_detail` 
* `interface_list`
* `software_version`
* `cpu_load`
* `memory`
* `memory_low`
* `disk`
* `session_four`
* `session_six`
* `hardware_health`

## Example Implementation for Icinga 2

### CheckCommand

```
object CheckCommand "check_fortigate" {
  import "plugin-check-command"
   command = [ PluginDir + "check_fortigate" ]
  arguments = {
    "-i" = "$check_fortigate_address$"
    "-c" = "$check_fortigate_community$"
    "-m" = "$check_fortigate_mode$"
  }

  vars.check_fortigate_address = "$address$"
  vars.check_fortigate_community = "public"
}
```
### Service object

```
apply Service "Fortigate disk" {
  import "generic-service"
  check_command = "check_fortigate"
  vars.check_fortigate_mode = "disk"

  assign where match ( "Fortigate", host.name)
}
