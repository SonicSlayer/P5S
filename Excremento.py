import os
import csv

def unificar_csvs_corrigido(pasta_entrada, arquivo_saida):
    """
    Unifica dados de múltiplos arquivos CSV em um único arquivo, de forma mais robusta.

    Lê todos os arquivos .csv da 'pasta_entrada'. Se um arquivo contiver
    as colunas 'string' e 'sheet_id' (ignorando maiúsculas/minúsculas),
    seus dados são extraídos e adicionados ao 'arquivo_saida'.
    Usa a codificação 'utf-8-sig' para compatibilidade com BOM.

    Args:
        pasta_entrada (str): O caminho para la pasta contendo os arquivos CSV.
        arquivo_saida (str): O caminho para o arquivo CSV de saída unificado.
    """
    cabecalho_saida = ['NomeDoArquivo', 'string', 'sheet_ID']

    with open(arquivo_saida, 'w', newline='', encoding='utf-8') as outfile:
        escritor = csv.writer(outfile)
        escritor.writerow(cabecalho_saida)

        if not os.path.exists(pasta_entrada):
            print(f"ERRO: A pasta de entrada '{pasta_entrada}' não existe.")
            return

        for nome_arquivo in os.listdir(pasta_entrada):
            if nome_arquivo.lower().endswith('.csv'):
                caminho_arquivo = os.path.join(pasta_entrada, nome_arquivo)

                try:
                    # Usar 'utf-8-sig' para remover o BOM (Byte Order Mark) invisível
                    with open(caminho_arquivo, 'r', newline='', encoding='utf-8-sig') as infile:
                        leitor = csv.DictReader(infile)
                        cabecalho_entrada = leitor.fieldnames

                        # Pula arquivos vazios ou sem cabeçalho
                        if not cabecalho_entrada:
                            print(f"Arquivo ignorado (vazio ou sem cabeçalho): {nome_arquivo}")
                            continue
                        
                        # Para diagnóstico: mostra os cabeçalhos como o script os vê
                        print(f"Verificando arquivo: '{nome_arquivo}'. Cabeçalhos detectados: {cabecalho_entrada}")

                        # Converte os cabeçalhos para minúsculas para verificação
                        cabecalho_lower = [h.lower().strip() for h in cabecalho_entrada]

                        if 'string' in cabecalho_lower and 'sheet_id' in cabecalho_lower:
                            # Encontra os nomes originais das colunas para usar como chaves
                            string_key = cabecalho_entrada[cabecalho_lower.index('string')]
                            sheet_id_key = cabecalho_entrada[cabecalho_lower.index('sheet_id')]
                            
                            print(f"-> Processando arquivo: {nome_arquivo}")
                            for linha in leitor:
                                string_data = linha.get(string_key, '')
                                sheet_id_data = linha.get(sheet_id_key, '')
                                escritor.writerow([nome_arquivo, string_data, sheet_id_data])
                        else:
                            print(f"-> Arquivo ignorado (cabeçalho não contém 'string' e 'sheet_id'): {nome_arquivo}")

                except Exception as e:
                    print(f"Erro ao processar o arquivo {nome_arquivo}: {e}")

    print(f"\nProcesso concluído! Os dados foram salvos em '{arquivo_saida}'")

# --- Configuração ---
# Pasta onde os arquivos CSV de entrada estão localizados.
PASTA_DOS_CSVS = 'arquivos_csv'
# Nome do arquivo CSV que será gerado.
ARQUIVO_FINAL = 'resultado_unificado.csv'
# --------------------

# Chama a função principal para iniciar o processo
unificar_csvs_corrigido(PASTA_DOS_CSVS, ARQUIVO_FINAL)