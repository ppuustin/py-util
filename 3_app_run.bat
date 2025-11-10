set pyv=%UserProfile%\AppData\Local\Programs\Python\Python39\
set pyt=%pyv%\python.exe
:: set pyt="%~dp0\venv\Scripts\python.exe"
:: set pyi="%~dp0\venv\Scripts\pyinstaller.exe"
:: set pip="%penv%\Scripts\pip.exe"

:: call set_python.bat
:: %pyt% -c "import tensorflow as tf;print(tf.__version__)" && ( pause ) || ( pause )
:: %pyt% -c "import torch;print(torch.__version__);print(torch.version.cuda);print(torch.cuda.is_available())" && ( pause ) || ( pause )
:: %pyt% -c "" && ( pause ) || ( pause )

:: set mname=fi_core_news_sm
:: set vers=3.5.0
:: set model=https://github.com/explosion/spacy-models/releases/download/%mname%-%vers%/%mname%-%vers%-py3-none-any.whl
:: %pip% install --no-deps %model% && ( pause ) || ( pause )
:: %pyt% -c "import spacy;spacy.load('%mname%').to_disk('src/input/%mname%')" && ( pause ) || ( pause )

set main=%~dp0\main.py 
:: set exe=%~dp0\main.exe 

:: %exe% && ( pause ) || ( pause )
:: %pyi% %main% --onefile --clean --noconfirm --specpath build --distpath . && ( pause ) || ( pause )
%pyt% %main% && ( pause ) || ( pause )
