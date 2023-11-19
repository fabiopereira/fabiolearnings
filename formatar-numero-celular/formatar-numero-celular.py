import pandas as pd
from phonenumbers import PhoneNumberFormat, parse as phone_parse, format_number as phone_format
from io import StringIO

numeros = """ColNum
551143247524
5541998264638
11 98189 0214
43999763219
54999730540
43999335571
43 991655705
11965209887
71991011908
18981311292
15981209898
41999628750
41 996230017 
45991350505
91992656484
46991194527
27-988197561 
46 99919-1483 
41999905553
"""

def formatar_numero(n):
    n = phone_format(phone_parse(n, 'BR'), PhoneNumberFormat.E164)
    n = adicionar_nove_ao_celular(n)
    return n

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

df['ColNum_Formatado'] = df['ColNum'].apply(lambda n: formatar_numero(n))

print(df)