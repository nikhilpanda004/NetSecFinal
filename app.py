from flask import Flask, render_template, request
import xml.etree.ElementTree as ET
import numpy as np
import pickle

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/', methods=['POST'])
# def upload_file():
#     xml_file = request.files['file']
#     tree = ET.parse(xml_file)
#     root = tree.getroot()
#     values = []
#     for key in root.iter('key'):
#         value = key.text
#         values.append(value)
#     # Pass the values to the model and get the output
#     output = my_model(values)
#     return render_template('output.html', output=output)

@app.route('/analyze', methods=['POST'])
def analyze():
    xml_string = request.files['xml-file'] #.read().decode('utf-8')
    permissions_list = process_xml(xml_string)
    prediction = model_eval(permissions_list)
    if prediction == 1:
        output = 'Malware Application'
    else:
        output = 'Benign Application'
    output_class = 'success' if prediction == 0 else 'error'
    return render_template('output.html', permissions=permissions_list, output=output, output_class=output_class)

def process_xml(xml_string):
    #root = ET.fromstring(xml_string)
    tree = ET.parse(xml_string)
    root = tree.getroot()
    ns = {'android': 'http://schemas.android.com/apk/res/android'}
    permissions = root.findall('.//uses-permission')
    permissions_list = []
    for p in permissions:
        name = p.get('{' + ns['android'] + '}name')
        permissions_list.append(name)
    return permissions_list

def model_eval(permissions_list):
    arr = np.zeros(60)
    selected_features = ['android.permission.GET_ACCOUNTS', 'com.sonyericsson.home.permission.BROADCAST_BADGE', 'android.permission.READ_PROFILE', 'android.permission.READ_EXTERNAL_STORAGE', 'android.permission.RECEIVE_SMS', 'android.permission.WRITE_SETTINGS', 'com.google.android.providers.gsf.permission.READ_GSERVICES', 'android.permission.GET_TASKS', 'android.permission.WRITE_EXTERNAL_STORAGE', 'android.permission.RECORD_AUDIO', 'com.huawei.android.launcher.permission.CHANGE_BADGE', 'com.oppo.launcher.permission.READ_SETTINGS', 'com.android.launcher.permission.INSTALL_SHORTCUT', 'android.permission.CALL_PHONE', 'android.permission.WRITE_CONTACTS', 'android.permission.READ_PHONE_STATE', 'com.samsung.android.providers.context.permission.WRITE_USE_APP_FEATURE_SURVEY', 'android.permission.ACCESS_LOCATION_EXTRA_COMMANDS', 'android.permission.MOUNT_UNMOUNT_FILESYSTEMS', 'com.majeur.launcher.permission.UPDATE_BADGE', 'com.htc.launcher.permission.READ_SETTINGS', 'android.permission.ACCESS_WIFI_STATE', 'android.permission.READ_APP_BADGE', 'android.permission.USE_CREDENTIALS', 'android.permission.CHANGE_CONFIGURATION', 'com.anddoes.launcher.permission.UPDATE_COUNT', 'com.google.android.c2dm.permission.RECEIVE', 'android.permission.KILL_BACKGROUND_PROCESSES', 'com.sonymobile.home.permission.PROVIDER_INSERT_BADGE', 'com.sec.android.provider.badge.permission.READ', 'android.permission.WRITE_CALENDAR', 'android.permission.SEND_SMS', 'com.huawei.android.launcher.permission.WRITE_SETTINGS', 'android.permission.REQUEST_INSTALL_PACKAGES', 'android.permission.SET_WALLPAPER', 'com.oppo.launcher.permission.WRITE_SETTINGS', 'android.permission.RESTART_PACKAGES', 'me.everything.badger.permission.BADGE_COUNT_WRITE', 'android.permission.ACCESS_COARSE_LOCATION', 'android.permission.READ_LOGS', 'com.amazon.device.messaging.permission.RECEIVE', 'android.permission.SYSTEM_ALERT_WINDOW', 'android.permission.USE_FINGERPRINT', 'me.everything.badger.permission.BADGE_COUNT_READ', 'android.permission.CHANGE_WIFI_STATE', 'android.permission.READ_CONTACTS', 'com.android.vending.BILLING', 'android.permission.READ_CALENDAR', 'android.permission.RECEIVE_BOOT_COMPLETED', 'android.permission.ACCESS_FINE_LOCATION', 'android.permission.BLUETOOTH', 'android.permission.FOREGROUND_SERVICE', 'android.permission.BLUETOOTH_ADMIN', 'android.permission.NFC', 'com.android.launcher.permission.UNINSTALL_SHORTCUT', 'com.htc.launcher.permission.UPDATE_SHORTCUT', 'com.sec.android.provider.badge.permission.WRITE', 'com.google.android.finsky.permission.BIND_GET_INSTALL_REFERRER_SERVICE', 'com.huawei.android.launcher.permission.READ_SETTINGS', 'android.permission.READ_SMS']
    for p in permissions_list:
        if p in selected_features:
            index = selected_features.index(p)
            arr[index] = 1
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)
    return model.predict([arr])

if __name__ == '__main__':
    app.run(debug=True)