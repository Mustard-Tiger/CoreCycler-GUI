import os

def launch_readme():
    """Open the CoreCycler GUI documentation from the base directory."""
    try:
        os.startfile('README.md')
    except Exception as e:
        print(f"Error opening README.md: {e}")

def launch_license():
    """Open LICENSE from the base directory."""
    try:
        os.startfile('LICENSE')
    except Exception as e:
        print(f"Error opening LICENSE: {e}")

def setup_menu_connections(ui):
    """Connect menu actions to their respective functions."""
    ui.actionReadME_2.triggered.connect(launch_readme)
    ui.actionLicense_2.triggered.connect(launch_license)
