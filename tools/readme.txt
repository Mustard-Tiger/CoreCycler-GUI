In this directory are some helpful tools that you might find interesting.



APICID.exe
----------
https://github.com/sp00n/APICID

Simple tool to display the APIC ID for each logical core / virtual core.
Helpful for linking the message in a WHEA Error entry to an actual core.



BoostTester.exe
---------------
https://github.com/jedi95/BoostTester

Simple tool for generating loads that should trigger maximum CPU boost clocks.

This is helpful to check the maximum possible boost clock on the various cores. It generates a very light load so the cores
should boost as high as they can. Unfortunately there is no error checking for this tool.



BoostTester.sp00n.exe
---------------------
https://github.com/sp00n/BoostTester

Modified version of the original BoostTester tool, which correctly works with Intel P- and E-Cores.
Also includes the modifications done by mann1x which apparently generates an even higher core clock.

Sources:
https://github.com/jedi95/BoostTester
https://github.com/mann1x/BoostTesterMannix



CoreTunerX.exe
--------------
https://github.com/CXWorld/CoreTunerX

This tool reads the Windows CPU cores rating from the event viewer and saves them in a text document (results.txt).
The read out values have no unit and are only used to compare the cores of this one CPU with each other, not with other CPUs.

How to interpret the performance numbers:
The higher the score, the higher the priority from the windows sheduler.



enable_performance_counter.bat
------------------------------
Sometimes the Perfomance Counters can corrupt on a Windows installation, which breaks CoreCycler if it set to use them.
This batch file tries to fix/reset these Performance Counters.
It requires Administator priviliges and will try to get them / complain otherwise.



IntelVoltageControl
-------------------
https://github.com/jamestut/IntelVoltageControl

This command line application allows setting up FIVR voltage offset directly from Microsoft Windows of some Intel CPUs,
notably 4th gen (Haswell) and newer.
Note that this software operates by writing to MSR 0x150, just like many undervolting utilities do.
If other utilities cannot change the voltage offsets, then this software will not work either.

Usage:
To show all currently configured FIVR offsets:
IntelVoltageControl.exe show

Apply a -50mv voltage offset to the CPU (and to the CPU Cache, it is required to set both to the same value):
IntelVoltageControl.exe set --commit 0 -50 2 -50



ryzen-smu-cli
-------------
https://github.com/rawhide-kobayashi/ryzen-smu-cli

A CLI tool for the ZenStates SMU library. See ZenStates-Core for compatibility.

Requires .NET Framework 8.

Usage:
To get the currently applied Curve Optimizer values:
ryzen-smu-cli --get-offsets-terse

To set new Curve Optimizer values:
ryzen-smu-cli --offset CO_Core0,CO_Core1,[...],CO_CoreMax

For example, to set the Curve Optimizer values for a 6 core processor:
ryzen-smu-cli --offset -20,2,-15,-20,-19,-5

Note the minus sign for negative Curve Optimizer values.



SMUDebugTool
------------
https://github.com/irusanov/SMUDebugTool

A tool that allows you to set various properties for Ryzen processors, including the Curve Optimizer values, Scalar value,
P-States, the BCLK, and some others.

It also allows you to save a profile, which can be restored on startup.