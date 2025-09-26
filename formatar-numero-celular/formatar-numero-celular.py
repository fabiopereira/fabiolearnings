import pandas as pd
from phonenumbers import PhoneNumberFormat, parse as phone_parse, format_number as phone_format
from io import StringIO

numeros = """ColNum
19981124084
65981013000
12992063862
12991718728
12991625330
12997597592
12991174514
12997722459
12991344169
12992405941
21994704988
19993736482
42991116020
11943187115
13981217652
18981969452
24992069330
61983705990
61920033591
17991700798
13997554394
17981996100
11971712875
11982113897
11947712623
14981164837
11946692207
11989998645
16988272864
11932471106
61981387749
13991199960
19992351993
11976623895
16997101987
11986182155
11945903244
11980387192
61982090273
13988689145
48996332645
16997312886
13997996270
11993805748
64981323903
11992715825
16997893612
11961248584
11948554342
5511996697896
15981143352
15997569112
35998083346
11949836630
11941952564
17991352324
16981481513
11994042803
11998986970
+5511950275382
08062461170
64992115314
19991880399
11943863958
11914506815
35991676968
11999099926
11949311728
61983705990
11986798023
11999914588
13996816627
11939071713
18981969452
19997027372
11977702121
83996250631
65984616838
17988148742
5515998558017
11977106894
13997192118
62998304361
11997783015
+5511950275382
11977106894
19991252441
62999278870
11972770472
11951210416
11993040458
11992808086
12988000034
11981891047
11993912133
11930574697
61992985577
11981513309
92992975409
19991925225
19993287523
83999366077
21967103045
11986760468
11992429172
12997397738
51992661884
47996895940
48991083699
24981860028
19997083078
18998249863
11966078871
11986338945
954234370
11992000338
74988153093
11958096385
11998162471
11914323874
951305331
11944572972
79996078514
5511998619088
11960578076
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