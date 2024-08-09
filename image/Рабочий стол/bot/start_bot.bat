@echo off
cd C:\Users\380674914614\Desktop\bot
:begin
echo launch bot2.py
py bot2.py
echo bot2.py kill session 10 second
timeout 10
echo restart bot2.py
goto begin
