import tkinter as tk
from tkinter import filedialog
import re
import os

# Função para verificar se a linha contém pelo menos uma letra do alfabeto latino
def tem_letra_latina(texto):
    return bool(re.search('[a-zA-Z]', texto))

# Função principal
def processar_arquivos():
    # Abre o gerenciador de arquivos para selecionar os arquivos
    root = tk.Tk()
    root.withdraw()  # Esconde a janela principal do tkinter
    caminhos_arquivos = filedialog.askopenfilenames(
        title="Select text files.",
        filetypes=[("Text files", "*.txt"), ("Every file", "*.*")]
    )
    
    if not caminhos_arquivos:
        print("No file selected.")
        return

    # Define o nome do arquivo de saída unificado (.tsv)
    pasta = os.path.dirname(caminhos_arquivos[0])  # Usa a pasta do primeiro arquivo
    nome_saida = os.path.join(pasta, "Unification.tsv")
    
    # Lista para armazenar todas as linhas filtradas
    linhas_filtradas = []
    
    # Processa cada arquivo selecionado
    for caminho_arquivo in caminhos_arquivos:
        with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo_entrada:
            linhas = arquivo_entrada.readlines()
            
            # Itera pelas linhas com numeração
            for numero_linha, linha in enumerate(linhas, 1):
                linha_limpa = linha.strip()
                # Ignora a linha específica "[1b]Z"
                if linha_limpa == "[1b]Z":
                    continue
                # Verifica se tem letra latina
                if tem_letra_latina(linha_limpa):
                    # Adiciona na lista no formato desejado
                    linhas_filtradas.append(f"{os.path.basename(caminho_arquivo)}\t{numero_linha}\t{linha_limpa}")
    
    # Salva tudo em um único arquivo .tsv
    if linhas_filtradas:
        with open(nome_saida, 'w', encoding='utf-8') as arquivo_saida:
            arquivo_saida.write('\n'.join(linhas_filtradas))
        print(f"Saved as: {nome_saida}")
        print(f"Total of lines copied: {len(linhas_filtradas)}")
    else:
        print("No text found.")

# Executa o script
if __name__ == "__main__":
    processar_arquivos()