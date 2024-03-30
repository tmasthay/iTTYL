on run argv
    set filename to item 1 of argv
    set buddyName to item 2 of argv
    set attach to POSIX file filename
    tell application "Messages" to send attach to buddy buddyName
end run
