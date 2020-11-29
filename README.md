![IOTA Workshop](https://i.ibb.co/q79SgmW/IOTA-WORKSHOP-BLACK.png)

# Video
Please watch the video demonstration here: https://youtu.be/LRsAu9jn_a0

# Statement of Purpose
Previous IOTA applications have shown transfer of digital goods, and electricity. This is the first project to have IOTA step into the material world by enabling people to use physical tools using IOTA. The details of this project offer the details on how to safely rent valuable and useful equipment to anyone through the use of a vending equipment chassis. 

The demand for rental equipment exists, [through an analysis I did on HomeDepot](https://docs.google.com/document/d/1urIHW2seTBf1eWDFGsHMb8kDok1n1w5KCycBOFp-prs/edit?usp=sharing), on a subset of basic handheld rental tools HomeDepot has a lower bound on revenue of 80 million dollars a year. The conclusion from this, is a non-profit, potentially operated by a DAO, can enter the market by offering tools as a service.

In most converations on automation, it brings up hard feelings of lost jobs. In this instance, to operate a business that offers tools and equipment, which are the instuments of labor, at the lowest cost possible by the implementation of automation, would enable new jobs through their own employment as entrepenurs. The cost and  availablity of specialized tools of manufacturing is the barrier to entry for new firms in a market. IOTA Workshop is the proof that this technology can offer the neccesities for anyone to start producing goods without having their wage cut by the employer and the owner of the capital.

Peter Kropotin, in *The Conquest of Bread*, vivdly depicts the destitute lives of workers born into a stratum unable to own their instruments of labour, "The shafts of the mine still bear on their rocky walls the marks made by the pick of workman who toiled to excavate them. The space between each prop in the underground galleries might be marked as a miner's grave; and who can tell what each of these graves has cost, in tears, in privitations, in unspeakable wretchedness to the family who depenen on the scanty wage of the worker cut off in his prime by fire-damp, rock-fall, or flood?"

To learn more about the ideology about behind the IOTA Workshop, I urge you to take a look at the [white paper](https://gist.github.com/Tsangares/6a6521ae66a4a4c75f5c55a15242ce13#file-iota_workshop-md).

# Content

Please view the [wiki](https://github.com/Tsangares/iotaworkshop/wiki) to see a list of the components and how to compile them together to replicate the IOTA Workshop proof of concept. To view the website and see the current go to https://iotaworkshop.gradstudent.me.

The following is a abstract on how this proof of concept operates. This project contains the logic involved with creaing a vending equipment serivce; fully autonomous and operated using the IOTA ledger. An e-paper display interfaces with the user to guiding them through depositing IOTA into an escrow account. This operates a servo that is pick proof to unlock a box that gives access to an tool which is the instrument of producion. When the user retuns the tool, an RFID sensor will detect and confirm the tool has been returned and will finish the escrow by returning the deposit on the tool. The servo then proceeds to lock the box, disabling people from trying to steal the tool inside. 

# IOTA Streams

This project uses iota streams to store the state of the chassis in the iota ledger and keep the prices and fees transparent. To view the log of the escrow from this project please visit: https://iotaworkshop.gradstudent.me/states


The current channel for this POC is: `0538eddf3842a62cc48f58d706245e3b987896de454da36576d81e32af62d90b0000000000000000:da3d2e69622ed8f730f2ddaa`

# Installation

First please check with the [wiki](https://github.com/Tsangares/iotaworkshop/wiki) on the parts you need and the how to wire the device, then you can proceed on installing the software.


To run this program you need to clone the repo or pull the `iotaworkshop.py` file, then install the dependencies,

    pip install iotaescrow servo_lock pibeep piepd rc522
    
You will also need `RPi.GPIO`, which because I was running an arch arm operation system I installed it using the arch aur repo using,

    yay -S python-raspberry-gpio
	
If you are using ubuntu orrasbian you can use,

    pip install RPi.GPIO


# Dependencies

All of the code used in this project is encapulsated into a easy to use pip package. Many of them have command line interfaces to use the tool and they can all be imported as a module to have enable advanced usage. The following project uses these packages that I built, each of which holds a general purpose beyond this project.

 - <a href="https://github.com/Tsangares/iotaescrow" target="_blank">iotaescrow</a>: A escrow implementation using IOTA.
 - <a href="https://github.com/Tsangares/servo_lock" target="_blank">servo_lock</a>: A general purpose, high level servo controller.
 - <a href="https://github.com/Tsangares/pibeep" target="_blank">pibeep</a>: A buzzer utility that offers a variety of sounds and enables tools to make any sound possible using buzzers.
 - <a href="https://github.com/Tsangares/piepd" target="_blank">piepd</a>: A e-paper controller that displays text or QR codes using any of the waveshare screens.
 - <a href="https://github.com/Tsangares/rc522" target="_blank">rc522</a>: An RFID sensor utility used to confirm and verify RFID tags for the rc522 sensor.

# Optional Dependencies

This project uses IOTA streams to publish the current state of the ledger. We used,

 - [iot2tangle Streams Http Gateway](https://github.com/iot2tangle/Streams-http-gateway): A rust lib that offers IOTA streams through an API.
 - [iot2tangle Keepy](https://github.com/iot2tangle/Keepy): A nodejs api that connects to the streams gateway and stores a copy of the streams in a mysql database.

With these two dependencies installed, when using the `iotaworkshop.py` if you set the `--keepy` argument, the escrow data will be stored in streams. The data we store from the escrow include:
 - `tool`: The name of the tool
 - `collateral`: The refundable collateral cost
 - `fee`: The non-refundable fee
 - `available`: Availability of the tool (if the tool is being used)
 - `verification`: The verification condition that is required for a refund of collateral
 - `esrow_address`: The escrow address
 - `deposit_address`: The deposit address
 - `status`: A string that represents the current status of the chassis
 
# CLI Examples
Here are a few examples on how to run the code through cli,

	#The following will request 1.01KIOTA as a deposit, take 10 IOTA as a fee for a hammer
    python iotaworkshop.py --collateral 1010 --fee 10 --name "hammer"
	
	#The following will implement iotastreams and store the state of the escrow in the ledger
	python iotaworkshop.py --collateral 105 --fee 5 --name "lock pick" --keepy http://192.168.1.100:3002
	

# Images of POC
Here is a video demonstation of the IOTA Workshop chasis: https://youtu.be/LRsAu9jn_a0

![The Chassis](https://i.imgur.com/cgAl9GN.jpg)
