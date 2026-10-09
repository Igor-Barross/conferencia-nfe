@echo off
setlocal

REM Acentos e caracteres do rich corretamente no terminal
chcp 65001 >nul
set PYTHONUTF8=1
set "CODIGO=0"

REM Vai para a pasta do projeto (onde este .bat esta)
pushd "%~dp0"
if errorlevel 1 (
    echo [ERRO] Nao foi possivel acessar a pasta do projeto.
    set "CODIGO=1"
    goto :fim
)

REM Usa o Python do ambiente virtual (.env); se nao existir, usa o do sistema
if exist ".env\Scripts\python.exe" (
    set "PYTHON=.env\Scripts\python.exe"
) else (
    set "PYTHON=python"
)

"%PYTHON%" --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao encontrado. Crie o ambiente virtual ou instale o Python.
    set "CODIGO=1"
    goto :fim
)

if not exist "src\main.py" (
    echo [ERRO] Arquivo src\main.py nao encontrado. Deixe este .bat na raiz do projeto.
    set "CODIGO=1"
    goto :fim
)

REM Executa o programa
"%PYTHON%" "src\main.py"
set "CODIGO=%errorlevel%"

:fim
echo.
if "%CODIGO%"=="0" (
    echo Execucao concluida.
) else (
    echo A execucao terminou com erro, codigo %CODIGO%. Leia a mensagem acima.
)
echo.
echo Pressione qualquer tecla para fechar esta janela...
pause >nul
popd
exit /b %CODIGO%