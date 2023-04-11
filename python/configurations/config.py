import os
import json
import operator
from functools import reduce
from cds_py_logger import logger
from dotenv import load_dotenv

load_dotenv()
DSCOPE_DEVICE_TYPE = 23
PCT_DEVICE_TYPE = 22
TTS_DEVICE_TYPE = 24
FIBER_CUT_DEVICE_TYPE = 26
LOCAL_MQTT_CONFIGS = {}
MQTT_CONFIGS = {}
HTTP_CONFIGS = {}
DEVICE_CONFIGS = {}
DATABASE_CONFIGS = {}
ZEBRA_CONFIG = {}
RFID_CONFIGS = {}
DEVICE_PIN_CONFIG = {}
D280_CONFIG = {}
SERIAL_BARCODE_CONFIGS = {}
SOCKET_UDP_CONFIGS = {}
SOCKET_TCP_CONFIGS = {}
UHF_CONFIG = {}
TEMPLATES_CONFIGS = {}
DEBUG_ENABLE = False
VALID_EPC_LENGTH = 32
RUNNING_ENVIROMENT = None
_json_config = None
json_config_loaded = False
device_type_chart = {
    "22": "PCT",
    "23": "DSCOPE",
    "24": "TTS",
    "26": "FIBER_CUT"
}


def get_device_type_tag(device_type):
    return device_type_chart[str(device_type)]


def get_json_configs_from_file(json_file_path):
    global json_config_loaded
    try:
        with open(json_file_path, "r") as config_file:
            __json_out = json.load(config_file)
            json_config_loaded = True
            return __json_out
    except Exception as e:
        json_config_loaded = False
        logger.LOG_ERROR("Unable to load json config: {}".format(e))
        return None


def get_json_config(item):
    global json_config_loaded
    if json_config_loaded:
        item = item.split(",")
        return get_from_dict(_json_config, item)
    return None


def get_from_dict(dataDict, mapList):
    try:
        return reduce(operator.getitem, mapList, dataDict)
    except Exception as e:
        return None


def get(item):
    if os.environ.get(item) != None:
        return os.environ.get(item)
    else:
        return 0


def get_bool(a, b, c):
    b = str_to_bool(b)
    return a if isinstance(a, bool) else b if isinstance(b, bool) else c


def str_to_bool(item):
    if item == "True":
        return True
    elif item == "False":
        return False
    return None


def load_configs(DEVICE_TYPE,json_file_path="config.json"):
    global _json_config, DEBUG_ENABLE,VALID_EPC_LENGTH,RUNNING_ENVIROMENT
    _json_config = get_json_configs_from_file(json_file_path)
    # ###################--RUN ENVIROMENT--#################
    RUNNING_ENVIROMENT = (
        get_json_config("RUN_ENVIRONMENT,RUN_ENV") or get("RUN_ENV") or "PROD"
    )
    # ###################--ENVIRONMENT SPECIFIC CONFIG--#################
    MQTT_HOST = (
        get_json_config(RUNNING_ENVIROMENT + ",MQTT_HOST")
        or get("MQTT_HOST_" + RUNNING_ENVIROMENT)
        or "mdm.viaphoton.com"
    )
    API_HOST = (
        get_json_config(RUNNING_ENVIROMENT + ",API_HOST")
        or get("API_HOST_" + RUNNING_ENVIROMENT)
        or "https://api.viaphoton.cowlar.com/v1/"
    )
    DEVICE_EMAIL = (
        get_json_config(RUNNING_ENVIROMENT + ",DEVICE_EMAIL")
        or get("DEVICE_EMAIL_" + RUNNING_ENVIROMENT)
        or "viaphoton.cowlar.com"
    )
    DEVICE_PASSWORD = (
        get_json_config(RUNNING_ENVIROMENT + ",DEVICE_PASSWORD")
        or get("DEVICE_PASSWORD_" + RUNNING_ENVIROMENT)
        or "123456"
    )
    MQTT_SECURE = get_bool(
        get_json_config(RUNNING_ENVIROMENT + ",MQTT_SECURE"),
        get("MQTT_SECURE_" + RUNNING_ENVIROMENT),
        True,
    )
    # ###################--MQTT TOPICS--#################
    GS_CONFIG_TOPIC = (
        get_json_config("MQTT,MQTT_TOPICS,GS_CONFIG_TOPIC")
        or get("GS_CONFIG_TOPIC")
        or "gs/config"
    )
    USER_UPDATE_TOPIC = (
        get_json_config("MQTT,MQTT_TOPICS,USER_UPDATE_TOPIC")
        or str(get("USER_UPDATE_TOPIC"))
        or "d/all/users"
    )
    HARDWARE_VERSION_TOPIC = get_json_config("MQTT,MQTT_TOPICS,HARDWARE_VERSION_TOPIC") or str(
        get("HARDWARE_VERSION_TOPIC") or "hw_ver")
    USER_TEST_TIMEOUT_TOPIC = get_json_config(
        "MQTT,MQTT_TOPICS,GS_CONFIG_TOPIC") or str(get("GS_CONFIG_TOPIC") or "gs/config")
    TTS_WRITE_STATUS_TOPIC = get_json_config("MQTT,MQTT_TOPICS,TTS_WRITE_STATUS_TOPIC") or str(
        get("TTS_WRITE_STATUS_TOPIC") or "s/tts/ws")
    # ###################--MQTT CONFIGS--#################
    MQTT_PORT = get_json_config(
        "MQTT,CONFIGS,MQTT_PORT") or int(get("MQTT_PORT")) or 8080
    MQTT_USERNAME = get_json_config("MQTT,CONFIGS,MQTT_USERNAME") or str(
        get("MQTT_USERNAME") or "dockersim-dispenser"
    )
    MQTT_PASSWORD = get_json_config("MQTT,CONFIGS,MQTT_PASSWORD") or str(
        get("MQTT_PASSWORD") or "CowlarGeyser7890"
    )
    MQTT_KEEPALIVE = get_json_config("MQTT,CONFIGS,MQTT_KEEPALIVE") or int(
        get("MQTT_KEEPALIVE")
    ) or 10
    MQTT_CLEAN_SESSION = get_bool(
        get_json_config("MQTT,CONFIGS,MQTT_CLEAN_SESSION"),
        get("MQTT_CLEAN_SESSION"),
        False,
    )
    MQTT_RECONNECT_DELAY_MAX = get_json_config(
        "MQTT,CONFIGS,MQTT_RECONNECT_DELAY_MAX"
    ) or int(get("MQTT_RECONNECT_DELAY_MAX")) or 10
    MQTT_PUBLISH_DELAY = get_json_config("MQTT,CONFIGS,MQTT_PUBLISH_DELAY") or float(
        get("MQTT_PUBLISH_DELAY")
    ) or 1.0
    # ###################--DEVICE CONFIGS--#################

    DEVICE_SERIAL =  (get_json_config(
        "APP_CONFIGS,DEVICE_SERIAL") or str(get("DEVICE_SERIAL")))  + get_device_type_tag(DEVICE_TYPE)

    DEVICE_PIN = get_json_config(
        "DEVICE,CONFIGS,DEVICE_PIN") or int(get("DEVICE_PIN")) or 1111
    # ###################--DATABASE--#################
    DATABASE_PATH = (
        get_json_config("DEVICE,DATABASE_PATH")
        or str(get("DATABASE_PATH")
        or "/database")
    )
    # ###################--DEBUG--#################
    DEBUG_ENABLE = get_bool(get_json_config(
        "RUN_ENVIRONMENT,DEBUG_ENABLE"), get("DEBUG_ENABLE"), False)
    # ###################--SOCKET--#################
    SOCKET_UDP_PORT = get_json_config("SOCKETS,SOCKET_UDP_PORT") or int(
        get("SOCKET_UDP_PORT")
    ) or 4000
    SOCKET_UDP_APPLICATION_TYPE = get_json_config(
        "SOCKETS,SOCKET_UDP_APPLICATION_TYPE"
    ) or str(get("SOCKET_UDP_APPLICATION_TYPE")) or "CLIENT"

    SOCKET_TCP_PORT = get_json_config("SOCKETS,SOCKET_TCP_PORT") or int(
        get("SOCKET_TCP_PORT")
    ) or 5000
    SOCKET_TCP_APPLICATION_TYPE = get_json_config(
        "SOCKETS,SOCKET_TCP_APPLICATION_TYPE"
    ) or str(get("SOCKET_TCP_APPLICATION_TYPE")) or "CLIENT"
    # ###################--BARCODE--#################

    ZEBRA_BAUDRATE = get_json_config("BARCODE,ZEBRA,BAUDRATE") or get("ZEBRA_BAUDRATE") or 9600
    
    ZEBRA_PORT = get_json_config("BARCODE,ZEBRA,PORT") or get("ZEBRA_PORT") or "/dev/zebra"
    ZEBRA_SCANNER_VID = get_json_config("BARCODE,ZEBRA,SCANNER_VID") or get(
        "ZEBRA_SCANNER_VID"
    ) or "0000"
    ZEBRA_SCANNER_PID = get_json_config("BARCODE,ZEBRA,SCANNER_PID") or get(
        "ZEBRA_SCANNER_PID"
    ) or "0000"

    D280_BAUDRATE = get_json_config("BARCODE,D280,BAUDRATE") or get("D280_BAUDRATE") or 115200
    D280_PORT = get_json_config("BARCODE,D280,PORT") or get("D280_PORT") or "/dev/d280"
    D280_SCANNER_VID = get_json_config("BARCODE,D280,SCANNER_VID") or get("D280_SCANNER_VID") or "0000"
    D280_SCANNER_PID = get_json_config("BARCODE,D280,SCANNER_PID") or get("D280_SCANNER_PID") or "0000"

    BARCODE_XONXOFF = get_bool(
        get_json_config("BARCODE,SETTINGS,BARCODE_XONXOFF"),
        get("BARCODE_XONXOFF"),
        False,
    )
    BARCODE_RTSCTS = get_bool(
        get_json_config("BARCODE,SETTINGS,BARCODE_RTSCTS"), get(
            "BARCODE_RTSCTS"), False
    )
    BARCODE_DSRDTR = get_bool(
        get_json_config("BARCODE,SETTINGS,BARCODE_DSRDTR"), get(
            "BARCODE_DSRDTR"), False
    )
    BARCODE_SUBSYSTEM = get_json_config("BARCODE,SETTINGS,BARCODE_SUBSYSTEM") or get(
        "BARCODE_SUBSYSTEM"
    ) or "tty" 
    BARCODE_TIMEOUT_CONFIG = get_json_config(
        "BARCODE,SETTINGS,BARCODE_TIMEOUT_CONFIG"
    ) or get("BARCODE_TIMEOUT_CONFIG") or None

    BUZZER_TIME = (
        get_json_config("APP_CONFIGS,DSCOPE,BUZZER_TIME") or get(
            "BUZZER_TIME") or 0.5
    )

    RFID_VID = get_json_config("RFID_CONFIGS,HID,VID") or get("RFID_VID") or "0000"
    RFID_PID = get_json_config("RFID_CONFIGS,HID,PID") or get("RFID_PID") or "0000"
    RFID_SUB = get_json_config("RFID_CONFIGS,HID,SUB") or get("RFID_SUB") or "input"
    RFID_DEVICE_PATH = get_json_config("RFID_CONFIGS,HID,PATH") or get("RFID_DEVICE_PATH") or "/dev/rfid"


    #####################TEMPLATE_PATH_CONFIGURATIONS########################
    
    TEMPLATE_PATH = get_json_config("TEMPLATE,TEMPLATE_PATH") or get("TEMPLATE_PATH") or "templates/"
    TEMPLATE_ZERO_NAME = get_json_config("TEMPLATE,TEMPLATE_ZERO_NAME") or get("TEMPLATE_ZERO_NAME") or "logo.png"
    TEMPLATE_ONE_NAME = get_json_config("TEMPLATE,TEMPLATE_ONE_NAME") or get("TEMPLATE_ONE_NAME") or "template.png"
    BACKGROUND_IMAGE_PATH = get_json_config("TEMPLATE,BACKGROUND_IMAGE_PATH") or get("BACKGROUND_IMAGE_PATH") or "background.png"
    
    #####################LOCAL_MQTT_CONFIG_TTS_SPECIFIC######################
    
    MQTT_HOST_LOCAL = (
        get_json_config("APP_CONFIGS,TTS" + ",MQTT_HOST")
        or get("MQTT_HOST_" + "LOCAL")
    ) # no default
    
    MQTT_SECURE_LOCAL = get_bool(
        get_json_config("APP_CONFIGS,TTS" + ",MQTT_SECURE"),
        get("MQTT_SECURE_" + "LOCAL"),
        False,
    )

    MQTT_USERNAME_LOCAL = get_json_config("APP_CONFIGS,TTS,MQTT_USERNAME") or str(
        get("MQTT_USERNAME_LOCAL") or "dockersim-dispenser"
    )
    MQTT_PASSWORD_LOCAL = get_json_config("APP_CONFIGS,TTS,MQTT_PASSWORD") or str(
        get("MQTT_PASSWORD_LOCAL") or "CowlarGeyser7890"
    )





    FONGWAH_PORT = get_json_config(
        "RFID_CONFIGS,FONGWAH,PORT") or get("FONGWAH_PORT") or "/dev/uhf"
    FONGWAH_BAUDRATE = get_json_config("RFID_CONFIGS,FONGWAH,BAUDRATE") or get("FONGWAH_BAUDRATE") or 115200
    
    FONGWAH_TIMEOUT = get_json_config("RFID_CONFIGS,FONGWAH,TIMEOUT") or get("FONGWAH_TIMEOUT") or None
    
    FONGWAH_XONXOFF = get_bool(
        get_json_config("RFID_CONFIGS,FONGWAH,XONXOFF"), get(
            "FONGWAH_XONXOFF"), False
    )
    FONGWAH_RTSCTS = get_bool(
        get_json_config("RFID_CONFIGS,FONGWAH,RTSCTS"), get(
            "FONGWAH_RTSCTS"), False
    )
    FONGWAH_DSRDTR = get_bool(
        get_json_config("RFID_CONFIGS,FONGWAH,DSRDTR"), get(
            "FONGWAH_DSRDTR"), False
    )
    FONGWAH_NAME = get_json_config("RFID_CONFIGS,FONGWAH,NAME") or get("FONGWAH_NAME") or "fongwah"
    FONGWAH_VID = get_json_config("RFID_CONFIGS,FONGWAH,VID") or get("FONGWAH_VID") or "0000"
    FONGWAH_PID = get_json_config(
        "RFID_CONFIGS,FONGWAH,PID") or get("FONGWAH_PID") or "0000"
    FONGWAH_SUBSYSTEM = get_json_config("RFID_CONFIGS,FONGWAH,SUBSYSTEM") or get(
        "FONGWAH_SUBSYSTEM"
    ) or "tty"
    FONGWAH_QUEUE_READ_TIMEOUT = (
        get_json_config("RFID_CONFIGS,FONGWAH,QUEUE_READ_TIMEOUT")
        or get("FONGWAH_QUEUE_READ_TIMEOUT")
        or 1.0
    )
    FONGWAH_COMMAND_RESPONSE_TIMEOUT = (
        get_json_config("RFID_CONFIGS,FONGWAH,COMMAND_RESPONSE_TIMEOUT")
        or get("FONGWAH_COMMAND_RESPONSE_TIMEOUT")
        or 1.0
    )
    FONGWAH_WRITE_RESPONSE_TIMEOUT = (
        get_json_config("RFID_CONFIGS,FONGWAH,WRITE_RESPONSE_TIMEOUT")
        or get("FONGWAH_WRITE_RESPONSE_TIMEOUT")
        or 5.0
    )
    VALID_EPC_LENGTH = (get_json_config("APP_CONFIGS,TTS,VALID_EPC_LENGTH")
        or get("FONGWAH_VALID_EPC_LENGTH")
        or 32
    )

    RECEIVER_DEVICE = get_bool(
        get_json_config("APP_CONFIGS,TTS,RECEIVER_DEVICE"),
        get("RECEIVER_DEVICE"),
        False,
    )

    HARDWARE_VERSION = get_json_config("APP_CONFIGS,{},HARDWARE_VERSION".format(
        get_device_type_tag(DEVICE_TYPE))) or str(get("HARDWARE_VERSION") or "v0.0.1")
    logger.LOG_INFO(
        "Loading Configs for {}-ENVIROMENT".format(RUNNING_ENVIROMENT))
    HTTP_CONFIGS.update({"API_HOST": API_HOST})
    MQTT_CONFIGS.update(
        {
            "MQTT_HOST": MQTT_HOST,
            "MQTT_PORT": MQTT_PORT,
            "MQTT_USERNAME": MQTT_USERNAME,
            "MQTT_PASSWORD": MQTT_PASSWORD,
            "GS_CONFIG_TOPIC": GS_CONFIG_TOPIC,
            "MQTT_KEEPALIVE": MQTT_KEEPALIVE,
            "MQTT_CLEAN_SESSION": MQTT_CLEAN_SESSION,
            "MQTT_RECONNECT_DELAY_MAX": MQTT_RECONNECT_DELAY_MAX,
            "MQTT_PUBLISH_DELAY": MQTT_PUBLISH_DELAY,
            "MQTT_SECURE": MQTT_SECURE,
            "USER_UPDATE_TOPIC":USER_UPDATE_TOPIC,
            "HARDWARE_VERSION_TOPIC":HARDWARE_VERSION_TOPIC,
            "USER_TEST_TIMEOUT_TOPIC":USER_TEST_TIMEOUT_TOPIC,
            "TTS_WRITE_STATUS_TOPIC":TTS_WRITE_STATUS_TOPIC
        }
    )
    LOCAL_MQTT_CONFIGS.update(
        {
            "MQTT_HOST": MQTT_HOST_LOCAL,
            "MQTT_PORT": MQTT_PORT,
            "MQTT_USERNAME": MQTT_USERNAME_LOCAL,
            "MQTT_PASSWORD": MQTT_PASSWORD_LOCAL,
            "GS_CONFIG_TOPIC": GS_CONFIG_TOPIC,
            "MQTT_KEEPALIVE": MQTT_KEEPALIVE,
            "MQTT_CLEAN_SESSION": MQTT_CLEAN_SESSION,
            "MQTT_RECONNECT_DELAY_MAX": MQTT_RECONNECT_DELAY_MAX,
            "MQTT_PUBLISH_DELAY": MQTT_PUBLISH_DELAY,
            "MQTT_SECURE": MQTT_SECURE_LOCAL,
            "USER_UPDATE_TOPIC":USER_UPDATE_TOPIC,
            "HARDWARE_VERSION_TOPIC":HARDWARE_VERSION_TOPIC,
            "USER_TEST_TIMEOUT_TOPIC":USER_TEST_TIMEOUT_TOPIC,
            "TTS_WRITE_STATUS_TOPIC":TTS_WRITE_STATUS_TOPIC
        }
    )
    DEVICE_CONFIGS.update(
        {
            "DEVICE_SERIAL": DEVICE_SERIAL,
            "DEVICE_PIN": DEVICE_PIN,
            "DEVICE_TYPE": DEVICE_TYPE,
            "DEVICE_EMAIL": DEVICE_EMAIL,
            "DEVICE_PASSWORD": DEVICE_PASSWORD,
            "HARDWARE_VERSION":HARDWARE_VERSION,
            "RECEIVER_DEVICE":RECEIVER_DEVICE
        }
    )
    DATABASE_CONFIGS.update({"DATABASE_PATH": DATABASE_PATH})
    ZEBRA_CONFIG.update(
        {
            "DEVICE_CONFIG": {
                "PORT": ZEBRA_PORT,
                "BAUDRATE": ZEBRA_BAUDRATE,
                "TIMEOUT": None,
                "XONXOFF": BARCODE_XONXOFF,
                "RTSCTS": BARCODE_RTSCTS,
                "DSRDTR": BARCODE_DSRDTR,
            },
            "DEVICE_ATTR": {
                "NAME": "Zebra",
                "VID": ZEBRA_SCANNER_VID,
                "PID": ZEBRA_SCANNER_PID,
                "SUBSYSTEM": BARCODE_SUBSYSTEM,
            },
        }
    )
    D280_CONFIG.update(
        {
            "DEVICE_CONFIG": {
                "PORT": D280_PORT,
                "BAUDRATE": D280_BAUDRATE,
                "TIMEOUT": None,
                "XONXOFF": BARCODE_XONXOFF,
                "RTSCTS": BARCODE_RTSCTS,
                "DSRDTR": BARCODE_DSRDTR,
            },
            "DEVICE_ATTR": {
                "NAME": "D280",
                "VID": D280_SCANNER_VID,
                "PID": D280_SCANNER_PID,
                "SUBSYSTEM": BARCODE_SUBSYSTEM,
            },
        }
    )
    SERIAL_BARCODE_CONFIGS.update(
        {
            "ZEBRA_CONFIG": ZEBRA_CONFIG,
            "D280_CONFIG": D280_CONFIG,
            "BARCODE_TIMEOUT_CONFIG": BARCODE_TIMEOUT_CONFIG,
            "BUZZER_TIME": BUZZER_TIME,
        }
    )
    logger.LOG_WARN(
        "HTTP_HOST:{http},MQTT_HOST:{mqtt}".format(
            http=HTTP_CONFIGS["API_HOST"], mqtt=MQTT_CONFIGS["MQTT_HOST"]
        )
    )
    RFID_CONFIGS.update(
        {
            "RFID_VID": RFID_VID,
            "RFID_PID": RFID_PID,
            "RFID_SUB": RFID_SUB,
            "RFID_DEVICE_PATH": RFID_DEVICE_PATH
        }
    )
    if DEVICE_TYPE == DSCOPE_DEVICE_TYPE:
        DEVICE_PIN_CONFIG.update(
            {
                "USER_LED_RED": 6,
                "USER_LED_GREEN": 13,
                "USER_LED_BLUE": 5,
                "BUZZER": 21,
                "BARCODE_LED_RED": 12,
                "BARCODE_LED_GREEN": 16,
                "BARCODE_LED_BLUE": 20,
            }
        )
    elif DEVICE_TYPE == PCT_DEVICE_TYPE:
        if HARDWARE_VERSION == "v0.1.0":
            logger.LOG_INFO("Loading Pin Config for version 1.0")
            DEVICE_PIN_CONFIG.update(
                {
                    "CABLE_RED_PIN": 20,
                    "CABLE_YELLOW_PIN": 15,
                    "CABLE_BLACK_PIN": 18,
                    "WAND_RED_PIN": 25,
                    "WAND_YELLOW_PIN": 8,
                    "WAND_BLACK_PIN": 7,
                    "WAND_LED_WHITE": 23,
                    "WAND_LED_GREEN": 24,
                    "IR_SENSOR": 12,
                    "BUZZER": 21,
                    "USER_LED_RED": 26,
                    "USER_LED_GREEN": 19,
                    "USER_LED_BLUE": 13,
                }
            )
        elif HARDWARE_VERSION == "v0.2.0" or "v0.2.1":
            logger.LOG_INFO(
                "Loading Pin Config for version: {}".format(HARDWARE_VERSION)
            )
            DEVICE_PIN_CONFIG.update(
                {
                    "CABLE_RED_PIN": 17,
                    "CABLE_YELLOW_PIN": 18,
                    "CABLE_BLACK_PIN": 27,
                    "WAND_RED_PIN": 25,
                    "WAND_YELLOW_PIN": 8,
                    "WAND_BLACK_PIN": 7,
                    "WAND_LED_WHITE": 23,
                    "WAND_LED_GREEN": 24,
                    "IR_SENSOR": 12,
                    "BUZZER": 21,
                    "USER_LED_RED": 13,
                    "USER_LED_GREEN": 6,
                    "USER_LED_BLUE": 5,
                }
            )
        else:
            DEVICE_PIN_CONFIG.update(
                {
                    "CABLE_RED_PIN": 20,
                    "CABLE_YELLOW_PIN": 15,
                    "CABLE_BLACK_PIN": 18,
                    "WAND_RED_PIN": 25,
                    "WAND_YELLOW_PIN": 8,
                    "WAND_BLACK_PIN": 7,
                    "WAND_LED_WHITE": 23,
                    "WAND_LED_GREEN": 24,
                    "IR_SENSOR": 12,
                    "BUZZER": 21,
                    "USER_LED_RED": 26,
                    "USER_LED_GREEN": 19,
                    "USER_LED_BLUE": 13,
                }
            )
    elif DEVICE_TYPE == TTS_DEVICE_TYPE:
        DEVICE_PIN_CONFIG.update(
            {
                "USER_LED_RED": 13,
                "USER_LED_GREEN": 6,
                "USER_LED_BLUE": 5,
                "BUZZER": 21,
                "BARCODE_LED_RED": 12,
                "BARCODE_LED_GREEN": 16,
                "BARCODE_LED_BLUE": 20,
                "TROLLEY_LED_RED": 6,
                "TROLLEY_LED_GREEN": 13,
                "TROLLEY_LED_BLUE": 5,
            }
        )
    elif DEVICE_TYPE == FIBER_CUT_DEVICE_TYPE:
        pass
    DATABASE_CONFIGS.update({"DATABASE_PATH": DATABASE_PATH})
    logger.LOG_WARN(
        "HTTP_HOST:{http},MQTT_HOST:{mqtt}".format(
            http=HTTP_CONFIGS["API_HOST"], mqtt=MQTT_CONFIGS["MQTT_HOST"]
        )
    )
    SOCKET_TCP_CONFIGS.update(
        {
            "SOCKET_PORT": SOCKET_TCP_PORT,
            "PROTOCOL": "TCP",
            "SOCKET_APPLICATION_TYPE": SOCKET_TCP_APPLICATION_TYPE,
        }
    )
    SOCKET_UDP_CONFIGS.update(
        {
            "SOCKET_PORT": SOCKET_UDP_PORT,
            "PROTOCOL": "UDP",
            "SOCKET_APPLICATION_TYPE": SOCKET_UDP_APPLICATION_TYPE,
        }
    )
    UHF_CONFIG.update(
        {
            "DEVICE_CONFIG": {
                "PORT": FONGWAH_PORT,
                "BAUDRATE": FONGWAH_BAUDRATE,
                "TIMEOUT": None,
                "XONXOFF": FONGWAH_XONXOFF,
                "RTSCTS": FONGWAH_RTSCTS,
                "DSRDTR": FONGWAH_DSRDTR,
            },
            "DEVICE_ATTR": {
                "NAME": FONGWAH_NAME,
                "RFID_VID": FONGWAH_VID,
                "RFID_PID": FONGWAH_PID,
                "SUBSYSTEM": FONGWAH_SUBSYSTEM,
            },
            "FONGWAH_CONFIG": {
                "READ_TIMEOUT": FONGWAH_QUEUE_READ_TIMEOUT, #fix this to be updated from the 3 configs down the road
            },
        }
    )
    TEMPLATES_CONFIGS.update(
        {
            "TEMPLATE_PATH": TEMPLATE_PATH,
            "TEMPLATE_ZERO_NAME": TEMPLATE_ZERO_NAME,
            "TEMPLATE_ONE_NAME": TEMPLATE_ONE_NAME,
            "BACKGROUND_IMAGE_PATH": BACKGROUND_IMAGE_PATH,
        }
    )
