SCRIPT_PATH=extra_features/sync_notes/sync_notes.applescript
osascript $SCRIPT_PATH 2>&1 | sed -e 's/<[^>]*>//g'

