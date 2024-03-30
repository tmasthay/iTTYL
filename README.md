# schedule-texts-from-notes
Schedule iMessage or SMS texts from your notes app from your Mac and iPhone. 

# Messages get sent from your Mac
If your Mac is completely off, this will not work. See directions below. "Power nap" is a useful way to accomplish this, or see `rwake` add on in the instructions below.

# Setup devices and iCloud
1. Make sure iCloud syncing is ON for the Notes app for both your Mac and iPhone.
2. Make two folders in your Notes app titled "Texts" and "Sent", and make sure they are recognized as synced folders for iCloud.

# Setup on terminal in Mac
1. Clone this repo to your computer 
2. `cd private_scheduler`
3. `cp SETTINGS_TEMPLATE.txt SETTINGS.txt`  and set your preferences (details below).
4. Open your terminal to this project directory and run these commands in order
   1. `virtualenv venv`
   2. `source activate.sh` 
   3. `pip install -r requirements.txt`
   4. `python send_scheduled_messages.py`
5. `source .schedulerc` (creates syntactic sugar commands in terminal)
6. `addon wake_scheduler` (creates a `launchd` process to periodically scan for new scheduled texts)
7. Optionally, you can run `addon rwake` if you want to schedule automatic wakes of your Mac (nice fallback when not on power).
8. `addon contacts`
   1. Copy and paste the parts of text for contacts that you want into your SETTINGS.txt file. This will give you an alias for phone numbers. Note that underscores are NECESSARY; this is an artifact of the design of the ``schedule-texts-from-txt`` repo.
9. ``addon group_chats``
   1. Sample output will look like
   ```
   iMessage;+;chatXXXXXXXX
       contact_name1
       contact_name2
       XXX-XXX-XXXX (a phone number in a group chat that is not in your contacts)
   ```
   2. Take the "iMessage;+;chatXXXXX" part and copy ONLY the "chatXXXX" part
   3. Go into SETTINGS.txt and give it an alias such as `my_group_chat=chatXXXX`.
   4. NOTE: the indented contacts and phone numbers there are simply to make it easier to identify which group chat is which. `chatXXXX` is the only identifier to be used in the script.

# Send a message
1. Go into Notes app on your Mac.
2. Make a note in the "Texts" directory you made earlier.
3. At the top of the note put `myself now` or `myself +1m` (schedule for 1 minute in the future).
4. On the next line, type `Hello World`.
5. (Optional) Paste an image after that.
6. There *should* be a daemon running on your Mac that will periodically check the Notes app and it *should* send just fine. There is latency here, so see the following section for more details on `SETTINGS.txt` to customize your setup.

# SETTINGS.txt
Make sure to read the `SYNC_MODE` row carefully. Its instructions sum up the important nuances of how to use this program pretty well.

| Variable | Description | Options / Examples |
|---|---|---|
| `MAX_OVERTIME_MINS` | The maximum minutes allowed for overtime; helps control how much extra time can be accumulated beyond regular scheduling limits. | `10000` minutes |
| `DEBUG_TEXTING` | Enables or disables debug mode for texting operations; helpful for troubleshooting without sending actual texts. | `False` (disabled), `True` (enabled) |
| `SCHEDULED_TEXTS_DIRECTORY` | The directory where scheduled texts are stored. This path is relative to the script's location. | `./texts` |
| `YOUR_NAME` | The name of the user or the identifier used in the scripts. | `tyler` |
| `WAKE_FREQUENCY` | The frequency in minutes at which the scheduler wakes to check if any texts need to be sent. | `15` minutes |
| `RWAKE_FREQUENCY` | The recovery wake frequency in minutes, used perhaps for a more rapid check in special circumstances. | `1` minute |
| `OUTPUT_PATH` | The path where output logs from the script are stored. | `/tmp/text_scheduler.out` |
| `ABSOLUTE_PYTHON_PATH` | The absolute path to the Python executable used by the script. | `/Users/tylermasthay/anaconda3/bin/python` |
| `SYNC_MODE` | Controls how the texting script synchronizes and schedules texts based on their readiness and specified conditions. <br><br> - **`"always"`**: Texts are scheduled every time the script is called, regardless of their designated times. <br> - **`"never"`**: Disables all scheduling; typically used temporarily. <br> - **`"only_if_ready"`** or **`"conditional"`**: Texts are scheduled only if they are ready to be sent immediately. These are aliases and operate the same way. For example, say you schedule "my_contact_name +1d3h11m" for "send text to contact_name after 1 day, 3 hours, and 11 minutes after the last edit of this note" and after 1 day, 3 hours, and 10 minutes you realize you want to edit something...the file will still be there, unscheduled, for you to edit the text. The last modification time is now updated, so you would need to change it to "my_contact_name +1m" if you want it to be sent at the same time as your original intention, else it will take a TOTAL of 2 days, 3 hours, and 22 minutes to send (+ notation is ALWAYS with respect to LAST MODIFICATION TIME) | `"always"`, `"never"`, `"only_if_ready"`, `"conditional"` |
| `WAKE_BUFFER_TIME` | The buffer time in minutes added around wake events to prevent scheduling conflicts or overlaps. | `30` minutes |
| `MAX_IDLE_EDIT_TIME` | The maximum time allowed for editing a scheduled text before it is sent, formatted as a string with time units. | `30s` |

# Example
Assume the example config below.

| Variable | Description 
|---|---
| `MAX_OVERTIME_MINS` | `10000` minutes |
| `DEBUG_TEXTING` | `False`
| `SCHEDULED_TEXTS_DIRECTORY` | `./texts`
| `YOUR_NAME` | `tyler`
| `WAKE_FREQUENCY` | `15`
| `RWAKE_FREQUENCY` | `2`
| `OUTPUT_PATH` | `/tmp/text_scheduler.out` 
| `ABSOLUTE_PYTHON_PATH` | `/Users/tylermasthay/anaconda3/bin/python` 
| `SYNC_MODE` | always
| `WAKE_BUFFER_TIME` | `30`
| `MAX_IDLE_EDIT_TIME` | `30s` 

Assume you create a note in your `Texts` directory at `December 25, 2024 08:00:00 AM`. 
```
willem_dafoe January 1, 2025 12:00:00 AM
Happy New Year, William!
```
You don't touch that note for `MAX_IDLE_EDIT_TIME=30s`, so at `08:00:30 AM`, that note is now fair game to be scheduled. Your script runs every `WAKE_FREQUENCY=15` minutes, so you are guaranteed for this text to be scheduled some time between `08:00:00 AM` and `08:15:00 AM` (assuming your mac is, indeed, on that whole time). At that point, the note will be moved to the `Sent` directory and a local version will be stored in a `txt` file on the Mac, meaning nothing done on the Notes app will prevent this from being sent at New Years, and Willem will think you forgot his name! To cancel it, simply go into your mac and delete the corresponding `txt` file named `./texts/Text willem_dafoe January 1, 2025 12:00:00 AM` before the ball drops! 

Now suppose we change to `SYNC_MODE=only_if_ready`. This mode checks the current time and the scheduled time and *rejects* scheduling the text until *after* the scheduled time has already occurred. Therefore, you will see that note remain in the notes app until the ball drops, and you've now got multiple days to correct the error instead of just 30 seconds! 

# Example with relative time
Let's consider the same scenario again but with slightly different text
```
willem_dafoe +6d16h
Happy New Year, William!
```
Since it is 8AM on Christmas morning, this will also be scheduled for New Years since that is exactly `+6d16h`, i.e., 6 days and 16 hours, in the *future*. `SYNC_MODE=always` will, again, only give you `MAX_IDLE_EDIT_TIME=30s` to correct the mistake, but now `SYNC_MODE=only_if_ready` will act slightly differently. Say you notice the typo at `December 31, 2024 11:00:00 PM` and change the contents to
```
willem_dafoe +6d16h
Happy New Year, Willem!
```
In this scenario, the text will actually not send until *January 6* because the `+` notation is always with respect to the *last modification time*! So if you still wanted to use this notation and have it send at midnight of New Year's, you would need to modify the content to 
```
willem_dafoe +1h
Happy New Year, Willem!
```

# How it works
The code conforms to the `schedule-texts-from-txt` repo by `reidjs` with some added features located in the `extra_features` directory.
I plan to pull request directly into his repo one day, but I need to graduate college and there's a bunch of merge conflicts I don't want to sort through lol.

# Help & Feedback
Please create a GitHub issue if you have feedback or need help. Thanks! 

Made by Reid JS on March 9, 2024
