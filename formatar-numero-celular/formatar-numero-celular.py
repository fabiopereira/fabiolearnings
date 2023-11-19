import pandas as pd
from phonenumbers import PhoneNumberFormat, parse as phone_parse, format_number as phone_format
from io import StringIO

numeros = """ColNum
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

def adicionar_nove_ao_celular(numero):
    # Verifica se o número já possui um "9" após o DDD
    if len(numero) == 13 and numero[0] == '+':
        return numero[:5] + '9' + numero[5:]

    return numero

# Testando adicionar_nove_ao_celular
# numero_celular = "+551143247524"  # Substitua pelo número de celular desejado
# novo_numero_celular = adicionar_nove_ao_celular(numero_celular)
# print(f"Número original: {numero_celular}")
# print(f"Novo número: {novo_numero_celular}")


df = pd.read_csv(StringIO(numeros), sep=';')

df['ColNum'] = df['ColNum'].apply(lambda n: phone_format(phone_parse(n, 'BR'), PhoneNumberFormat.E164))
df['ColNum'] = df['ColNum'].apply(lambda n: adicionar_nove_ao_celular(n))

print(df)