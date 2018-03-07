import logging

from sinara import Sinara
from i2c import Kasli, EEPROM


logger = logging.getLogger(__name__)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    serial = "Kasli-v1.0-8"
    slot = 3
    ee_data = Sinara(
        name="DIO-BNC",
        id=Sinara.ids.index("DIO-BNC"),
        data_rev=0, major=1, minor=1, variant=0, port=0,
        vendor=Sinara.vendors.index("Technosystem"))

    bus = Kasli()
    bus.configure("ftdi://ftdi:4232h:{}/2".format(serial))
    with bus:
        bus.reset()
        bus.enable(bus.EEM[slot])
        ee = EEPROM(bus)
        try:
            logger.warning("valid data %s", Sinara.unpack(ee.dump()))
        except:
            logger.warning("invalid data", exc_info=True)
        eui48 = ee.eui48()
        data = ee_data._replace(eui48=eui48)
        ee.write(0, data.pack()[:128])
        open("data/{}.bin".format(ee.fmt_eui48(eui48)), "wb").write(data.pack())
        try:
            logger.info("data readback valid %s", Sinara.unpack(ee.dump()))
        except:
            logger.error("data readback invalid", exc_info=True)