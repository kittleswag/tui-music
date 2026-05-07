import subprocess


def _run(cmd):
    try:
        return subprocess.check_output(cmd, shell=True, text=True).strip()
    except subprocess.CalledProcessError:
        return None


def is_running():
    status = _run("playerctl status")
    return status is not None


def get_metadata():
    meta = _run("playerctl metadata --format '{{artist}} - {{title}}'")
    return meta


def get_position():
    pos = _run("playerctl position")
    try:
        return float(pos)
    except:
        return 0.0


def get_status():
    return _run("playerctl status")