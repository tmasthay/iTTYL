on run {filePath}
    -- Set the path to the image file
    -- set filePath to "/Users/tylermasthay/Pictures/text_scheduler/1.heic"
    
    -- Open Finder
    tell application "Finder"
        activate
        
        -- Open a new Finder window (if none is open)
        if (count of windows) is 0 then
            make new Finder window
        end if
        
        -- Use the Go to Folder command
        tell application "System Events"
            -- Bring up the Go to Folder dialog
            keystroke "g" using {shift down, command down}
            delay 1  -- Wait for the dialog to appear
            
            -- Enter the file path
            keystroke filePath
            delay 1  -- Allow time for text entry
            
            -- Press Enter to open the folder
            keystroke return
            delay 2  -- Wait for navigation

            -- hit command + c
            keystroke "c" using command down
            delay 2
        end tell
    end tell
end run
