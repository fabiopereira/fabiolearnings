import pandas as pd
from phonenumbers import PhoneNumberFormat, parse as phone_parse, format_number as phone_format
from io import StringIO

numeros = """Número
+5585988001677
85 85460364
85 99221-8211
(85) 9862-64842
(85)987989342
85 9852-36542
85 9971 19741
85986124985
85 985374355
85988881389
85999202078
"""

df = pd.read_csv(StringIO(numeros), sep=';')

df['Número'] = df['Número'].apply(lambda n: phone_format(phone_parse(n, 'BR'), PhoneNumberFormat.E164))

print(df)