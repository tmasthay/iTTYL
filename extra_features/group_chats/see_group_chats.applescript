tell application "Messages"
    -- Initialize a string to hold participant information for group chats
    set participantInfo to ""
    
    -- Iterate through each chat in Messages
    repeat with aChat in every chat
        -- Check if the chat has more than one participant
        if (count of participants of aChat) > 1 then
            -- Append the chat's ID to the participant information string
            set participantInfo to participantInfo & id of aChat & "\n    "
            -- Iterate through each participant in the chat
            repeat with aParticipant in participants of aChat
                -- Append each participant's ID (phone number or Apple ID) to the string
                set participantInfo to participantInfo & id of aParticipant & "\n    "
            end repeat
            -- Add a newline for better readability between group chats
            set participantInfo to participantInfo & "\n\n"
        end if
    end repeat
    
    -- Return the compiled participant information for all group chats
    participantInfo
end tell
