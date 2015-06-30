from sqlalchemy.testing.requirements import SuiteRequirements

from sqlalchemy.testing import exclusions


class Requirements(SuiteRequirements):
    @property
    def table_reflection(self):
        return exclusions.open()

    @property
    def schemas(self):
        return exclusions.open()

    @property
    def temp_table_names(self):
        return exclusions.open()

    @property
    def views(self):
        return exclusions.open()

    @property
    def datetime_literals(self):
        return exclusions.open()

    @property
    def sequences_optional(self):
        return exclusions.open()

    @property
    def percent_schema_names(self):
        return exclusions.open()

    # #########################################################################
    # DEFECTS IN NUODB
    # #########################################################################

    @property
    def unique_constraint_reflection(self):
        # TODO: Defect: NuoDB ignores CONSTRAINT names; a ticket has been
        # opened. REVISIT!
        return exclusions.closed()

    # #########################################################################
    # DEFECTS IN PYNUODB DRIVER
    # #########################################################################

    @property
    def precision_numerics_many_significant_digits(self):
        # TODO: Defect: Python NuoDB driver does not handle all Decimal types
        # properly. REVISIT!
        return exclusions.open()

    @property
    def precision_numerics_enotation_large(self):
        # TODO: Defect: Python NuoDB driver does not handle all Decimal types
        # properly. REVISIT!
        return exclusions.open()

    @property
    def precision_numerics_retains_significant_digits(self):
        # TODO: Defect: Python NuoDB driver has a fix pending the 2.3 release
        # of the driver that until which these tests will fail. REVISIT!
        return exclusions.open()

    @property
    def implements_get_lastrowid(self):
        # TODO: Defect: PyNuoDB is missing support for getting generated ids.
        # REVISIT!
        return exclusions.closed()

    @property
    def dbapi_lastrowid(self):
        # TODO: Defect: PyNuoDB is missing the lastrowid method on the Cursor
        # class. REVISIT!
        return exclusions.closed()

    # #########################################################################
    # UNSUPPORTED / INTENTIONAL
    # #########################################################################

    @property
    def foreign_key_constraint_reflection(self):
        # NuoDB does not support foreign keys, in particular foreign key names.
        return exclusions.closed()

    @property
    def self_referential_foreign_keys(self):
        # NuoDB does not support foreign keys.
        return exclusions.closed()

    @property
    def datetime_historic(self):
        # NuoDB does not support historic datetimes (datetimes before 1900).
        return exclusions.closed()

    @property
    def date_historic(self):
        # NuoDB does not support historic dates (dates before 1900).
        return exclusions.closed()

    @property
    def returning(self):
        # NuoDB does not support the RETURNING keyword for INSERT.
        return exclusions.closed()
