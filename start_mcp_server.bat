@echo off
setlocal

echo ========================================
echo Iniciando MCP Server
echo ========================================
echo.

echo Ativando ambiente Conda: exemplo_api_mcp
call conda activate exemplo_api_mcp
if errorlevel 1 (
    echo ERRO: nao foi possivel ativar o ambiente 'exemplo_api_mcp'.
    pause
    exit /b 1
)

echo.
echo Iniciando servidor MCP em modo streamable-http...
python run_mcp_server.py

echo.
pause
