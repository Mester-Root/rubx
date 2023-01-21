#!/bin/python

class Device(dict):
    defaultDevice: dict = {
        'app_version'           :   'MA_2.9.8',
        'device_hash'           :   'CEF34215E3E610825DC1C4BF9864D47A',
        'device_model'          :   'rubx-lib',
        'is_multi_account'      :   False,
        'lang_code'             :   'fa',
        'system_version'        :   'SDK 22',
        'token'                 :   'cgpzI3mbTPKddhgKQV9lwS:APA91bE3ZrCdFosZAm5qUaG29xJhCjzw37wE4CdzAwZTawnHZM_hwZYbPPmBedllAHlm60v5N2ms-0OIqJuFd5dWRAqac2Ov-gBzyjMx5FEBJ_7nbBv5z6hl4_XiJ3wRMcVtxCVM9TA-',
        'token_type'            :   'Firebase'
    }

class Infos:
    citys, proxys, auth_, sent = [], [], [], lambda data: False if data.get('status').lower() != 'ok' else True

class clients(dict):
    (
        web,
        android,
        rubx
        ) = (
            {
                'app_name'      :   'Main',
                'app_version'   :   '4.1.11',
                'platform'      :   'Web',
                'package'       :   'web.rubika.ir',
                'lang_code'     :   'fa'
                },
            {
                'app_name'      :   'Main',
                'app_version'   :   '2.8.1',
                'platform'      :   'Android',
                'package'       :   'ir.resaneh1.iptv',
                'lang_code'     :   'fa'
                },
            {
                'app_name'      :   'Main',
                'app_version'   :   '3.0.8',
                'platform'      :   'Android',
                'package'       :   'app.rbmain.a',
                'lang_code'     :   'en'
                }
        )