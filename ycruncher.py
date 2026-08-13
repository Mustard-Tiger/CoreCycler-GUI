import configparser


def _modern_test_widgets(ui):
    return {
        'BKT': ui.ycruncher_tests_bkt_checkBox,
        'BBP': ui.ycruncher_tests_bbp_checkBox,
        'SFT': ui.ycruncher_tests_sft_checkBox,
        'SFTv4': ui.ycruncher_tests_sftv4_checkBox,
        'SNT': ui.ycruncher_tests_snt_checkBox,
        'SVT': ui.ycruncher_tests_svt_checkBox,
        'FFT': ui.ycruncher_tests_fft_checkBox,
        'FFTv4': ui.ycruncher_tests_fftv4_checkBox,
        'N63': ui.ycruncher_tests_n63_checkBox,
        'VT3': ui.ycruncher_tests_vt3_checkBox,
    }


def _old_test_widgets(ui):
    return {
        'BKT': ui.ycruncher_old_tests_bkt_checkBox,
        'BBP': ui.ycruncher_old_tests_bbp_checkBox,
        'SFT': ui.ycruncher_old_tests_sft_checkBox,
        'FFT': ui.ycruncher_old_tests_fft_checkBox,
        'N32': ui.ycruncher_old_tests_n32_checkBox,
        'N64': ui.ycruncher_old_tests_n64_checkBox,
        'HNT': ui.ycruncher_old_tests_hnt_checkBox,
        'VST': ui.ycruncher_old_tests_vst_checkBox,
        'C17': ui.ycruncher_old_tests_c17_checkBox,
    }


MODERN_DEFAULT_TESTS = {'BKT', 'BBP', 'SFTv4', 'SNT', 'SVT', 'FFTv4', 'N63', 'VT3'}
OLD_DEFAULT_TESTS = {'BKT', 'BBP', 'SFT', 'FFT', 'N32', 'N64', 'HNT', 'VST'}


def _set_selected_tests(test_widgets, selected_tests):
    for test, checkbox in test_widgets.items():
        checkbox.setChecked(test in selected_tests)


def _parse_tests(value):
    return [test.strip() for test in value.split(',') if test.strip()]


def _selected_tests(test_widgets):
    return [test for test, checkbox in test_widgets.items() if checkbox.isChecked()]


def update_ycruncher_test_availability(ui):
    """Enable only the workload set belonging to the selected y-cruncher version."""
    modern_enabled = ui.general_stressTestProgram_radioButton_ycruncher.isChecked()
    old_enabled = ui.general_stressTestProgram_radioButton_ycruncher_old.isChecked()

    ui.ycruncher_tests_label.setEnabled(modern_enabled)
    ui.gridLayoutWidget_4.setEnabled(modern_enabled)
    ui.ycruncher_old_tests_label.setEnabled(old_enabled)
    ui.gridLayoutWidget_5.setEnabled(old_enabled)

def load_ycruncher_config(ui):
    """
    Load settings from the [yCruncher] section of config.ini into the GUI.

    Args:
        ui: The GUI object containing the widgets to be updated.
    """
    config = configparser.ConfigParser()
    config.read('config.ini')

    if 'yCruncher' in config:
        ycruncher = config['yCruncher']

        # 1. Load mode
        mode = ycruncher.get('mode', '04-P4P')  # Default to '04-P4P' if not specified
        ui.ycruncher_mode_spinBox.setCurrentText(
            'Auto (CPU detected)' if mode.strip().lower() == 'auto' else mode
        )

        # 2. Load tests based on stress test program selection
        stress_test_program = config['General'].get('stresstestprogram', '').lower()
        tests = _parse_tests(ycruncher.get('tests', ''))

        modern_tests_map = _modern_test_widgets(ui)
        old_tests_map = _old_test_widgets(ui)
        if 'ycruncher_old' in stress_test_program:
            # Older GUI versions carried the modern defaults across when switching,
            # leaving only the two names shared by both versions.
            legacy_selection = (
                OLD_DEFAULT_TESTS
                if set(tests) == {'BKT', 'BBP'}
                else (tests or OLD_DEFAULT_TESTS)
            )
            _set_selected_tests(old_tests_map, legacy_selection)
            _set_selected_tests(modern_tests_map, MODERN_DEFAULT_TESTS)
        else:
            _set_selected_tests(modern_tests_map, tests or MODERN_DEFAULT_TESTS)
            _set_selected_tests(old_tests_map, OLD_DEFAULT_TESTS)

        # 3. Load testDuration
        test_duration = ycruncher.get('testduration', '60')  # Default to 60 seconds
        try:
            ui.ycruncher_testDuration_spinBox.setValue(int(test_duration))
        except ValueError:
            ui.ycruncher_testDuration_spinBox.setValue(60)

        # 4. Load memory
        memory = ycruncher.get('memory', 'Default')
        ui.ycruncher_memory_lineEdit.setText(memory)
        if memory.lower() == 'default':
            ui.ycruncher_memory_default_checkBox.setChecked(True)
        else:
            ui.ycruncher_memory_default_checkBox.setChecked(False)

        # 5. Load enableYcruncherLoggingWrapper
        logging_wrapper = ycruncher.get('enableycruncherloggingwrapper', '0')
        ui.ycruncher_enableYcruncherLoggingWrapper_checkBox.setChecked(logging_wrapper == '1')
    else:
        # Set default values if [yCruncher] section is missing
        ui.ycruncher_mode_spinBox.setCurrentText('04-P4P')
        _set_selected_tests(_modern_test_widgets(ui), MODERN_DEFAULT_TESTS)
        _set_selected_tests(_old_test_widgets(ui), OLD_DEFAULT_TESTS)
        ui.ycruncher_testDuration_spinBox.setValue(60)
        ui.ycruncher_enableYcruncherLoggingWrapper_checkBox.setChecked(False)
        # Set default memory settings
        ui.ycruncher_memory_default_checkBox.setChecked(True)
        ui.ycruncher_memory_lineEdit.setText('Default')

    update_ycruncher_test_availability(ui)

def apply_ycruncher_config(ui):
    """
    Apply current GUI settings to the [yCruncher] section of config.ini.

    Args:
        ui: The GUI object containing the widgets with current values.
    """
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Ensure [yCruncher] section exists
    if 'yCruncher' not in config:
        config['yCruncher'] = {}

    ycruncher = config['yCruncher']

    # 1. Apply mode
    selected_mode = ui.ycruncher_mode_spinBox.currentText()
    ycruncher['mode'] = 'auto' if selected_mode == 'Auto (CPU detected)' else selected_mode

    # 2. Apply tests based on stress test program selection
    stress_test_program = ''
    if ui.general_stressTestProgram_radioButton_ycruncher.isChecked():
        stress_test_program = 'ycruncher'
    elif ui.general_stressTestProgram_radioButton_ycruncher_old.isChecked():
        stress_test_program = 'ycruncher_old'

    modern_tests = _selected_tests(_modern_test_widgets(ui))
    old_tests = _selected_tests(_old_test_widgets(ui))

    if stress_test_program == 'ycruncher_old':
        tests = old_tests
    else:
        tests = modern_tests
    ycruncher['tests'] = ', '.join(tests)

    # 3. Apply testDuration
    ycruncher['testduration'] = str(ui.ycruncher_testDuration_spinBox.value())

    # 4. Apply memory
    if ui.ycruncher_memory_default_checkBox.isChecked():
        ycruncher['memory'] = 'Default'
    else:
        ycruncher['memory'] = ui.ycruncher_memory_lineEdit.text()

    # 5. Apply enableYcruncherLoggingWrapper
    ycruncher['enableycruncherloggingwrapper'] = '1' if ui.ycruncher_enableYcruncherLoggingWrapper_checkBox.isChecked() else '0'

    # Write the updated config to file
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
