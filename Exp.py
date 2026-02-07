import os
import csv
import re

def extrair_numero(filename):
    """
    Extrai o primeiro número encontrado no nome de um arquivo.
    Usado como chave para ordenação numérica.
    Retorna 0 se nenhum número for encontrado.
    """
    match = re.search(r'(\d+)', filename)
    if match:
        return int(match.group(1))
    return 0

def unificar_csv_final(pasta_entrada, arquivo_saida):
    """
    Unifica, filtra e ordena dados de múltiplos arquivos CSV, incluindo a coluna 'unknown_1'.

    Primeiro, ordena os arquivos da 'pasta_entrada' numericamente.
    Depois, para cada arquivo que contiver 'string', 'sheet_id' e 'unknown_1',
    extrai as linhas onde a coluna 'string' contém caracteres do alfabeto latino.
    Os dados filtrados (NomeDoArquivo, string, unknown_1, sheet_ID) são salvos no 'arquivo_saida'.

    Args:
        pasta_entrada (str): O caminho para a pasta contendo os arquivos CSV.
        arquivo_saida (str): O caminho para o arquivo CSV de saída unificado.
    """
    # --- CABEÇALHO DE SAÍDA ATUALIZADO ---
    cabecalho_saida = ['NomeDoArquivo', 'string', 'unknown_1', 'sheet_ID']

    if not os.path.exists(pasta_entrada):
        print(f"ERRO: A pasta de entrada '{pasta_entrada}' não existe.")
        return

    arquivos_csv = [f for f in os.listdir(pasta_entrada) if f.lower().endswith('.csv')]
    arquivos_csv_ordenados = sorted(arquivos_csv, key=extrair_numero)
    
    print("Arquivos serão processados na seguinte ordem:")
    print(arquivos_csv_ordenados)
    print("-" * 30)

    with open(arquivo_saida, 'w', newline='', encoding='utf-8') as outfile:
        escritor = csv.writer(outfile)
        escritor.writerow(cabecalho_saida)

        for nome_arquivo in arquivos_csv_ordenados:
            caminho_arquivo = os.path.join(pasta_entrada, nome_arquivo)
            try:
                with open(caminho_arquivo, 'r', newline='', encoding='utf-8-sig') as infile:
                    leitor = csv.DictReader(infile)
                    cabecalho_entrada = leitor.fieldnames

                    if not cabecalho_entrada:
                        print(f"Arquivo ignorado (vazio): {nome_arquivo}")
                        continue
                    
                    cabecalho_lower = [h.lower().strip() for h in cabecalho_entrada]

                    # --- VERIFICAÇÃO DE CABEÇALHO ATUALIZADA ---
                    if 'string' in cabecalho_lower and 'sheet_id' in cabecalho_lower and 'unknown_1' in cabecalho_lower:
                        print(f"Processando arquivo: {nome_arquivo}")
                        
                        # Mapeia os nomes das colunas (ignorando maiúsculas/minúsculas)
                        string_key = cabecalho_entrada[cabecalho_lower.index('string')]
                        sheet_id_key = cabecalho_entrada[cabecalho_lower.index('sheet_id')]
                        unknown_1_key = cabecalho_entrada[cabecalho_lower.index('unknown_1')] # Nova chave
                        
                        for linha in leitor:
                            string_data = linha.get(string_key, '')
                            if re.search(r'[a-zA-Z]', string_data):
                                # --- EXTRAÇÃO E ESCRITA ATUALIZADAS ---
                                sheet_id_data = linha.get(sheet_id_key, '')
                                unknown_1_data = linha.get(unknown_1_key, '') # Extrai o novo dado
                                
                                # Escreve na nova ordem
                                escritor.writerow([nome_arquivo, string_data, unknown_1_data, sheet_id_data])
                    else:
                        print(f"Arquivo ignorado (cabeçalho inválido, falta 'string', 'sheet_id' ou 'unknown_1'): {nome_arquivo}")

            except Exception as e:
                print(f"Erro ao processar o arquivo {nome_arquivo}: {e}")

    print(f"\nProcesso concluído! Os dados foram salvos em '{arquivo_saida}'")


# --- Configuração ---
PASTA_DOS_CSVS = 'forgor'
ARQUIVO_FINAL = 'resultado_unificado.csv'
# --------------------

unificar_csv_final(PASTA_DOS_CSVS, ARQUIVO_FINAL)