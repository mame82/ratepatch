#!/bin/bash
# find and save working dir of script
wdir=$( cd $(dirname $BASH_SOURCE[0]) && pwd)
start_dir=$(pwd)

if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

rndis_modpath="/lib/modules/$(uname -r)/kernel/drivers/usb/gadget/function/usb_f_rndis.ko"

cd $wdir/rndis

echo "Starting bitrate patch for RNDIS composite module"
echo "================================================="
echo "..Creating backup of module at $(pwd)/usb_f_rndis.ko.orig"
cp $rndis_modpath ./usb_f_rndis.ko.orig

if python rndis_patch.py; then
	echo "RNDIS patch failed"
else
	echo "Patch succeeded"
	echo "..Overwriting module"
	cat usb_f_rndis.ko.patched > $rndis_modpath
	echo "You need to reboot for the patch to work, preinstalled RNDIS windows drivers have to be reinstalled"
fi
