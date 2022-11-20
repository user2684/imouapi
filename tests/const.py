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
}
