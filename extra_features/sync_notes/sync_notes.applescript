tell application "Notes"
    -- Get a reference to the specific 'Texts' subfolder in iCloud
    set textsFolder to folder "Texts" of account "iCloud"

    -- Search for notes within the 'Texts' folder only
    set searchResults to notes of textsFolder
    
    -- Get a reference to the 'Sent' subfolder in iCloud where notes will be moved
    set sentFolder to folder "Sent" of account "iCloud"

    log textsFolder
        
    -- Iterate over each note in the searchResults
    repeat with aNote in searchResults
        -- log aNote
        -- set noteText to the body of aNote
        set noteText to the body of aNote
        set lastModified to the modification date of aNote
        set lastModifiedStr to lastModified as string
        set noteTextEscaped to quoted form of noteText
        log "*** SCHEDULED TEXT ***"
        log lastModifiedStr
        log noteText
        log aNote
        
        -- -- Construct and execute the Python command
        -- set pythonCommand to pythonPath & " " & pythonScriptPath & " " & quoted form of lastModifiedStr & " " & noteTextEscaped
        -- try
        --     set exitCode to do shell script pythonCommand
        -- on error errMsg
        --     -- log errMsg
        --     set exitCode to "1"
        -- end try
        
        -- -- Process based on exit code from Python script
        -- if exitCode is "0" then
        --     log "*** SCHEDULED TEXT ***"
        --     log lastModifiedStr
        --     log noteText
            
        --     -- Move the note to the 'Sent' folder
        --     move aNote to sentFolder
        -- else 
        --     log "Not moving note due to Python script logic:"
        --     log "Last Modified: " & lastModifiedStr
        -- end if
    end repeat
end tell
