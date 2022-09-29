"""Constants for imouapi."""

# default url to connect to
API_URL = "https://openapi.easy4ip.com/openapi"

# default connection timeout
DEFAULT_TIMEOUT = 10

# Imou capabilities and their description (https://open.imoulife.com/book/en/faq/ability.html)
IMOU_CAPABILITIES = {
    "WLAN": "Support access to wireless local area network",
    "DHP2P": "Support Dahua P2P Service",
    "MT": "Support streaming media forwarding capability",
    "NetSDK": "Support NetSDK",
    "HSEncrypt": "Support Huashi WeChat Stream Encryption",
    "CloudStorage": "Support for cloud storage of China Vision WeChat platform",
    "DPS": "Support automatic modification of device password according to DPS (device password seed)",
    "AGW": "Support Accessory Access, that is, the device is an Accessory Gateway (AccessoryGateway)",
    "LocalStorage": "Support device local storage, such as SD card or hard disk",
    "LocalStorageEnable": "Support device local storage enable switch",
    "PlaybackByFilename": "The device supports playback based on the file name",
    "BreathingLight": "The device has a breathing light (indicator light)",
    "ShineLight": "Equipment with lighting",
    "RegCode": "The device has a verification code",
    "RD": "The device has remote debugging capabilities and supports log extraction (RemoteDebug)",
    "RDV2": "Support RD capability, support data burying point control, support debugging log upload",
    "FaceCapture": "Face Recognition Capture Capability",
    "CK": "The device supports CustomKey (CustomKey)",
    "NMPv1": "The device supports network music playback (NetworkMusicPlayer)",
    "NMPRC": "The device supports network song playback remote control (NetworkMusicPlayerRemoteControl)",
    "TextPush": "Device supports text push",
    "SLAlarm": "The device supports sound and light alarm (sound and light alarm)",
    "LocalRecord": "Support device local recording settings",
    "SR": "Device supports speech recognition (speechrecognition)",
    "QA": "Voice Q&A Tuning Function",
    "AntiAddiction": "Anti-addiction",
    "AntiAddictionSet": "Anti-Addiction Set",
    "AntiAddictionForbid": "Mandatory anti-addiction lock",
    "XUpgrade": "Cloud Upgrade",
    "AGWDisarm": "Gateway alarm de-configuration",
    "REMINDER": "Schedule Reminder Ability",
    "Auth": "Device end loopback RTSP requires authentication",
    "ModifyPassword": "Support user name password information verification and password modification",
    "TimeSync": "Device supports time synchronization",
    "BRestartFormat": "Need to restart after formatting",
    "Siren": "Siren",
    "LinkageSiren": "Alarm Linkage Siren",
    "SirenTime": "Support siren duration configuration",
    "WhiteLight": "White Light",
    "WLV2": "White light, does not support brightness adjustment ability",
    "InfraredLight": "Infrared Light",
    "SearchLight": "Searchlight",
    "NonAccessoriesAdd": "Gateway does not support C-side signaling to add accessories",
    "CallAbility": "Support Call Ability",
    "CAV2": "Support call ability, and can choose to play custom ringtones when rejecting a call",
    "NoVA": "Does not support Voice Announcements",
    "Dormant": "Sleepable, with wake-up and sleep states",
    "RTSV1": "Real-time streaming supports private protocol to pull streaming",
    "PBSV1": "Playback stream supports private protocol to pull stream",
    "TSV1": "Voice intercom streaming supports private protocol to pull streaming",
    "RTSV2": "Real-time streaming supports private protocol streaming, supports dynamic port modification",
    "PBSV2": "The playback stream supports private protocol streaming and supports dynamic port modification",
    "TSV2": "Voice intercom streaming supports private protocol streaming, supports dynamic port modification",
    "ESV1": "Support 0x95 extension header encryption",
    "CallByRtsp": "Indicates that answering and hanging up can be implemented directly based on the RTSP protocol",
    "DaySummerTime": "The device supports daily summer time",
    "WeekSummerTime": "The device supports weekly daylight saving time",
    "SummerTimeOffset": "The device supports summer time offset",
    "TAP": "Time supports 12-hour and 24-hour switching",
    "SceneMode": "Support arming and disarming at home mode configuration",
    "SMT": "Support arming and disarming at home mode time period",
    "TimeFormat": "Support time format setting",
    "DDT": "Support arming delay time configuration",
    "ACT": "Support alarm duration configuration",
    "SIMCA": "SIM Card Related",
    "OpenDoorByFace": "Face to open the door",
    "OpenDoorByTouch": "Touch to open the door",
    "Ring": "Only supports ringtone settings",
    "CustomRing": "Custom Ring",
    "CustomReply": "Custom reply settings, corresponding to the reply type",
    "LinkDevAlarm": "Associated Device Alarm",
    "LinkAccDevAlarm": "Associated accessories alarm",
    "AbAlarmSound": "Abnormal alarm sound",
    "PlaySound": "Device sound switch capability",
    "PlaySoundModify": "Device sound adjustment capability",
    "DLOCS": "Door lock switch status",
    "CheckAbDecible": "Abnormal detection tone decibel threshold",
    "Reboot": "The device supports restarting",
    "SCCode": "The device supports SC security code",
    "RingAlarmSound": "Doorbell volume setting",
    "RASV1": "Unmute volume, 1-5 gears, default 4 gears",
    "AccessoryAlarmSound": "Alarm gateway accessories alarm sound settings",
    "InstantDisAlarm": "Support one-key disarming capability",
    "IDAP": "Support periodic disarming",
    "DeviceAlarmSound": "Device alarm sound settings",
    "AX": "All-in-one security machine",
    "TimingGraphics": "Support the device to capture multiple pictures",
    "TalkV2": "Support device intercom parameter is 2",
    "ErrReport": "Abnormal report fault code",
    "DevReset": "Device Reset",
    "TLSEnable": "Support TLS transmission",
    "TCM": "Support Three code megre",
    "NEC": "The device supports No encrypt capture",
    "ME": "Support Message Engine",
    "EWL": "Event whitelist event whitelist",
    "TSVO": "Private protocol exclusive link",
    "TSVS": "Private Protocol Shared Link",
    "DLS": "Direct log storage",
    "DHPenetrate": "Dahua 3rd Generation Protocol Transparent Transmission",
    "MesTrans": "Message Subscription Transparent Transmission",
    "PicTrans": "Picture subscription transparent transmission",
    "DataTrans": "Data Subscription Transparent Transmission",
    "LRRF": "Local recording supports fast forward LocalRecordReplayForward",
    "LRRB": "Local recording supports fast rewind LocalRecordReplayBackward (only private protocol support)",
    "UPNP": "The device supports UPNP mapping",
    "AH": "The device supports Anheng encryption",
    "IOTTUNNEL": "Device supports IoT tunnel",
    "AlarmMD": "Support motion detection alarm",
    "PTZ": "Support PTZ and digital zoom operation",
    "PT": "Support PTZ operation",
    "PT1": "Ranger2 only supports 4-way pan/tilt capability. Does not support zoom in and out Does not support\
        digital zoom operation",
    "PT2": "Only supports pan/tilt capabilities that can rotate in two directions. Does not support zoom in and \
        zoom out. Does not support digital zoom operations",
    "AudioEncodeOff": "No audio input",
    "AudioEncodeControl": "Support audio encoding control (on or off)",
    "AudioEncodeControlV2": "Supports audio encoding control (on or off), only affects real-time video, video \
        audio, and does not affect intercom audio control",
    "FrameReverse": "Support screen flip",
    "RemoteControl": "Support remote linkage",
    "Panorama": "Support Panorama",
    "PanoOrder": "After the screen is flipped, the panorama points are uploaded in reverse order",
    "WideAngle": "Wide Angle Capability",
    "MDW": "motion-detect-window supports motion detection window settings",
    "MDS": "motion-detect-sensitive supports motion detection sensitivity setting",
    "HeaderDetect": "Support head detection",
    "FaceDetect": "Support face detection (pre-smart)",
    "CollectionPoint": "Support collection points",
    "TimedCruise": "Support timed cruise",
    "SmartLocate": "Support listening position recognition",
    "SmartTrack": "Support Smart Tracking",
    "NumberStat": "Passing Passenger Flow Data Collection",
    "ManNumDec": "Regional passenger flow data collection",
    "AlarmPIR": "With PIR capability, without PIR enable switch, without PIR detection area setting",
    "AlarmPIRV2": "With PIR capability, with PIR enable switch, without PIR detection area setting",
    "HUBAlarmPIRV2": "HUB devices have PIR capability, PIR enable switch, and no PIR detection area setting",
    "AlarmPIRV3": "PIR capability, PIR enable switch, PIR detection area setting",
    "AlarmPIRV4": "PIR capability, no PIR enable switch, PIR detection area setting, no alarm message",
    "MobileDetect": "Mobile Detection (Merged with PIR)",
    "ZoomFocus": "Support zoom focus",
    "CloseCamera": "Support to close the camera",
    "HoveringAlarm": "Hovering Alarm",
    "HAV2": "Wandering alarm V2, supports unified detection distance setting and stay time setting",
    "HAV3": "Wandering alarm V3, V2 downgraded version, does not support the length of stay immediate setting",
    "HAV4": "Wandering alarm V4, V3 downgrade version, does not support distance detection",
    "BeOpenedDoor": "Normally open the door, namely successfully open the door (K5 battery door lock)",
    "RtFaceDetect": "Smart after face detection",
    "RtFaceCompa": "Smart after face comparison",
    "CloseDormant": "Can close dormant",
    "ElecReport": "Support power report",
    "WifiReport": "Support wifi report",
    "HeatMap": "Thermal Analysis",
    "AiHumanCar": "Humanoid Vehicle Intelligence",
    "AiHuman": "Humanoid Intelligence",
    "AiCar": "Vehicle Intelligence",
    "WideDynamic": "Wide Dynamic",
    "WDRV2": "Wide dynamic v2, support 0-100 gear configuration",
    "TalkSoundModify": "Intercom volume adjustment",
    "VideoMotionSMD": "Motion detection SMD capability, when the device has this capability, motion detection \
        events include human figures and vehicles",
    "ChnLocalStorage": "Support channel local storage, such as SD card or hard disk",
    "OSD": "Support video channel OSD configuration",
    "1080P": "Maximum capability set supported by the device",
    "MSS": "Staff retention information, support ManNumDetection reporting and query",
    "ChnErrReport": "Abnormal report fault code",
    "CCR": "Channel custom ringtone ChanCustomRing",
    "CLW": "Channel alarm linkage white light ChanLinkageWhiteLight",
    "CLDA": "Channel-associated device alarm ChanLinkDevAlarm",
    "NVM": "Night Vision Mode",
    "LEDS": "Fill light sensitivity",
    "ELCM": "Electricity Mode",
    "RL": "Video duration",
    "CCS": "Privacy time period",
    "CCSS": "Privacy Time Zone Switch",
    "SDLIFE": "SD card life",
    "PostFaceDetect": "Support face detection (post-intelligence)",
    "PostFaceAnalysis": "Support face recognition (post-intelligence)",
    "OPLOG": "Support smart lock user operation record query",
    "INTERALARM": "Support alarm interval time",
    "RUNLOG": "Support equipment operation record reporting",
    "LEDSW": "Fill light switch",
    "DEVSHA": "Support Device Shadow",
    "AudioTalk": "Support voice intercom",
    "AudioTalkV1": "Support voice intercom",
    "AlarmSound": "Support alarm sound setting",
    "Electric": "Device Support Battery Capability",
    "WIFI": "The device supports WIFI capability",
}


# Imou switches and their description (https://open.imoulife.com/book/en/faq/feature.html)
IMOU_SWITCHES = {
    "localRecord": "Local Record",
    "motionDetect": "Motion detection",
    "faceCapture": "Automatic face capture",
    "speechRecognition": "device speech recognition",
    "breathingLight": "Breathing light",
    "smartLocate": "Listening and positioning",
    "smartTrack": "Smart Tracking",
    "localAlarmRecord": "Local alarm linkage recording	channel, the enable switch depends on the motion \
        detection enable switch",
    "regularCruise": "Scheduled Cruise",
    "headerDetect": "Head Detection",
    "numberStat": "Cross-line passenger flow statistics",
    "manNumDec": "Regional passenger flow statistics",
    "alarmPIR": "PIR alarm",
    "autoZoomFocus": "Automatic zoom focus",
    "audioEncodeControl": "Support audio encoding control (on or off)",
    "aecv3": "Support audio encoding control (on or off)",
    "faceDetect": "Face Detection",
    "localStorageEnable": "Device local storage",
    "whiteLight": "White Light",
    "linkageWhiteLight": "alarm linkage white light",
    "linkageSiren": "alarm linkage siren",
    "infraredLight": "infrared light",
    "searchLight": "Searchlight",
    "hoveringAlarm": "Hovering Alarm",
    "beOpenedDoor": "Normally open the door, namely successfully open the door",
    "closeCamera": "close camera",
    "mobileDetect": "Mobile detection",
    "rtFaceDetect": "Smart after face detection",
    "rtFaceCompa": "Smart after face comparison",
    "closeDormant": "Sleepable devices support close dormancy",
    "heatMap": "Heat analysis",
    "tlsEnable": "easy4ip dedicated tls enable switch",
    "aiHumanCar": "Humanoid Vehicle Intelligent Enable Switch",
    "aiHuman": "Humanoid Smart Enable Switch",
    "aiCar": "Vehicle Intelligent Enable Switch",
    "openDoorByFace": "Face open door enable switch",
    "openDoorByTouch": "Touch to open the door enable switch",
    "linkDevAlarm": "Associated device alarm",
    "linkAccDevAlarm": "Associated accessory alarm",
    "abAlarmSound": "Abnormal alarm sound",
    "playSound": "Device sound",
    "wideDynamic": "Wide Dynamic",
    "smdHuman": "SMD People",
    "smdVehicle": "SMD car",
    "instantDisAlarm": "One-click disarming",
    "periodDisAlarm": "Period disarm",
    "ccss": "Privacy Plan Switch",
    "inll": "Indicator light linkage",
    "ledsw": "Fill light switch",
}

SUPPORTED_SWITCHES = ["motionDetect", "headerDetect", "abAlarmSound", "breathingLight"]
SWITCH_ICONS = {
    "motionDetect": "mdi:motion-sensor",
    "headerDetect": "mdi:human",
    "abAlarmSound": "mdi:alarm-bell",
    "breathingLight": "mdi:television-ambient-light",
}

# sensors supported by this library
SENSORS = {"lastAlarm": "Last alarm"}
SENSOR_ICONS = {"lastAlarm": "mdi:timer"}

# sensors supported by this library
BINARY_SENSORS = {"online": "Online"}
BINARY_SENSOR_ICONS = {"online": "mdi:lan-connect"}