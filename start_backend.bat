@echo off
setlocal

echo ========================================
echo Iniciando Backend - API FastAPI
echo ========================================
echo.

echo Ativando ambiente Conda: exemplo_api_mcp
call conda activate exemplo_api_mcp
if errorlevel 1 (
    echo.
    echo ERRO: nao foi possivel ativar o ambiente 'exemplo_api_mcp'.
    echo Certifique-se de que ele existe:
    echo   conda create -n exemplo_api_mcp python=3.11 -y
    pause
    exit /b 1
)

echo.
echo Ambiente pronto. Inicializando API em http://localhost:8000 ...
python run_api.py

if errorlevel 1 (
    echo.
    echo A execucao da API terminou com erro (%errorlevel%).
) else (
    echo.
    echo API finalizada.
)

echo.
pause
