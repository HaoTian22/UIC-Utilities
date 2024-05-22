# AutoRestartWIFI

[Here is a link to the bat](./AutoRestartWIFI.bat)

This bat script tackles the problem of "No Internet Connection" due to hardware and Windows problems.  
It allows the PC to attempt to reconnect Wi-Fi, boosting experience of remote control.  

## Summary of Online Results

[Some people](https://www.zhihu.com/question/27914005/answer/2470199887) say that it could be an issue with the computer's WiFi adapter driver, and that you need to replace the driver.

[Others](https://www.zhihu.com/question/28422159) suggest that there might be interference between the USB and WiFi, so you need to place the USB devices and WiFi module farther apart.

There are also some people who focus on the registry, which I don't really understand.

Among these solutions, some might genuinely solve the problem, but the trigger condition for the disconnection is too random. I don't know which solution is truly effective, and verifying them would also take time.

So, I thought of a simple solution—write a script to automatically disconnect and reconnect the WiFi when a disconnection is detected. This can be used as a temporary workaround, and I can later analyze the script's log to see what caused the disconnection.

## Script logic

1. Check whether the network device is enabled. If not, enable it.
2. Retrieve the local network gateway address using the ipconfig /all command.
3. If the gateway address cannot be detected, wait for 60 seconds and go back to step 1.
4. If the gateway address is detected, `ping` the gateway to check its availability.
5. If the gateway responds to the ping, wait for 60 seconds and go back to step 1 to check again.
6. If the gateway does not respond to the ping, attempt to toggle the network device (Wi-Fi) and go back to step 1.
7. If the gateway still does not respond after three consecutive attempts, skip steps 4 to 6 in the next round until a response is received.

## How to use

1. Download the [batch file](./AutoRestartWIFI.bat)
2. Modify configuration (Line 4-20) in the script if necessary
3. Double click it to run

To use this script efficiently, you can implement some extra operations:

1. Open `Task Scheduler`, create a basic task
2. Choose `trigger` as `When the computer starts`
3. Choose `Start a program` action and select the local location of this script.  
4. **Follow the screenshots below to further configure the script**  

![image](https://github.com/HaoTian22/UIC-Utilities/assets/48882584/d2390d98-ccda-4b71-8d48-b968783bbafd)

![image](https://github.com/HaoTian22/UIC-Utilities/assets/48882584/6a4f966d-a60a-4d43-9965-65f3344afcf1)

![image](https://github.com/HaoTian22/UIC-Utilities/assets/48882584/2f7e70cb-5b71-497b-a962-e40ef69655d6)

## More

If you want a script with simliar funtions in Powershell, you can also try [this](https://github.com/doodlehuang/keep_wifi_connection)
