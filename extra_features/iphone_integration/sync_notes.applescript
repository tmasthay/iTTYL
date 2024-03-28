tell application "Notes"
    -- Get a reference to the specific 'Texts' subfolder in iCloud
    set textsFolder to folder "Texts" of account "iCloud"
    -- Search for notes within the 'Texts' folder only
    -- set searchResults to notes of textsFolder whose name contains "Text"
    set searchResults to notes of textsFolder
    
    -- Get a reference to the 'Sent' subfolder in iCloud where notes will be moved
    set sentFolder to folder "Sent" of account "iCloud"
    
    repeat with aNote in searchResults
        set noteText to the body of aNote
        log "*** SCHEDULED TEXT ***"
        set lastModified to the modification date of aNote
        log lastModified
        log noteText
        
        -- Move the note to the 'Sent' folder instead of deleting it
        move aNote to sentFolder
    end repeat
end tell


