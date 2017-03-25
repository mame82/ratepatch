Bitrate patch for P4wnP1
========================

Features (TL;TR)
----------------
* **RNDIS** interfaces bitrate is at **20 GBit per second**
* **ECM** interfaces bitrate is at **4 GBit per second**

See requirements and issues

Remarks
-------

The real bitrate achieved by both, RNDIS and CDC ECM, depends on the effective transfer rate of the underlying USB stack.
To be more clear, P4wnP1 and most other USB devices are HIGH SPEED devices (USB 2.0), which means the maximum transfer rate is limited to 450 MBits per second.
Anyway, both protocols allow to offer a maximum (theoretical) transfer rate to the USB host.
Exactly this maximum transfer rate is changed by this patch.

So what is this good for? 
-------------------------

The patch is meant to be used with `P4nP1 USB attack platform <https://github.com/mame82/P4wnP1>`_ which could benefit the increased maximum bitrate. 

How does P4wnP1 benefit from this ?
-----------------------------------

P4wnP1 runs different USB attacks. In many cases it runs a network adapter and a DHCP server to add static routes to the target host or to promote itself as defualt gateway. Often these routing entries compete with the given routing entries of the target (for instance if there's already a default gateway). If the target has two routes it could choose from, it basically decides which one to take based on the so called metric. Guess which fact is used by the target OS to decide which metric to apply to a new route ? Yes, you get it - it is the interface speed in most cases. No its not the effective speed, but the theoretical maximum. That's how P4wnP1 benefits from this.

Reuirements and issues
======================

The patch targets usb_f_rndis.ko and usb_f_ecm.ko on Raspbian with **Kernel 4.4.50+**
As the whole code is position independant, the patch could possibly apply to other versions of these kernel modules - USE IT AT YOUR OWN RISK.

The patch doesn't change the ethernet gadget (g_ether), but the RNDIS and CDC ECM function, which have to be used with the composite gadget (as done by P4wnP1).

Windows 10 issue
----------------

The RNDIS part of the patch has been tested on Windows 7 and Windows 10. While Windows 7 works well, the NDIS 6 stack on **Windows 10 does speed recognition** in a different manner. This results in an issue:

The RNDIS device is detected with the desired device speed (20 GBit/s) on initial driver install. Reconnecting the device, the Windows 10 RNDIS driver detects the device with a bitrate of 0 Bps. This could be circumvented by deactivating and reactivating the device or reinstalling the driver. **This behavior is caused by the RNDIS gadget function driver delivered with raspbian, not by this patch!** Anyway, I haven't fixed this (because the patch does work on the compiled module binary, not on the source code). 
From the perspective of P4wnP1 this is less an issue, because one-time USB drive-by attacks work (correct speed at innitial driver installation) and the device stays perfectly connectable, even if the link theoretical speed drops to 0 Bps. Of course a low metric couldn't be achieved when this issue occures.

There're two additional ways, to circumvent this without touching the target host:
1) Change product and vendor ID of P4wnP1 to values unused so far, in order to force driver reinstall (and link speed detection with correct bitrate) 
2) Use vendor ID "04B3" and product ID "4010" to force Windows 10 to install a "IBM USB Remote NDIS Device". The corresponding driver doesn't produce the bitrate issue. The shortcoming of this approach would be, that only the RNDIS interface will be enumerated (no HID, no USB mass storage, no serial ...)

ECM bitrate limit
-----------------

The link speed of an ECM interface is encoded differently (32 Bit value), which results in a maximum of 4 GBit per second which could be set. On MacOS the patched P4wnP1 ECM interface gets detected as 1 Gbit/s device (backed with 4 GBit/s) which is enough to achieve a better metric than most devices present.

Installation
============

The RNDIS patch could be installed by running ``runpatch.sh`` with root privileges. This fires a python script which checks if ``usb_f_rndis.ko`` fits the requirements to be patched and creates a backup of the original Kernel driver module. The ``usb_f_ecm.ko`` module won't be patched automatically, as the according script isn't fnished yet. But unlike the RNDIS patch, the ECM patch is very simple. So a prepatched binary is provided in the ``ecm`` subfolder (only for **Kernel 4.4.50+**). The ECM patch will be included as soon as testing has been finished.



