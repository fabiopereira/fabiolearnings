import os
import csv
import shutil
import unicodedata

# Processar pastas de negócios
def processar_pastas(negocios_pipedrive_arquivo, base_dir):
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
        if os.path.isdir(pasta_path) and not pasta.startswith('ARCHIVE'):
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
                else:
                    print(f"✅ Pasta {pasta} do negócio na Etapa: {etapa} está no dir raiz")

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
                else:
                    print(f"✅ Negócio '{titulo}' com Etapa '{etapa}' está na NegociosSheet")



def encontrar_arquivo_CSV_mais_recente(diretorio, filtro_extensao=None):
    arquivos = []

    # Listar todos os arquivos no diretório
    for nome_arquivo in os.listdir(diretorio):
        caminho_arquivo = os.path.join(diretorio, nome_arquivo)
        
        # Filtrar apenas arquivos (não pastas)
        if os.path.isfile(caminho_arquivo):
            # Se houver filtro por extensão, aplica o filtro
            if filtro_extensao:
                if nome_arquivo.startswith(filtro_extensao) and nome_arquivo.endswith(".csv"):
                    arquivos.append(caminho_arquivo)
            else:
                arquivos.append(caminho_arquivo)

    if not arquivos:
        print("🛑🛑🛑 Nenhum arquivo encontrado com o filtro especificado.")
        return None

    # Ordenar os arquivos pela data de modificação (do mais antigo para o mais recente)
    arquivos.sort(key=lambda x: os.path.getmtime(x))

    # Retornar o mais recente
    return arquivos[-1]

if __name__ == "__main__":
    # Exemplo de uso
    diretorio_base = "/Users/fabiopereira/Library/CloudStorage/GoogleDrive-fabiopereira.me@gmail.com/My Drive/NCD Equipe Fabio Nudge - Estagio e Outros/🎤💰🛎️ BFN Business Fabio Nudge/Negocios/🛎️Pipe/🛎️ 2025 Pipe Negocios"
    negocios_pipedrive_arquivo = encontrar_arquivo_CSV_mais_recente("/Users/fabiopereira/Downloads", "deals-")
    print(f"📂 Processando arquivo mais recente: {negocios_pipedrive_arquivo}")
    negocios_sheet_arquivo = encontrar_arquivo_CSV_mais_recente("/Users/fabiopereira/Downloads", "Negócios BFN Business Fabio Nudge")
    print(f"📂 Processando arquivo mais recente: {negocios_sheet_arquivo}")
    print("----------- Processando Pastas dos Negócios -----------")
    processar_pastas(negocios_pipedrive_arquivo, diretorio_base)
    print("----------- Validando Inconsistências -----------")
    validar_inconsistencias(negocios_pipedrive_arquivo, diretorio_base, negocios_sheet_arquivo)
