import os
import csv
import shutil
import unicodedata

# Função principal
def processar_pastas(csv_path, base_dir):
    # Ler CSV e criar um dicionário {Título: Etapa}
    negocios = {}
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
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
                    print(f"🔲 Pasta {pasta} do negócio na Etapa: {etapa}")

if __name__ == "__main__":
    # Exemplo de uso
    diretorio_base = "/Users/fabiopereira/Library/CloudStorage/GoogleDrive-fabiopereira.me@gmail.com/My Drive/NCD Equipe Fabio Nudge - Estagio e Outros/🎤💰🛎️ BFN Business Fabio Nudge/Negocios/🛎️Pipe/🛎️ 2025 Pipe Negocios"
    csv_arquivo = "/Users/fabiopereira/Downloads/deals-21241211-21.csv"
    processar_pastas(csv_arquivo, diretorio_base)
