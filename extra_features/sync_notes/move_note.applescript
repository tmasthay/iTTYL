on run argv
    tell application "Notes"
        set noteID to item 1 of argv
        -- set noteID to "x-coredata://1A8D080C-4F75-40D7-9A13-50BF7DBCA487/ICNote/p649"
        set theNote to first note whose id is noteID
        set sentFolder to folder "Sent" of account "iCloud"

        -- Move the note to the 'Sent' folder
        move theNote to sentFolder
    end tell
end run

