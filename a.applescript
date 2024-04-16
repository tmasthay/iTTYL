on run {buddyPhone, serviceType, msg, filenames}
    tell application "Messages"
        -- Convert service type string to AppleScript constant
        if serviceType is "iMessage" then
            set targetService to first service whose service type = iMessage
        else if serviceType is "SMS" then
            set targetService to first service whose service type = SMS
        else
            display dialog "Invalid service type: " & serviceType
            return
        end if

        set targetBuddy to buddy buddyPhone of targetService
        set filename_list to my split(filenames, ",")

        -- Ensure the buddy is valid and the file exists
        if targetBuddy is not missing value then
            if msg is not "" then
                send msg to targetBuddy
            end if

            -- loop over attachments
            repeat with i from 1 to (count of filename_list)
                set filename to item i of filename_list
                if filename is not "" then
                    set attach to POSIX file filename as alias
                    send attach to targetBuddy
                end if
            end repeat
        else
            display dialog "Could not find a buddy with the phone number: " & buddyPhone
        end if
    end tell
end run

-- define function for python equivalent of u = s.split(char)
on split(s, char)
    set oldDelimiters to AppleScript's text item delimiters
    set AppleScript's text item delimiters to char
    set splitList to text items of s
    set AppleScript's text item delimiters to oldDelimiters
    return splitList
end split


