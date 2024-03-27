tell application "Notes"
    set searchResults to notes whose name contains "Text"
    repeat with aNote in searchResults
        set noteText to the body of aNote
        log "*** SCHEDULED TEXT ***"
        set lastModified to modification date of aNote
        log lastModified
        log noteText

        delete aNote
    end repeat
end tell

