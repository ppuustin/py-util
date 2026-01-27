set name=venv
set penv=%~dp0\%name%

set pyt="%penv%\Scripts\python.exe"
set pip="%penv%\Scripts\pip.exe"

:: %pip% install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu117

:: set pkg=numpy
:: echo %PATH% && ( pause ) || ( pause )
:: %pyt% -V  && ( pause ) || ( pause )
:: %pip% show %pkg% && ( pause ) || ( pause )
:: %pip% uninstall %pkg% && ( pause ) || ( pause )
:: %pip% install --upgrade %pkg% && ( pause ) || ( pause )
%pip% install -r "%~dp0\requirements.txt" && ( pause ) || ( pause )

::%pyt% -c "import pkg_resources;pp=[str(p) for p in pkg_resources.working_set];pp.sort();[print(p) for p in pp]" && ( pause ) || ( pause )

