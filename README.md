Adapted from https://scadahoneynet.sourceforge.net/ (SourceForge project scadahoneynet) by Venkat Pothamsetty and Matthew Franz, Critical Infrastructure Assurance Group (CIAG), Cisco Systems, Inc.

# SCADA HoneyNet Project: Building Honeypots for Industrial Networks (Python 3)

This repository holds the SCADA HoneyNet PLC simulation scripts with the changes needed to run them on Python 3. The original scripts were written for Python 2 (2004 to 2005), which current Linux distributions no longer ship. The history starts with the three releases published on SourceForge (plc-sim 0.1 of 2004-03-20, plc-sim 0.2 of 2004-06-01 and scada-honeyd 0.3 of 2005-07-15, unchanged), followed by the Python 3 changes.

## Original introduction

> The short-term goal of the project is to determine the feasibility of building a software-based framework to simulate a variety of industrial networks such as SCADA, DCS, and PLC architectures. We plan to document the requirements and release proof of concept code (in the form of honeyd scripts) so that a single Linux host can simulate multiple industrial devices and complex network topologies. [...] Assuming deployment of "SCADA HoneyNets" ever reach critical mass, the longer term objective of the project is to gather information about general attack patterns and specific exploits that could be used to write signature for commercial and Open Source IDS products.

Version 0.3 (July 2005) converted the stand-alone scripts of 0.1 and 0.2 into Honeyd subsystem scripts.

From the 0.3 release notes:

* `honeyd-telnet.py`: a VxWorks-style shell (`ls`, `cd`, `help`).
* `honeyd-ftpd.py`: a VxWorks FTP server with its error messages.
* `honeyd-modbus.py`: a Modbus/TCP server (read coils, write multiple registers, exception for other function codes).
* `honeyd-html.py`: a PLC web page with "Statistics", "Diagnostics" and "Protocols" pages, and an optional (commented out) e-mail alert when a page is accessed.

> Intentionally, our scripts are written in a crude manner for two reasons. First, we want to respect the copy rights of the PLC makers. Second, we want the users to modify the scripts as per their own needs, so that all Scada Honeynet deployments won't look the same.

## Usage

1. Install Honeyd (for example https://github.com/DataSoft/Honeyd, version 1.6d).
2. Copy `honeyd.conf.sample` to your Honeyd configuration, replace `IP` with an address routed to Honeyd, and point the commands at the `plc/` directory.
3. Create the log file `/var/log/scadahoneynet.log`, writable by the user Honeyd runs its scripts as.
4. Run Honeyd, for example: `honeyd -d -i eth1 --disable-webserver -f honeyd.conf IP`

The scripts read the connection on standard input and answer on standard output, as Honeyd subsystems do.

## Changes for Python 3

Only what Python 3 needs; responses, behaviour and log lines are the same as with Python 2.

* All scripts: `python3` shebang where there was one; the unused `thread` and `cgi` imports removed; `string.splitfields` and `string.rstrip` replaced with the equivalent `str` methods.
* `honeyd-ftpd.py`, `honeyd-telnet.py`, `honeyd-html.py`: standard input and output use Latin-1 and no newline translation, so bytes and line endings pass through unchanged as they did under Python 2.
* `honeyd-modbus.py`: reads and writes bytes (`sys.stdin.buffer`, `sys.stdout.buffer`), byte-string defaults, integer division for the coil byte count.
* `honeyd-html.py`: `print` statements as function calls.
* `honeyd.conf.sample`: the sample configuration from the 0.3 release notes, with `python3`.
* `COPYING`: the text of the GNU General Public License version 2, which the scripts' headers refer to.

## Licence

GNU General Public License, version 2 (see the headers of the scripts and `COPYING`).
