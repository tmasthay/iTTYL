on run
    tell application "System Events"
        tell application process "Messages"
            set frontmost to true
            delay 3  -- Wait for Messages to respond

            -- Get the first window
            -- set theWindow to button 1 of group 1 of group 1 of window 1
            set theWindow to menu 1 of menu bar 1
            my report(description of theWindow, role of theWindow, name of theWindow)
        end tell
    end tell
end run

on report(elementDescription, elementRole, elementName)
    log elementDescription & " (" & elementRole & ") [" & elementName & "]"
end report
