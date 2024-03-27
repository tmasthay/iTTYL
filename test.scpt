tell application "Notes"
    set searchResults to notes whose name contains "Text"
    repeat with aNote in searchResults
        set noteText to the body of aNote
        log "*** SCHEDULED TEXT ***"
        log noteText
        -- Perform your processing here, and then mark the note as scheduled
        set name of aNote to my replaceText(name of aNote, "Text", "Scheduled")
    end repeat
end tell

-- Function to perform search and replace in a string
on replaceText(theText, oldText, newText)
    set AppleScript's text item delimiters to oldText
    set theTextItems to text items of theText
    set AppleScript's text item delimiters to newText
    set theText to theTextItems as text
    set AppleScript's text item delimiters to ""
    return theText
end replaceText


