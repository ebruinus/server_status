import subprocess

def ping(host):
    """Ping een server en retourneer True als het succesvol is."""
    try:
        # Dit werkt voor Windows, waar de ping-command anders is dan op Linux/Mac
        result = subprocess.run(["ping", "-n", "1", host], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.returncode == 0  # Als de returncode 0 is, is de server bereikbaar
    except Exception as e:
        print(f"Error tijdens pingen van {host}: {e}")
        return False