import RTDE_Python_Client_Library.rtde.rtde as rtde
import RTDE_Python_Client_Library.rtde.rtde_config as rtde_config
from RTDE_Python_Client_Library.rtde.rtde import ConnectionState

import time



class Robot:
    HOST: str
    PORT: int = 30004
    config_filename: str = 'config.xml'
    connection_state: ConnectionState
    keep_running: bool

    def __init__(self, host="10.103.0.201") -> None:
        self.HOST = host

        self.state_names = []
        self.state_types = []
        self.setup_types = []
        self.setup_names = []
        self.watchdog_names = []
        self.watchdog_types = []

        self.setup = None
        self.watchdog = None

        self.__con = None

        self.keep_running = True

    def load_config_filename(self, config_filename='config.xml') -> None:
        self.config_filename = config_filename

    def connect_to_robot(self):
        conf = rtde_config.ConfigFile(self.config_filename)
        self.state_names, self.state_types = conf.get_recipe('state')
        self.setup_names, self.setup_types = conf.get_recipe('setup')
        self.watchdog_names, self.watchdog_types = conf.get_recipe('watchdog')

        self.__con = rtde.RTDE(self.HOST, self.PORT)
        self.connection_state = self.__con.connect()

        while (self.connection_state is None) or (self.connection_state == 0):
            print("Connection State: ", self.connection_state)
            time.sleep(0.5)
            self.connection_state = self.__con.connect()

        print("Connected to the robot!")
        self.__con.get_controller_version()

    def get_connection_state(self):
        return self.connection_state

    def setup_recipes(self):
        self.__con.send_output_setup(self.state_names, self.state_types)
        self.setup = self.__con.send_input_setup(self.setup_names, self.setup_types)
        self.watchdog = self.__con.send_input_setup(self.watchdog_names, self.watchdog_types)

        self.init_key_values()

    def init_key_values(self):
        """
        Just to initialize all the values that will be send to the roboter
        :return: None
        """
        # self.setup.input_double_register_0 = 0
        # self.setup.input_double_register_1 = 0
        # self.setup.input_double_register_2 = 0
        # self.setup.input_double_register_3 = 0
        # self.setup.input_double_register_4 = 0
        # self.setup.input_double_register_5 = 0

        self.setup.standard_digital_output = 0
        self.setup.standard_digital_output_mask = 0

        self.setup.configurable_digital_output = 0
        self.setup.configurable_digital_output_mask = 0

        # The function "rtde_set_watchdog" in the "rtde_control_loop.urp" creates a 1 Hz watchdog
        self.watchdog.input_int_register_0 = 0

    @staticmethod
    def setup_to_list(self, setup) -> list:
        lst = []
        for i in range(0, 6):
            lst.append(setup.__dict__["input_double_register_%i" % i])
        return lst

    @staticmethod
    def list_to_setup(self, setup, lst: list):
        # for i in range(0, 6):
        #     setup.__dict__["input_double_register_%i" % i] = lst[i]
        setup.__dict__["standard_digital_output"] = 5
        return setup

    def send_start(self):
        return self.__con.send_start()

    def get_current_state(self):
        return self.__con.receive()

    def send(self, input_data):
        """
        Damit man einen Ausgang steuern kann, muss die Maske mit angegeben werden.
        Das wird wie im TCP/IP benutzt mit dem 255.255.255.0
        Damit der Ausgang 3 (int = 4) durch das Programm angesteuert werden kann, muss die Maske min. 4 wie bei get_digital

        :param input_data:
        :return:
        """
        self.__con.send(input_data)

    def send_pause(self):
        self.__con.send_pause()

    def disconnect(self):
        self.__con.disconnect()

    def set_setup(self, part: str, value):
        if part in self.setup_names:
            self.setup.__dict__[part] = value
            return
        raise Exception("Es gibt kein passenden Übergabewert in der %s Datei", self.config_filename)

    def get_setup(self, part: str):
        if part in self.setup_names:
            return self.setup.__dict__[part]
        raise Exception("Es gibt kein passenden Übergabewert in der %s Datei", self.config_filename)

    def get_state(self, part: str):
        if part in self.state_names:
            return self.setup.__dict__[part]
        raise Exception("Es gibt kein passenden Übergabewert in der %s Datei", self.config_filename)
