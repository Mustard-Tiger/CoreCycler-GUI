# Third-party notices

CoreCycler GUI brings together the CoreCycler engine and a number of separate
stress-testing, diagnostic and hardware-control components. Those components
remain the work of their respective authors and are governed by their own
licences and terms.

This file is an attribution and source index. It does not replace the complete
licence texts distributed in `LICENSE` or alongside individual components.
Where there is any conflict, the component's own licence controls.

## Core projects

### CoreCycler

- Author: sp00n
- Source: <https://github.com/sp00n/corecycler>
- Bundled revision: post-v0.11.0.3 development revision, internally identified
  as v0.11.0.4
- Licence: Creative Commons Attribution-NonCommercial-ShareAlike 4.0
- Local licence: `LICENSE`
- Upstream documentation: `CORECYCLER-README.txt`

The bundled engine has been integrated with and adapted for this graphical
interface. The original author does not necessarily endorse these changes.

### Original CoreCycler-GUI

- Author: LucidLuxxx
- Source: <https://github.com/LucidLuxxx/CoreCycler-GUI>
- Continued project: <https://github.com/Mustard-Tiger/CoreCycler-GUI>

This repository preserves the original Git history and continues the
discontinued GUI project with compatibility, packaging and usability changes.

## Stress-test programs

### Prime95

- Author/publisher: Mersenne Research, Inc. / George Woltman
- Source and downloads: <https://www.mersenne.org/download/>
- Bundled version: 30.19
- Terms: <https://www.mersenne.org/legal/>
- Local licence: `test_programs/p95/license.txt`

### y-cruncher

- Author: Alexander J. Yee
- Project and downloads: <http://www.numberworld.org/y-cruncher/>
- Licence: <http://www.numberworld.org/y-cruncher/license.html>
- Bundled variants: the current CoreCycler-supported package and legacy
  y-cruncher 0.7.10
- Local documentation: `test_programs/y-cruncher/Read Me.txt` and
  `test_programs/y-cruncher-0.7.10/Read Me.txt`

### Intel Optimized LINPACK Benchmark

- Publisher: Intel Corporation
- Current Windows benchmark package:
  <https://www.intel.com/content/www/us/en/download/780789/intel-oneapi-math-kernel-library-onemkl-benchmarks-suite-for-windows.html>
- Bundled versions: 2018.0.3.1, 2019.0.3.1, 2021.4.1.0 and 2024.2.1.0
- Local licence: `test_programs/linpack/license.rtf`
- Local documentation: `test_programs/linpack/readme.txt`

The older packages used by CoreCycler were obtained from Intel distributions
archived at the following locations:

- 2024.2.1.0: <https://web.archive.org/web/20240722184607/https://registrationcenter-download.intel.com/akdlm/IRC_NAS/7816a8cf-2378-4d49-bfa6-6013a3d7be6a/w_onemkl_p_2024.2.0.662_offline.exe>
- 2021.4.1.0: <https://web.archive.org/web/20211115133152/https://registrationcenter-download.intel.com/akdlm/irc_nas/18230/w_onemkl_p_2021.4.0.640_offline.exe>
- 2019.0.3.1: <https://web.archive.org/web/20190509182800/https://registrationcenter-download.intel.com/akdlm/irc_nas/tec/15247/w_mkl_2019.3.203.exe>
- 2018.0.3.1: <https://web.archive.org/web/20220412021802/https://registrationcenter-download.intel.com/akdlm/irc_nas/9752/w_mklb_p_2018.3.011.zip>

### AIDA64

- Publisher: FinalWire Ltd.
- Website: <https://www.aida64.com/downloads>

AIDA64 is supported but is not included in the release. Users must supply their
own licensed copy of the Portable Engineer edition.

## Utilities

### APICID

- Author: sp00n
- Source: <https://github.com/sp00n/APICID>
- Bundled version: 0.1.2.0
- Licence: MIT

### BoostTester

- Original author/project: jedi95, <https://github.com/jedi95/BoostTester>
- Additional source: <https://github.com/mann1x/BoostTesterMannix>
- CoreCycler variant: <https://github.com/sp00n/BoostTester>
- Licence for the CoreCycler variant: The Unlicense

### CoreTunerX

- Author/project: CXWorld
- Source: <https://github.com/CXWorld/CoreTunerX>
- Bundled version: 1.0.0.0
- Licence and terms: see the upstream repository

### IntelVoltageControl

- Author/project: jamestut
- Source: <https://github.com/jamestut/IntelVoltageControl>
- Licence: MIT
- Bundled driver component: WinRing0, modified BSD licence
- Local licences: `tools/IntelVoltageControl/LICENSE.txt` and
  `tools/IntelVoltageControl/WinRing0.LICENSE.txt`

### ryzen-smu-cli

- Author/project: rawhide-kobayashi
- Source: <https://github.com/rawhide-kobayashi/ryzen-smu-cli>
- Bundled version: 0.1.5.0-sp00n, source revision
  `4eef23b4093fa8f27a2f6c12dee24fb3bddf30e5`
- Licence: GNU General Public License v3.0
- Related source: <https://github.com/irusanov/ZenStates-Core>
- Additional local notices: `tools/ryzen-smu-cli/InpOut.LICENSE.txt` and
  `tools/ryzen-smu-cli/WinIo32.LICENSE.txt`

### SMUDebugTool

- Author: Ivan Rusanov
- Source: <https://github.com/irusanov/SMUDebugTool/tree/v1.41>
- Bundled version: 1.41
- Licence: GNU General Public License v3.0
- Local licence: `tools/SMUDebugTool/LICENSE`
- Related source: <https://github.com/irusanov/ZenStates-Core>
- Additional local notices are stored in `tools/SMUDebugTool`

### ZenTimings

- Author: Ivan Rusanov
- Source: <https://github.com/irusanov/ZenTimings/tree/v1.39>
- Bundled version: 1.39.487 (release v1.39)
- Related source: <https://github.com/irusanov/ZenStates-Core>
- Local documentation and checksums: `tools/ZenTimings/README.txt` and
  `tools/ZenTimings/CHECKSUMS.txt`
- Driver notices for InpOut and PawnIO are stored in `tools/ZenTimings`

## CoreCycler helper components

### WriteConsoleToWriteFileWrapper

- DLL source: <https://github.com/sp00n/WriteConsoleToWriteFileWrapperDll>
- EXE source: <https://github.com/sp00n/WriteConsoleToWriteFileWrapperExe>
- Licence: MIT

## Driver and library notices

The utilities above may include third-party drivers and managed libraries,
including InpOut, WinIo, WinRing0, PawnIO, ZenStates-Core, Newtonsoft.Json and
Microsoft .NET libraries. Licence files supplied by their authors are retained
next to the components wherever provided. Consult the component directories
before redistributing individual files separately from the complete package.

## Modifications and responsibility

CoreCycler GUI changes integration, configuration, launch behaviour and
packaging around these components. Unless explicitly stated otherwise, the
third-party binaries themselves are redistributed builds from their respective
projects. Inclusion does not imply that their authors endorse CoreCycler GUI or
this maintained continuation.
