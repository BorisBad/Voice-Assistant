class Field():
    __is_not_null = False
    __is_primary = False
    __is_autoinc = False
    __is_foreign = False
    __attributes = ""

    def __init__(self, column_name, column_type, is_not_null, is_primary, is_autoinc, is_foreign) -> None:
        self._column_name = column_name
        self._column_type = column_type
        self.__is_not_null = is_not_null
        self.__is_primary = is_primary
        self.__is_autoinc = is_autoinc
        self.__is_foreign = is_foreign
    





            
