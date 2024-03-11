SCRIPT_PATH=extra_features/sync_notes/sync_notes.applescript
# osascript $SCRIPT_PATH 2>&1 | sed -e 's/<[^>]*>//g'
osascript $SCRIPT_PATH > /tmp/sync_notes.log 2>&1
cat /tmp/sync_notes.log

