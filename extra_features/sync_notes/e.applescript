tell application "Contacts"

    -- List to hold results
    set iPhoneUsers to {}
    set noniPhoneUsers to {}

    -- Go through each contact
    repeat with aPerson in people
        set hasiPhone to false
        set personName to name of aPerson

        -- Check each phone number label
        repeat with aPhone in phones of aPerson
            if label of aPhone is "iPhone" then
                set hasiPhone to true
                exit repeat
            end if
        end repeat

        -- Optionally, check email addresses
        if not hasiPhone then -- Only check if no iPhone label was found
            repeat with anEmail in emails of aPerson
                if address of anEmail ends with "@icloud.com" or address of anEmail ends with "@me.com" or address of anEmail ends with "@mac.com" then
                    set hasiPhone to true
                    exit repeat
                end if
            end repeat
        end if

        -- Store the result
        if hasiPhone then
            set end of iPhoneUsers to personName & " (iPhone)"
        else
            set end of noniPhoneUsers to personName & " (non-iPhone)"
        end if
    end repeat

    -- Output the results
    return {"iPhone Users:", iPhoneUsers, "Non-iPhone Users:", noniPhoneUsers}
end tell
