
<h1> What? </h1>
Pulsemon allows you to pick a pulseaudio output (sink) and input (source) as
the preferred devices. It will then monitor for changes to the usb bus. If your
preferred pulseaudio sound device is removed and then re-added later it will remember
that device and restore it to its rightful state as "active".  

<h1> Why? </h1>
I wrote this because I have 3 sound devices (webcam, mic, usb sound card) all plugged
into my KVM monitor so that they get switched to the selected computer. The
problem is when I switch back to my linux box the wrong sound devices would always
get selected as "active". This tool solves the problem. 

<h1> How? </h1>
The utility monitors the usb bus using the pyudev module. If it sees a change then it
enumerates the pulseaudio devices and compares them against what you have set as the
"preferred" device. If it finds a match then it goes to work.

This utility saves its settings in ~/.pulsmonrc so it should reliably remember
state between runs. Set it to start at login and you should be good to go (I think.)

<h1> Future? </h1>
I could probably change it to monitor pulseaudio directly for changes instead of 
monitoring the usb bus through pyudev but that's for another day.

Hope this helps someone out. 

<h1> Install? </h1>

There's a binary in the "releases" section to the right. Built with Pyinstaller on 
Solus Linux 4.2.

https://github.com/voltaire321/pulsemon/releases

Alternatively you could clone this archive and run from the source. If you're gonna
do that you probably know how to use "pipenv" to create the environment for it to run
in. 

Also I've included a pyinstaller .spec file if you need to roll your own. 

Cheers! - Tim


