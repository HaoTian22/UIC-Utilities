@echo off
setlocal EnableDelayedExpansion

set retry_count=0
set max_retries=3
set retry_enabled=1
set log_file=D:\auto_connect\wifi.log
set interval=60
set interval_reattempt=15
set "interfaceName=WLAN"

:check_network

for /f "tokens=1,2,3*" %%x in ('netsh interface ipv4 show config name^="!interfaceName!" ^| findstr /C:"Default Gateway"') do (
    set "wlan_gateway=%%z"
    REM 清除前导空格
    set "wlan_gateway=!wlan_gateway: =!"
)

echo Try connecting !wlan_gateway!
ping !wlan_gateway! -n 1 -w 1000 >nul
if %errorlevel% neq 0 (
    if !retry_enabled! equ 1 (
        if !retry_count! lss !max_retries! (
            set /a retry_count+=1
            echo Network connection failed, attempting to reconnect...
            netsh interface set interface name="WLAN" admin=disabled
            timeout 2 >nul
            netsh interface set interface name="WLAN" admin=enabled
            timeout /t %interval_reattempt% >nul
            goto :check_network
        ) else (
            echo Maximum attempts reached. Disabling Wi-Fi restart.
            set retry_enabled=0
        )
    )
) else (
    echo Internet connected
    set retry_count=0
    set retry_enabled=1
)

timeout /t %interval% /nobreak >nul
goto :check_network