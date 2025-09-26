import os
import sys

def criar_pasta_novo_negocio(nome_negocio):
    subpastas = ['briefing', 'contrato', 'docs', 'logistica', 'proposta']
    
    # Criar pasta principal
    if not os.path.exists(nome_negocio):
        os.mkdir(nome_negocio)
        print(f"📁 Pasta criada: {nome_negocio}")
    else:
        print(f"⚠️ Pasta '{nome_negocio}' já existe.")

    # Mudar para a pasta criada
    os.chdir(nome_negocio)

    # Criar subpastas
    for subpasta in subpastas:
        if not os.path.exists(subpasta):
            os.mkdir(subpasta)
            print(f"  └── Subpasta criada: {subpasta}")
        else:
            print(f"  ⚠️ Subpasta '{subpasta}' já existe.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python criar-pasta-novo-negocio.py <nome_da_pasta>")
    else:
        nome_pasta = sys.argv[1]
        criar_pasta_novo_negocio(nome_pasta)
