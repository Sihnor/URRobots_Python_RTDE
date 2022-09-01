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

    def get_actual_digital_output_bytes(self) -> bytes:
        """
        Gibt den digitalen Ausgängen als Byte in der Reihenfolge aus.\n
        1st Byte: Digitaler Ausgang\n
        2nd Byte: Konfigurierbarer Ausgang\n
        3rd Byte: Werkzeugausgang

        :return:
        """
        return self.state.actual_digital_output_bits.to_bytes(3, byteorder='big')

    def get_actual_digital_output_int(self) -> int:
        """
        Gibt der aktuelle Integerwert aller digitalen Ausgaenge an
        :return: (int)der DO
        """
        return self.state.actual_digital_output_bits

    def get_digital_output_normal(self, output: int) -> bool:
        """
        Bekommt den aktuellen Wert des Ausganges im Register "Digitaler Ausgang".

        :param output: (int)jeweiliger Ausgang des Feldes
        :return: (bool)wenn der Ausgang angesteuert ist
        """
        if output < 0 or output > 7:
            raise Exception("Die Zahl darf nicht kleiner als 0 oder groesser als 7 sein!")

        bits = format(self.state.actual_digital_output_bits.to_bytes(3, byteorder='big')[2], '#010b')[2:]
        return bool(int(bits[(output * -1) - 1]))

    def get_configurable_output(self, output):
        """
        Bekommt den aktuellen Wert des Ausganges im Register "Konfigurierbarer Ausgang".

        :param output: (int)jeweiliger Ausgang des Feldes
        :return: (bool)wenn der Ausgang angesteuert ist
        """
        if output < 0 or output > 7:
            raise Exception("Die Zahl darf nicht kleiner als 0 oder groesser als 7 sein!")

        bits = format(self.state.actual_digital_output_bits.to_bytes(3, byteorder='big')[1], '#010b')[2:]
        return bool(int(bits[(output * -1) - 1]))

    def get_tool_output(self, output):
        """
        Bekommt den aktuellen Wert des Ausganges im Register "Werkzeug Ausgang".

        :param output: (int)jeweiliger Ausgang des Feldes
        :return: bool
        """
        if output < 0 or output > 2:
            raise Exception("Die Zahl darf nicht kleiner als 0 oder groesser als 2 sein!")

        bits = format(self.state.actual_digital_output_bits.to_bytes(3, byteorder='big')[0], '#04b')[2:]
        return bool(int(bits[(output * -1) - 1]))

    def get_digital_output(self, field, output):
        """
        Bekommt den aktuellen Wert des Ausganges.\n
        Dabei ist das Register freiwaehltbar.

        :param field: 0:"Werkzeug Ausgang"; 1: "Konfigurierbarer Ausgang"; 2: "Digitaler Ausgang"
        :param output: (int)jeweiliger Ausgang des Feldes
        :return: (bool)wenn der Ausgang angesteuert ist
        """
        if (field == 0 and output > 2) or output < 0 or output > 7:
            raise Exception("Die Zahl darf nicht kleiner als 0 oder groesser als 2 sein!")

        bits = format(self.state.actual_digital_output_bits.to_bytes(3, byteorder='big')[field], '#010b')[2:]
        return bool(int(bits[(output * -1) - 1]))

    def set_single_standard_digital_output(self, output: int, value: bool) -> None:
        """
        Es wird nur der Ausgang mit dem Wert beschrieben.
        :param value: (bool) Ausgang zustand
        :param output: (int) Welcher Ausgang angesprochen werden soll
        :return: None
        """
        standard_digital_output_list = self.int_to_maskList(self.get_setup("standard_digital_output"))
        standard_digital_output_list[output] = value
        self.set_setup("standard_digital_output", self.maskList_to_int(standard_digital_output_list))

    def set_list_standard_digital_output(self, output: list) -> None:
        """
        Es werden nur die Ausgänge vom Reiter 'Digitaler Ausgang' die ein True in der List haben.
        :param output: (list) Liste der Ausgaenge
        :return: None
        """
        self.set_setup("standard_digital_output", self.maskList_to_int(output))

    def set_single_standard_digital_output_mask(self, output: int):
        """
        Es wird ein einziger Digitaler Ausgang hinzugefuegt oder entfernt welcher der Computer kontrolliert.
        :param output: (int) Ausgangs Nummer
        :return: None
        """
        mask_list = self.int_to_maskList(self.get_setup("standard_digital_output_mask"))
        mask_list[output] = not mask_list[output]
        self.set_setup("standard_digital_output_mask", self.maskList_to_int(mask_list))

    def set_list_standard_digital_output_mask(self, output: list):
        """
        Es wird bestimmt welcher Digitaler Ausgang von dem Computer kontrolliert wird.
        :param output: (list) Eine Liste der Ausgaenge zum Kontrollieren
        :return: None
        """
        self.set_setup("standard_digital_output_mask", self.maskList_to_int(output))

    def set_configurable_digital_out(self, output: int, value: bool) -> None:
        pass

    def set_tcp(self, tup: tuple) -> None:
        # self.tcp = tup
        pass
