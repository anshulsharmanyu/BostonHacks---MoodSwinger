import boto3
import os
import requests
#import colorgram
#import webcolors
import time
import numpy as np
#import cv2
#import statistics
import pandas as pd
import shlex
import subprocess
from flask import Flask, render_template, request
from libsoundtouch import soundtouch_device
from libsoundtouch.utils import Source, Type
#from json2table import convert
from werkzeug import secure_filename



os.environ['AWS_DEFAULT_REGION'] = 'us-east-2'

def is_nan(x):
    return (x is np.nan or x != x)

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('template.html')



def color(file):
    colors = colorgram.extract(file, 2)
    first_color = colors[1]
    rgb = first_color.rgb
    return (rgb)


def closest_colour(requested_colour):
    min_colours = {}
    for key, name in webcolors.css3_hex_to_names.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]


def get_colour_name(requested_colour):
    try:
        closest_name = actual_name = webcolors.rgb_to_name(requested_colour)
    except ValueError:
        closest_name = closest_colour(requested_colour)
        actual_name = None
    return actual_name, closest_name

@app.route('/my-link/', methods = ['GET', 'POST'])
def main():

    # Getting the emotions from the IBM Watson Cloud Visual Recognition
#     cmd = '''curl -u "apikey:9t_w3I8yzOheBd9syHpyPFEeCN21DSw0NX8tnYJCvdBe" "https://gateway.watsonplatform.net/visual-recognition/api/v3/classify?url=https://us.123rf.com/450wm/bowie15/bowie151401/bowie15140100080/39843138-sad-man.jpg?ver=6&version=2018-03-19&classifier_ids=DefaultCustomModel_1963778161"
#     '''
	  
    # args = shlex.split(cmd)
#     process = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#     stdout, stderr = process.communicate()
#     stdout1 = stdout.decode("utf-8")
    url ='https://gateway.watsonplatform.net/visual-recognition/api/v3/classify?version=2016-04-19&classifier_ids=DefaultCustomModel_2222222' 
    files = {'images_file': open("./XTYZZ.jpg",'rb')} 
    stdout = requests.post(url, auth=('apikey','XXXXXXXXXXXXXXXX'), files=files)
    stdout1 = str(stdout.content)
    # Splitting the string returned to get the emotion "Sad" "Happy" "Angry" "Depressed"
    emotion = stdout1.split('"class":')[1].split('",')[0].replace(' "','')
    
    print(emotion)
    id = ""

    if emotion == "Happy":
        id = "spotify:playlist:XDXDXDXDXD"
        cmd = '''curl -d \\ "<play_info><app_key>XXXXXDXDXDXD</app_key><url>http://www.fromtexttospeech.com/output/111111/222222.mp3</url><service>service text</service><reason>reason text</reason><message>message text</message><volume>25</volume></play_info>" http://192.170.100.160:9090/speaker'''
    elif emotion == "Sad":
        id = "spotify:playlist:DDDDDDDDDDD"
        cmd = '''curl -d \\ "<play_info><app_key>DDDDDDDDDDDD</app_key><url>http://www.fromtexttospeech.com/output/222222/333333.mp3</url><service>service text</service><reason>reason text</reason><message>message text</message><volume>25</volume></play_info>" http://192.170.100.160:9090/speaker'''
    elif emotion == "Angry":
        id = "spotify:playlist:XXXXXXXXXX"
        cmd = '''curl -d \\ "<play_info><app_key>XXXXXXXXXX</app_key><url>http://www.fromtexttospeech.com/output/333333/444444.mp3</url><service>service text</service><reason>reason text</reason><message>message text</message><volume>25</volume></play_info>" http://192.170.100.160:9090/speaker'''


    args = shlex.split(cmd)
    process = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    st, sd = process.communicate()
    st1 = st.decode("utf-8")
    time.sleep(10)

    # Switching on the device
    device = soundtouch_device('193.170.100.120')
    device.power_on()
    # Config object
    print(device.config.name)

    # Status object
    # device.status() will do an HTTP request. Try to cache this value if needed.
    #device.play_media(Source.INTERNET_RADIO, '4712')
    #device.play()
    #device.pause()

    #Spotify Username
    spot_user_id = 'mnuk68asijvbj6nzapegd4p94' # Should be filled in with your Spotify userID
    # This userID can be found by playing Spotify on the
    # connected SoundTouch speaker, and calling
    #print(device.status().content_item.source_account)
    # time.sleep(10)
    device.play_media(Source.SPOTIFY,id,spot_user_id)
    return ""
    #device.play()
#     if request.method == 'POST':
#       f = request.files['file']
#       f.save(secure_filename(f.filename))
#       file = str(f.filename)
#
#     # print(file)
#     #
#     # requested_colour = color(file)
#     # actual_name, closest_name = get_colour_name(requested_colour)
#     # print ("Actual colour name:", actual_name, ", closest colour name:", closest_name)
#     # aN = str(actual_name)
#     # cN = str(closest_name)
#     # return(cN)
#
#
# # @app.route('/my-link/')
# # def main():
# #     file="test_image_10.jpg"
#     # requested_colour = color(file)
#     # actual_name, closest_name = get_colour_name(requested_colour)
#     # print ("Actual colour name:", actual_name, ", closest colour name:", closest_name)
#     # aN = str(actual_name)
#     # cN = str(closest_name)
#     # print(cN)
#     # return(cN)
#
#     s3 = boto3.client('s3')
#     bucket = 'avadakadaba'
#     photo = file
#     s3.upload_file(photo, bucket, photo)
#     client = boto3.client('rekognition')
#     response = client.detect_text(Image={'S3Object': {'Bucket': 'avadakadaba', 'Name': photo}})
#     textDetections = response['TextDetections']
#     text2 = ""
#     for text in textDetections:
#         if text['DetectedText'] not in text2:
#             text2 = text2 + text['DetectedText']
#     text2 = ''.join(text2.split())
#
#     # Getting color
#     requested_colour = color(photo)
#     actual_name, closest_name = get_colour_name(requested_colour)
#     if "grey" in closest_name:
#         closest_name = "WHITE"
#     if "rose" in closest_name:
#         closest_name = "PINK"
#     if "red" in closest_name:
#         closest_name = "RED"
#     if "yellow" in closest_name:
#         closest_name = "YELLOW"
#     if "blue" in closest_name:
#         closest_name = "BLUE"
#
#
#     # Getting shape
#     shape=""
#     img = cv2.imread(photo)
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     gray = cv2.Canny(np.asarray(gray), 50, 250)
#
#     _,contours, h = cv2.findContours(gray, 1, 2)
#
#     avgArray = []
#     for cnt in contours:
#         approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
#         avgArray.append(len(approx))
#
#     # print((avgArray))
#     edges = statistics.median(avgArray)
#     # print(edges)
#
#     if edges < 15:
#         shape = "OVAL"
#         # cv2.drawContours(photo, [cnt], 0, 255, -1)
#     # elif edges == 3:
#     #     print("triangle")
#     #     cv2.drawContours(img, [cnt], 0, (0, 255, 0), -1)
#     # elif edges == 4:
#     #     print("square")
#     #     cv2.drawContours(img, [cnt], 0, (0, 0, 255), -1)
#     # elif edges == 9:
#     #     print("half-circle")
#     #     cv2.drawContours(img, [cnt], 0, (255, 255, 0), -1)
#     elif edges > 15:
#
#         shape = "CIRCLE"
#
#     data = {"uploadName":photo,"text":text2,"color":closest_name,"shape":shape}
#     print(data)
#     # print(data)
#
#     dataframe = pd.read_csv("out.csv")
#
#     for index, row in dataframe.iterrows():
#         name = str(row["Imprint"]).replace(";","")
#         if not is_nan(row["Name"]):
#             if name == text2 and row["Color"] == color and row["Shape"] == shape:
#                 return '''<style>
#                 table, th, td {
#                     border: 1px solid black;
#                     border-collapse: collapse;
#                 }
#                 th, td {
#                     padding: 5px;
#                     text-align: left;
#                 }
#                 </style><b>Pill Details</b><table style="width:100%">
#                   <tr>
#                     <th>Author</th>
#                     <th>Name</th>
#                     <th>Color</td>
#                     <th>Imprint</td>
#                     <th>Size</td>
#                     <th>Shape</td>
#                     <th>Ingredients</td>
#                   </tr>
#                   <tr>
#                     <td>'''+str(row["Author"])+'''</td>
#                     <td>'''+str(row["Name"])+'''</td>
#                     <td>'''+str(row["Color"])+'''</td>
#                     <td>'''+str(row["Imprint"])+'''</td>
#                     <td>'''+str(row["Size"])+'''</td>
#                     <td>'''+str(row["Shape"])+'''</td>
#                     <td>'''+str(row["Ingredients"])+'''</td>
#                   </tr>
#                 </table>'''
#
#
#
#     for index, row in dataframe.iterrows():
#         name = str(row["Imprint"]).replace(";","")
#         if not is_nan(row["Name"]):
#             if name == text2 and row["Color"] == color:
#                 return '''<style>
#                 table, th, td {
#                     border: 1px solid black;
#                     border-collapse: collapse;
#                 }
#                 th, td {
#                     padding: 5px;
#                     text-align: left;
#                 }
#                 </style><b>Pill Details</b><table style="width:100%">
#                   <tr>
#                     <th>Author</th>
#                     <th>Name</th>
#                     <th>Color</td>
#                     <th>Imprint</td>
#                     <th>Size</td>
#                     <th>Shape</td>
#                     <th>Ingredients</td>
#                   </tr>
#                   <tr>
#                     <td>'''+str(row["Author"])+'''</td>
#                     <td>'''+str(row["Name"])+'''</td>
#                     <td>'''+str(row["Color"])+'''</td>
#                     <td>'''+str(row["Imprint"])+'''</td>
#                     <td>'''+str(row["Size"])+'''</td>
#                     <td>'''+str(row["Shape"])+'''</td>
#                     <td>'''+str(row["Ingredients"])+'''</td>
#                   </tr>
#                 </table>'''
#
#     for index, row in dataframe.iterrows():
#         name = str(row["Imprint"]).replace(";","")
#         if not is_nan(row["Name"]):
#             if name == text2:
#                 return '''<style>
#                 table, th, td {
#                     border: 1px solid black;
#                     border-collapse: collapse;
#                 }
#                 th, td {
#                     padding: 5px;
#                     text-align: left;
#                 }
#                 </style><b>Pill Details</b><table style="width:100%">
#                   <tr>
#                     <th>Author</th>
#                     <th>Name</th>
#                     <th>Color</td>
#                     <th>Imprint</td>
#                     <th>Size</td>
#                     <th>Shape</td>
#                     <th>Ingredients</td>
#                   </tr>
#                   <tr>
#                     <td>'''+str(row["Author"])+'''</td>
#                     <td>'''+str(row["Name"])+'''</td>
#                     <td>'''+str(row["Color"])+'''</td>
#                     <td>'''+str(row["Imprint"])+'''</td>
#                     <td>'''+str(row["Size"])+'''</td>
#                     <td>'''+str(row["Shape"])+'''</td>
#                     <td>'''+str(row["Ingredients"])+'''</td>
#                   </tr>
#                 </table>'''

if __name__ == "__main__":
    app.run(debug=True)
