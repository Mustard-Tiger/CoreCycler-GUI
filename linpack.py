import configparser
import winreg

from PyQt6 import QtWidgets


FASTEST_ONLY_VERSIONS = {'2021', '2024'}


def update_linpack_mode_availability(ui):
    """Keep the mode control aligned with the selected Linpack version."""
    fastest_only = ui.linpack_version_comboBox.currentText() in FASTEST_ONLY_VERSIONS
    if fastest_only:
        ui.linpack_mode_comboBox.setCurrentText('Fastest')
        ui.linpack_mode_comboBox.setToolTip(
            'Linpack 2021 and 2024 always use FASTEST (AVX2).'
        )
    else:
        ui.linpack_mode_comboBox.setToolTip('Select the instruction/performance mode.')
    ui.linpack_mode_comboBox.setEnabled(not fastest_only)


def _processor_name():
    try:
        with winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r'HARDWARE\DESCRIPTION\System\CentralProcessor\0',
        ) as key:
            return str(winreg.QueryValueEx(key, 'ProcessorNameString')[0])
    except OSError:
        return ''


def validate_linpack_selection(ui, parent=None):
    """Warn about a known unsupported old-MKL mode on AMD processors."""
    is_linpack = ui.general_stressTestProgram_radioButton_linpack.isChecked()
    processor_name = _processor_name().lower()
    is_problem_combination = (
        ui.linpack_version_comboBox.currentText() == '2018'
        and ui.linpack_mode_comboBox.currentText().lower() == 'slowest'
        and ('amd' in processor_name or 'ryzen' in processor_name)
    )
    if not is_linpack or not is_problem_combination:
        return True

    answer = QtWidgets.QMessageBox.warning(
        parent,
        'Linpack 2018 SLOWEST Compatibility',
        'Linpack 2018 SLOWEST can exit with “Intel MKL ERROR: CPU 1 is not '
        'supported” on modern AMD Ryzen processors. No stress test will run if '
        'that happens.\n\nUse MEDIUM or FASTEST, or choose Linpack 2019/2024, '
        'unless you specifically want to retry this combination.',
        QtWidgets.QMessageBox.StandardButton.Yes |
        QtWidgets.QMessageBox.StandardButton.Cancel,
        QtWidgets.QMessageBox.StandardButton.Cancel,
    )
    return answer == QtWidgets.QMessageBox.StandardButton.Yes

def load_linpack_config(ui):
    """
    Load settings from the [Linpack] section of config.ini and update the GUI combo boxes.
    
    Args:
        ui: The UI object from mainwindow.py containing the GUI elements.
    """
    config = configparser.ConfigParser()
    config.read('config.ini')
    
    if 'Linpack' in config:
        linpack = config['Linpack']
        
        # Load version setting into linpack_version_comboBox
        version = linpack.get('version', '2021')  # Default to '2021' if not found
        ui.linpack_version_comboBox.setCurrentText(version)
        
        # Load mode setting into linpack_mode_comboBox
        mode = linpack.get('mode', 'Fast')  # Default to 'Fast' if not found
        ui.linpack_mode_comboBox.setCurrentText(mode)
        
        # Load memory setting into linpack_memory_comboBox
        memory = linpack.get('memory', '6GB')  # Default to '6GB' if not found
        ui.linpack_memory_comboBox.setCurrentText(memory)
    else:
        # If [Linpack] section doesn't exist, set combo boxes to their first item
        ui.linpack_version_comboBox.setCurrentIndex(0)
        ui.linpack_mode_comboBox.setCurrentIndex(0)
        ui.linpack_memory_comboBox.setCurrentIndex(0)

    update_linpack_mode_availability(ui)

def apply_linpack_config(ui):
    """
    Update the [Linpack] section in config.ini based on current GUI combo box selections.
    
    Args:
        ui: The UI object from mainwindow.py containing the GUI elements.
    """
    config = configparser.ConfigParser()
    config.read('config.ini')
    
    # Create [Linpack] section if it doesn't exist
    if 'Linpack' not in config:
        config['Linpack'] = {}
    
    linpack = config['Linpack']
    
    # Update version setting from linpack_version_comboBox
    version = ui.linpack_version_comboBox.currentText()
    linpack['version'] = version
    
    # Update mode setting from linpack_mode_comboBox
    mode = ui.linpack_mode_comboBox.currentText()
    linpack['mode'] = mode
    
    # Update memory setting from linpack_memory_comboBox
    memory = ui.linpack_memory_comboBox.currentText()
    linpack['memory'] = memory
    
    # Write the updated configuration back to config.ini
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
