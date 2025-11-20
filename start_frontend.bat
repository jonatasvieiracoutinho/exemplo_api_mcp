@echo off
setlocal

echo ========================================
echo Iniciando Frontend - React
echo ========================================
echo(

cd /d "%~dp0frontend"
if errorlevel 1 (
    echo ERRO: pasta frontend nao encontrada.
    pause
    exit /b 1
)

echo Verificando dependencias do npm...
if not exist "node_modules" (
    goto INSTALL_DEPENDENCIES
)
goto START_FRONTEND

:INSTALL_DEPENDENCIES
echo node_modules nao encontrado. Instalando dependencias...
call npm install
if errorlevel 1 (
    echo(
    echo ERRO: falha ao instalar dependencias npm.
    echo Verifique se Node.js e npm estao instalados (node --version / npm --version).
    pause
    exit /b 1
)

:START_FRONTEND
echo(
echo Iniciando servidor: npm run dev (porta padrao 5173)
echo Pressione Ctrl+C para encerrar.
echo(
call npm run dev

echo(
pause
