from pymodbus.client import ModbusTcpClient

# Konfiguration des Modbus-Clients
client = ModbusTcpClient('modbus02', port=502)  # Stelle sicher, dass die IP-Adresse korrekt ist

# Verbindung zum Gerät herstellen
client.connect()

# Auslesen des Registers 0079 (Register 79 in dezimaler Form)
address = 0x0079  # Registeradresse
address = 0x0105  # Registeradresse

for device_address in range(247):
    print("device: ", device_address)
    try:
        result = client.read_holding_registers(address, count=1, device_id=device_address)

        if result.isError():
            print("Fehler beim Auslesen des Registers:", result)
        else:
            value = result.registers[0]
            print(f"Wert von Register {address}: {value}")
    except Exception as e:
        print("\t", e)

# Verbindung schließen
client.close()
