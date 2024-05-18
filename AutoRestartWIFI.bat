@echo off
setlocal EnableDelayedExpansion

set retry_count=0
set max_retries=3
set retry_enabled=1
set log_file=D:\auto_connect\wifi.log
set interval=60
set interval_reattempt=15

:check_network

set "interfaceName=WLAN"
set "gatewayFound=false"
set "wlan_gateway="
set "gatewayDetected=false"

REM 使用 ipconfig /all 命令获取网络接口信息并逐行处理
for /f "tokens=*" %%i in ('ipconfig /all') do (
    set "line=%%i"

    REM 检查是否找到指定的网络接口
    echo !line! | findstr /C:"%interfaceName%" >nul && (
        set "gatewayFound=true"
    )

    REM 如果找到了匹配的接口，检查后续行是否包含 Default Gateway
    if "!gatewayFound!"=="true" (
        echo !line! | findstr /C:"Default Gateway" >nul && (
            for /f "tokens=2 delims=:" %%j in ("!line!") do (
                set "wlan_gateway=%%j"
                REM 清除前导空格
                set "wlan_gateway=!wlan_gateway: =!"
                echo WLAN Default Gateway: !wlan_gateway!
                set "gatewayFound=false"
                set "gatewayDetected=true"
            )
        )
    )
)

REM 检查是否找到了默认网关
REM 因为没连接任何网络的话，我即使重启网卡也是不会自动连上的
if "!gatewayDetected!"=="false" (
    echo No default gateway detected for %interfaceName%. The network may not be connected.
    timeout /t %interval% /nobreak >nul
    goto :check_network
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