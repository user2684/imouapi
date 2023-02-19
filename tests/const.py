"""Constants."""

MOCK_RESPONSES = {
    "accessToken_ok": {
        "result": {
            "msg": "Operation is successful.",
            "code": "0",
            "data": {
                "expireTime": 190805,
                "currentDomain": "https://openapi-fk.easy4ip.com:443",
                "accessToken": "At_0000ea19a5687d45443399c8b8814e4a",
            },
        },
        "id": "14",
    },
    "accessToken_wrong_app_id": {"result": {"msg": "app ID id null.", "code": "OP1008"}, "id": "9"},
    "accessToken_expired": {
        "result": {"msg": "Token expired or does not exist, please get token again.", "code": "TK1002"},
        "id": "24",
    },
    "accessToken_invalid_response_1": {
        "result": {
            "msg": "Operation is successful.",
            "code": "0",
            "daXXXta": {
                "expireTime": 190805,
                "currentDomain": "https://openapi-fk.easy4ip.com:443",
                "accessTXXXXoken": "At_0000ea19a5687d45443399c8b8814e4a",
            },
        },
        "id": "14",
    },
    "accessToken_invalid_response_2": {
        "result": {
            "msg": "Operation is successful.",
            "data": {
                "expireTime": 190805,
                "currentDomain": "https://openapi-fk.easy4ip.com:443",
                "accessToken": "At_0000ea19a5687d45443399c8b8814e4a",
            },
        },
        "id": "14",
    },
    "deviceBaseList_ok": {
        "result": {
            "msg": "Operation is successful.",
            "code": "0",
            "data": {
                "count": 1,
                "deviceList": [
                    {
                        "channels": [{"channelName": "8L0DF93PAZ55FD2-1", "channelId": "0"}],
                        "deviceId": "8L0DF93PAZ55FD2",
                        "bindId": 1,
                        "aplist": [],
                    },
                ],
            },
        },
        "id": "26",
    },
    "deviceBaseList_wrong_device_id": {"result": {"msg": "No right, cannot operate.", "code": "OP1009"}, "id": "23"},
    "deviceBaseList_malformed": {
        "result": {
            "msg": "Operation is successful.",
            "code": "0",
            "data": {"count": 1},
        },
        "id": "26",
    },
    "deviceOpenList_ok": {
        "result": {
            "msg": "Operation is successful.",
            "code": "0",
            "data": {
                "count": 1,
                "deviceList": [
                    {
                        "channels": [{"channelName": "8L0DF93PAZ55FD2-1", "channelId": "0"}],
                        "deviceId": "8L0DF93PAZ55FD2",
                        "bindId": 1,
                        "aplist": [],
                    },
                ],
            },
        },
        "id": "26",
    },
    "deviceBaseDetailList_ok": {
        "result": {
            "msg": "Operation is successful.",
            "code": "0",
            "data": {
                "count": 1,
                "deviceList": [
                    {
                        "expandChanNum": "",
                        "trackFollowStatus": "",
                        "catalog": "IPC",
                        "httpPort": "80",
                        "privatePort": "37777",
                        "rtspPort": "554",
                        "deviceId": "8L0DF93PAZ55FD2",
                        "version": "2.680.0000000.25.R.220527",
                        "aplist": [],
                        "accessType": "PaaS",
                        "channels": [
                            {
                                "storageStrategyStatus": "notExist",
                                "picUrl": "",
                                "shareFunctions": "",
                                "cameraStatus": "off",
                                "remindStatus": "off",
                                "channelName": "8L0DF93PAZ55FD2-1",
                                "resolutions": [],
                                "ability": "",
                                "deviceId": "8L0DF93PAZ55FD2",
                                "channelId": "0",
                                "shareStatus": "",
                                "status": "online",
                            }
                        ],
                        "encryptMode": 1,
                        "tlsPrivatePort": "443",
                        "name": "webcam",
                        "deviceModel": "IPC-C22C",
                        "ability": "WLAN,Siren,MT,HSEncrypt,CloudStorage,LocalStorage,PlaybackByFilename,BreathingLight,RD,LocalRecord,XUpgrade,Auth,ModifyPassword,LocalStorageEnable,RTSV1,PBSV1,TSV1,ESV1,TimeFormat,Reboot,InfraredLight,AbAlarmSound,SCCode,RDV2,DaySummerTime,WeekSummerTime,TLSEnable,TimingGraphics,TCM,LRRF,CDD,CDDV2,DLS,CDD-OSS,CDD-OBS,CDD-US3,CDD-BOS,CDD-COS,AUTODSTV2,AlarmMD,AudioEncodeControlV2,FrameReverse,RemoteControl,MDW,MDS,HeaderDetect,WifiReport,WideDynamic,CheckAbDecible,CCSC,RQD,CLOUDAIV1,EventFilter,RSRS,WIFI,NVM",  # noqa: E501
                        "brand": "easy4Ip",
                        "playToken": "8YdkSe1O9=",
                        "shareStatus": "owner",
                        "status": "online",
                    }
                ],
            },
        },
        "id": "21",
    },
    "deviceBaseDetailList_missing_data": {
        "result": {
            "msg": "Operation is successful.",
            "code": "0",
            "data": {
                "count": 1,
                "deviceList": [
                    {
                        "expandChanNum": "",
                        "trackFollowStatus": "",
                        "catalog": "IPC",
                        "httpPort": "80",
                        "privatePort": "37777",
                        "rtspPort": "554",
                        "deviceId": "8L0DF93PAZ55FD2",
                        "aplist": [],
                        "accessType": "PaaS",
                        "channels": [
                            {
                                "storageStrategyStatus": "notExist",
                                "picUrl": "",
                                "shareFunctions": "",
                                "cameraStatus": "off",
                                "remindStatus": "off",
                                "channelName": "8L0DF93PAZ55FD2-1",
                                "resolutions": [],
                                "ability": "",
                                "deviceId": "8L0DF93PAZ55FD2",
                                "channelId": "0",
                                "shareStatus": "",
                                "status": "online",
                            }
                        ],
                        "encryptMode": 1,
                        "tlsPrivatePort": "443",
                        "name": "webcam",
                        "deviceModel": "IPC-C22C",
                        "ability": "WLAN,Siren,MT,HSEncrypt,CloudStorage,LocalStorage,PlaybackByFilename,BreathingLight,RD,LocalRecord,XUpgrade,Auth,ModifyPassword,LocalStorageEnable,RTSV1,PBSV1,TSV1,ESV1,TimeFormat,Reboot,InfraredLight,AbAlarmSound,SCCode,RDV2,DaySummerTime,WeekSummerTime,TLSEnable,TimingGraphics,TCM,LRRF,CDD,CDDV2,DLS,CDD-OSS,CDD-OBS,CDD-US3,CDD-BOS,CDD-COS,AUTODSTV2,AlarmMD,AudioEncodeControlV2,FrameReverse,RemoteControl,MDW,MDS,HeaderDetect,WifiReport,WideDynamic,CheckAbDecible,CCSC,RQD,CLOUDAIV1,EventFilter,RSRS,WIFI",  # noqa: E501
                        "brand": "easy4Ip",
                        "playToken": "8YdkSe1O9=",
                        "shareStatus": "owner",
                        "status": "online",
                    }
                ],
            },
        },
        "id": "21",
    },
    "deviceOpenDetailList_ok": {
        "result": {
            "msg": "Operation is successful.",
            "code": "0",
            "data": {
                "count": 1,
                "deviceList": [
                    {
                        "expandChanNum": "",
                        "trackFollowStatus": "",
                        "catalog": "IPC",
                        "httpPort": "80",
                        "privatePort": "37777",
                        "rtspPort": "554",
                        "deviceId": "8L0DF93PAZ55FD2",
                        "version": "2.680.0000000.25.R.220527",
                        "aplist": [],
                        "accessType": "PaaS",
                        "channels": [
                            {
                                "storageStrategyStatus": "notExist",
                                "picUrl": "",
                                "shareFunctions": "",
                                "cameraStatus": "off",
                                "remindStatus": "off",
                                "channelName": "8L0DF93PAZ55FD2-1",
                                "resolutions": [],
                                "ability": "",
                                "deviceId": "8L0DF93PAZ55FD2",
                                "channelId": "0",
                                "shareStatus": "",
                                "status": "online",
                            }
                        ],
                        "encryptMode": 1,
                        "tlsPrivatePort": "443",
                        "name": "webcam",
                        "deviceModel": "IPC-C22C",
                        "ability": "WLAN,Siren,MT,HSEncrypt,CloudStorage,LocalStorage,PlaybackByFilename,BreathingLight,RD,Siren,LocalRecord,XUpgrade,Auth,ModifyPassword,LocalStorageEnable,RTSV1,PBSV1,TSV1,ESV1,TimeFormat,Reboot,InfraredLight,AbAlarmSound,SCCode,RDV2,DaySummerTime,WeekSummerTime,TLSEnable,TimingGraphics,TCM,LRRF,CDD,CDDV2,DLS,CDD-OSS,CDD-OBS,CDD-US3,CDD-BOS,CDD-COS,AUTODSTV2,AlarmMD,AudioEncodeControlV2,FrameReverse,RemoteControl,MDW,MDS,HeaderDetect,WifiReport,WideDynamic,CheckAbDecible,CCSC,RQD,CLOUDAIV1,EventFilter,RSRS,WIFI",  # noqa: E501
                        "brand": "easy4Ip",
                        "playToken": "8YdkSe1O9=",
                        "shareStatus": "owner",
                        "status": "online",
                    }
                ],
            },
        },
        "id": "21",
    },
    "deviceOnline_ok": {
        "result": {
            "msg": "Operation is successful.",
            "code": "0",
            "data": {"channels": [{"channelId": "0", "onLine": "1"}], "deviceId": "8L0DF93PAZ55FD2", "onLine": "1"},
        },
        "id": "8",
    },
    "deviceOnline_malformed": {
        "result": {
            "msg": "Operation is successful.",
            "code": "0",
            "data": {"channels": [{"channelId": "0", "onLine": "1"}], "deviceId": "8L0DF93PAZ55FD2"},
        },
        "id": "8",
    },
    "getDeviceCameraStatus_ok": {
        "result": {
            "msg": "Operation is successful.",
            "code": "0",
            "data": {"enableType": "headerDetect", "status": "on"},
        },
        "id": "22",
    },
    "setDeviceCameraStatus_ok": {"result": {"msg": "Operation is successful.", "code": "0"}, "id": "32"},
    "setDeviceCameraStatus_error": {"result": {"msg": "Error.", "code": "200"}, "id": "32"},
    "getAlarmMessage_ok": {
        "result": {
            "msg": "Operation is successful.",
            "code": "0",
            "data": {
                "alarms": [
                    {
                        "msgType": "human",
                        "alarmId": "1623428357863536",
                        "name": "8L0DF93PAZ55FD2-1",
                        "time": 1664127393,
                        "localDate": "2022-09-25 17:36:33",
                        "type": "120",
                        "thumbUrl": "xxxx",
                        "deviceId": "8L0DF93PAZ55FD2",
                        "picurlArray": ["xxxx"],
                        "channelId": "0",
                        "token": "12375a23d4e64c2f84120bc76a7fa6c5_big",
                    },
                    {
                        "msgType": "human",
                        "alarmId": "1640588402878576",
                        "name": "8L0DF93PAZ55FD2-1",
                        "time": 1664021890,
                        "localDate": "2022-09-24 12:18:10",
                        "type": "120",
                        "thumbUrl": "xxx",
                        "deviceId": "8L0DF93PAZ55FD2",
                        "picurlArray": ["xxxx"],
                        "channelId": "0",
                        "token": "adf288fd0a8a47d6848a2b67d335f473_big",
                    },
                ],
                "count": 2,
                "nextAlarmId": 1489575655024752,
            },
        },
        "id": "28",
    },
    "getAlarmMessage_malformed": {
        "result": {
            "msg": "Operation is successful.",
            "code": "0",
            "data": {
                "test": "asds",
            },
        },
        "id": "28",
    },
    "listDeviceAbility_ok": {
        "result": {
            "msg": "Operation is successful.",
            "code": "0",
            "data": {
                "deviceList": [
                    {
                        "channels": [
                            {
                                "channelAbility": "WLAN,MT,HSEncrypt,CloudStorage,LocalStorage,PlaybackByFilename,BreathingLight,RD,LocalRecord,XUpgrade,Auth,ModifyPassword,LocalStorageEnable,Siren,RTSV1,PBSV1,TSV1,ESV1,TimeFormat,PlaySound,Reboot,LinkDevAlarm,AbAlarmSound,SCCode,RDV2,DaySummerTime,WeekSummerTime,TLSEnable,TimingGraphics,CK,LRRF,CDD,CDDV2,DLS,CDD-OSS,CDD-OBS,CDD-US3,CDD-BOS,CDD-COS,AUTODSTV2,AlarmMD,AudioEncodeControlV2,FrameReverse,RemoteControl,MDW,MDS,HeaderDetect,WifiReport,WideDynamic,CheckAbDecible,NVM,CCSC,RQD,CLOUDAIV1,EventFilter,RSRS,AudioTalk,WIFI",  # noqa: E501
                                "channelId": "0",
                            }
                        ],
                        "aps": [],
                        "ability": "WLAN,MT,HSEncrypt,CloudStorage,LocalStorage,PlaybackByFilename,BreathingLight,RD,LocalRecord,XUpgrade,Auth,ModifyPassword,LocalStorageEnable,Siren,RTSV1,PBSV1,TSV1,ESV1,TimeFormat,PlaySound,Reboot,LinkDevAlarm,AbAlarmSound,SCCode,RDV2,DaySummerTime,WeekSummerTime,TLSEnable,TimingGraphics,CK,LRRF,CDD,CDDV2,DLS,CDD-OSS,CDD-OBS,CDD-US3,CDD-BOS,CDD-COS,AUTODSTV2,AlarmMD,AudioEncodeControlV2,FrameReverse,RemoteControl,MDW,MDS,HeaderDetect,WifiReport,WideDynamic,CheckAbDecible,NVM,CCSC,RQD,CLOUDAIV1,EventFilter,RSRS,AudioTalk,WIFI",  # noqa: E501
                        "deviceId": "8L0DF93PAZ55FD2",
                    }
                ],
            },
        },
        "id": "28",
    },
    "deviceStorage_ok": {
        "result": {
            "msg": "Operation is successful.",
            "code": "0",
            "data": {
                "totalBytes": 31254904832,
                "usedBytes": 27553759232,
            },
        },
        "id": "28",
    },
    "getNightVisionMode_ok": {
        "result": {
            "msg": "Operation is successful.",
            "code": "0",
            "data": {
                "mode": "Intelligent",
                "modes": ["Intelligent", "FullColor", "Infrared", "Off"],
            },
        },
        "id": "28",
    },
    "setNightVisionMode_ok": {
        "result": {
            "msg": "Operation is successful.",
            "code": "0",
            "data": {},
        },
        "id": "28",
    },
    "getMessageCallback_ok": {
        "result": {
            "msg": "Operation is successful.",
            "code": "0",
            "data": {
                "callbackFlag": "",
                "callbackUrl": "",
                "status": "off",
            },
        },
        "id": "28",
    },
    "setMessageCallbackOn_ok": {
        "result": {
            "msg": "Operation is successful.",
            "code": "0",
            "data": {},
        },
        "id": "28",
    },
    "setMessageCallbackOff_ok": {
        "result": {
            "msg": "Operation is successful.",
            "code": "0",
            "data": {},
        },
        "id": "28",
    },
    "restartDevice_ok": {
        "result": {
            "msg": "The operation was successful.",
            "code": "0",
        },
        "id": "28",
    },
    "deviceSdcardStatus_ok": {
        "result": {
            "msg": "The operation was successful.",
            "code": "0",
            "data": {
                "status": "normal",
            },
        },
        "id": "28",
    },
    "devicePTZInfo_ok": {
        "result": {
            "msg": "The operation was successful.",
            "code": "0",
            "data": {"h": "0.9", "v": "0.2", "z": "0.0"},
        },
        "id": "d5c287b4-5b2f-4f03-baf5-8032c5c354af",
    },
    "controlLocationPTZ_ok": {
        "result": {
            "msg": "The operation was successful.",
            "code": "0",
        },
        "id": "d5c287b4-5b2f-4f03-baf5-8032c5c354af",
    },
    "controlMovePTZ_ok": {
        "result": {
            "msg": "The operation was successful.",
            "code": "0",
        },
        "id": "d5c287b4-5b2f-4f03-baf5-8032c5c354af",
    },
    "setDeviceSnapEnhanced_ok": {
        "result": {
            "msg": "The operation was successful.",
            "code": "0",
            "data": {
                "url": "https://lechangecloud.oss-cn-hangzhou.aliyuncs.com/lechange/MEGREZ0000001842_img/Alarm/0/956fe604722b45fba0e098ba6eae3178.jpg?Expires=1603974760&OSSAccessKeyId=LTAIP4igXeEjYBoG&Signature=gtfNjV7MJI%2BC%2By6cciWYXiDv4LI%3D"  # noqa: E501
            },
        },
        "id": "ad9a278f-bedd-4c06-ad4a-ea0a971836d1",
    },
    "bindDeviceLive_ok": {
        "result": {
            "msg": "The operation was successful.",
            "code": "0",
            "data": {
                "liveType": 1,
                "coverUpdate": 90,
                "streams": [
                    {
                        "coverUrl": "http://livecloudpic.lechange.cn/LCO/MEGREZ0000001842/0/1/20201022T113914/dev_MEGREZ0000001842_20201022T113914.jpg",  # noqa: E501
                        "streamId": 1,
                        "hls": "http://cmgw-vpc.lechange.com:8888/LCO/MEGREZ0000001842/0/1/20201022T113914/dev_MEGREZ0000001842_20201022T113914.m3u8",  # noqa: E501
                    }
                ],
                "liveToken": "57877dd6774f4cbeb657568be0b7a621",
                "job": [{"period": "always", "status": True}],
                "deviceId": "MEGREZ0000001842",
                "liveStatus": 1,
                "channelId": "0",
            },
        },
        "id": "a25f887f-33f0-44ef-9ed3-f60f83193482",
    },
    "getLiveStreamInfo_ok": {
        "result": {
            "msg": "The operation was successful.",
            "code": "0",
            "data": {
                "streams": [
                    {
                        "streamId": 1,
                        "liveToken": "57877dd6774f4cbeb657568be0b7a621",
                        "hls": "http://cmgw-vpc.lechange.com:8888/LCO/MEGREZ0000001842/0/1/20201022T113914/dev_MEGREZ0000001842_20201022T113914.m3u8",  # noqa: E501
                        "status": "0",
                    },
                    {
                        "streamId": 0,
                        "liveToken": "57877dd6774f4cbeb657568be0b7a621",
                        "hls": "http://cmgw-vpc.lechange.com:8888/LCO/MEGREZ0000001842/0/0/20201022T113914/dev_MEGREZ0000001842_20201022T113914.m3u8",  # noqa: E501
                        "status": "0",
                    },
                    {
                        "streamId": 1,
                        "liveToken": "57877dd6774f4cbeb657568be0b7a621",
                        "hls": "https://cmgw-vpc.lechange.com:8890/LCO/MEGREZ0000001842/0/1/20201022T113914/dev_MEGREZ0000001842_20201022T113914.m3u8?proto=https",  # noqa: E501
                        "status": "0",
                    },
                    {
                        "streamId": 0,
                        "liveToken": "57877dd6774f4cbeb657568be0b7a621",
                        "hls": "https://cmgw-vpc.lechange.com:8890/LCO/MEGREZ0000001842/0/0/20201022T113914/dev_MEGREZ0000001842_20201022T113914.m3u8?proto=https",  # noqa: E501
                        "status": "0",
                    },
                ]
            },
        },
        "id": "051824b1-9655-4755-9cc2-adcc9ab5fef1",
    },
    "liveList_ok": {
        "result": {
            "msg": "successful operation。",
            "code": "0",
            "data": {
                "lives": [
                    {
                        "liveType": 2,
                        "coverUpdate": 90,
                        "streams": [
                            {
                                "coverUrl": "http://alhlscdn.lechange.cn/LCO/3f35d2d41758dc707e614c2999f8b922/20190429155036/stream_20190429155036_71e53mz34pcaprgb.jpg",  # noqa: E501
                                "hls": "http://alhlsgw.lechange.com:9001/LCO/3f35d2d41758dc707e614c2999f8b922/20190429155036/stream_20190429155036_71e53mz34pcaprgb.m3u8",  # noqa: E501
                            }
                        ],
                        "liveToken": "stream_20190429155036_71e53mz34pcaprgb",
                        "job": [{"period": "always", "status": True}],
                        "liveStatus": 1,
                    },
                    {
                        "liveType": 2,
                        "coverUpdate": 90,
                        "streams": [
                            {
                                "coverUrl": "http://alhlscdn.lechange.cn/LCO/aaf71e228f1da90232c0ac87803ce4b6/20191023171615/stream_20191023171615_qahzm4ml2bk93l72.jpg",  # noqa: E501
                                "hls": "http://alhlsgw.lechange.com:9001/LCO/aaf71e228f1da90232c0ac87803ce4b6/20191023171615/stream_20191023171615_qahzm4ml2bk93l72.m3u8",  # noqa: E501
                            }
                        ],
                        "liveToken": "stream_20191023171615_qahzm4ml2bk93l72",
                        "job": [{"period": "always", "status": True}],
                        "liveStatus": 1,
                    },
                    {
                        "liveType": 1,
                        "coverUpdate": 90,
                        "streams": [
                            {
                                "coverUrl": "http://livecloudpic.lechange.cn/LCO/MEGREZ0000001375/0/0/20200907T032254/dev_MEGREZ0000001375_20200907T032254.jpg",  # noqa: E501
                                "streamId": 0,
                                "hls": "https://cmgw-vpc.lechange.com:8890/LCO/MEGREZ0000001375/0/0/20200907T032254/dev_MEGREZ0000001375_20200907T032254.m3u8?proto=https",  # noqa: E501
                            },
                            {
                                "coverUrl": "http://livecloudpic.lechange.cn/LCO/MEGREZ0000001375/0/0/20200907T032254/dev_MEGREZ0000001375_20200907T032254.jpg",  # noqa: E501
                                "streamId": 1,
                                "hls": "https://cmgw-vpc.lechange.com:8890/LCO/MEGREZ0000001375/0/1/20200907T032254/dev_MEGREZ0000001375_20200907T032254.m3u8?proto=https",  # noqa: E501
                            },
                            {
                                "coverUrl": "http://livecloudpic.lechange.cn/LCO/MEGREZ0000001375/0/0/20200907T032254/dev_MEGREZ0000001375_20200907T032254.jpg",  # noqa: E501
                                "streamId": 0,
                                "hls": "http://cmgw-vpc.lechange.com:8888/LCO/MEGREZ0000001375/0/0/20200907T032254/dev_MEGREZ0000001375_20200907T032254.m3u8",  # noqa: E501
                            },
                            {
                                "coverUrl": "http://livecloudpic.lechange.cn/LCO/MEGREZ0000001375/0/0/20200907T032254/dev_MEGREZ0000001375_20200907T032254.jpg",  # noqa: E501
                                "streamId": 1,
                                "hls": "http://cmgw-vpc.lechange.com:8888/LCO/MEGREZ0000001375/0/1/20200907T032254/dev_MEGREZ0000001375_20200907T032254.m3u8",  # noqa: E501
                            },
                        ],
                        "liveToken": "63813c4aa4b442069748437c1bd0b749",
                        "job": [{"period": "always", "status": True}],
                        "deviceId": "MEGREZ0000001375",
                        "liveStatus": 1,
                        "channelId": "0",
                    },
                    {
                        "liveType": 1,
                        "coverUpdate": 90,
                        "streams": [
                            {
                                "coverUrl": "http://livecloudpic.lechange.cn/LCO/MEGREZ0000001842/0/1/20201022T113914/dev_MEGREZ0000001842_20201022T113914.jpg",  # noqa: E501
                                "streamId": 1,
                                "hls": "http://cmgw-vpc.lechange.com:8888/LCO/MEGREZ0000001842/0/1/20201022T113914/dev_MEGREZ0000001842_20201022T113914.m3u8",  # noqa: E501
                            },
                            {
                                "coverUrl": "http://livecloudpic.lechange.cn/LCO/MEGREZ0000001842/0/1/20201022T113914/dev_MEGREZ0000001842_20201022T113914.jpg",  # noqa: E501
                                "streamId": 0,
                                "hls": "http://cmgw-vpc.lechange.com:8888/LCO/MEGREZ0000001842/0/0/20201022T113914/dev_MEGREZ0000001842_20201022T113914.m3u8",  # noqa: E501
                            },
                            {
                                "coverUrl": "http://livecloudpic.lechange.cn/LCO/MEGREZ0000001842/0/1/20201022T113914/dev_MEGREZ0000001842_20201022T113914.jpg",  # noqa: E501
                                "streamId": 1,
                                "hls": "https://cmgw-vpc.lechange.com:8890/LCO/MEGREZ0000001842/0/1/20201022T113914/dev_MEGREZ0000001842_20201022T113914.m3u8?proto=https",  # noqa: E501
                            },
                            {
                                "coverUrl": "http://livecloudpic.lechange.cn/LCO/MEGREZ0000001842/0/1/20201022T113914/dev_MEGREZ0000001842_20201022T113914.jpg",  # noqa: E501
                                "streamId": 0,
                                "hls": "https://cmgw-vpc.lechange.com:8890/LCO/MEGREZ0000001842/0/0/20201022T113914/dev_MEGREZ0000001842_20201022T113914.m3u8?proto=https",  # noqa: E501
                            },
                        ],
                        "liveToken": "57877dd6774f4cbeb657568be0b7a621",
                        "job": [{"period": "always", "status": True}],
                        "deviceId": "MEGREZ0000001842",
                        "liveStatus": 1,
                        "channelId": "0",
                    },
                ],
                "count": 4,
            },
        },
        "id": "1cd43fdb-810b-44f4-8652-9d232dd95f1b",
    },
    "unbindLive_ok": {
        "id": "78d81c6a-3968-40dc-8854-ccaee5d6ab03",
        "result": {
            "code": "0",
            "msg": "The operation was successful",
        },
    },
    "getDevicePowerInfo_ok": {
        "id": "b8f45dbb-79ad-4a7e-8b24-7eb618c5191f",
        "result": {
            "code": "0",
            "msg": "The operation was successful",
            "data": {
                "electricitys": [
                    {
                        "alkElec": "90",
                        "litElec": "90",
                        "electric": "89",
                        "type": "battery",
                    }
                ]
            },
        },
    },
}
