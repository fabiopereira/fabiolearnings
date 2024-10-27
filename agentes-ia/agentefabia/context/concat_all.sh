#!/bin/bash

# Nome do arquivo de saída
output_file="all-FabIA-data.txt"


echo "Apagando o arquivo de saída se ele já existir"
rm -f "$output_file"

echo "Concatenando todos os arquivos .txt do diretório atual e subdiretórios no arquivo de saída"
cat *.txt > "$output_file"

echo "Arquivos .txt concatenados em $output_file"

