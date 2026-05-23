@echo off
setlocal

set "SRC=%~dp0"

for /d %%S in ("%SRC%*") do (
    if /i not "%%~nxS"==".git" (
        if exist "%USERPROFILE%\.agents\skills\" (
            robocopy "%%S" "%USERPROFILE%\.agents\skills\%%~nxS" /E /IS /IT >nul
        )
        if exist "%USERPROFILE%\.claude\skills\" (
            robocopy "%%S" "%USERPROFILE%\.claude\skills\%%~nxS" /E /IS /IT >nul
        )
        echo %%~nxS
    )
)

echo Done.
