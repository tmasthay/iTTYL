on run argv
    -- Extract the chat ID and message from the arguments
    set chatID to item 1 of argv
    set message to item 2 of argv
    
    -- Your sendMessageToChat function adapted for command line
    tell application "Messages"
        -- Variable to hold the reference to the target chat
        set foundChat to missing value
        
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
end run
