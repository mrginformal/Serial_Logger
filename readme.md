# Test_Serial_Logger

## How to install:
1. Download this GitHub repoas zip and all of its contents to your local computer(only works on Linux and windows based systems for now)
2. Ensure the latest version of python3 is installed on your machine.       https://www.python.org/downloads/
Note: don't forget to add python to PATH during the installation process (there will be a little check box at the bottom of the install window at one point).
3. Ensure you have the lastest FTDI USB to Serial adapter driver for your cable, else the device will not be detected.(currently doesn't work with silabs chips)
I have had better luck not using the universal and instead using the VCP driver.
4. Install pip.   https://www.geeksforgeeks.org/how-to-install-pip-on-windows/
5. Use pip to run the following command:

```
 pip install -r /path/to/requirments.txt
```

## How to Make a Cable

To everyone that'll be involved in the Yeti 6G project, you'll need your own serial to USB converter, much like the one I showed at the training earlier this week. I have the converter PCBs at my desk, so the only part you'll need aside from that is a male USB to bare wire cable. You will need the D+ D- pins, so the USB to APP adapters will NOT work. However, an old USB mini/USB micro cable will work. With the bare wires exposed, you'll only need the black, white, and baja blast™ green colored cables. You can trim the red one back as we will not be using it. You will then solder these wires to the pins of the serial converter according to the picture below.

<img src="images\serial_logger_pic1.PNG" alt="Converter" title="Converter">

Once this is done, and is tested to confirm that it works, you should then hot glue for strain relief and to make sure these connections do not desolder or snap off. 

Note: Ensure that the switch is only ever used in the "5V" position. NOT the "3.3V" position. You can hot glue this part too if you'd like. We have a bunch of fun colors to help track whose is whose and to add a little flare and sass into your test equipment

## How to use

First connect the cable to the yeti you wish to log from, it should have PCU Firmware at or above 5.12. Turn on the port, then hold it until the usb light begins to blink, this means data is being sent. 
You can now launch the script in what ever way you like. You will be asked for the filename you wish to save the data as, then you will select the parameters you wish to display(all parameters are logged dispite selections). Click Continue and data will begin to appear in the terminal as it is recieved. This will run until you end the program with a keyboard interrupt. This is done by preccing control + c for windows and command + c for mac. 