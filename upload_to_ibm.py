from libsoundtouch import soundtouch_device
from libsoundtouch.utils import Source, Type
import shlex
import subprocess



# Getting the emotions from the IBM Watson Cloud Visual Recognition
cmd = '''curl -u "apikey:XXXX" "https://gateway.watsonplatform.net/visual-recognition/api/v3/classify?url=https://us.123rf.com/450wm/bowie15/bowie151401/bowie15140100080/39843138-sad-man.jpg?ver=6&version=2018-03-19&classifier_ids=DefaultCustomModel_196000000"'''
args = shlex.split(cmd)
process = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = process.communicate()
stdout1 = stdout.decode("utf-8")

# Splitting the string returned to get the emotion "Sad" "Happy" "Angry" "Depressed"
emotion = stdout1.split('"class":')[1].split('",')[0].replace(' "','')
print(emotion)

# Switching on the device
device = soundtouch_device('194.168.109.111')
device.power_on()

# Config object
print(device.config.name)

# Status object
# device.status() will do an HTTP request. Try to cache this value if needed.
#device.play_media(Source.INTERNET_RADIO, '4712')
#device.play()
#device.pause()

#Spotify Username
spot_user_id = 'XXXXXXXXXXX' # Should be filled in with your Spotify userID
# This userID can be found by playing Spotify on the
# connected SoundTouch speaker, and calling
#print(device.status().content_item.source_account)

device.play_media(Source.SPOTIFY,'spotify:playlist:34trheyYTRghfyT',spot_user_id)
#device.play()
