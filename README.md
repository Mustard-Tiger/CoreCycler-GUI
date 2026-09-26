# CoreCycler GUI

A maintained Windows GUI for [CoreCycler](https://github.com/sp00n/corecycler),
updated to work with the current CoreCycler engine and its supporting tools.

> This is a community-maintained continuation of the discontinued
> [CoreCycler-GUI](https://github.com/LucidLuxxx/CoreCycler-GUI) project. It is not an official release from the original
> CoreCycler or CoreCycler-GUI authors.

## Download

Download the latest packaged release from the
[Releases page](https://github.com/Mustard-Tiger/CoreCycler-GUI/releases).

Extract the entire ZIP archive to a writable folder before starting the GUI.
Do not run the application from inside the ZIP.

## What is CoreCycler GUI?

CoreCycler is a PowerShell-based stability-testing tool that cycles a selected
stress test through individual CPU cores. Testing cores separately allows them
to reach higher boost clocks and can expose instabilities that may not appear
during a conventional all-core stress test.

CoreCycler GUI provides a graphical interface for configuring and starting
CoreCycler. It supports AMD Ryzen Curve Optimizer testing and can also be used
to test Intel Active-Core Turbo Boost settings.

The GUI itself is written in Python using PyQt6. The underlying CoreCycler
engine remains a PowerShell application.

## Important safety warning

Stress testing can produce very high CPU temperatures and sustained electrical
load. Inadequate cooling, unsafe voltage or frequency settings, or prolonged
operation at high temperatures may cause instability, degradation, data loss,
or hardware damage. Monitor temperatures and use this software entirely at your own risk.

## Installation

1. Download the latest release ZIP.
2. Extract the complete archive to a folder of your choice.
3. Run `CoreCycler.exe`.
4. Configure the desired stress test and options in the GUI.
5. Select **Start** to save the displayed settings and begin the test.

Keep all included folders and files together. CoreCycler relies on the bundled
configuration files, helper scripts, stress-test programs, and utilities.

### AIDA64

AIDA64 is supported but is not redistributed because of its licence. To use
it, obtain the **Portable Engineer** edition from the
[official AIDA64 website](https://www.aida64.com/downloads) and extract it into
`test_programs/aida64`.

The regular Extreme edition does not provide the command-line functionality
required by CoreCycler.

## Quick start

1. Choose a stress-test program and test mode.
2. Choose how long each core should be tested.
3. Review the core order and any cores that should be ignored.
4. Check the remaining settings for the selected stress test.
5. Start the test and monitor CPU temperatures throughout the run.

CoreCycler records its results in the `logs` directory. If an error occurs on
a particular core, adjust that core's voltage, Curve Optimizer value, or boost
settings before testing again.

For explanations of individual settings, see the comments in
`configs/default.config.ini`.

## Video guide

[CoreCycler-GUI setup guide on YouTube](https://youtu.be/GWfc_CxLYgY)

Good guide by the author of the earlier CoreCycler-GUI version. The general
workflow remains useful, but some controls, available tools, and configuration
options have changed in this maintained release.

## What's updated in this continuation?

This maintained version includes, among other changes:

- integration with a post-v0.11.0.3 CoreCycler development revision,
  internally identified as v0.11.0.4, and its current configuration format;
- compatibility handling for older or incomplete GUI-generated configurations;
- updated current and legacy y-cruncher support;
- updated Prime95 and Linpack integration;
- improved Automatic Test Mode support;
- updated ZenTimings and SMUDebugTool components;
- Ryzen Curve Optimizer adjustment through `ryzen-smu-cli`;
- removal of obsolete `PBO2Tuner` and `pbocli` integration;
- safer launching of the Intel Voltage Control command-line utility;
- numerous layout, labelling, validation, and usability fixes; and
- reproducible GUI and release packaging scripts.

See [CHANGELOG.txt](CHANGELOG.txt) for the detailed list of changes.

## Included stress tests and utilities

CoreCycler can work with:

- [Prime95](https://www.mersenne.org/download/)
- [y-cruncher](http://www.numberworld.org/y-cruncher/)
- [Intel Optimized LINPACK Benchmark](https://www.intel.com/content/www/us/en/download/780789/intel-oneapi-math-kernel-library-onemkl-benchmarks-suite-for-windows.html)
- [AIDA64 Portable Engineer](https://www.aida64.com/downloads) (not included)

The release also contains supporting hardware-information and tuning tools.
Those components remain the work of their respective authors and retain their
own licences. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for their
source repositories, versions, attribution and licence information.

## Troubleshooting

### CoreCycler reports a Windows performance-counter error

Some test modes use the Windows `PerfProc` performance counter to monitor CPU
utilisation. The counter may need to be enabled or rebuilt. Click 'Enable Perf Counters'
in the `tools` section.

### AIDA64 will not start

Confirm that the Portable Engineer edition has been extracted into
`test_programs/aida64` and that at least one AIDA64 test mode has been selected
in the GUI.

### Where can I find descriptions of all settings?

See `configs/default.config.ini`, which documents the available CoreCycler
configuration options.

For more detailed information about the underlying engine, consult the
[CoreCycler repository](https://github.com/sp00n/corecycler).

## Project lineage and credits

This repository builds on the work of several maintainers:

- [sp00n](https://github.com/sp00n) created CoreCycler and maintains the
  underlying PowerShell engine.
- [LucidLuxxx](https://github.com/LucidLuxxx) created and maintained the
  original CoreCycler-GUI project.

The original authors retain credit for their work. Maintenance of this fork
does not imply that the original authors endorse its subsequent changes.

## Contributing

Bug reports and proposed improvements are welcome through the
[issue tracker](https://github.com/Mustard-Tiger/CoreCycler-GUI/issues).

When reporting a problem, include the selected stress test, relevant settings,
the application log, and enough system information to reproduce the issue.
Do not publish private information or licence keys.

## Licence

CoreCycler is distributed under the
[Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
licence](https://creativecommons.org/licenses/by-nc-sa/4.0/). In summary, you
may share and adapt the work for non-commercial purposes provided that you give
appropriate credit, indicate changes, and distribute adaptations under the
same licence.

See [LICENSE](LICENSE) for the licence included with this repository.

Bundled third-party programs and libraries retain their original licences.
Refer to [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) and the licence and
readme files included alongside those components.
