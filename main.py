import configparser
import sys
import os
import shutil
import subprocess
import start
import menu_bar
from config_compat import ensure_current_config
from PyQt6 import QtWidgets, QtCore
from mainwindow import Ui_MainWindow
from general import load_general_config, apply_general_config, launch_configs_folder, save_config_to_file, load_all_configs, apply_all_configs
from zentimings import launch_zentimings
from linpack import update_linpack_mode_availability, validate_linpack_selection
from aida64 import clear_aida64_mode_warning, validate_aida64_selection
from ycruncher import update_ycruncher_test_availability
from functools import partial
from reset import reset_config
from tools import (
    launch_boost_tester,
    launch_intel_voltage_control,
    launch_apic_ids,
    launch_core_tuner_x,
    launch_smu_debug_tool,
    launch_enable_performance_counters,
    open_helpers_folder
)

if sys.platform == "win32":
    import ctypes
    kernel32 = ctypes.WinDLL('kernel32')
    user32 = ctypes.WinDLL('user32')
    hWnd = kernel32.GetConsoleWindow()
    if hWnd:
        user32.ShowWindow(hWnd, 0)  # 0 is SW_HIDE

# Set working directory to the .exe's location when compiled
if getattr(sys, 'frozen', False):
    exe_dir = os.path.dirname(sys.executable)
    os.chdir(exe_dir)
base_dir = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))
# All configuration modules use paths relative to the application directory.
os.chdir(base_dir)

# Function to handle config file checkbox (unchanged)
def handle_config_file_checkbox(ui, state):
    if state == QtCore.Qt.CheckState.Unchecked.value:
        ui.general_useConfigFile_lineEdit.clear()
        apply_all_configs(ui)
        load_all_configs(ui)
    elif state == QtCore.Qt.CheckState.Checked.value and ui.general_useConfigFile_lineEdit.text():
        config_path = os.path.join(base_dir, 'config.ini')
        custom_config_path = os.path.join(base_dir, ui.general_useConfigFile_lineEdit.text())
        
        if os.path.exists(custom_config_path):
            default_config_path = os.path.join(base_dir, 'configs', 'default.config.ini')
            if os.path.exists(default_config_path):
                shutil.copyfile(default_config_path, config_path)
            else:
                QtWidgets.QMessageBox.warning(None, "Warning", f"Default config file not found at {default_config_path}.")
                return
            
            custom_config = configparser.ConfigParser()
            custom_config.read(custom_config_path)
            main_config = configparser.ConfigParser()
            main_config.read(config_path)
            
            for section in custom_config.sections():
                if section not in main_config:
                    main_config[section] = {}
                for key, value in custom_config[section].items():
                    main_config[section][key] = value
            
            with open(config_path, 'w') as configfile:
                main_config.write(configfile)
            
            load_all_configs(ui)
        else:
            QtWidgets.QMessageBox.warning(None, "Warning", f"Config file not found at {custom_config_path}.")

# New function to ensure config.ini exists
def ensure_config_exists(ui):
    config_path = os.path.join(base_dir, 'config.ini')
    default_config_path = os.path.join(base_dir, 'configs', 'default.config.ini')
    
    try:
        if ensure_current_config(config_path, default_config_path):
            print(f"Created or upgraded {config_path}")
    except (OSError, configparser.Error) as error:
        QtWidgets.QMessageBox.critical(None, "Configuration Error", str(error))
        return
    
    # Load the settings into the GUI
    load_all_configs(ui)

# New function to open the logs folder
def open_logs_folder(ui):
    """
    Open the 'logs' folder located in the base directory.
    """
    logs_folder = os.path.join(base_dir, 'logs')
    
    # Ensure the logs folder exists (create it if it doesn't)
    if not os.path.exists(logs_folder):
        os.makedirs(logs_folder)
    
    # Open the folder using the appropriate command for the OS
    if sys.platform == "win32":
        subprocess.Popen(['explorer', logs_folder])
    elif sys.platform == "darwin":
        subprocess.Popen(['open', logs_folder])
    else:
        subprocess.Popen(['xdg-open', logs_folder])


def settings_are_valid(ui, main_window):
    return (
        validate_aida64_selection(ui, main_window)
        and validate_linpack_selection(ui, main_window)
    )


def apply_current_settings(ui, main_window):
    if not settings_are_valid(ui, main_window):
        return False
    try:
        apply_all_configs(ui)
        return True
    except (OSError, ValueError, configparser.Error) as error:
        QtWidgets.QMessageBox.critical(
            main_window, 'Unable to Apply Settings', str(error)
        )
        return False


def start_test(ui, main_window):
    if apply_current_settings(ui, main_window):
        start.run_corecycler(main_window)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    
    # Ensure config.ini exists and load settings
    ensure_config_exists(ui)
    
    # Connect signals
    ui.apply_config_pushButton.clicked.connect(
        lambda: apply_current_settings(ui, MainWindow)
    )
    ui.reset_config_pushButton.clicked.connect(partial(reset_config, ui, load_all_configs))
    ui.saveConfig_pushButton.clicked.connect(
        lambda: save_config_to_file(ui)
        if settings_are_valid(ui, MainWindow) else None
    )
    ui.boostTester_pushButton.clicked.connect(launch_boost_tester)
    ui.intelVoltageControl_pushButton.clicked.connect(launch_intel_voltage_control)
    ui.apicIds_pushButton.clicked.connect(launch_apic_ids)
    ui.coreTunerX_pushButton.clicked.connect(launch_core_tuner_x)
    ui.smuDebugTool_pushButton.clicked.connect(lambda: launch_smu_debug_tool(MainWindow))
    ui.enablePerformanceCounters_pushButton.clicked.connect(launch_enable_performance_counters)
    ui.helpers_pushButton.clicked.connect(open_helpers_folder)
    ui.zenTimings_pushButton.clicked.connect(launch_zentimings)
    ui.general_stressTestProgram_radioButton_ycruncher.toggled.connect(
        lambda: update_ycruncher_test_availability(ui)
    )
    ui.general_stressTestProgram_radioButton_ycruncher_old.toggled.connect(
        lambda: update_ycruncher_test_availability(ui)
    )
    update_ycruncher_test_availability(ui)
    ui.linpack_version_comboBox.currentTextChanged.connect(
        lambda: update_linpack_mode_availability(ui)
    )
    for aida64_mode_checkbox in (
        ui.aida64_mode_cache_checkBox,
        ui.aida64_mode_cpu_checkBox,
        ui.aida64_mode_fpu_checkBox,
        ui.aida64_mode_ram_checkBox,
    ):
        aida64_mode_checkbox.toggled.connect(
            lambda: clear_aida64_mode_warning(ui)
        )
    menu_bar.setup_menu_connections(ui)
    ui.configsFolder_toolButton.clicked.connect(lambda: launch_configs_folder(ui))
    ui.start_test_pushButton.clicked.connect(lambda: start_test(ui, MainWindow))
    ui.main_logsFolder_toolButton.clicked.connect(lambda: open_logs_folder(ui))  # Connect the logs button
    
    MainWindow.show()
    sys.exit(app.exec())
