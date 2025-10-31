from datetime import datetime, date, timedelta
import os
import csv
import shutil
import unicodedata
import argparse


from datetime import datetime, timedelta

def normalizar(texto):
    return unicodedata.normalize('NFC', texto.strip())

class EventoAgenda:
    def __init__(self, titulo, inicio=None, fim=None):
        self.titulo = titulo
        self._inicio = inicio
        self._fim = fim

    def titulo_normalizado(self):
        return normalizar(self.titulo)

    def inicio(self):
        return self._inicio

    def fim(self):
        return self._fim

    def inicio_no_passado(self):
        return self._inicio and self._inicio < date.today()
    
    def inicio_nos_proximos_x_dias(self, em_x_dias):
        hoje = date.today()
        limite = hoje + timedelta(days=em_x_dias)
        return self._inicio and hoje <= self._inicio <= limite

    def esta_entre(self, data_inicio, data_fim):
        return self._inicio and data_inicio <= self._inicio <= data_fim

    def eh_save(self):
        return self.titulo.startswith("SAVE")

    def __repr__(self):
        return f"<Evento: {self.titulo} - {self._inicio}>"
    
class Agenda:
    def __init__(self, eventos=None):
        self._eventos = eventos if eventos else []

    def eventos(self):
        return self._eventos

    def titulos(self):
        return [evento.titulo for evento in self._eventos]

    def filtrar_por_prefixo(self, prefixo):
        return [e for e in self._eventos if e.titulo.startswith(prefixo)]

    def __iter__(self):
        return iter(self._eventos)


def carregar_eventos_agenda(arquivo_agenda_ics):
    eventos = []
    evento = {}

    with open(arquivo_agenda_ics, 'r', encoding='utf-8') as arquivo:
        for linha in arquivo:
            linha = linha.strip()

            if linha == "BEGIN:VEVENT":
                evento = {}

            elif linha.startswith("SUMMARY:"):
                evento["titulo"] = normalizar(linha.replace("SUMMARY:", ""))

            elif linha.startswith("DTSTART"):
                data_raw = linha.split(":")[1]
                try:
                    evento["inicio"] = datetime.strptime(data_raw[:8], "%Y%m%d").date()
                except:
                    evento["inicio"] = None

            elif linha.startswith("DTEND"):
                data_raw = linha.split(":")[1]
                try:
                    evento["fim"] = datetime.strptime(data_raw[:8], "%Y%m%d").date()
                except:
                    evento["fim"] = None

            elif linha == "END:VEVENT":
                if evento.get("titulo"):
                    eventos.append(EventoAgenda(
                        titulo=evento["titulo"],
                        inicio=evento.get("inicio"),
                        fim=evento.get("fim")
                    ))

    return Agenda(eventos)


def validar_que_negocios_tem_save_na_agenda(negocios_pipedrive_arquivo, arquivo_agenda_ics):
    etapas_que_precisam_de_save = [
        "Preparando Proposta",
        "Proposta Pronta",
        "Proposta Enviada",
        "🔥Quente"
    ]

    etapas_que_precisam_de_check = [
        "Contratado",
        "Documentação Pós Venda",
        "Logística e Briefing",
        "Prep Entrega",
        "Esperando Entrega",
        "Pós Entrega"
    ]

    agenda = carregar_eventos_agenda(arquivo_agenda_ics)
    titulos_eventos = agenda.titulos()    

    print(f"--------- Negócios que tem SAVE no passado. Considerar FUP")
    for evento in agenda:
        if evento.eh_save() and evento.inicio_no_passado():
            print(f"⚠️ '{evento.titulo}' em {evento.inicio()}")


    print(f"--------- Negócios que tem SAVE próximo.")
    for evento in agenda:
        if evento.eh_save() and evento.inicio_nos_proximos_x_dias(10):
            # print(f"📆 Evento SAVE nos próximos 10 dias: {evento.titulo} em {evento.inicio()}")
            dias_faltando = (evento.inicio() - date.today()).days
            print(f"📆 Evento SAVE em {dias_faltando} dias: {evento.titulo} — {evento.inicio().strftime('%d/%m/%Y')}")

    ################################################################
    ######## Imprimir todos os SAVEs e todas as confirmações ########
    ################################################################
    # print("\n💾💾💾💾💾💾💾 Eventos SAVE encontrados na agenda:")
    # for titulo in titulos_eventos:
    #     if titulo.startswith("SAVE "):
    #         print(f"- {titulo}")
    # print("\n✅🎤 Eventos de Confirmação (✅🎤) encontrados na agenda:")
    # for titulo in titulos_eventos:
    #     if titulo.startswith("✅🎤 "):
    #         print(f"- {titulo}")

    # Ler os negócios do PipeDrive
    print(f"--------- Negócios que  precisam ter um SAVE na agenda e não tem.")
    with open(negocios_pipedrive_arquivo, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            titulo_negocio = normalizar(row['Título'])
            etapa = normalizar(row['Etapa'])

            if etapa in etapas_que_precisam_de_save:
                encontrou_save = any(titulo.startswith(f"SAVE {titulo_negocio}") for titulo in titulos_eventos)
                if not encontrou_save:
                    print(f"⚠️  Negócio '{titulo_negocio}' com etapa '{etapa}'")

    # Ler os negócios do PipeDrive
    print(f"--------- Negócios que  precisam ter confirmação ✅🎤 e 🎤📦🔴 ENTREGA na agenda e não tem.")
    with open(negocios_pipedrive_arquivo, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            titulo_negocio = normalizar(row['Título'])
            etapa = normalizar(row['Etapa'])

            if etapa in etapas_que_precisam_de_check:
                encontrou_check = any(
                    titulo == f"✅🎤 {titulo_negocio}" or titulo == f"✅🎤 Palestra {titulo_negocio}" or titulo == f"✅🎤Palestra {titulo_negocio}"
                    for titulo in titulos_eventos
                )

                if not encontrou_check:
                    print(f"⚠️  Negócio '{titulo_negocio}' com etapa '{etapa}' precisa de ✅🎤 na agenda e não tem")

                # Só exige ENTREGA se houver um ✅🎤 no presente ou futuro
                hoje = date.today()
                evento_check = next(
                    (
                        e for e in agenda 
                        if e.titulo in [
                            f"✅🎤 {titulo_negocio}",
                            f"✅🎤 Palestra {titulo_negocio}",
                            f"✅🎤Palestra {titulo_negocio}"
                        ]
                    ), None
                )

                if evento_check and evento_check.inicio() and evento_check.inicio() >= hoje:
                    encontrou_entrega = any(
                        e.titulo in [
                            f"🎤📦🔴 ENTREGA {titulo_negocio}",
                            f"🎤📦🔴ENTREGA {titulo_negocio}"
                        ]
                        for e in agenda
                    )
                    if not encontrou_entrega:
                        print(f"⚠️  Tem ✅🎤 mas NÃO tem '🎤📦🔴 ENTREGA {titulo_negocio}' com etapa '{etapa}'")



def validar_que_negocios_tem_pastas(negocios_pipedrive_arquivo, diretorio_base):
    etapas_que_precisam_de_pasta = [
        "Preparando Proposta",
        "Proposta Pronta",
        "Proposta Enviada",
        "🔥Quente",
        "Contratado",
        "Documentação Pós Venda",
        "Logística e Briefing",
        "Prep Entrega",
        "Esperando Entrega",
        "Pós Entrega"
    ]

    # Ler os negócios do CSV
    negocios = []
    with open(negocios_pipedrive_arquivo, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            titulo = normalizar(row['Título'])
            etapa = normalizar(row['Etapa'])
            if etapa in etapas_que_precisam_de_pasta:
                negocios.append((titulo, etapa))

    # Listar todas as pastas existentes no diretório
    pastas_existentes = set()
    for nome_pasta in os.listdir(diretorio_base):
        caminho_pasta = os.path.join(diretorio_base, nome_pasta)
        if os.path.isdir(caminho_pasta):
            pastas_existentes.add(normalizar(nome_pasta))

    # Validar se cada negócio tem uma pasta correspondente
    for titulo, etapa in negocios:
        if titulo not in pastas_existentes:
            print(f"⚠️  Negócio do PipeDrive com etapa '{etapa}' não tem pasta correspondente: {titulo}")
            if args.criarPastasDrive:
                print("ℹ️ Modo --criarPastasDrive ativado")
                resposta = input(f"Quer criar a pasta do Drive do Negócio '{titulo}'? (y/n): ").strip().lower()
                if resposta == 'y':
                    print(f"✅ Criando Drive do Negócio '{titulo}")
                    criar_pasta_com_template(titulo, diretorio_base)


def criar_pasta_com_template(titulo, diretorio_base):
    pasta_destino = os.path.join(diretorio_base, titulo)
    pasta_template = os.path.join(diretorio_base, "TEMPLATE-NOVA-PASTA-NOVO-NEGOCIO")

    # Criar a nova pasta se não existir
    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)
        print(f"📁 Pasta criada: {pasta_destino}")
    else:
        print(f"⚠️ Pasta já existe: {pasta_destino}")

    # Copiar conteúdo do template
    if not os.path.exists(pasta_template):
        print(f"❌ Template não encontrado: {pasta_template}")
        return

    for item in os.listdir(pasta_template):
        src_path = os.path.join(pasta_template, item)
        dst_path = os.path.join(pasta_destino, item)

        if os.path.isdir(src_path):
            shutil.copytree(src_path, dst_path, dirs_exist_ok=True)
        else:
            shutil.copy2(src_path, dst_path)

    print(f"✅ Conteúdo copiado de {pasta_template} para {pasta_destino}")

    # Renomeando DocNegocio com o nome do negócio
    nome_antigo = os.path.join(pasta_destino, "DocNegocio NOME_DO_NEGOCIO.docx")
    nome_novo   = os.path.join(pasta_destino, f"DocNegocio {titulo}.docx")
    os.rename(nome_antigo, nome_novo)



# Processar pastas de negócios
def processar_pastas(negocios_pipedrive_arquivo, base_dir, args):
    # Ler CSV e criar um dicionário {Título: Etapa}
    negocios = {}
    with open(negocios_pipedrive_arquivo, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:            
            titulo = unicodedata.normalize('NFC', row['Título'].strip())
            etapa = unicodedata.normalize('NFC', row['Etapa'].strip())
            negocios[titulo] = etapa

    # print(negocios)

    # Listar todas as pastas no diretório base
    for pasta in os.listdir(base_dir):
        pasta = unicodedata.normalize('NFC', pasta)
        pasta_path = os.path.join(base_dir, pasta)
        
        # Verificar se é pasta e se não começa com ARCHIVE
        if os.path.isdir(pasta_path) and not pasta.startswith('ARCHIVE') and not pasta.startswith('TEMPLATE'):
            if pasta not in negocios:
                print(f"⚠️ Pasta '{pasta}' não possui Negócio no PipeDrive")
            else:
                etapa = negocios[pasta]
                if etapa in ['✅ Entregue', 'Perdido']:
                    destino = os.path.join(base_dir, f'ARCHIVE-{etapa}')
                    if not os.path.exists(destino):
                        os.makedirs(destino)
                    shutil.move(pasta_path, os.path.join(destino, pasta))
                    print(f"✅ Pasta {pasta} movida para {destino}")
                # else:
                #     print(f"✅ Pasta {pasta} do negócio na Etapa: {etapa} está no dir raiz")

def validar_inconsistencias(negocios_pipedrive_arquivo, diretorio_base, negocios_sheet_arquivo):

    # Ler CSV e criar um dicionário de negocios_sheet
    negocios_sheet = {}
    with open(negocios_sheet_arquivo, newline='', encoding='utf-8') as csvfile:
        next(csvfile) # Os títulos estão na linha 2
        reader = csv.DictReader(csvfile)
        for row in reader:            
            titulo = unicodedata.normalize('NFC', row['TÍTULO DO NEGÓCIO'].strip())
            data_palestra = unicodedata.normalize('NFC', row['Data Palestra'].strip())
            negocios_sheet[titulo] = data_palestra
            # print(titulo)


    negocios = {}
    with open(negocios_pipedrive_arquivo, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:            
            titulo = unicodedata.normalize('NFC', row['Título'].strip())
            etapa = unicodedata.normalize('NFC', row['Etapa'].strip())
            negocios[titulo] = etapa

            if etapa in ['Documentação Pós Venda', 'Logística e Briefing', 'Prep Entrega', 'Esperando Entrega', 'Pós Entrega']:
                if titulo not in negocios_sheet:
                    print(f"⚠️ Negócio '{titulo}' com Etapa '{etapa}' deveria estar na NegociosSheet")
                # else:
                #     print(f"✅ Negócio '{titulo}' com Etapa '{etapa}' está na NegociosSheet")



def encontrar_arquivo_mais_recente(diretorio, filtro_inicio, filtro_final):
    arquivos = []

    # Listar todos os arquivos no diretório
    for nome_arquivo in os.listdir(diretorio):
        caminho_arquivo = os.path.join(diretorio, nome_arquivo)
        
        # Filtrar apenas arquivos (não pastas)
        if os.path.isfile(caminho_arquivo):
            # Se houver filtro por extensão, aplica o filtro
            if filtro_inicio:
                if nome_arquivo.startswith(filtro_inicio) and nome_arquivo.endswith(filtro_final):
                    arquivos.append(caminho_arquivo)
            else:
                arquivos.append(caminho_arquivo)

    if not arquivos:
        print("🛑🛑🛑 Nenhum arquivo encontrado com o filtro especificado.")
        return None

    # Ordenar os arquivos pela data de modificação (do mais antigo para o mais recente)
    arquivos.sort(key=lambda x: os.path.getmtime(x))

    # Retornar o mais recente
    arquivo_mais_recente = arquivos[-1]
    print(f"📂 Arquivo mais recente encontrado: {arquivo_mais_recente}")
    return arquivo_mais_recente


def extrair_eventos_ics(arquivo_ics):
    eventos = []
    with open(arquivo_ics, 'r', encoding='utf-8') as arquivo:
        evento = {}
        for linha in arquivo:
            if linha.startswith('BEGIN:VEVENT'):
                evento = {}
            elif linha.startswith('SUMMARY:'):
                evento['titulo'] = normalizar(linha.replace('SUMMARY:', '').strip())
                # print(f"📆📆📆📆 EVENTO {evento['titulo']}")
            elif linha.startswith('DTSTART;'):
                data_raw = linha.split(":")[1].strip()
                try:
                    evento['inicio'] = datetime.strptime(data_raw[:8], "%Y%m%d").date()
                except:
                    evento['inicio'] = None
            elif linha.startswith('DTEND;'):
                data_raw = linha.split(":")[1].strip()
                try:
                    evento['fim'] = datetime.strptime(data_raw[:8], "%Y%m%d").date()
                except:
                    evento['fim'] = None
            elif linha.startswith('END:VEVENT'):
                if 'titulo' in evento:
                    eventos.append(evento)
    return eventos

def validar_pos_entrega_para_data_palestra_no_passado(negocios_pipedrive_arquivo, negocios_sheet_arquivo):
    print("\n🔍 Os negócios abaixo têm Data Palestra no passado e já deveriam estar em uma outra etapa:")

    hoje = date.today()

    # 1. Carrega etapas do PipeDrive
    etapas_pipedrive = {}
    with open(negocios_pipedrive_arquivo, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            titulo = normalizar(row['Título'])
            etapa = normalizar(row['Etapa'])
            etapas_pipedrive[titulo] = etapa

    # 2. Percorre negócios da Sheet (onde tem a Data Palestra)
    with open(negocios_sheet_arquivo, newline='', encoding='utf-8') as csvfile:
        next(csvfile)  # Pula a linha 1 se os títulos estiverem na linha 2
        reader = csv.DictReader(csvfile)
        for row in reader:
            titulo = normalizar(row['TÍTULO DO NEGÓCIO'])
            data_palestra_raw = row.get('Data Palestra', '').strip()

            if not data_palestra_raw:
                continue  # sem data, ignora

            data_palestra = datetime.strptime(data_palestra_raw, "%d/%m/%Y").date()

            etapa = etapas_pipedrive.get(titulo)

            if etapa and data_palestra < hoje and etapa not in ['Pós Entrega', '✅ Entregue']:
                print(f"⚠️ Negócio '{titulo}' com etapa '{etapa}' e Data Palestra em {data_palestra.strftime('%d/%m/%Y')}")

def validar_save_em_futuro_proximo(arquivo_ics):
    eventos = extrair_eventos_ics(arquivo_ics)
    hoje = datetime.today().date()
    um_mes = hoje + timedelta(days=30)

    for evento in eventos:
        titulo = evento.get('titulo')
        data_inicio = evento.get('inicio')
        print(f"📆🟢🟢🟢🟢 EVENTO {titulo} - {data_inicio}")
        if titulo and data_inicio:
            if titulo.startswith("SAVE"):
                if hoje <= data_inicio <= um_mes:
                    print(f"⚠️ Atenção evento SAVE próximo na data {data_inicio.strftime('%d/%b/%Y')} - fazer FUP")




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script para criação de pastas no Google Drive")
    parser.add_argument("--criarPastasDrive", action="store_true", help="Ativa a criação de pastas no Google Drive")
    args = parser.parse_args()
    if args.criarPastasDrive:
        print("ℹ️ Modo --criarPastasDrive ativado")
    else:
        print("ℹ️ Pastas no drive não são criadas. Use --criarPastasDrive para criar.")

    # Exemplo de uso
    diretorio_base = "/Users/fabiopereira/Library/CloudStorage/GoogleDrive-fabiopereira.me@gmail.com/My Drive/NCD Equipe Fabio Nudge - Estagio e Outros/🎤💰🛎️ BFN Business Fabio Nudge/Negocios/🛎️Pipe/🛎️ 2025 Pipe Negocios"
    negocios_pipedrive_arquivo = encontrar_arquivo_mais_recente("/Users/fabiopereira/Downloads", "deals-", ".csv")
    negocios_sheet_arquivo = encontrar_arquivo_mais_recente("/Users/fabiopereira/Downloads", "NegociosBFNBusinessFabioNudge", ".csv")
    arquivo_agenda_ics = encontrar_arquivo_mais_recente("/Users/fabiopereira/Downloads", "fabio", ".ics")
    print("----------- Processando Pastas dos Negócios -----------")
    processar_pastas(negocios_pipedrive_arquivo, diretorio_base, args)
    print("----------- Validando que Negócios tem suas pastas no Drive -----------")
    validar_que_negocios_tem_pastas(negocios_pipedrive_arquivo, diretorio_base)
    print("----------- Validando Inconsistências -----------")
    validar_inconsistencias(negocios_pipedrive_arquivo, diretorio_base, negocios_sheet_arquivo)
    print("----------- validar_que_negocios_tem_save_na_agenda -----------")
    validar_que_negocios_tem_save_na_agenda(negocios_pipedrive_arquivo, arquivo_agenda_ics)

    print("----------- validar_pos_entrega_para_data_palestra_no_passado -----------")
    validar_pos_entrega_para_data_palestra_no_passado(negocios_pipedrive_arquivo, negocios_sheet_arquivo)


    # print("----------- validar_save_em_futuro_proximo -----------")
    # validar_save_em_futuro_proximo(arquivo_agenda_ics)
