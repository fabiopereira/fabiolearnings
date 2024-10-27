import pandas as pd
from phonenumbers import PhoneNumberFormat, parse as phone_parse, format_number as phone_format
from io import StringIO



print(phone_format(phone_parse('44313424', 'BR'), PhoneNumberFormat.E164))
