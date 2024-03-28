SCRIPT_PATH=extra_features/iphone_integration/sync_notes.applescript
osascript $SCRIPT_PATH 2>&1 | sed -e 's/<[^>]*>//g'

