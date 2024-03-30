on run {targetBuddyPhone, targetMessage, imagePaths}
    tell application "Messages"
        set targetService to 1st service whose service type = iMessage
        set targetBuddy to buddy targetBuddyPhone of targetService
        if targetMessage is not "" then
            send targetMessage to targetBuddy
        end if
    end tell
    if imagePaths is not "" then
        set imageFiles to my split(imagePaths, ",")
        repeat with imagePath in imageFiles
            set attach to POSIX file imagePath
            tell application "Messages" to send attach to targetBuddy
        end repeat
    end if
end run

-- Helper function to split a string by a delimiter
on split(input, delimiter)
    set AppleScript's text item delimiters to delimiter
    set inputList to every text item of input
    set AppleScript's text item delimiters to {""} -- Resets back to default
    return inputList
end split
