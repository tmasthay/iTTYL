on run argv
    -- Assign command line arguments to variables
    set phoneNumber to item 1 of argv
    set msgContent to item 2 of argv
    set filePath to item 3 of argv

    -- log phoneNumber
    -- set phoneNumber to quoted form of phoneNumber
    -- set msgContent to quoted form of msgContent


    -- check if filePath is empty, in which case we don't need Finder
    if (filePath is not "") then
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
    end if

    -- Use System Events to interact with the Messages app
    tell application "Messages"
        activate 

        delay 1 -- Allow the app to respond

        tell application "System Events"
            keystroke "n" using {command down}
            delay 1

            keystroke tab
            delay 1


            if (filePath is not "")
                keystroke "v" using {command down}
                delay 1
            end if
        
            -- copy msgContent to clipboard
            set the clipboard to msgContent
            delay 1

            -- paste the message
            keystroke "v" using {command down}
            delay 1

            -- return back to the "To: " part (a nice trick!)
            keystroke "n" using {command down}
            delay 1

            -- split phone numbers into array by comma
            set phoneNumber to my split(phoneNumber, "&amp")
            repeat with i from 1 to count of phoneNumber
                set thisPhoneNumber to item i of phoneNumber
                keystroke thisPhoneNumber
                delay 1
                keystroke return
                delay 1
            end repeat

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

on split(theString, theDelimiter)
    set oldDelimiters to AppleScript's text item delimiters
    set AppleScript's text item delimiters to theDelimiter
    set theArray to every text item of theString
    set AppleScript's text item delimiters to oldDelimiters
    return theArray
end split