set CURRENT_USER=%USERNAME%

if /I "%CURRENT_USER%"=="StarPetsAdmin1" (
    set USER_DIR=Administrator
) else (
    set USER_DIR=%CURRENT_USER%
)

set dir="C:\Users\%USER_DIR%\Desktop\cv-preparation-stat"

cd /d %dir%

python -m venv venv
call "venv\Scripts\activate.bat"
pip install -r requirements.txt

python "__main__.py"

pause