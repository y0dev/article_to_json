@echo off

echo Building posts
python ./main.py --os "pc" --action "single" 

echo Running pug and cleaning up html
pug -P ./output/pug -o ./output/html
@REM pug -w ./output/pug -o ./output/html/latest
@REM timeout /t 5
@REM Won't run since pug is continous
@REM python ./clean_html_pages.py