echo Create virtual environment 
python -m venv venv
call venv\Scripts\activate

echo Install requirements
pip install -r requirements.txt

echo Execute pytest
pytest tests\

echo.
echo Tests End !!!
pause

REM deactivate