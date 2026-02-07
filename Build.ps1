# =================================================================================
# CONFIGURACAO INICIAL
# =================================================================================
# Define que o script deve parar no primeiro erro. Muito mais seguro.
$ErrorActionPreference = "Stop"

# Define o diretorio de trabalho para a pasta onde o script esta localizado.
try {
    Set-Location -Path $PSScriptRoot
    Write-Host "Diretorio de trabalho definido para: $(Get-Location)" -ForegroundColor Green
} catch {
    Write-Host "ERRO: Nao foi possivel determinar a pasta do script. Saindo." -ForegroundColor Red
    exit
}

# Define o numero maximo de tarefas a serem executadas em paralelo.
# Um bom valor padrao e o numero de nucleos logicos do processador.
$throttleLimit = [System.Environment]::ProcessorCount
Write-Host "Executando tarefas em paralelo com um limite de $throttleLimit processos simultaneos." -ForegroundColor Cyan

# =================================================================================
# ETAPA 1: Executar P5S_Teste.exe nos arquivos .bin da pasta BIN (EM PARALELO)
# =================================================================================
Write-Host "`n[ETAPA 1 de 8] Executando P5S_Teste.exe em todos os arquivos .bin da pasta BIN (em paralelo)..."
Get-ChildItem -Path "BIN\*.bin" | ForEach-Object -Parallel {
    # NOTA: A saida do Write-Host pode ficar embaralhada por ser de varios processos.
    Write-Host "Iniciando processamento de: $($_.FullName)"
    
    # O '&' e necessario para executar o comando dentro do bloco de script paralelo.
    & ".\P5S_Teste.exe" $_.FullName
    
} -ThrottleLimit $throttleLimit
Write-Host "Etapa 1 concluida. Todos os processos paralelos terminaram." -ForegroundColor Green

# =================================================================================
# ETAPA 2: Executar o script Python
# =================================================================================
Write-Host "`n[ETAPA 2 de 8] Executando o script Python 'MainImp.py'..."
& python "MainImp.py"
Write-Host "Etapa 2 concluida." -ForegroundColor Green

# =================================================================================
# ETAPA 3: Copiar arquivos .csv ESPECIFICOS da pasta "Text" para a pasta BIN
# =================================================================================
Write-Host "`n[ETAPA 3 de 8] Copiando arquivos .csv especificos da pasta 'Text' para a pasta BIN..."
$csvFilesToCopy = @('0', '8', '16', '24', '32', '40', '48', '56', '64', '80', '88', '96')

foreach ($fileName in $csvFilesToCopy) {
    $sourcePath = "Text\$fileName.csv"
    if (Test-Path $sourcePath) {
        Write-Host "Copiando $sourcePath para a pasta BIN..."
        Copy-Item -Path $sourcePath -Destination "BIN\" -Force
    } else {
        Write-Host "AVISO: O arquivo $sourcePath nao foi encontrado e sera ignorado." -ForegroundColor Yellow
    }
}
Write-Host "Etapa 3 concluida." -ForegroundColor Green

# =================================================================================
# ETAPA 4: Executar P5S_Teste.exe nos arquivos .csv da pasta BIN (EM PARALELO)
# =================================================================================
Write-Host "`n[ETAPA 4 de 8] Executando P5S_Teste.exe em todos os arquivos .csv da pasta BIN (em paralelo)..."
Get-ChildItem -Path "BIN\*.csv" | ForEach-Object -Parallel {
    Write-Host "Iniciando processamento de: $($_.FullName)"
    & ".\P5S_Teste.exe" $_.FullName
} -ThrottleLimit $throttleLimit
Write-Host "Etapa 4 concluida. Todos os processos paralelos terminaram." -ForegroundColor Green

# =================================================================================
# ETAPA 5: Mover e renomear os arquivos .rebuilt.bin
# =================================================================================
Write-Host "`n[ETAPA 5 de 8] Movendo e renomeando arquivos .rebuilt.bin para a pasta Rebuilt..."
if (-not (Test-Path -Path "Rebuilt")) {
    New-Item -Path "Rebuilt" -ItemType Directory | Out-Null
}

Get-ChildItem -Path "BIN\*.rebuilt.bin" | ForEach-Object {
    $newName = $_.BaseName -replace '\.rebuilt', ''
    $destinationPath = "Rebuilt\$newName.bin"
    Write-Host "Movendo $($_.Name) para $destinationPath"
    Move-Item -Path $_.FullName -Destination $destinationPath -Force
}
Write-Host "Etapa 5 concluida." -ForegroundColor Green

# =================================================================================
# ETAPA 6: Copiar arquivos LINKDATA
# =================================================================================
Write-Host "`n[ETAPA 6 de 8] Criando copias de trabalho dos arquivos LINKDATA..."
Copy-Item -Path "LINKDATA_Original.BIN" -Destination "LINKDATA.BIN" -Force
Copy-Item -Path "LINKDATA_Original.IDX" -Destination "LINKDATA.IDX" -Force
Write-Host "Etapa 6 concluida." -ForegroundColor Green

# =================================================================================
# ETAPA 7: Injetar arquivos da pasta Rebuilt em LINKDATA.BIN (SEQUENCIALMENTE)
# =================================================================================
Write-Host "`n[ETAPA 7 de 8] Injetando arquivos da pasta Rebuilt em LINKDATA.BIN (um por um)..."
# AVISO: Esta operacao e executada sequencialmente (nao em paralelo) para evitar
# corromper o arquivo LINKDATA.BIN, ja que cada execucao o modifica.

# Coleta a lista de arquivos .bin para injetar.
$filesToInject = Get-ChildItem -Path "Rebuilt" -Filter "*.bin" -File

if ($filesToInject.Count -gt 0) {
    # Loop para executar o comando para CADA arquivo, um de cada vez.
    foreach ($file in $filesToInject) {
        Write-Host "Injetando arquivo: $($file.FullName)"
        
        # Executa o comando para o arquivo atual.
        & ".\LDP5S.exe" -inject "LINKDATA.BIN" $file.FullName "-Enc"
    }
    
    Write-Host "Etapa 7 concluida." -ForegroundColor Green
} else {
    Write-Host "AVISO: Nenhum arquivo .bin encontrado na pasta 'Rebuilt'. Etapa 7 ignorada." -ForegroundColor Yellow
}


# =================================================================================
# ETAPA 8: Limpeza
# =================================================================================
Write-Host "`n[ETAPA 8 de 8] Limpando arquivos temporarios..."
Get-ChildItem -Path "BIN\*.csv" | Remove-Item
Write-Host "Etapa 8 concluida." -ForegroundColor Green

# =================================================================================
# FINALIZACAO
# =================================================================================
Write-Host "`n============================" -ForegroundColor Cyan
Write-Host "Processo finalizado com sucesso!" -ForegroundColor Cyan
Write-Host "============================" -ForegroundColor Cyan
Write-Host ""
Pause