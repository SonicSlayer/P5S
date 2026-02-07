import os
import csv

# --- Configuração ---
# Pasta onde os arquivos CSV originais (numerados) estão.
PASTA_DOS_ARQUIVOS_ORIGINAIS = 'BIN'

# Arquivo CSV que contém a coluna "traduzido" e os IDs.
ARQUIVO_COM_TRADUCOES = 'Text\TheNewMain.csv'
# --------------------


def carregar_traducoes(caminho_arquivo_traducoes):
    """
    Lê o arquivo de traduções e o organiza em um dicionário para fácil acesso.
    Estrutura: {'nome_do_arquivo.csv': {'sheet_id': 'texto traduzido', ...}}
    """
    dados_traducao = {}
    try:
        with open(caminho_arquivo_traducoes, 'r', newline='', encoding='utf-8') as infile:
            leitor = csv.DictReader(infile)
            for linha in leitor:
                nome_arquivo = linha.get('NomeDoArquivo')
                sheet_id = linha.get('sheet_ID')
                texto_traduzido = linha.get('traduzido')

                # Adiciona apenas se houver um texto traduzido para processar
                if nome_arquivo and sheet_id and texto_traduzido:
                    if nome_arquivo not in dados_traducao:
                        dados_traducao[nome_arquivo] = {}
                    dados_traducao[nome_arquivo][sheet_id] = texto_traduzido
        
        print(f"Traduções carregadas com sucesso do arquivo '{caminho_arquivo_traducoes}'.")
        return dados_traducao
    except FileNotFoundError:
        print(f"ERRO: O arquivo de traduções '{caminho_arquivo_traducoes}' não foi encontrado.")
        return None
    except Exception as e:
        print(f"ERRO ao ler o arquivo de traduções: {e}")
        return None

def atualizar_arquivos_originais(pasta_originais, dados_traducao):
    """
    Percorre os arquivos CSV originais e atualiza a coluna 'string' com base nos dados de tradução.
    """
    if not os.path.isdir(pasta_originais):
        print(f"ERRO: A pasta com os arquivos originais '{pasta_originais}' não foi encontrada.")
        return

    print("\nIniciando a atualização dos arquivos originais...")
    
    # Itera sobre cada arquivo que tem tradução disponível
    for nome_arquivo, traducoes_neste_arquivo in dados_traducao.items():
        caminho_arquivo_original = os.path.join(pasta_originais, nome_arquivo)

        if not os.path.exists(caminho_arquivo_original):
            print(f"- AVISO: Arquivo '{nome_arquivo}' listado nas traduções não foi encontrado na pasta de originais. Pulando.")
            continue

        linhas_atualizadas = []
        cabecalho = []
        arquivo_modificado = False

        try:
            # Primeiro, lê o arquivo original inteiro na memória
            with open(caminho_arquivo_original, 'r', newline='', encoding='utf-8-sig') as infile:
                leitor = csv.DictReader(infile)
                cabecalho = leitor.fieldnames
                
                # Garante que 'string' e 'sheet_id' existem no arquivo original
                if not cabecalho or 'string' not in cabecalho or 'sheet_id' not in cabecalho:
                     print(f"- ERRO: Arquivo '{nome_arquivo}' não tem o formato esperado (falta 'string' ou 'sheet_id'). Pulando.")
                     continue

                for linha in leitor:
                    sheet_id_original = linha.get('sheet_id')
                    # Verifica se existe uma tradução para este sheet_id
                    if sheet_id_original in traducoes_neste_arquivo:
                        texto_antigo = linha['string']
                        texto_novo = traducoes_neste_arquivo[sheet_id_original]
                        linha['string'] = texto_novo # Atualiza o valor na coluna 'string'
                        arquivo_modificado = True
                    
                    linhas_atualizadas.append(linha)
            
            # Se alguma modificação foi feita, reescreve o arquivo original
            if arquivo_modificado:
                with open(caminho_arquivo_original, 'w', newline='', encoding='utf-8') as outfile:
                    escritor = csv.DictWriter(outfile, fieldnames=cabecalho)
                    escritor.writeheader()
                    escritor.writerows(linhas_atualizadas)
                print(f"- Arquivo '{nome_arquivo}' foi atualizado com sucesso.")
            else:
                print(f"- Nenhuma tradução correspondente encontrada para o arquivo '{nome_arquivo}'. Nenhum alteração feita.")

        except Exception as e:
            print(f"- ERRO ao processar o arquivo '{nome_arquivo}': {e}")
            
    print("\nProcesso de atualização concluído.")


# --- Execução Principal ---
if __name__ == "__main__":
    # Carrega os dados do arquivo de traduções
    traducoes = carregar_traducoes(ARQUIVO_COM_TRADUCOES)

    # Se as traduções foram carregadas, atualiza os arquivos
    if traducoes:
        atualizar_arquivos_originais(PASTA_DOS_ARQUIVOS_ORIGINAIS, traducoes)