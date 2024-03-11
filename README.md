# iTTYL

_Continuously_ schedule iMessage or SMS texts _with file attachments_ from your Mac and iPhone.

As long as you have a Mac, this software allows for _continuous_ message scheduling from your _iPhone_, _Mac_, and _any device that can access the internet_ (e.g., a Linux machine).

This repo is largely inspired by [great work by reidjs](https://github.com/reidjs/schedule-texts-from-txt), which originally made me realize that this project was possible and whose code serves as the skeleton of this project.

# Hello World

Assuming you have all the setup below this section complete, here is how you use this software.

1. Go into Notes app on your Mac _or_ your iPhone.
2. Make a note in the "Texts" directory you made earlier.
3. At the top of the note put `me now` or `me +1m` (schedule for 1 minute in the future).
4. On the next line, type `Hello World`.
5. (Optional) Paste an image after that.
6. There _should_ be a daemon running on your Mac that will periodically check the Notes app and it _should_ send just fine. There is latency here, as defined by `SETTINGS.txt` in your custom setup.

## Examples

Below are some examples of what a typical note will look like.

### Relative time (what I personally find most useful)

Schedule text for 1 day, 2 hours, and 10 minutes in advance.

```
kevin_durant +1d2h10m
Hi KD, sorry we defeated you by 30 points.
Not cool on our part rubbing it like this.
I'd just like to let you know that the Suns are so bad that I was confident
   enough to schedule this message 1 day, 2 hours, and 10 minutes ago,
   which is around the time I thought the third quarter would start (right now)

:) Lebron
```

### Absolute time

Schedule text for January 1, 2025 midnight.

```
anderson_cooper January 1, 2025 12:00:00 AM
Happy New Year, Anderson!
Sincere apologies that we make you do this show every year.
```

### Now and images

Equivalently, just replace `now` with `+0m`.

```
mom now
My phone is dead, but I plan to be home in 2 hours.
I had to message you with my nifty iTTYL software from my office's Windows
   machine by signing into iCloud on Firefox (got the two-factor finished just before it died!)
   and making a note in the Notes app.
Then iCloud syncing allowed this message to be sent to you through a daemon on my Mac.
I've kept "Keep Me Signed In" for iCloud on my office Windows machine in case
   this ever happens again!
Ned has this setup on his Linux machine too after I told him about this haha.

Neat right?!
I almost forgot, here's a photo of the event today, which I was still able to
   include through my iCloud account!

https://share.icloud.com/photos/....
```

### Note on Image Sending

There are three ways to send images ranked from "most general, most annoying" to "least general, least annoying" ways.

1. iCloud share link
   1. Any device
   2. Mac daemon will go to the link, download the file locally, and send it.
   3. If the download fails for any reason, the link will itself will be sent.
      1. The most common reason for failure is rate limiting by iCloud's website, but this is unlikely unless you message a lot or are extending this software.
2. "Share" from photos
   1. iPhone (on Mac too, but use [3] on mac since it's easier)
   2. Go into Notes app, press camera icon, and share.
      1. This is necessary due to Apple security restrictions. If you directly

# Setup things "Apple-side"

## Setup iCloud and Notes app

1. Make sure iCloud syncing is ON for the Notes app for both your Mac and iPhone.
2. Make two folders in your Notes app titled "Texts" and "Sent", and make sure they are recognized as synced folders for iCloud.

## Setup Power Nap on your Mac

1. On your Mac, `CMD+Spacebar` and search `Power Nap`
2. Click the dropdown for `Wake for network access` and select either `Always` or `Only on Power Adapter`. If you select `Never`, then texts will only be sent when your Mac is _fully_ on. It is simply a tradeoff of Mac power consumption versus continuity of text scheduling on which setting you choose.

## Setup Accessibility on your Mac

1. Open `System Settings` by pressing `CMD+Spacebar`, searching `System Settings`, and pressing `Enter`.
2. Search `Full disk` in `System Settings` and click `Allow applications to access all user files`.
3. Press the `+` sign on the right and give full-disk access to the following apps.
   1. Messages
   2. Notes
   3. Terminal

# Setup things "iTTYL-side"

## Setup on terminal in Mac

1. Clone this repo to your computer
2. `cd private_scheduler`
3. `cp SETTINGS_TEMPLATE.txt SETTINGS.txt` and set your preferences (details below).
4. Open your terminal to this project directory and run these commands in order
   1. `virtualenv venv` or `conda create -n ittyl python=3.10`
   2. `source activate.sh` or `conda activate ittyl`
   3. `pip install -r requirements.txt`
5. `source .schedulerc` (creates syntactic sugar commands in terminal)
6. `addon wake_scheduler` (creates a `launchd` process to periodically scan for new scheduled texts)
7. Optionally, you can run `addon rwake` if you want to schedule automatic wakes of your Mac (nice fallback when not on power).
8. `addon contacts`
   1. Copy and paste the parts of text for contacts that you want into your SETTINGS.txt file. This will give you an alias for phone numbers. Note that underscores are currently _necessary_ but which I hope to refactor out in the near future to make a more user-friendly UI.
9. `addon group_chats`
   1. Sample output will look like
   ```
   iMessage;+;chatXXXXXXXX
       contact_name1
       contact_name2
       XXX-XXX-XXXX (a phone number in a group chat that is not in your contacts)
   ```
   2. Copy _only_ the "iMessage;+;chatXXXX" or "SMS;+;chatXXX" parts (indented, individual contacts are just there to help _you_ distinguish which group chat is which).
   3. Go into SETTINGS.txt and give it an alias such as `my_group_chat=iMessage;+;chatXXXX` or `my_group_chat=SMS;+;chatXXX`.
10. cp `SMS_CONTACTS_TEMPLATE.txt SMS_CONTACTS.txt`. Put the identifiers for non-iPhone users from your `SETTINGS.txt`. There are a few examples in the template for cases to consider so that things do not break.

# SETTINGS.txt

Make sure to read the `SYNC_MODE` row carefully. Its instructions sum up the important nuances of how to use this program pretty well.

| Variable                    | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | Options / Examples                                        |
| --------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------- |
| `MAX_OVERTIME_MINS`         | The maximum minutes allowed for overtime; helps control how much extra time can be accumulated beyond regular scheduling limits.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | `10000` minutes                                           |
| `DEBUG_TEXTING`             | Enables or disables debug mode for texting operations; helpful for troubleshooting without sending actual texts.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | `False` (disabled), `True` (enabled)                      |
| `SCHEDULED_TEXTS_DIRECTORY` | The directory where scheduled texts are stored. This path is relative to the script's location.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             | `./texts`                                                 |
| `YOUR_NAME`                 | The name of the user or the identifier used in the scripts.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | `your_name`                                               |
| `WAKE_FREQUENCY`            | The frequency in minutes at which the scheduler wakes to check if any texts need to be sent.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | `15` minutes                                              |
| `RWAKE_FREQUENCY`           | The recovery wake frequency in minutes, used perhaps for a more rapid check in special circumstances.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | `1` minute                                                |
| `OUTPUT_PATH`               | The path where output logs from the script are stored.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | `/tmp/text_scheduler.out`                                 |
| `ABSOLUTE_PYTHON_PATH`      | The absolute path to the Python executable used by the script.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | `~/anaconda3/bin/python`                                  |
| `SYNC_MODE`                 | Controls how the texting script synchronizes and schedules texts based on their readiness and specified conditions. <br><br> - **`"always"`**: Texts are scheduled every time the script is called, regardless of their designated times. <br> - **`"never"`**: Disables all scheduling; typically used temporarily. <br> - **`"only_if_ready"`** or **`"conditional"`**: Texts are scheduled only if they are ready to be sent immediately. These are aliases and operate the same way. For example, say you schedule "my_contact_name +1d3h11m" for "send text to contact_name after 1 day, 3 hours, and 11 minutes after the last edit of this note" and after 1 day, 3 hours, and 10 minutes you realize you want to edit something...the file will still be there, unscheduled, for you to edit the text. The last modification time is now updated, so you would need to change it to "my_contact_name +1m" if you want it to be sent at the same time as your original intention, else it will take a TOTAL of 2 days, 3 hours, and 22 minutes to send (+ notation is ALWAYS with respect to LAST MODIFICATION TIME) | `"always"`, `"never"`, `"only_if_ready"`, `"conditional"` |
| `WAKE_BUFFER_TIME`          | The buffer time in minutes added around wake events to prevent scheduling conflicts or overlaps.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | `30` minutes                                              |
| `MAX_IDLE_EDIT_TIME`        | The maximum time allowed for editing a scheduled text before it is sent, formatted as a string with time units.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             | `30s`                                                     |

TODO: Describe the above better or make a youtube video (probably easier this way).
