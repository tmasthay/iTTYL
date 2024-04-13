on run argv
    -- Assign command line arguments to variables
    set phoneNumber to item 1 of argv
    set filePath to item 2 of argv

    tell application "Finder"
        activate
        
        delay 1

        -- Open a new Finder window (if none is open)
        if (count of windows) is 0 then
            make new Finder window
        end if

        delay 1
        
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

    -- Use System Events to interact with the Messages app
    tell application "Messages"
        activate 

        delay 1 -- Allow the app to respond

        tell application "System Events"
            keystroke "n" using {command down}
            delay 1

            keystroke tab
            delay 1

            keystroke "v" using {command down}
            delay 1
        
            -- return back to the "To: " part (a nice trick!)
            keystroke "n" using {command down}
            delay 1

            -- paste the phone number
            keystroke phoneNumber
            delay 1

            keystroke return
            delay 1

            -- go back to the message part
            keystroke tab
            delay 1

            -- send 
            keystroke return
            delay 1
        end tell
    end tell    
end run