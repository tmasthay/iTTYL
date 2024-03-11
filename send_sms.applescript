on run argv
    -- Assign command line arguments to variables
    set phoneNumber to item 1 of argv
    set msgContent to item 2 of argv
    set filePath to item 3 of argv

    -- log phoneNumber
    -- set phoneNumber to quoted form of phoneNumber
    -- set msgContent to quoted form of msgContent

    set phoneNumber to my split(phoneNumber, "&amp")
    
    if (count of phoneNumber) is 0 then
        display dialog "No phone number provided. Please provide a phone number to send the message to." buttons {"OK"} default button "OK" giving up after 15
        return
    end if

    if (count of phoneNumber) is 1 and (filePath is "") then
        tell application "Messages"
            set targetService to 1st service whose service type = SMS
            set targetBuddy to buddy (item 1 of phoneNumber) of targetService
            send msgContent to targetBuddy
            return 
        end tell
    end if
    
    try
        display dialog "Continue with scheduled message?" buttons {"Continue", "Cancel"} default button "Continue" cancel button "Cancel" giving up after 15
        on error number -128 -- User pressed 'Cancel'
            -- Uncomment the following line to enable voice feedback
            -- say "Operation cancelled"
            return
    end try
    -- Uncomment "say" clauses to enable voice feedback
    -- say "Sending message to " & phoneNumber & " with content: " & msgContent & " and file path: " & filePath
    -- say "Sending message now. Avoid pressing any keys until the message is sent."
    -- Use System Events to interact with the Messages app
    tell application "Messages"
        -- if no files and only one phone number, then simply send the message
        --     without need to dummy user interaction with GUI

        activate 

        delay 1 -- Allow the app to respond

        tell application "System Events"
            keystroke "n" using {command down}
            delay 1

            repeat with i from 1 to count of phoneNumber
                set thisPhoneNumber to item i of phoneNumber
                keystroke thisPhoneNumber
                delay 1
                keystroke return
                delay 1
            end repeat

            keystroke tab
            delay 1


            -- if (filePath is not "")
            --     keystroke "v" using {command down}
            --     delay 1
            -- end if
        
            -- copy msgContent to clipboard
            set the clipboard to msgContent
            delay 1

            -- paste the message
            keystroke "v" using {command down}
            delay 1


            if (filePath is not "") then
                keystroke return using {shift down}
                delay 1
                set files_to_send to my split(filePath, ",")
                repeat with i from 1 to count of files_to_send
                    set thisFile to item i of files_to_send
                    set filePath to thisFile
                    -- log filePath
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
                            tell application "Messages" to activate
                            delay 1
                            keystroke "v" using {command down}
                            delay 1
                            keystroke return using {shift down}
                            -- tell application "Messages"
                            --     activate
                            --     delay 1
                            --     keystroke "v" using {command down}
                            --     delay 1
                            --     keystroke return using {shift down}
                            --     delay 1
                            -- end tell
                        end tell
                    end tell
                end repeat
            end if
            keystroke return
        end tell
    end tell    
end run

on split(theString, theDelimiter)
    set oldDelimiters to AppleScript's text item delimiters
    set AppleScript's text item delimiters to theDelimiter
    set theArray to every text item of theString
    set AppleScript's text item delimiters to oldDelimiters
    return theArray
end split