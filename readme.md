# PocketStrava

Run Strava on your PocketC.H.I.P.! Once you are up and running, you can expect two things out of this project:
* Recording your mega bike adventure from start to finish with the use of a GPS breakout.
* Uploading all of your sweet rides using the Strava API.

## Getting Started
This project will require a light amount of python knowledge as well as a bit of soldering. If you are up to the challenge, then carry on!

## Requirements
* [PocketC.H.I.P. by Next Thing Co.](https://nextthing.co/pages/pocketchip)
* [Adafruit Ultimate GPS Breakout - 66 channel w/10 Hz updates - Version 3](https://www.adafruit.com/product/746)
* [USB to TTL Serial Cable](https://www.amazon.com/gp/product/B01N4X3BJB/ref=oh_aui_detailpage_o01_s00?ie=UTF8&psc=1)
* Soldering Iron
* Solder
* Some wire
* A Bike

## Software Installation
First and foremost, this is all for the most part doable exclusively on the PocketC.H.I.P. however it may be a heck of a lot of typing. As you go through the instructions, I suggest you use ssh (unless specifically otherwise noted). If you aren't, you are living life in God Mode and probably don't need my little instructions anyway.

### Step One: Log in via ssh
Make sure you have a good connection to your PocketC.H.I.P, either USB or WIFI.
```
ssh chip@chip.local
```
If you haven't changed the password, the default password is 'chip'.

### Step Two: Download the code to your PocketC.H.I.P
Once the project is done downloading, you will want to open the directory.
```
git clone XXX
cd PocketStrava
```

### Step Three: Prepare your PocketC.H.I.P.
First you will want to make sure your PocketC.H.I.P is up to date with the latest and greatest. You will find a file called "install.sh" in the directory. This file will make updates to your PocketC.H.I.P and install any prerequisites. Please review the files contents before installing so you know what is happening in this step.
```
sudo bash install.sh
```
You may have to type in 'y' to confirm that you are okay with installing a few of the prerequisites.

### Step Four: Open PocketStrava!
Okay, this is where we need to switch over to the terminal on your PocketC.H.I.P. On the PocketCHIP, type in the following:
```
cd /PocketStrava
sudo bash launcher.sh
```
You should see the sweet loading screen, followed by the UI! Congrats! BUT WAIT, you will be presented with a warning:
'Looks like you need to add your access token to PocketStrava.cfg. See documentation.'

"Well what the heck man?"

This error is actually okay. From here we can determine that the application is working, and all of your updates and prerequisites are operable. What isn't working right now is the fact that you need to provide three pieces of information to your config file: PocketStrava.cfg. There are values from the Strava API we need to supply in order to talk with Strava correctly. In order to do this, we need to register an api application.

Press the power button in the lower left to exit the application.

### Step Five: Register an API on Strava.com
I suggest checking out Strava's information for developers. You can find this here: http://labs.strava.com/developers/

Basically, you will need to follow their documentation to create an API application in which this application will be interfacing. Once you do so, you will get a couple pieces of basic information: A Client ID and a Client Secret. You will use these to get an access token which will allow you to upload files to Strava.  

### Step Six: Add client_id and client_secret to PocketStrava.cfg
In order to talk with the Strava API, we need to provide a client_id and client_secret values. After we supply these, we can retrieve a Strava user's access_token.

Open PocketStrava.cfg (again, I suggest doing this through ssh)
~~~
sudo nano PocketStrava.cfg
~~~

Modify the following variables with what the Strava API has supplied you:
~~~
client_id = [YOUR CLIENT ID]
client_secret = [YOUR CLIENT SECRET]
~~~

Save the file (ctrl-x, y, enter).

### Step Seven: Retrieve the access_token
Making progress! So this is where the process gets a little silly. In order to authenticate the Strava API, you need to open a browser to complete the process since the Strava API utilizes JavaScript to complete the process. Here's how I currently suggest doing this:

First and foremost, load up a real gritty web server (via ssh):
```
python -m stravalib.tests.auth_responder --port=8000 --client-id=[YOUR CLIENT ID] --client-secret=[YOUR CLIENT SECRET]
```
Then follow these steps to aquire the authorization key:
* Open PocketStrava like we did in step four.
* You'll receive the error again. This time, instead of closing the application, tap the Login button on the lower right.
* Wait a bit, your default browser will open (if you haven't installed a browser, check out iceweasel).
* Supply your Strava login credentials.
* Accept the authorization form.

If successful, you will be presented with a real long authorization key. Set access_token to this authorization key in PocketStrava.cfg. Also, it should be noted that this key will be presented in the ssh terminal on your computer for your copying-and-pasting pleasure.

Once the authorization code is slammed in that config file, PocketStrava is ready to talk with the API!

## Hardware Installation
At this point, the software should be good to go, with exception that you can't actually record a trip yet, bummer! We first need to install the GPS Breakout in order to get a latitude and longitude of your current location. Fortunately PocketC.H.I.P. makes this heckin' easy.

### Step One: Examine the GPS breakout.
If you went with the Adafruit Ultimate GPS Breakout, you'll likely notice that it comes packed with a lot of cool features. For this project, we are only really using tip-o'-the-iceberg features it supplies. You'll notice it has 9 pins. We are only going to use four of them: VIN, GND, RX and TX. It also comes with some pins that you can solder right onto the breakout, which I suggest doing since it'll be easier to interface with the USB to TTL cable.

### Step Two: Plug the USB to TTL cable into the GPS Breakout
So, you do have the potential to really fry the GPS unit and/or CHIP computer. For the sake of your safety, and the safety of your hardware, that you read Adafruit's [guide on getting your Breakout set up the right way](https://learn.adafruit.com/adafruit-ultimate-gps-on-the-raspberry-pi/setting-everything-up).

If you are feeling reckless, here's the pin/color combos:
* VIN: Red wire
* GND: Black wire
* RX: Green wire
* TX: White wire

### Step Three: Plug it into the PocketCHIP
When I initially built this, I plugged the USB cable in before I turned the PocketCHIP on. I later learned that you can willy-nilly plug and unplug the breakout as needed with no repercussions.

### Step Four: Run the Launcher!
From here, everything should be hooked up and ready to go. You have your authorization key, you have your breakout connected to your PocketCHIP, and you have a sweet adventure lined up that needs recording. Time to try and record a trip. Run the launcher again.
```
cd /PocketStrava
sudo bash launcher.sh
```
## Troubleshooting
A few things to know right off the bat to minimize stress and confusion:
* If you start somewhere within WIFI, you should be notified at the bottom right that you are logged in. It's generally good to load the application while you are connected, especially for your first ride. If you aren't, that's okay, but you won't be able to upload your adventures until you have a connection.
* When you press "Record an Epic Adventure!", the screen will say, "Acquiring signal...". Keep in mind that your GPS unit needs some time to triangulate and do whatever GPS receivers do. It will not start your trip until your GPS unit has a connection.
* If "Acquiring signal..." displays for a very long time (over two minutes), it would be worth running "cgps -s" in another terminal to review the raw GPS input. This will let you know pretty immediately if there are issues you need to debug with the hardware or with the operating system.
* Once you have a successful GPS signal, the "Acquiring signal..." message will go away and it will start to display your current lat/lon.
* When it records, all it's doing is creating a GPX file, which is an XML file. If there are any issues with uploading, there are two primary reasons for this: Either you are not connected to your Strava API correctly, or it's likely that my programming sucks. Please let me know if you have any issues!

## Author
Nick Davis
Email: nick@nicholasdavis.info
Twitter: @armaexmachina
Instagram: armageddonmachine

## Acknowledgements

Power button icon by "Yo! Baba" from the Noun Project
