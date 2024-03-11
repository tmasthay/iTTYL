tell application "Contacts"
    -- Initialize a variable to hold the final output
    set finalOutput to ""
    
    set contactList to every person
    
    repeat with aContact in contactList
        set contactName to the name of aContact
        -- Start building the string for each contact
        set phoneNumbersString to contactName & ": "
        
        try
            set phoneList to the phones of aContact -- Retrieve the list of phones
            if phoneList is not {} then -- Check if the phoneList is not empty
                repeat with aPhone in phoneList
                    set phoneValue to value of aPhone
                    -- Append each phone number with a comma
                    set phoneNumbersString to phoneNumbersString & phoneValue & ","
                end repeat
                -- Optionally, remove the trailing comma from the last phone number
                if length of phoneNumbersString > 2 then
                    set phoneNumbersString to text 1 thru -2 of phoneNumbersString -- Remove last comma
                end if
            else
                set phoneNumbersString to phoneNumbersString & "NONE"
            end if
        on error errMsg
            set phoneNumbersString to phoneNumbersString & "Error accessing phones: " & errMsg
        end try
        
        -- Append this contact's information to the final output, with a newline for each contact
        set finalOutput to finalOutput & phoneNumbersString & "\n"
    end repeat
    
    -- Final output preparation
    -- set finalOutput to finalOutput & "Finished processing contacts."
end tell

-- Output the final result
return finalOutput
