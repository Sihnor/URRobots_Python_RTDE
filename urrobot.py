from robot import Robot


class URRobot(Robot):
    state: None
    digital_output_mask: list

    def __init__(self, host="10.103.0.201") -> None:
        super(URRobot, self).__init__(host)
        pass

    @staticmethod
    def maskList_to_int(mask: list) -> int:
        mask_int = 0
        bit = 1
        for value in mask:
            if value:
                mask_int += bit
            bit *= 2
        return mask_int

    @staticmethod
    def int_to_maskList(value: int) -> list:
        mask = []

        for i in range(7, -1, -1):
            if (value - 2**i) >= 0:
                mask.insert(0, True)
                value -= 2**i
            else:
                mask.insert(0, False)

        return mask

    # Inputs getter
    def get_actual_digital_input_int(self) -> int:
        """
        Gibt den aktuellen Integerwert alles digitalen Eingaenge aus
        :return: (int) Wert der Eingaenge
        """
        return self.get_state("actual_digital_input_bits")

    def get_actual_digital_input_bytes(self) -> bytes:
        """
        Gibt den digitalen Eingaenge als Byte in der folgenden Reihenfolge aus.\n
        [2] Byte: Digitaler Eingang\n
        [1] Byte: Konfigurierbarer Eingang\n
        [0] Byte: Werkzeugeingang
        :return: (byte) Zustand aller Eingaenge
        """
        return self.get_actual_digital_input_int().to_bytes(3, byteorder="big")

    def get_digital_input(self, inputNum: int) -> bool:
        """
        Gibt den aktuellen Zustand des Ausganges im Feld von "Digitaler Eingang" aus.
        :param inputNum: Nummer des Einganges
        :return:
        """
        if inputNum < 0 or inputNum > 7:
            raise Exception("Die Zahl darf nicht kleiner als 0 oder groesser als 7 sein!")

        bits = format(self.get_actual_digital_input_bytes()[2], '#010b')[2:]
        return bool(int(bits[(inputNum * -1) - 1]))

    def get_configurable_digital_input(self, inputNum: int):
        """
        NICHT GETESTET\n
        Gibt den aktuellen Zustand des Ausganges im Feld von "Konfigurierbarer Eingang" aus.
        :param inputNum:
        :return:
        """
        if inputNum < 0 or inputNum > 7:
            raise Exception("Die Zahl darf nicht kleiner als 0 oder groesser als 7 sein!")

        bits = format(self.get_actual_digital_input_bytes()[1], '#010b')[2:]
        return bool(int(bits[(inputNum * -1) - 1]))

    def get_tool_digital_input(self, inputNum: int):
        """
        NICHT GETESTET\n
        Gibt den aktuellen Zustand des Ausganges im Feld von "Werkzeug Eingang" aus.
        :param inputNum: (int)jeweiliger Eingang des Feldes
        :return: bool
        """
        if inputNum < 0 or inputNum > 2:
            raise Exception("Die Zahl darf nicht kleiner als 0 oder groesser als 2 sein!")

        bits = format(self.get_actual_digital_input_bytes()[0], '#04b')[2:]
        return bool(int(bits[(inputNum * -1) - 1]))

    # Outputs getter
    def get_actual_digital_output_int(self) -> int:
        """
        Gibt der aktuelle Integerwert aller digitalen Ausgaenge aus
        :return: (int)Wert der Ausgaenge
        """
        return self.get_state("actual_digital_output_bits")

    def get_actual_digital_output_bytes(self) -> bytes:
        """
        Gibt den digitalen Ausgängen als Byte in der Reihenfolge aus.\n
        [2] Byte: Digitaler Ausgang\n
        [1] Byte: Konfigurierbarer Ausgang\n
        [0] Byte: Werkzeugausgang
        :return: (byte) Zustand aller Ausgaenge
        """
        return self.get_actual_digital_output_int().to_bytes(3, byteorder='big')

    def get_digital_output(self, outputNum: int) -> bool:
        """
        Bekommt den aktuellen Wert des Ausganges im Register "Digitaler Ausgang".
        :param outputNum: (int)jeweiliger Ausgang des Feldes
        :return: (bool)wenn der Ausgang angesteuert ist
        """
        if outputNum < 0 or outputNum > 7:
            raise Exception("Die Zahl darf nicht kleiner als 0 oder groesser als 7 sein!")

        bits = format(self.get_actual_digital_output_bytes()[2], '#010b')[2:]
        return bool(int(bits[(outputNum * -1) - 1]))

    def get_configurable_output(self, outputNum: int):
        """
        Bekommt den aktuellen Wert des Ausganges im Register "Konfigurierbarer Ausgang".

        :param outputNum: (int)jeweiliger Ausgang des Feldes
        :return: (bool)wenn der Ausgang angesteuert ist
        """
        if outputNum < 0 or outputNum > 7:
            raise Exception("Die Zahl darf nicht kleiner als 0 oder groesser als 7 sein!")

        bits = format(self.get_actual_digital_output_bytes()[1], '#010b')[2:]
        return bool(int(bits[(outputNum * -1) - 1]))

    def get_tool_output(self, outputNum):
        """
        Bekommt den aktuellen Wert des Ausganges im Register "Werkzeug Ausgang".

        :param outputNum: (int)jeweiliger Ausgang des Feldes
        :return: bool
        """
        if outputNum < 0 or outputNum > 2:
            raise Exception("Die Zahl darf nicht kleiner als 0 oder groesser als 2 sein!")

        bits = format(self.get_actual_digital_output_bytes()[0], '#04b')[2:]
        return bool(int(bits[(outputNum * -1) - 1]))

    def get_all_digital_output(self, field, outputNum):
        """
        Bekommt den aktuellen Wert des Ausganges.\n
        Dabei ist das Register freiwaehltbar.
        :param field: [0]"Werkzeug Ausgang"---[1]"Konfigurierbarer Ausgang"---[2]"Digitaler Ausgang"
        :param outputNum: (int)jeweiliger Ausgang des Feldes
        :return: (bool)wenn der Ausgang angesteuert ist
        """
        if (field == 0 and outputNum > 2) or outputNum < 0 or outputNum > 7:
            raise Exception("Die Zahl darf nicht kleiner als 0 oder groesser als 2 sein!")

        if field == 0:
            bits = format(self.get_actual_digital_output_bytes()[field], '#04b')[2:0]
        else:
            bits = format(self.get_actual_digital_output_bytes()[field], '#010b')[2:0]
        return bool(int(bits[(outputNum * -1) - 1]))

    # ROBOT CONTROLLER INPUTS
    def set_speed_slider_mask(self, integer: int):
        """
        This will enable to set the speed slider to be controlled by the PC
        :param integer: (int) 0:disable 1:enable
        :return: None
        """
        self.set_setup("speed_slider_mask", integer)
        pass

    def set_speed_slider_fraction(self, value: float):
        """
        This will set the speed slider.
        :param value: (float) 0 = 0% | 1 = 100%
        :return:
        """
        if 0.2 <= value <= 1:
            self.set_setup("speed_slider_fraction", value)
        else:
            raise Exception("Please enter a value between 0.2 and 1!")

    def set_standard_digital_output_mask(self, integer: int):
        self.set_setup("standard_digital_output_mask", integer)

    def set_configurable_digital_output_mask(self, integer: int):
        self.set_setup("configurable_digital_output_mask", integer)

    def set_standard_digital_output(self, integer: int):
        self.set_setup("standard_digital_output", integer)

    def set_configurable_digital_output(self, integer: int):
        self.set_setup("configurable_digital_output", integer)

    def set_standard_analog_output_mask(self, integer: int):
        """
        Select the analoge output with a bit
        :param integer: (int) 0 bit: output_0; 1 bit: output_1
        :return: None
        """
        self.set_setup("standard_analog_output_mask", integer)

    def set_standard_analog_output_type(self, integer: int):
        """
        It will set the output domain for both outputs
        :param integer: (int) 0: both current; 1: Voltage and Current; 2: Current and Voltage; 3: both voltage
        :return: None
        """
        self.set_setup("standard_analog_output_type", integer)

    def set_standard_analog_output_0(self, value: float):
        """
        This will set the output with the percentage
        :param value: Percentage of the output
        :return: None
        """
        self.set_setup("standard_analog_output_0", value)
        pass

    def set_standard_analog_output_1(self, value: float):
        """
        This will set the output with the percentage.
        :param value: Percentage of the output
        :return: None
        """
        self.set_setup("standard_analog_output_1", value)

    def set_input_bit_registers0_to_31(self):
        # TODO input_bit_registers0_to_31
        pass

    def set_input_bit_registers32_to_63(self):
        # TODO input_bit_registers32_to_63
        pass

    def set_input_bit_register_X(self):
        # TODO input_bit_register_X
        pass

    def set_input_int_register_X(self):
        # TODO input_int_register_X
        pass

    def set_input_double_register_X(self):
        # TODO input_double_register_X
        pass

    def set_external_force_torque(self):
        # TODO external_force_torque
        pass

    # ROBOT CONTROLLER OUTPUTS
    def get_timestamp(self):
        # TODO timestamp - (Time elapsed since the controller was started [s])
        pass

    def get_target_q(self):
        # TODO target_q - (Target joint positions)
        pass

    def get_target_qd(self):
        # TODO target_qd - (Target joint velocities)
        pass

    def get_target_qdd(self):
        # TODO target_qdd - (Target joint accelerations)
        pass

    def get_target_current(self):
        # TODO target_current - (Target joint currents)
        pass

    def get_target_moment(self):
        # TODO target_moment - (Target joint moments (torques))
        pass

    def get_actual_q(self):
        # TODO actual_q - (Actual joint positions)
        pass

    def get_actual_qd(self):
        # TODO actual_qd - (Actual joint velocities)
        pass

    def get_actual_current(self):
        # TODO actual_current
        pass

    def get_joint_control_output(self):
        # TODO joint_control_output
        pass

    def get_actual_TCP_pose(self):
        # TODO actual_TCP_pose
        pass

    def get_actual_TCP_speed(self):
        # TODO actual_TCP_speed
        pass

    def get_actual_TCP_force(self):
        # TODO actual_TCP_force
        pass

    def get_target_TCP_pose(self):
        # TODO target_TCP_pose
        pass

    def get_target_TCP_speed(self):
        # TODO target_TCP_speed
        pass

    def get_actual_digital_input_bits(self):
        # TODO actual_digital_input_bits
        pass

    def get_joint_temperatures(self):
        # TODO joint_temperatures
        pass

    def get_actual_execution_time(self):
        # TODO actual_execution_time
        pass

    def get_robot_mode(self):
        # TODO robot_mode
        pass

    def get_joint_mode(self):
        # TODO joint_mode
        pass

    def get_safety_mode(self):
        # TODO safety_mode
        pass

    def get_safety_status(self):
        # TODO safety_status
        pass

    def get_actual_tool_accelerometer(self):
        # TODO actual_tool_accelerometer
        pass

    def get_speed_scaling(self):
        # TODO speed_scaling
        pass

    def get_target_speed_fraction(self):
        # TODO target_speed_fraction
        pass

    def get_actual_momentum(self):
        # TODO actual_momentum
        pass

    def get_actual_main_voltage(self):
        # TODO actual_main_voltage
        pass

    def get_actual_robot_voltage(self):
        # TODO actual_robot_voltage
        pass

    def get_actual_robot_current(self):
        # TODO actual_robot_current
        pass

    def get_actual_joint_voltage(self):
        # TODO actual_joint_voltage
        pass

    def get_actual_digital_output_bits(self):
        # TODO actual_digital_output_bits
        pass

    def get_runtime_state(self):
        # TODO runtime_state
        pass

    def get_elbow_position(self):
        # TODO elbow_position
        pass

    def get_elbow_velocity(self):
        # TODO elbow_velocity
        pass

    def get_robot_status_bits(self):
        # TODO robot_status_bits
        pass

    def get_safety_status_bits(self):
        # TODO safety_status_bits
        pass

    def get_analog_io_types(self):
        # TODO analog_io_types
        pass

    def get_standard_analog_input0(self):
        # TODO standard_analog_input0
        pass

    def get_standard_analog_input1(self):
        # TODO standard_analog_input1
        pass

    def get_standard_analog_output0(self):
        # TODO standard_analog_output0
        pass

    def get_standard_analog_output1(self):
        # TODO standard_analog_output1
        pass

    def get_io_current(self):
        # TODO io_current
        pass

    def get_euromap67_input_bits(self):
        # TODO euromap67_input_bits
        pass

    def get_euromap67_output_bits(self):
        # TODO euromap67_output_bits
        pass

    def get_euromap67_24V_voltage(self):
        # TODO euromap67_24V_voltage
        pass

    def get_euromap67_24V_current(self):
        # TODO euromap67_24V_current
        pass

    def get_tool_mode(self):
        # TODO tool_mode
        pass

    def get_tool_analog_input_types(self):
        # TODO tool_analog_input_types
        pass

    def get_tool_analog_input0(self):
        # TODO tool_analog_input0
        pass

    def get_tool_analog_input1(self):
        # TODO tool_analog_input1
        pass

    def get_tool_output_voltage(self):
        # TODO tool_output_voltage
        pass

    def get_tool_output_current(self):
        # TODO tool_output_current
        pass

    def get_tool_temperature(self):
        # TODO tool_temperature
        pass

    def get_tcp_force_scalar(self):
        # TODO tcp_force_scalar
        pass

    def get_output_bit_registers0_to_31(self):
        # TODO output_bit_registers0_to_31
        pass

    def get_output_bit_registers32_to_63(self):
        # TODO output_bit_registers32_to_63
        pass

    def get_output_bit_register_X(self):
        # (X=[64 .. 127])
        # TODO output_bit_register_X
        pass

    def get_output_int_register_X(self):
        # (X=[0 .. 47])
        # TODO output_int_register_X
        pass

    def get_output_double_register_X(self):
        # (X=[0 .. 47])
        # TODO output_double_register_X
        pass

    def get_input_bit_registers0_to_31(self):
        # TODO input_bit_registers0_to_31
        pass

    def get_input_bit_registers32_to_63(self):
        # TODO input_bit_registers32_to_63
        pass

    def get_input_bit_register_X(self):
        # (X=[64 .. 127])
        # TODO input_bit_register_X
        pass

    def get_input_int_register_X(self):
        # (X=[0 .. 48])
        # TODO input_int_register_X
        pass

    def get_input_double_register_X(self):
        # (X=[0 .. 48])
        # TODO input_double_register_X
        pass

    def get_tool_output_mode(self):
        # TODO tool_output_mode
        pass

    def get_tool_digital_output0_mode(self):
        # TODO tool_digital_output0_mode
        pass

    def get_tool_digital_output1_mode(self):
        # TODO tool_digital_output1_mode
        pass

    def get_payload(self):
        # TODO payload
        pass

    def get_payload_cog(self):
        # TODO payload_cog
        pass

    def get_payload_inertia(self):
        # TODO payload_inertia
        pass

    def get_script_control_line(self):
        # TODO script_control_line
        pass

    def get_ft_raw_wrench(self):
        # TODO ft_raw_wrench
        pass

    # MODIFIED DIGITAL OUTPUT MASK SETTER
    def set_single_standard_digital_output_mask(self, outputNum: int):
        """
        Es wird ein einziger Digitaler Ausgang hinzugefuegt oder entfernt welcher der Computer kontrolliert.
        :param outputNum: (int) Ausgangs Nummer
        :return: None
        """
        mask_list = self.int_to_maskList(self.get_setup("standard_digital_output_mask"))
        mask_list[outputNum] = not mask_list[outputNum]
        self.set_standard_digital_output_mask(self.maskList_to_int(mask_list))

    def set_list_standard_digital_output_mask(self, outputNum: list):
        """
        Es wird bestimmt welcher Digitaler Ausgang von dem Computer kontrolliert wird.
        :param outputNum: (list) Eine Liste der Ausgaenge zum Kontrollieren
        :return: None
        """
        self.set_standard_digital_output_mask(self.maskList_to_int(outputNum))

    def set_single_configurable_digital_output_mask(self, outputNum: int):
        """
        Es wird ein einziger Digitaler Ausgang hinzugefuegt oder entfernt welcher der Computer kontrolliert.
        :param outputNum: (int) Ausgangs Nummer
        :return: None
        """
        mask_list = self.int_to_maskList(self.get_setup("configurable_digital_output_mask"))
        mask_list[outputNum] = not mask_list[outputNum]
        self.set_configurable_digital_output_mask(self.maskList_to_int(mask_list))

    def set_list_configurable_digital_output_mask(self, outputNum: list):
        """
        Es wird bestimmt welcher Digitaler Ausgang von dem Computer kontrolliert wird.
        :param outputNum: (list) Eine Liste der Ausgaenge zum Kontrollieren
        :return: None
        """
        self.set_configurable_digital_output_mask(self.maskList_to_int(outputNum))

    # MODIFIED DIGITAL OUTPUT SETTER
    def set_single_standard_digital_output(self, outputNum: int, value: bool) -> None:
        """
        Es wird nur der Ausgang mit dem Wert beschrieben.
        :param value: (bool) Ausgang zustand
        :param outputNum: (int) Welcher Ausgang angesprochen werden soll
        :return: None
        """
        standard_digital_output_list = self.int_to_maskList(self.get_setup("standard_digital_output"))
        standard_digital_output_list[outputNum] = value
        self.set_standard_digital_output(self.maskList_to_int(standard_digital_output_list))

    def set_list_standard_digital_output(self, outputNum: list) -> None:
        """
        Es werden nur die Ausgänge vom Reiter 'Digitaler Ausgang' die ein True in der List haben.
        :param outputNum: (list) Liste der Ausgaenge
        :return: None
        """
        self.set_standard_digital_output(self.maskList_to_int(outputNum))

    def set_single_configurable_digital_output(self, outputNum: int, value: bool) -> None:
        """
        Es wird nur der Ausgang mit dem Wert beschrieben.
        :param value: (bool) Ausgang zustand
        :param outputNum: (int) Welcher Ausgang angesprochen werden soll
        :return: None
        """
        configurable_digital_output_list = self.int_to_maskList(self.get_setup("configurable_digital_output"))
        configurable_digital_output_list[outputNum] = value
        self.set_configurable_digital_output(self.maskList_to_int(configurable_digital_output_list))

    def set_list_configurable_digital_output(self, outputNum: list) -> None:
        """
        Es werden nur die Ausgänge vom Reiter 'Digitaler Ausgang' die ein True in der List haben.
        :param outputNum: (list) Liste der Ausgaenge
        :return: None
        """
        self.set_configurable_digital_output(self.maskList_to_int(outputNum))
