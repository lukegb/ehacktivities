class EActivitiesException(Exception):
    pass

class EActivitiesServerException(EActivitiesException):
    def __init__(self, inner):
        self.inner = inner

    def __str__(self):
        return "EActivitiesServerException(" + str(self.inner) + ")"

    def __unicode__(self):
        return u"EActivitiesServerException(" + unicode(self.inner) + u")"

    def __repr__(self):
        return "<EActivitiesServerException(" + repr(self.inner) + ">"

class EActivitiesError(EActivitiesException):
    def __init__(self, error_code, return_code):
        self.error_code = error_code
        self.return_code = return_code

    @property
    def nice_str(self):
        ec, rc = int(self.error_code), int(self.return_code)
        if ec == 1:  # HTTP error?
            if rc == 1:
                return u"Chosen file is too large, please choose a different file."
            elif rc == 4:
                return u"No file(s) chosen for upload."
            elif rc == 5:
                return u"Unable to save file based on permissions, please choose a different file."
            elif rc == 8:
                return u"Unable to save file(s) due to timeout reached. Please try again later."
            elif rc == 60001:
                return u"Unable to save file due to a very similar one already used, please rename the file if this is a mistake."
            elif rc == 60002:
                return u"Only the first 20 files have been uploaded due to file limit, please re-upload the other files separately."
            else:
                return u"Unknown HTTP error %d" % (rc,)
        elif rc == 2: # SQL errors
            if rc == -1:
                return u"No connection exists. The database may be down."
            elif rc == -15:
                return u"Something did not work (-15)."
            elif rc == 5:
                return u"NOT NULL field is null."
            elif rc == 102:
                return u"Bad SQL syntax - field type mismatch?"
            elif rc == 235:
                return u"Unusual character(s) in amount field."
            elif rc == 245 or rc == 8114:
                return u"Unusual character(s) in number field."
            elif rc == 264:
                return u"Nothing to submit?!?"
            elif rc == 515:
                return u"NOT NULLable fields were null."
            elif rc == 547:
                return u"SQL constraint violation."
            elif rc == 2601 or rc == 2627:
                return u"Information replication detected. (SQL)"
            elif rc == 8152:
                return u"Too many characters in field."
            elif rc == 50000:
                return u"Custom SQL error"
            elif rc == 60001:
                return u"Multiple fields updated?!?"
            elif rc == 60002:
                return u"Update conflict resolution by page refresh."
            elif rc == 60003:
                return u"Record did not insert."
            elif rc == 60004:
                return u"Multiple rows just got inserted."
            elif rc == 60005:
                return u"Primary key violation."
            elif rc == 60006:
                return u"Access denied (SQL)"
            elif rc == 60007:
                return u"Required fields missing."
            else:
                return u"Unknown SQL error %d" % (rc,)
        elif ec == 3:  # general errors
            if rc == 1:
                return u"Data integrity error (WTF?)"
            elif rc == 2:
                return u"You have no roles or your session has expired."
            elif rc == 3:
                return u"Bad AJAX request."
            elif rc == 4:
                return u"No AJAX object specified."
            elif rc == 5:
                return u"Generic coding error."
            elif rc == 6:
                return u"No AJAX handler found."
            elif rc == 7:
                return u"Bad object seeking AJAX - no nav?"
            elif rc == 8:
                return u"No matches."
            elif rc == 9:
                return u"Readonly field update detected."
            elif rc == 10:
                return u"Login failed - no roles."
            elif rc == 11:
                return u"You have no further roles."
            elif rc == 12:
                return u"No such rule."
            elif rc == 13:
                return u"Not logged in - cannot upload files."
            elif rc == 14:
                return u"You are viewing non-natural data, therefore do not have permission to do that. Honestly, you should not even see this, so if you do, please tell someone."
            elif rc == 15:
                return u"You are already viewing that data!"
            elif rc == 16:
                return u"No records"
            elif rc == 17:
                return u"Minimum character length on field violation"
            elif rc == 18:
                return u"Please choose search information."
            elif rc == 19:
                return u"No data in that lookup."
            else:
                return u"Unknown general error %d" % (rc,)
        elif ec == 4:  # file errors
            if rc == 1:
                return u"Image has 'bad aspect ratio'."
            elif rc == 2:
                return u"Image has unusable file type."
            elif rc == 3:
                return u"Image too small."
            elif rc == 4:
                return u"File missing size?!?"
            elif rc == 5:
                return u"Complete fields, THEN upload a file!"
            elif rc == 6:
                return u"File type not yet allowed."
            elif rc == 7: 
                return u"Image too large."
            elif rc == 8:
                return u"'Something' is wrong with the file."
            else:
                return u"Unknown file error %d" % (rc,)
        elif ec == 5:  # validation errors
            if rc == 1:
                return u"Negative number entered in field."
            elif rc == 2:
                return u"Date out of range."
            elif rc == 3:
                return u"Date selection required."
            elif rc == 4:
                return u"Something is wrong."
            elif rc == 5:
                return u"Dates do not make sense."
            elif rc == 6:
                return u"DATE HOLIDAY VIOLATION!"
            else:
                return u"Unknown validation error %d" % (rc,)
        elif ec == 7:  # ladder errors
            if rc == 1:
                return u"Error inserting data (in ladder)."
            elif rc == 2:
                return u"Error committing submission (in ladder)."
            elif rc == 3:
                return u"Further authorisation required, but there is no-one available to do so because you can't authorise twice!"
            elif rc == 4:
                return u"Authorisation is being updated elsewhere?"
            elif rc == 5:
                return u"Submission failed (in ladder)."
            elif rc == 6:
                return u"Form not complete (in ladder)."
            elif rc == 8:
                return u"No-one is available at next rung (in ladder)."
            elif rc == 9:
                return u"Your role is wrong. Change role."
            else:
                return u"Unknown ladder error %d" % (rc,)
        else:
            return u"Unknown error %d:%d" % (ec, rc)

    def __str__(self):
        return "EActivitiesError(%s)" % (self.nice_str,)

    def __unicode__(self):
        return "EActivitiesError(%s)" % (self.nice_str,)

    def __repr__(self):
        return "EActivitiesError(%s, %s)" % (self.error_code, self.return_code)

class AuthenticationFailed(EActivitiesException):
    pass

class DoesNotExist(EActivitiesException):
    pass

class EActivitiesHasChanged(EActivitiesException):
    pass
