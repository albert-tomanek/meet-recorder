# Requirements:
#  - Chrome
#  - Pulseaudio
#  - GStreamer (gst-launch is in gstreamer1.0-tools package iirc)

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import *

import os, time, re

options = webdriver.ChromeOptions()
options.add_experimental_option("prefs", { "profile.default_content_setting_values.notifications": 1}) # disable notificaitons so that there's no popup
options.add_argument('--use-fake-device-for-media-stream')
options.add_argument('--use-file-for-fake-video-capture=albert.mjpeg')
# options.add_argument('--use-file-for-fake-audio-capture=fake_cam.mjpeg')
# options.add_argument('--use-fake-ui-for-media-stream')
options.add_argument('--disable-notifications ')

options = webdriver.FirefoxOptions()
options.set_preference("media.navigator.streams.fake", True)

record_rect = {'x': 100, 'y': 100, 'w': 800, 'h': 600}  # Keep this order. It's the order of args for selenium

class NotAMeetLinkException(Exception):
    pass

class MeetRecorder:
    driver: webdriver.Chrome
    pa_device_name: str

    def __init__(self):
        input('You need to set up a few things before we can start recording. Press ENTER to proceed.')
        print('\nAvailable sound devices:')
        os.system("pacmd list-sources | grep -e device.string -e 'name:'")
        self.pa_device_name = input('ID string of device to record audio from (device.string): ')

        self.driver = webdriver.Firefox(firefox_options=options)#webdriver.Chrome(chrome_options=options)
        self.driver.get('https://meet.google.com/')
        input('Log in if your meeting will be private. Then press ENTER.')
        self.driver.set_window_rect(*list(record_rect.values()))

        print('')
        print('Ready to record. You may now leave your computer.')

    def __del__(self):
        self.driver.quit()

    def join(self, link: str):
        match = re.search("meet.google.com\/([a-z\-]+)", link)
        if not match:
            raise NotAMeetLinkException()
        meeting_id = match.group(1)

        # Interact with meeting ID element

        meeting_id_elt = self._find_elt(
            'input',
            'return arguments[0].getAttribute("aria-label")',   # using 'aria-label' as opposed to other text is good because it ignores internationalization
            lambda aria_label: 'Enter a code or nickname' == aria_label
        )
        meeting_id_elt.send_keys(meeting_id)
        meeting_id_elt.send_keys(Keys.ENTER)

        time.sleep(5)

        # Interact with 'Allow Meet to use your camera and microphone' dialog
        import pdb; pdb.set_trace()
        dismiss_button = self._find_elt(
            'span',
            'return arguments[0].innerHTML',
            lambda innerHTML: innerHTML == 'Dismiss'
        )
        if dismiss_button:
            self._click(dismiss_button)

        # Disable camera and mic

        cam_button = self._find_elt(
            'div',
            'return arguments[0].getAttribute("aria-label")',
            lambda aria_label: 'Turn off camera' in str(aria_label)
        )
        if cam_button:  # If the camera's already disabled, the text will be 'Turn ON camera' and so no button will be found
            self._click(cam_button)

        mic_button = self._find_elt(
            'div',
            'return arguments[0].getAttribute("aria-label")',
            lambda aria_label: 'Turn off microphone' in str(aria_label)     # None becomes 'None' but the code's more readable
        )
        if mic_button:
            self._click(mic_button)

        time.sleep(1)

        # Click 'Join Now'

        join_button = self._find_elt(
            'span',
            'return arguments[0].innerHTML',
            lambda innerHTML: innerHTML == 'Join now' or innerHTML == 'Ask to join'
        )
        self._click(join_button)

    def leave(self):
        # Click the leave button
        leave_button = self._find_elt(
            'button',
            'return arguments[0].getAttribute("aria-label")',
            lambda aria_label: 'Leave call' == aria_label
        )
        self._click(leave_button)

        time.sleep(2)

        # 'Just leave the call' if the dialog pops up
        leave_button = self._find_elt(
            'span',
            'return arguments[0].innerHTML',
            lambda innerHTML: innerHTML == 'Just leave the call'
        )
        if leave_button:
            self._click(leave_button)

        time.sleep(2)

        # 'Return to home screen' so that we can join another call
        leave_button = self._find_elt(
            'span',
            'return arguments[0].innerHTML',
            lambda innerHTML: innerHTML == 'Return to home screen'
        )
        self._click(leave_button)

    def start(self, outfile: str):
        pass

    def stop(self):
        pass

    def _find_elt(self, tag, script, evaluate) -> WebElement:
        # elts = list(self.driver.find_elements_by_tag_name(tag)) # We've got to store a list because more elements may be created while we iterate creating an infinite loop.
        elts = self.driver.execute_script("return document.getElementsByTagName(arguments[0])", tag)
        if elts:
            for elt in elts:
                try:
                    if evaluate(self.driver.execute_script(script, elt)):
                        return elt
                except StaleElementReferenceException:
                    continue

        return None

    def _click(self, elt):
        assert elt != None
        self.driver.execute_script("arguments[0].click();", elt)
