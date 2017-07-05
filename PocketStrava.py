#!/usr/bin/python
# _____         _       _   _____ _____ _____ _____ _____ _____
#|  _  |___ ___| |_ ___| |_|   __|_   _| __  |  _  |  |  |  _  |
#|   __| . |  _| '_| -_|  _|__   | | | |    -|     |  |  |     |
#|__|  |___|___|_,_|___|_| |_____| |_| |__|__|__|__|\___/|__|__|
#
# Author: Nick Davis
# Email: nick@nicholasdavis.info

from Tkinter import *
from PIL import ImageTk, Image
from stravalib.client import Client
from gps import *
from time import *
from threading import *
import tkMessageBox
import sys
import threading
import time
import os
import ConfigParser
import webbrowser
import socket
# import gps

config = ConfigParser.RawConfigParser()
client = Client()
gpsd = None

class App():

    def __init__(self):

        self.root = Tk()
        self.root.configure(background='black')
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(1, weight=2)

        self.checkConnection = threading.Thread(target=self.strava_record_thread)
        self.checkConnection.daemon = True

        self.gpxFileName = ''
        self.gpxFileContents = ''
        self.recording = False
        self.stravaRecord = threading.Thread(target=self.connection_monitor)
        self.stravaRecord.daemon = True

        self.img = ImageTk.PhotoImage(Image.open('PocketStrava.gif'))
        self.icon_power = ImageTk.PhotoImage(Image.open('icon_power.gif'))

        self.load_splash()
        self.load_config()
        self.strava_init()

        self.stravaRecord.start()
        self.checkConnection.start()
        self.root.mainloop()
    def load_splash(self):
        try:
            #Display the rad splash screen.
            self.splash = Label(self.root,image=self.img,background='black')
            self.splash.grid()
        except Exception as e:
            tkMessageBox.showerror('Error: load_splash',str(e))
            pass
    def init_grid(self):
        try:
            #Place Holder
            self.lblLocation = Label(self.root, text='',background='black',fg='white', activebackground='black', activeforeground='white')
            self.lblLocation.grid(sticky=W,row=0,column=0)

            #Connection Status
            self.lblConnection = Label(self.root, text='Connection', background='black',fg='white', activebackground='black', activeforeground='white')
            self.lblConnection.grid(sticky=E,row=0,column=1)

            #GPS Information
            self.GPSInfo = Label(self.root, text='Welcome!', background='black',fg='white', activebackground='black', activeforeground='white',font=('Helvetica',16))
            self.GPSInfo.grid(row=1,column=0,columnspan=2)

            #Records Adventures
            self.btnRecord = Button(self.root, text='Record an Epic Adventure!', command=self.strava_record, pady=20,background='#eb008b',fg='white', activebackground='#eb008b', activeforeground='white')
            self.btnRecord.grid(row=2,column=0)

            #Uploads Adventure Queue
            self.btnUpload = Button(self.root, text='Upload Latest Adventures!', command=self.strava_upload, pady=20,background='#eb008b',fg='white', activebackground='#eb008b', activeforeground='white')
            self.btnUpload.grid(row=2,column=1)

            #Quit Button
            self.btnQuit = Button(self.root, image=self.icon_power, command=self.root.quit,background='black',fg='black', activebackground='black', activeforeground='black', highlightthickness = 0, bd = 0)
            self.btnQuit.grid(sticky=W,row=3,column=0,pady=10)

            #Strava Actions
            self.btnLogin = Button(self.root, text='Log In to Strava!', command=self.strava_login, background='#eb008b',fg='white', activebackground='#eb008b', activeforeground='white')
            self.btnLogin.grid(sticky=E,row=3,column=1)
        except Exception, e:
            tkMessageBox.showerror('Grid Error',str(e))
            pass
    def load_config(self):
        try:
            #Load the config settings
            config.read('PocketStrava.cfg')

            #Hide the super sweet splash screen.
            time.sleep(0.5)
            self.splash.grid_forget()
            self.init_grid()
        except:
            tkMessageBox.showerror('Error','There was an issue accessing the config file.')
    def connection_check(self):
        try:
            host = socket.gethostbyname('strava.com')
            s = socket.create_connection((host, 80), 2)
            return True
        except:
            pass
        return False
    def connection_monitor(self):
        while True:
            if self.connection_check() == False:
                self.lblConnection['text']='No Connection'
            else:
                self.lblConnection['text']='Online'
            time.sleep(5)
    def strava_init(self):
        try:
            #Check if there is a connection. If there isn't, don't bother trying to access Strava.
            if self.connection_check() == False:
                return False

            #Attempt to utilize the access token supplied in the config file.
            if config.get('Strava', 'access_token') != '0':
                client = Client(access_token=config.get('Strava', 'access_token'))
                athelete = client.get_athlete() # Get current athlete details

                #If we connected to Strava and returned an athelete, get rid of the log in button and replace it with the athelete's name.
                self.btnLogin.grid_forget()
                self.lblLogin = Label(self.root, text='Logged in as ' + athelete.firstname + ' ' + athelete.lastname,background='black',fg='white', activebackground='black', activeforeground='white')
                self.lblLogin.grid(sticky=E,row=3,column=1)

            else:
                tkMessageBox.showerror('Config Error','Looks like you need to add your access token to PocketStrava.cfg. See documentation.')
            return True
        except Exception, e:
            tkMessageBox.showerror('Error: strava_init',str(e))
            pass
    def strava_login(self):
        try:
            #Try and load the strava authorization form in the default web browser.
            url = client.authorization_url(client_id=config.get('Strava', 'client_id'), redirect_uri='http://localhost:8000/authorization', scope='write')
            webbrowser.open(url,new=2)
        except Exception, e:
            tkMessageBox.showerror('Error: strava_login',str(e))
            pass
    def strava_record(self):
        try:
            if self.recording == False:
                #If there is still a file name, it's possible that the thread has not finished creating the file.
                #This prevents tap-happy users.
                if self.gpxFileName != '':
                    return;

                self.recording = True
                self.btnRecord['text'] = 'Stop Recording'
                self.lblLocation['text'] = ''
                self.GPSInfo['text'] = 'Acquiring signal...'
            else:
                #If the file name is empty, it's possible that the service hasn't started creating the file.
                #This prevents tap-happy users.
                if self.gpxFileName == '':
                    return;

                self.recording = False
                self.btnRecord['text'] = 'Record an Epic Adventure!'
                self.lblLocation['text'] = ''
                self.GPSInfo['text'] = 'Saving adventure...'
            self.root.update()
        except Exception, e:
            tkMessageBox.showerror('Error: strava_record',str(e))
            pass
    def strava_record_thread(self):
        gpsp = GpsPoller() # create the thread
        gpsp.start()
        while True:
            try:
                #User sets self.recording from self.strava_record()
                if self.recording == True:

                    #Record info from GPS unit to GPX file.
                    if gpsp.session['class'] == 'TPV':
                        if hasattr(gpsp.session, 'lat'):
                            speed = str(gpsp.session.speed)
                            if self.gpxFileName == '':
                                self.gpxFileName = str(time.time()).split('.')[0] + '.gpx' #just name the file the current time.
                                self.gpxFileContents = open(os.getcwd() + '/adventures/' + self.gpxFileName, 'w+')

                                #We need to make the header stuff in the GPX file.
                                self.gpxFileContents.write('<?xml version="1.0" encoding="UTF-8"?>\n')
                                self.gpxFileContents.write('<gpx creator="StravaGPX" version="1.1" xmlns="http://www.topografix.com/GPX/1/1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd">\n')
                                self.gpxFileContents.write('<metadata>\n')
                                self.gpxFileContents.write('<time>' + str(gpsp.session.time) + '</time>\n')
                                self.gpxFileContents.write('</metadata>\n')
                                self.gpxFileContents.write('<trk>\n')
                                self.gpxFileContents.write('<name>Morning Run</name>\n')
                                self.gpxFileContents.write('<trkseg>\n')

                            self.gpxFileContents.write('<trkpt lat="' + str(gpsp.session.lat) + '" lon="' + str(gpsp.session.lon) + '">\n')
                            self.gpxFileContents.write('<ele>0</ele>\n')
                            self.gpxFileContents.write('<time>' + str(gpsp.session.time) + '</time>\n')
                            self.gpxFileContents.write('<extensions></extensions>\n')
                            self.gpxFileContents.write('</trkpt>\n')
                            self.lblLocation['text'] = 'GPS Online and Recording'
                            self.GPSInfo['text'] = str(gpsp.session.lat) + ', ' + str(gpsp.session.lon)
                            self.root.update()
                else:
                    if self.gpxFileName != '':
                        #We are done recording.
                        self.gpxFileContents.write('</trkseg>\n')
                        self.gpxFileContents.write('</trk>\n')
                        self.gpxFileContents.write('</gpx>\n')
                        self.gpxFileContents.close()
                        self.gpxFileName = ''
                        self.lblLocation['text'] = ''
                        self.GPSInfo['text'] = 'Adventure saved!'
                        self.root.update()
                    # else:
                    #     if gpsp.session != None & gpsp.session['class'] == 'TPV':
                    #         if hasattr(gpsp.session, 'lat'):
                    #             self.lblLocation['text'] = str(gpsp.session.lat) + ', ' + str(gpsp.session.lon)
                    #             self.root.update()
                time.sleep(10)
            except Exception, e:
                tkMessageBox.showerror('Recording Error',str(e))
                pass
    def strava_upload(self):
        try:
            #Try and initialize the Strava connection again. If it doesn't work, it's likely that one of the following occurred:
            #- No internet connection
            #- Your authorization code is bad
            if self.strava_init() == False:
                tkMessageBox.showerror('Connection Error','You must be connected to the internet before uploading.')
                return

            client = Client(access_token=config.get('Strava', 'access_token'))

            #Loop through all pending .gpx files found in the "adventures" folder.
            #TODO: Perhaps catch errors per file.
            for filename in os.listdir(os.getcwd() + '/adventures'):
                if filename.endswith('.gpx'):
                    with open(os.path.join(os.getcwd() + '/adventures', filename)) as fp:

                        #Try and upload the file.
                        uploader = client.upload_activity(activity_file=fp, data_type='gpx', description='Uploaded via PocketCHIP')
                        a = uploader.wait()

                        #Move the freshly uploaded .gpx file to the archive directory.
                        os.rename(os.getcwd() + '/adventures/' + filename, os.getcwd() + '/adventures/archive/' + filename)

                    continue
                else:
                    continue

            tkMessageBox.showerror('Success!','Your rides have been uploaded, yay!')
        except Exception, e:
            tkMessageBox.showerror('Upload Error',str(e))
            pass

class GpsPoller(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        global gpsd #bring it in scope
        gpsd = gps()
        gpsd.stream(WATCH_ENABLE | WATCH_NEWSTYLE)
        # self.current_value = None
        self.running = True #setting the thread running to true
        self.session = None

    def run(self):
        global gpsd
        while self.running:
            self.session = gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer

app = App()

 #-------- __@      __@       __@       __@      __~@
 #----- _`\<,_    _`\<,_    _`\<,_     _`\<,_    _`\<,_
 #---- (*)/ (*)  (*)/ (*)  (*)/ (*)  (*)/ (*)  (*)/ (*)
 #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
