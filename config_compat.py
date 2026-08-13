import configparser
import os
import shutil
import tempfile


def _read_config(path):
    config = configparser.ConfigParser(interpolation=None, strict=False)
    config.read(path, encoding="utf-8-sig")
    return config


def ensure_current_config(config_path, default_config_path):
    """Create config.ini and add defaults introduced by newer CoreCycler releases.

    Existing user values are authoritative. Only missing sections and options are
    copied from the bundled default configuration.
    """
    if not os.path.isfile(default_config_path):
        raise FileNotFoundError(
            f"Default CoreCycler configuration not found: {default_config_path}"
        )

    if not os.path.exists(config_path):
        shutil.copyfile(default_config_path, config_path)
        return True

    defaults = _read_config(default_config_path)
    current = _read_config(config_path)
    changed = False

    for section in defaults.sections():
        if not current.has_section(section):
            current.add_section(section)
            changed = True
        for option, value in defaults.items(section):
            if not current.has_option(section, option):
                current.set(section, option, value)
                changed = True

    if changed:
        directory = os.path.dirname(os.path.abspath(config_path))
        descriptor, temporary_path = tempfile.mkstemp(
            prefix="config-", suffix=".ini.tmp", dir=directory, text=True
        )
        try:
            with os.fdopen(descriptor, "w", encoding="utf-8", newline="") as handle:
                current.write(handle)
            os.replace(temporary_path, config_path)
        except Exception:
            if os.path.exists(temporary_path):
                os.unlink(temporary_path)
            raise

    return changed
