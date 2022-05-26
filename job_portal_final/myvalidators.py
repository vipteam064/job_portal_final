import datetime

# Functions to get values for validation dynamically
def passing_year_limit_value():
    return datetime.date.today().year

# should not start with space, ', (, ), - or .
# all characters must be a letter (A-ZÀ-ÖØ-Þ) or special character (\'()\-\.) or space
# special character cannot be followed by another special character
# space cannot be followed by itself
# should not end with space, ', ( or -
name_regex = r'^(?![ \'()\-\.])(?:[a-zA-Zà-öÀ-Öø-þØ-Þ]|[\'()\-\.](?![\'()\-\.])| (?! ))+(?<![ \'(\-])$'
# same as name_regex but removed ( and ) and added ,
person_name_regex = r'^(?![ \'\-\.,])(?:[a-zA-Zà-öÀ-Öø-þØ-Þ]|[\'\-\.,](?![\'\-\.,])| (?! ))+(?<![ \'\-,])$'
# same as name_regex but added , and digits are allowed
# NOTE: make sure to check that user doesn't enter only digits
# company_name_regex is also used for exam_name
company_name_regex = r'^(?![ \'()\-\.,])(?:[a-zA-Zà-öÀ-Öø-þØ-Þ\d]|[\'()\-\.,](?![\'()\-\.,])| (?! ))+(?<![ \'(\-,])$'
# same as name_regex but added ,
job_title_regex = r'^(?![ \'()\-\.,\+])(?:[a-zA-Zà-öÀ-Öø-þØ-Þ]|[\'()\-\.,\+](?![\'()\-\.,])| (?! ))+(?<![ \'(\-,])$'
