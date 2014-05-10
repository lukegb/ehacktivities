# vim: set fileencoding=utf-8


def enum(**enums):
    return type('Enum', (), enums)

EActivitiesErrorTypes = enum(HTTP=1, SQL=2, GENERAL=3, FILE=4, VALIDATION=5, LADDER=7)
EActivitiesHttpErrors = enum(
    FILE_TOO_LARGE=1,
    NO_FILES=4,
    FILE_PERMISSIONS_ERROR=5,
    FILE_UPLOAD_TIMEOUT=8,
    FILE_COLLISION=60001,
    FILE_MAX_COUNT=60002
)
EActivitiesSqlErrors = enum(
    NO_CONNECTION=-1,
    SOMETHING_BORKED=-15,
    NOT_NULL_NULLED=5,
    BAD_SYNTAX=102,
    UNUSUAL_AMOUNT_CHARACTERS=235,
    UNUSUAL_NUMBER_CHARACTERS=245,
    UNUSUAL_DATETIME_CHARACTERS=8114,
    NOTHING_TO_SUBMIT=264,
    NOT_NULLABLE_NULLED=515,
    CONSTRAINT_VIOLATION=547,
    UNIQUE_CONSTRAINT_VIOLATION=2601,
    UNIQUE_INDEX_VIOLATION=2627,
    TOO_MANY_CHARACTERS=8152,
    CUSTOM_SQL_ERROR=50000,
    MULTIPLE_FIELDS_UPDATED=60001,
    CONFLICT_DETECTED=60002,
    INSERTION_FAILED=60003,
    MULTIPLE_ROWS_INSERTED=60004,
    PRIMARY_KEY_VIOLATION=60005,
    ACCESS_DENIED=60006,
    REQUIRED_FIELDS_MISSING=60007,
)
EActivitiesGeneralErrors = enum(
    DATA_INTEGRITY_ERROR=1,
    NO_ROLES=2,
    BAD_REQUEST=3,
    NO_AJAX_OBJECT=4,
    GENERIC_ERROR=5,
    NO_AJAX_HANDLER=6,
    NO_NAVIGATION=7,
    NO_MATCHES=8,
    READONLY_FIELD_UPDATE=9,
    LOGIN_FAILED_NO_ROLES=10,
    NO_MORE_ROLES=11,
    NO_SUCH_ROLE=12,
    NOT_LOGGED_IN_UPLOAD_DENIED=13,
    NONNATURAL_DATA=14,
    ALREADY_VIEWING=15,
    NO_RECORDS=16,
    MINIMUM_CHAR_LENGTH_VIOLATION=17,
    NO_SEARCH_INFORMATION=18,
    NO_LOOKUP_DATA=19,
)
EActivitiesFileErrors = enum(
    BAD_ASPECT_RATIO=1,
    UNUSABLE_FILE_TYPE=2,
    TOO_SMALL=3,
    NO_SIZE=4,
    FIELDS_INCOMPLETE=5,
    FILE_TYPE_NOT_PERMITTED=6,
    TOO_LARGE=7,
    SOMETHING_BORKED=8
)
EActivitiesValidationErrors = enum(
    NEGATIVE_NUMBER=1,
    DATE_OUT_OF_RANGE=2,
    DATE_SELECTION_REQUIRED=3,
    SOMETHING_BORKED=4,
    NONSENSICAL_DATES=5,
    DATE_HOLIDAY_VIOLATION=6
)
EActivitiesLadderErrors = enum(
    INSERTION_FAILED=1,
    COMMIT_FAILED=2,
    NO_MORE_AUTHORISERS=3,
    CONFLICT_DETECTED=4,
    SUBMISSION_FAILED=5,
    FORM_INCOMPLETE=6,
    NOONE_AVAILABLE_NEXT_RUNG=7,
    ROLE_INCORRECT=8
)


EACTIVITIES_ERRORS_STR = {
    EActivitiesErrorTypes.HTTP: {
        EActivitiesHttpErrors.FILE_TOO_LARGE: u"Chosen file is too large, please choose a different file.",
        EActivitiesHttpErrors.NO_FILES: u"No file(s) chosen for upload.",
        EActivitiesHttpErrors.FILE_UPLOAD_TIMEOUT: u"Unable to save file(s) due to timeout reached. Please try again later.",
        EActivitiesHttpErrors.FILE_COLLISION: u"Unable to save file due to a very similar one already used, " +
                                              u"please rename the file if this is a mistake.",
        EActivitiesHttpErrors.FILE_MAX_COUNT: u"Only the first 20 files have been uploaded due to file limit, " +
                                              u"please re-upload the other files separately.",
    },
    EActivitiesErrorTypes.SQL: {
        EActivitiesSqlErrors.NO_CONNECTION: u"No connection exists. The database may be down.",
        EActivitiesSqlErrors.SOMETHING_BORKED: u"Something did not work.",
        EActivitiesSqlErrors.NOT_NULL_NULLED: u"NOT NULL field is null.",
        EActivitiesSqlErrors.BAD_SYNTAX: u"Bad SQL syntax - field type mismatch?",
        EActivitiesSqlErrors.UNUSUAL_AMOUNT_CHARACTERS: u"Unusual character(s) in amount field.",
        EActivitiesSqlErrors.UNUSUAL_NUMBER_CHARACTERS: u"Unusual character(s) in number field.",
        EActivitiesSqlErrors.UNUSUAL_DATETIME_CHARACTERS: u"Unusual character(s) in datetime field.",
        EActivitiesSqlErrors.NOTHING_TO_SUBMIT: u"Nothing to submit?!?",
        EActivitiesSqlErrors.NOT_NULLABLE_NULLED: u"NOT NULLable fields were null.",
        EActivitiesSqlErrors.CONSTRAINT_VIOLATION: u"SQL constraint violation.",
        EActivitiesSqlErrors.UNIQUE_CONSTRAINT_VIOLATION: u"Unique constraint violated.",
        EActivitiesSqlErrors.UNIQUE_INDEX_VIOLATION: u"Unique index violated.",
        EActivitiesSqlErrors.TOO_MANY_CHARACTERS: u"Too many characters in field.",
        EActivitiesSqlErrors.CUSTOM_SQL_ERROR: u"Custom SQL error",
        EActivitiesSqlErrors.MULTIPLE_FIELDS_UPDATED: u"Multiple fields updated?!?",
        EActivitiesSqlErrors.CONFLICT_DETECTED: u"Update conflict resolution by page refresh.",
        EActivitiesSqlErrors.INSERTION_FAILED: u"Record did not insert.",
        EActivitiesSqlErrors.MULTIPLE_ROWS_INSERTED: u"Multiple rows just got inserted.",
        EActivitiesSqlErrors.PRIMARY_KEY_VIOLATION: u"Primary key violation.",
        EActivitiesSqlErrors.ACCESS_DENIED: u"Access denied (SQL)",
        EActivitiesSqlErrors.REQUIRED_FIELDS_MISSING: u"Required fields missing.",
    },
    EActivitiesErrorTypes.GENERAL: {
        EActivitiesGeneralErrors.DATA_INTEGRITY_ERROR: u"Data integrity error (WTF?)",
        EActivitiesGeneralErrors.NO_ROLES: u"You have no roles or your session has expired.",
        EActivitiesGeneralErrors.BAD_REQUEST: u"Bad AJAX request.",
        EActivitiesGeneralErrors.NO_AJAX_OBJECT: u"No AJAX object specified.",
        EActivitiesGeneralErrors.GENERIC_ERROR: u"Generic coding error.",
        EActivitiesGeneralErrors.NO_AJAX_HANDLER: u"No AJAX handler found.",
        EActivitiesGeneralErrors.NO_NAVIGATION: u"Bad object seeking AJAX - no nav?",
        EActivitiesGeneralErrors.NO_MATCHES: u"No matches.",
        EActivitiesGeneralErrors.READONLY_FIELD_UPDATE: u"Readonly field update detected.",
        EActivitiesGeneralErrors.LOGIN_FAILED_NO_ROLES: u"Login failed - no roles.",
        EActivitiesGeneralErrors.NO_MORE_ROLES: u"You have no further roles.",
        EActivitiesGeneralErrors.NO_SUCH_ROLE: u"No such role.",
        EActivitiesGeneralErrors.NOT_LOGGED_IN_UPLOAD_DENIED: u"Not logged in - cannot upload files.",
        EActivitiesGeneralErrors.NONNATURAL_DATA: u"You are viewing non-natural data, therefore do not have permission to do that.",
        EActivitiesGeneralErrors.ALREADY_VIEWING: u"You are already viewing that data!",
        EActivitiesGeneralErrors.NO_RECORDS: u"No records",
        EActivitiesGeneralErrors.MINIMUM_CHAR_LENGTH_VIOLATION: u"Minimum character length on field violation",
        EActivitiesGeneralErrors.NO_SEARCH_INFORMATION: u"Please choose search information.",
        EActivitiesGeneralErrors.NO_LOOKUP_DATA: u"No data in that lookup.",
    },
    EActivitiesErrorTypes.FILE: {
        EActivitiesFileErrors.BAD_ASPECT_RATIO: u"Image has 'bad aspect ratio'.",
        EActivitiesFileErrors.UNUSABLE_FILE_TYPE: u"Image has unusable file type.",
        EActivitiesFileErrors.TOO_SMALL: u"Image too small.",
        EActivitiesFileErrors.NO_SIZE: u"File missing size?!?",
        EActivitiesFileErrors.FIELDS_INCOMPLETE: u"Complete fields, THEN upload a file!",
        EActivitiesFileErrors.FILE_TYPE_NOT_PERMITTED: u"File type not yet allowed.",
        EActivitiesFileErrors.TOO_LARGE: u"Image too large.",
        EActivitiesFileErrors.SOMETHING_BORKED: u"'Something' is wrong with the file.",
    },
    EActivitiesErrorTypes.VALIDATION: {
        EActivitiesValidationErrors.NEGATIVE_NUMBER: u"Negative number entered in field.",
        EActivitiesValidationErrors.DATE_OUT_OF_RANGE: u"Date out of range.",
        EActivitiesValidationErrors.DATE_SELECTION_REQUIRED: u"Date selection required.",
        EActivitiesValidationErrors.SOMETHING_BORKED: u"Something is wrong.",
        EActivitiesValidationErrors.NONSENSICAL_DATES: u"Dates do not make sense.",
        EActivitiesValidationErrors.DATE_HOLIDAY_VIOLATION: u"DATE HOLIDAY VIOLATION!",
    },
    EActivitiesErrorTypes.LADDER: {
        EActivitiesLadderErrors.INSERTION_FAILED: u"Error inserting data (in ladder).",
        EActivitiesLadderErrors.COMMIT_FAILED: u"Error committing submission (in ladder).",
        EActivitiesLadderErrors.NO_MORE_AUTHORISERS: u"Further authorisation required, but no-one can because you can't authorise twice!",
        EActivitiesLadderErrors.CONFLICT_DETECTED: u"Authorisation is being updated elsewhere?",
        EActivitiesLadderErrors.SUBMISSION_FAILED: u"Submission failed (in ladder).",
        EActivitiesLadderErrors.FORM_INCOMPLETE: u"Form not complete (in ladder).",
        EActivitiesLadderErrors.NOONE_AVAILABLE_NEXT_RUNG: u"No-one is available at next rung (in ladder).",
        EActivitiesLadderErrors.ROLE_INCORRECT: u"Your role is wrong. Change role.",
    }
}


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

        ret = EACTIVITIES_ERRORS_STR.get(ec, None)
        if ret is not None:
            ret = ret.get(rc, None)

        rc = rc or u"Unknown error: %d:%d" % (ec, rc)

        return rc

    def __str__(self):
        return "EActivitiesError(%s)" % (self.nice_str,)

    def __unicode__(self):
        return "EActivitiesError(%s)" % (self.nice_str,)

    def __repr__(self):
        return "EActivitiesError(%s, %s)" % (self.error_code, self.return_code)


class AuthenticationFailed(EActivitiesException):
    pass


class NotLoggedIn(AuthenticationFailed):
    pass


class AccessDenied(EActivitiesException):
    pass


class DoesNotExist(EActivitiesException):
    pass


class YearNotAvailable(DoesNotExist):
    pass


class EActivitiesHasChanged(EActivitiesException):
    pass


class ThisShouldNeverHappen(EActivitiesException):
    pass
