on run
    tell application "System Events"
        tell application "Messages" to activate
        delay 1  -- Wait for Messages to activate

        tell application process "Messages"
            set frontmost to true
            delay 1  -- Give the application time to respond

            -- Open the 'New Message' window
            click menu item "New Message" of menu 1 of menu bar item "File" of menu bar 1
            delay 1  -- Allow time for the 'New Message' window to appear

            -- Attempt to target the "To:" field and set it to "me"
            -- Based on your hierarchy understanding
            try
                set toField to text field 1 of group 1 of group 1 of window 1
                set value of toField to "me"
                delay 1
                key code 36 -- Press Enter to resolve the contact
            on error errMsg
                log "Error when setting the 'To:' field: " & errMsg
            end try
        end tell
    end tell
end run
