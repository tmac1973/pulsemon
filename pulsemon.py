# MIT License
#
# Copyright (c) 2021 Timothy MacDonald
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from pyudev import Context, Monitor
from pyudev.pyqt5 import MonitorObserver
import pulsectl
import sys
import os
import qtmodern.styles
import qtmodern.windows
import pathlib
import json
from qtpy import QtWidgets, uic


class USBSoundMonitor(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        # detect if in Pyinstaller package and build appropriate base directory path
        if getattr(sys, 'frozen', False):
            basedir = sys._MEIPASS
        else:
            basedir = os.path.dirname(os.path.abspath(__file__))
        gui = pathlib.Path(basedir + '/ui/pulsemon.ui')
        uic.loadUi(gui, self)
        self.center()

        # setup udev monitor to look for USB changes
        context = Context()
        monitor = Monitor.from_netlink(context)
        monitor.filter_by(subsystem='usb')
        self.observer = MonitorObserver(monitor)
        self.observer.deviceEvent.connect(self.device_connected)
        monitor.start()
        self.populate_outputs()
        self.populate_sources()
        self.preferred_output = None
        self.preferred_source = None
        self.monitor = True
        self.toggle_monitor()
        self.load_state()
        self.update_output_label()
        self.update_source_label()

        # connect GUI elements to methods
        self.pushButtonRefresh.clicked.connect(self.populate_outputs)
        self.pushButtonRefresh.clicked.connect(self.populate_sources)
        self.checkBoxMonitor.stateChanged.connect(self.toggle_monitor)
        self.pushButtonSetOutput.clicked.connect(self.set_preferred_output)
        self.pushButtonSetInput.clicked.connect(self.set_preferred_source)
        self.pushButtonClearOutput.clicked.connect(self.clear_preferred_output)
        self.pushButtonClearInput.clicked.connect(self.clear_preferred_source)

    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def save_state(self):
        home = pathlib.Path.home()
        configfile = home / '.pulsemonrc'
        state = {'preferred_output': self.preferred_output,
                 'preferred_source': self.preferred_source}
        with open(configfile, 'w') as file:
            json.dump(state, file)

    def load_state(self):
        home = pathlib.Path.home()
        configfile = home / '.pulsemonrc'
        try:
            with open(configfile, 'r') as file:
                state = json.load(file)
            self.preferred_output = state['preferred_output']
            self.preferred_source = state['preferred_source']
        except:
            print('no file to load')

    def clear_preferred_output(self):
        self.preferred_output = None
        self.update_output_label()
        self.save_state()

    def clear_preferred_source(self):
        self.preferred_source = None
        self.update_source_label()
        self.save_state()

    def update_output_label(self):
        self.labelPreferredOutput.setText(f'Preferred Output: {str(self.preferred_output)}')

    def update_source_label(self):
        self.labelPreferredInput.setText(f'Preferred Output: {str(self.preferred_source)}')

    def set_preferred_output(self):
        selected = self.listWidgetOutputDevices.selectedItems()
        if len(selected) > 0:
            self.preferred_output = selected[0].description
            self.update_output_label()
            self.save_state()

    def set_preferred_source(self):
        selected = self.listWidgetInputDevices.selectedItems()
        if len(selected) > 0:
            self.preferred_source = selected[0].description
            self.update_source_label()
            self.save_state()

    def toggle_monitor(self):
        self.monitor = self.checkBoxMonitor.isChecked()

    def populate_outputs(self):
        self.listWidgetOutputDevices.clear()
        outputs = self.get_pulseaudio_sinks()
        for output in outputs:
            list_item = QtWidgets.QListWidgetItem(output.description)
            list_item.index = output.index
            list_item.name = output.name
            list_item.description = output.description
            list_item.sink = output
            self.listWidgetOutputDevices.addItem(list_item)

    def populate_sources(self):
        self.listWidgetInputDevices.clear()
        sources = self.get_pulseaudio_sources()
        for source in sources:
            list_item = QtWidgets.QListWidgetItem(source.description)
            list_item.index = source.index
            list_item.name = source.name
            list_item.description = source.description
            list_item.source = source
            self.listWidgetInputDevices.addItem(list_item)

    def get_pulseaudio_sinks(self):
        with pulsectl.Pulse("sinks") as pulse:
            sinks = pulse.sink_list()
        return sinks

    def get_pulseaudio_sources(self):
        with pulsectl.Pulse("sources") as pulse:
            sources = pulse.source_list()
        return sources

    def device_connected(self):
        self.populate_outputs()
        self.populate_sources()
        if self.monitor:
            sinks = self.get_pulseaudio_sinks()
            for sink in sinks:
                if sink.description == self.preferred_output:
                    with pulsectl.Pulse("sink-switch") as pulse:
                        pulse.sink_default_set(sink)
            sources = self.get_pulseaudio_sources()
            for source in sources:
                if source.description == self.preferred_source:
                    with pulsectl.Pulse("source-switch") as pulse:
                        pulse.source_default_set(source)


def main():

    app = QtWidgets.QApplication(sys.argv)
    qtmodern.styles.dark(app)
    window = qtmodern.windows.ModernWindow(USBSoundMonitor())
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

