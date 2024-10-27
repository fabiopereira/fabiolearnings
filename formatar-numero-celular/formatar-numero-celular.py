import pandas as pd
from phonenumbers import PhoneNumberFormat, parse as phone_parse, format_number as phone_format
from io import StringIO

numeros = """ColNum
11943326020
81996077392
21979928954
41992579765
81988878881
11991318897
21996211849
21969929621
51992401864
61983638661
11996705819
11951139533
47992801211
61993794243
21988045360
21994096770
31971098937
21999818218
31996222108
48984638180
51995581504
8192230948
21993385661
11948426551
21981114647
15981411615
11989232131
61981326566
11986674974
61983484306
11988353955
19997241914
81996575769
11981513309
18981152807
31999898383
17991416541
81997564335
973797502
14996516432
991228868
34998164606
19991996606
11974717077
11950619966
15991376128
081993936333
11971123300
11976518971
11982600738
41995210889
34999653341
11975483056
11977765936
17981850596
11948581521
11998545420
11985155742
11945922198
19997354964
42984269502
65996655122
44999031406
11975209634
31984212347
61982311327
21994587316
64999474517
65984125458
11942430145
48984049454
219999080031
61982704559
61981148484
31988451666
11998442943
21997676178
11998768021
64981337819
81986359225
12981566784
11949155546
11982591977
11953700557
62981282208
31993353286
5511964754038
17996754903
11915772112
81995503330
11974932610
41996397059
11998074856
5521993808116
12991024120
11941287633
13991065919
47988229185
12991620102
11993212141
17981108332
17991367883
48991640827
61993794243
11987607350
11960747032
41999776315
61981337443
11919973548
48998088818
992593079
11994148171
21995717133
11942500540
21988039824
11975516631
11947948054
31996222108
19974144567
11995915141
11982797445
"""

def formatar_numero_2(n):
    n = adicionar_codigo_pais_ao_celular('55', n)
    n = adicionar_nove_ao_celular(n)

def formatar_numero(n, ddd_default):
    n = phone_format(phone_parse(n, 'BR'), PhoneNumberFormat.E164)
    n = adicionar_nove_ao_celular(n)
    n = adicionar_ddd_default_ao_celular(n, ddd_default)
    return n

def adicionar_codigo_pais_ao_celular(codigo_pais, numero):
    if len(numero) == 11:
        return codigo_pais + numero
    
    return numero


def adicionar_nove_ao_celular(numero):
    # Verifica se o número já possui um "9" após o DDD
    if len(numero) == 13 and numero[0] == '+':
        return numero[:5] + '9' + numero[5:]

    return numero

def adicionar_ddd_default_ao_celular(numero, ddd_default):
    if len(numero) == 12 and numero[0] == '+':
        return numero[:3] + ddd_default + numero[3:]

    return numero


# Testando adicionar_nove_ao_celular
# numero_celular = "+551143247524"  # Substitua pelo número de celular desejado
# novo_numero_celular = adicionar_nove_ao_celular(numero_celular)
# print(f"Número original: {numero_celular}")
# print(f"Novo número: {novo_numero_celular}")

# print(formatar_numero('44313424'))

ddd_default = '11'

df = pd.read_csv(StringIO(numeros), sep=';')
# for index, row in df.iterrows():
#     n = row['ColNum']
#     # print(n)
#     formatar_numero(str(n))

df['ColNum_Formatado'] = df['ColNum'].apply(lambda n: formatar_numero(str(n), ddd_default))
# print(df)
df['ColNum_Formatado'].apply(lambda n: print(str(n)))