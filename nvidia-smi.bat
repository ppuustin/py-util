:: on other windows
:: set nvsmi="C:\Program Files\NVIDIA Corporation\NVSMI"

:: on windows 10
set nvsmi="C:\Windows\System32"

FOR /L %%y IN (0, 1, 50) DO (
  %nvsmi%\nvidia-smi.exe 
  timeout /t 6 /nobreak > NUL  
)

PAUSE
