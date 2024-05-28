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
    # hours_per_day = 24
    # num_schedules = int(hours_per_day / rwake)
    num_schedules = 900

    # find near "top of the hour with respect to now"
    now = datetime.now()
    now = now.replace(minute=0, second=0, microsecond=0)
    
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

    warn = lambda s: f"\033[31m{s}\033[0m"
    code = lambda s: f"\033[32m{s}\033[0m"

    num_scheduled_events = int(
        subprocess.check_output(
            'pmset -g sched | grep "\[[0-9][0-9]*\]" | wc -l', shell=True
        )
        .decode('utf-8')
        .strip()
    )
    max_scheduled_events_allowed_by_macos = 1000
    if (
        num_scheduled_events + num_schedules
        > max_scheduled_events_allowed_by_macos
    ):
        print(
            f'MAX SCHEDULED EVENTS ALLOWED BY MACOS: {max_scheduled_events_allowed_by_macos}'
        )
        print(
            f'NUM SCHEDULED EVENTS_IF_THIS_SCRIPT_RUNS: {num_scheduled_events + num_schedules}'
        )
        print(
            f'Therefore, we exit now. Run {code("pmset -g sched")} to see your schedule and decide which jobs you would like to cancel.'
        )
        return

    print(
        'Running wake commands...should not take more than a minute or two.\n'
        f'If you see {code("pmset: Error in scheduling command")}, then you are likely maxed out on scheduled jobs (probably from running this script previously)\n'
        f'    To help diagnose, run {code("pmset -g sched")} to see your schedule and decide which jobs you would like to cancel.\n'
        'If you wish to undo these commands, run "sudo pmset schedule cancelall"\n\n'
        '\033[31m**** WARNING ****\n'
        '    Be aware that this will cancel ALL scheduled events, not just the ones created by this script.\n'
        '    An easy fix for this is to just cancel them all and reboot your mac.\n'
        '    Mac OS X has a few built-in scheduled wakes for things like Do Not Disturb and Time Machine.\n'
        '    If you cancel all scheduled events, you will have to re-enable these manually.\n'
        '    However, an easy fix for this is to just cancel them all and reboot your mac.\n'
        '    But I am NOT a Mac expert, so please do your own research before blindly running that **SUGGESTED** command.\033[0m\n',
        flush=True,
    )
    subprocess.run(script_path, shell=True)

    # Check the schedule
    subprocess.run("pmset -g sched", shell=True)


if __name__ == "__main__":
    main()
