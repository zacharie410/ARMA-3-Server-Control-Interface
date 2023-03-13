@echo off

set "keys_dir=E:\a3master\keys"
set "mods_dirs=E:\a3mods;D:\a3mods;G:\a3mods"

:menu
  echo.
  echo ====================
  echo ARMA 3 Server Commands
  echo ====================
  echo.
  echo 1. Start server
  echo 2. Stop server
  echo 3. Update mod keys
  echo 4. Exit
  echo.
  set /p choice=Enter your choice:

  if "%choice%"=="1" (
    echo Starting server...
    goto start_server
  ) else if "%choice%"=="2" (
    echo Stopping server...
    for /f "tokens=2" %%a in ('tasklist /nh /fi "imagename eq arma3server_x64.exe" /fo table') do taskkill /f /pid %%a
    echo Server stopped.
    goto menu
  ) else if "%choice%"=="3" (
    goto update_mod_keys
  ) else if "%choice%"=="4" (
    echo Exiting...
    exit
  ) else (
    echo Invalid choice. Please enter a valid choice.
    goto menu
  )


:update_mod_keys
  set "checked_dirs="
  rem clear all .bikey files from the keys folder
  echo Clearing old .bikey files from the keys folder...
  for %%i in ("%keys_dir%\*.bikey") do (
    if not "%%~nxi"=="a3.bikey" del "%%i"
  )

  echo Updating mod keys...
  for %%d in (%mods_dirs%) do (
    for /d %%e in ("%%~d\*") do (
      for /d %%i in ("%%~e\*") do (
        set "mods_dir=%%i"
        if not "!checked_dirs!"=="!checked_dirs:%%i;=!" (
          set "checked_dirs=!checked_dirs!%%i;"
          for %%f in ("%%i\*.bikey") do (
            set "bikey=%%~nxf"
            setlocal enabledelayedexpansion
            set "name=!bikey:~0,-6!"
            set "name=!name:@=!"
            set "name=!name:%=!"
            set "name=!name:!=!"
            copy "%%f" "%keys_dir%\"
            echo Copied file: "%%f" to "%keys_dir%\"
            endlocal
          )
        )
      )
    )
  )

  echo Mod keys updated.
  goto :menu

:start_server
  setlocal enabledelayedexpansion
  set "server_exe=E:\a3master\arma3server_x64.exe"
  set "server_params=-profiles=E:\a3profiles\server -ranking=E:\rankings\ranks.log -cfg=basic.cfg -malloc=system -port=2302 -config=CONFIG_server.cfg -loadMissionToMemory -limitFPS=100"

  set "mods="

  rem loop through the mods folders and add all subfolders to the mods parameter
    for %%d in (%mods_dirs%) do (
      for /d %%i in ("%%~d\*") do (
        set "mods_dir=%%~i"
        set "mods=!mods!;!mods_dir!"
      )
  )

  set "server_params=%server_params% -mod="%mods:~1%""
  start /high "" "%server_exe%" %server_params%
  endlocal
  goto menu
