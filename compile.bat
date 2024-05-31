@echo off
chcp 65001
title Compiling exe...
pyinstaller --onefile --noconsole --uac-admin ApocalypseClient.py
cls
echo Build saved in dist/.
pause
exit
