@echo off
REM Este batch file executa o script PowerShell usando o PowerShell 7 (pwsh.exe).

TITLE Construtor de Arquivos

REM Define o diretorio de trabalho para a pasta onde o .bat esta localizado.
cd /d "%~dp0"

echo Executando o script PowerShell 'Build.ps1' com PowerShell 7...
echo.

REM Executa o script usando o pwsh.exe (PowerShell 7+).
pwsh.exe -ExecutionPolicy Bypass -File "Build.ps1"

echo.
echo Pressione qualquer tecla para sair...
pause > nul