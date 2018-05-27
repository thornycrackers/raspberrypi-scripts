import glob
import time
import Adafruit_CharLCD as LCD
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

def initialize_lcd():
    """Initialize LCD for usage."""
    lcd_backlight = 4
    lcd_rs = 25
    lcd_en = 24
    lcd_d4 = 23
    lcd_d5 = 17
    lcd_d6 = 18
    lcd_d7 = 22
    lcd_columns = 16
    lcd_rows    = 2
    return LCD.Adafruit_CharLCD(
        lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, 
        lcd_columns, lcd_rows, lcd_backlight)

def initialize_mcp3008():
    """Initialize mcp3008 for reading."""
    SPI_PORT   = 0
    SPI_DEVICE = 0
    return Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

def get_device_file():
    """Get the path to the the data file."""
    base_dir = '/sys/bus/w1/devices/'
    device_folder = glob.glob(base_dir + '28*')[0]
    device_file = device_folder + '/w1_slave'
    return device_file


def read_device_file(device_file):
    """Read the raw temperature from the device."""
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines


def parse_raw_input(raw_input):
    """Parse raw data into temperatures."""
    # Error reading, return nothing
    if raw_input[0].strip()[-3:] != 'YES':
        return None, None
    equals_pos = raw_input[1].find('t=')
    if equals_pos != -1:
        temp_string = raw_input[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f
    else:
        return None, None

def voltage_to_moisture(data):
    """Turn adc value into percent

    The value from the YL-69 can read between 0-1023 where 1023 is dry. If we
    want to display the moisture percent we need to do a bit of math.
    """
    val = 1024 - data
    return val / 1024 * 100

def main():
    """Main routine for reading values and printing to lcd."""
    lcd = initialize_lcd()
    temp_device_file = get_device_file()
    mcp3008 = initialize_mcp3008()
    print('Writing to LCD.')
    print('Press Ctrl-C to quit')
    while True:
        moisture = voltage_to_moisture(mcp3008.read_adc(0))
        raw_temp_input = read_device_file(temp_device_file)
        degrees_c, _ = parse_raw_input(raw_temp_input)
        msg = "Moisture: {:.2f}\nTemp: {:.2f}".format(moisture, degrees_c)
        lcd.clear()
        lcd.message(msg)
        time.sleep(1)

if __name__ == '__main__':
    main()
