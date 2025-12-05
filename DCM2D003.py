from pymodbus.client import ModbusTcpClient

class DCM2D003(object):


    REG_MODBUS_ADDRESS  = 0x0101
    REG_TURN_TIME       = 0x0105

    REG_TOTAL_ENERGY    = 0x0000
    REG_VOLTAGE         = 0x0131
    REG_CURRENT         = 0x0139
    REG_ACTIVE_POWER    = 0x0141

    REG_CT_PARAMETER_1  = 0x0076
    REG_CT_PARAMETER_2  = 0x0077

    def __init__(self, client, dev_address=1):
        self.client = client
        self.dev_address = dev_address

    ###########################################################################
    def readTurnTime(self):
        result = client.read_holding_registers(self.REG_TURN_TIME, count=1, device_id=self.dev_address)
        self.turn_time = result.registers[0]
        print("turn_time", self.turn_time)

    def writeTurnTime(self, turntime=2):
        self.client.write_register(self.REG_TURN_TIME, turntime, device_id=self.dev_address)
    ###########################################################################
    def readCTparameters(self):
        # rated signal strength 11 = 45mV, 22 = 60mV, 33 = 75mV
        result = self.client.read_holding_registers(self.REG_CT_PARAMETER_1, count=1, device_id=self.dev_address)
        print("Rated signal strength", result.registers[0])

        # rated current
        result = self.client.read_holding_registers(self.REG_CT_PARAMETER_2, count=1, device_id=self.dev_address)
        print("Rated current", result.registers[0])

    def writeCTparameters(self, strength=33, current=10):
        self.client.write_register(self.REG_CT_PARAMETER_1, strength, device_id=self.dev_address)
        self.client.write_register(self.REG_CT_PARAMETER_2, current, device_id=self.dev_address)
   
    ###########################################################################
    def writeModbusAddress(self, new_dev_address):
        self.client.write_register(self.REG_MODBUS_ADDRESS, new_dev_address, device_id=self.dev_address)
    ###########################################################################

    def readVoltage(self):
        result = self.client.read_input_registers(self.REG_VOLTAGE, count=1, device_id=self.dev_address)
        self.voltage = int(result.registers[0])/10
        print("U:", self.voltage)
        return self.voltage

    def readCurrent(self):
        result = self.client.read_input_registers(self.REG_CURRENT, count=2, device_id=self.dev_address)
        print(result)
        self.current = int(result.registers[1])/1000
        print("I:", self.current)
        return self.current

    def readTotalActiveEnergy(self):
        result = self.client.read_input_registers(self.REG_TOTAL_ENERGY, count=2, device_id=self.dev_address)
        print(result)
        #print( int(result.registers[0])/10)

    def readActivePower(self):
        result = self.client.read_input_registers(self.REG_ACTIVE_POWER, count=2, device_id=self.dev_address)
        print(result)
        print( int(result.registers[1])/10)

if __name__ == "__main__":
    client = ModbusTcpClient('modbus02', port=502)
    meter21 = DCM2D003(client, dev_address=21)
    meter22 = DCM2D003(client, dev_address=22)
    meter23 = DCM2D003(client, dev_address=23)

    for meter in [meter21, meter22, meter23]:
        print("#"*80)
        print("\tModbus Addr:", meter.dev_address)
        print()
        meter.writeTurnTime(2)
        meter.readTurnTime()

        meter.readCTparameters()
        meter.writeCTparameters()

        meter.readVoltage()
        meter.readCurrent()
        meter.readTotalActiveEnergy()
        meter.readActivePower()


