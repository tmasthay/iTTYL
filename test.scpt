tell application "Notes"
    set searchResults to notes whose name contains "Text"
    repeat with aNote in searchResults
        set noteText to the body of aNote
        log "*** SCHEDULED TEXT ***"
        log noteText 
    end repeat
end tell

