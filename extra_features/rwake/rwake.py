from dotenv import dotenv_values
import os
import subprocess
from datetime import datetime, timedelta

DOTENV_SETTINGS_PATH = "./SETTINGS.txt"
env_vars = dotenv_values(DOTENV_SETTINGS_PATH)


def main():
    rwake = float(env_vars["RWAKE_FREQUENCY"])
    base_cmd = "sudo pmset schedule wake"

    # Initialize command string
    cmd = "#!/bin/bash\n"
    hours_per_day = 24
    # num_schedules = int(hours_per_day / rwake)
    num_schedules = 900
    now = datetime.now()
    for i in range(1, num_schedules + 1):
        future_time = now + timedelta(hours=i * rwake)
        string_time = future_time.strftime("%m/%d/%Y %H:%M:%S")
        # string_time = future_time.strftime("%H:%M:%S")
        cmd += f"{base_cmd} '{string_time}'\n"

    script_path = "extra_features/rwake/wake_schedules.sh"
    with open(script_path, "w") as f:
        f.write(cmd)

    # Make the script executable and run it
    os.chmod(script_path, 0o755)
    subprocess.run(script_path, shell=True)

    # Check the schedule
    subprocess.run("pmset -g sched", shell=True)


if __name__ == "__main__":
    main()
