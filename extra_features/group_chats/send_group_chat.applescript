on run argv
    -- Extract the chat ID and message from the arguments
    set chatID to item 1 of argv
    set message to item 2 of argv
    set imagePaths to item 3 of argv
    
    set foundChat to missing value

    -- Your sendMessageToChat function adapted for command line
    tell application "Messages"        
        -- Iterate through each chat to find the one with the matching ID
        repeat with aChat in every chat
            if id of aChat is chatID then
                set foundChat to aChat
                exit repeat
            end if
        end repeat
        
        -- If the chat is found, send the message
        if foundChat is not missing value then
            send message to foundChat
        else
            display notification "Chat not found" with title "Error"
        end if
    end tell
    if imagePaths is not "" then
        set imageFiles to my split(imagePaths, ",")
        repeat with imagePath in imageFiles
            set attach to POSIX file imagePath
            tell application "Messages" to send attach to foundChat
        end repeat
    end if
    -- if imagePaths is not "" then
    --     set imageFiles to my split(imagePaths, ",")
    --     -- set foundChat to missing value
    --     if foundChat is not missing value then
    --         repeat with imagePath in imageFiles
    --             set attach to POSIX file imagePath
    --             ignoring application responses
    --             tell application "Messages" 
    --                 send attach to foundChat 
    --             end tell
    --         end repeat
    --     end if
    -- end if
end run

-- Helper function to split a string by a delimiter
on split(input, delimiter)
    set AppleScript's text item delimiters to delimiter
    set inputList to every text item of input
    set AppleScript's text item delimiters to {""} -- Resets back to default
    return inputList
end split
