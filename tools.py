import os
import subprocess
import ctypes
from PyQt6 import QtWidgets

def launch_boost_tester():
    """Launch BoostTester.sp00n.exe from the tools folder."""
    try:
        os.startfile(os.path.join('tools', 'BoostTester.sp00n.exe'))
    except Exception as e:
        print(f"Error launching BoostTester: {e}")

def launch_intel_voltage_control():
    """Show the current Intel FIVR offsets in an elevated, persistent console."""
    tool_directory = os.path.abspath(os.path.join('tools', 'IntelVoltageControl'))
    executable = os.path.join(tool_directory, 'IntelVoltageControl.exe')

    if not os.path.isfile(executable):
        QtWidgets.QMessageBox.critical(
            None,
            "Intel Voltage Control Not Found",
            f"IntelVoltageControl.exe was not found at:\n{executable}",
        )
        return

    try:
        # IntelVoltageControl is a command-line utility rather than an interactive
        # application. It also needs administrator rights to initialise WinRing0.
        # Run its read-only `show` command and leave the console open so the user
        # can read the result and enter another documented command if desired.
        command = (
            f'/k ""{executable}" show & echo. & '
            'echo IntelVoltageControl is a command-line tool. '
            'See IntelVoltageControl.txt for usage."'
        )
        result = ctypes.windll.shell32.ShellExecuteW(
            None,
            "runas",
            "cmd.exe",
            command,
            tool_directory,
            1,
        )
        if result <= 32:
            QtWidgets.QMessageBox.critical(
                None,
                "Unable to Start Intel Voltage Control",
                f"Windows could not open the elevated terminal (error {result}).",
            )
    except Exception as e:
        QtWidgets.QMessageBox.critical(
            None, "Unable to Start Intel Voltage Control", str(e)
        )

def launch_apic_ids():
    """Launch APICID.exe from the tools folder in a new terminal window without blocking the GUI."""
    try:
        apicid_exe_path = os.path.abspath(os.path.join('tools', 'APICID.exe'))
        if not os.path.exists(apicid_exe_path):
            QtWidgets.QMessageBox.critical(None, "Error", f"APICID.exe not found at: {apicid_exe_path}")
            return
        
        subprocess.Popen(['cmd.exe', '/k', f'.\\APICID.exe'],
                         cwd=os.path.dirname(apicid_exe_path),
                         creationflags=subprocess.CREATE_NEW_CONSOLE)
        
    except Exception as e:
        QtWidgets.QMessageBox.critical(None, "Error", f"Failed to launch APICID.exe: {e}")

def launch_core_tuner_x():
    """Launch CoreTunerX.exe from the tools folder."""
    try:
        os.startfile(os.path.join('tools', 'CoreTunerX.exe'))
    except Exception as e:
        print(f"Error launching CoreTunerX: {e}")

def launch_smu_debug_tool(parent=None):
    """Launch the advanced SMUDebugTool after an explicit safety warning."""
    exe_path = os.path.abspath(os.path.join('tools', 'SMUDebugTool', 'SMUDebugTool.exe'))
    if not os.path.isfile(exe_path):
        QtWidgets.QMessageBox.critical(
            parent, "SMU Debug Tool Not Found", f"SMUDebugTool.exe not found at:\n{exe_path}"
        )
        return

    answer = QtWidgets.QMessageBox.warning(
        parent,
        "Open Advanced Ryzen Tool?",
        "SMU Debug Tool can directly change Ryzen CPU settings, including Curve "
        "Optimizer, P-states, scalar and BCLK. Incorrect settings may cause crashes, "
        "data loss or unsafe operation.\n\nOnly continue if you understand the settings "
        "you intend to change.",
        QtWidgets.QMessageBox.StandardButton.Yes |
        QtWidgets.QMessageBox.StandardButton.Cancel,
        QtWidgets.QMessageBox.StandardButton.Cancel,
    )
    if answer == QtWidgets.QMessageBox.StandardButton.Yes:
        try:
            os.startfile(exe_path)
        except OSError as error:
            QtWidgets.QMessageBox.critical(parent, "Unable to Start SMU Debug Tool", str(error))

import os
import ctypes
import subprocess

def launch_enable_performance_counters():
    """Launch enable_performance_counter.bat from the tools folder with administrator privileges."""
    try:
        bat_path = os.path.abspath(os.path.join("tools", "enable_performance_counter.bat"))
        
        # Verify the batch file exists
        if not os.path.exists(bat_path):
            print(f"Batch file not found at: {bat_path}")
            return
        
        # Attempt to run with ShellExecuteW (preferred method for elevation)
        result = ctypes.windll.shell32.ShellExecuteW(None, "runas", "cmd.exe", f'/c "{bat_path}"', None, 1)
        if result <= 32:  # ShellExecuteW returns > 32 on success
            print(f"ShellExecuteW failed with code {result}. Possible UAC denial or insufficient permissions.")
        
    except AttributeError:
        # Fallback for non-Windows systems or if ctypes fails
        print("ShellExecuteW not available, attempting subprocess fallback...")
        try:
            subprocess.run([bat_path], shell=True, check=True, creationflags=subprocess.CREATE_NEW_CONSOLE)
        except subprocess.CalledProcessError as e:
            print(f"Subprocess failed with return code {e.returncode}")
        except Exception as e:
            print(f"Fallback error: {e}")
    except Exception as e:
        print(f"Error launching enable_performance_counter.bat: {e}")

def open_helpers_folder():
    """Open the helpers folder in the file explorer."""
    try:
        os.startfile('helpers')
    except Exception as e:
        print(f"Error opening helpers folder: {e}")
