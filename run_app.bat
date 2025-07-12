@echo off
cd /d %~dp0
python gui.py
python -m streamlit run gui.py
pause
