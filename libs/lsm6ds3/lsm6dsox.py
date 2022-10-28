
import array
from micropython import const

_CTRL3_C = const(0x12)
_CTRL1_XL = const(0x10)
_CTRL8_XL = const(0x17)
_CTRL9_XL = const(0x18)

_CTRL2_G = const(0x11)
_CTRL7_G = const(0x16)

_OUTX_L_G = const(0x22)
_OUTX_L_XL = const(0x28)
_MLC_STATUS = const(0x38)

_DEFAULT_ADDR = const(0x6A)
_WHO_AM_I_REG = const(0x0F)

_FUNC_CFG_ACCESS = const(0x01)
_FUNC_CFG_BANK_USER = const(0)
_FUNC_CFG_BANK_HUB = const(1)
_FUNC_CFG_BANK_EMBED = const(2)

_MLC0_SRC = const(0x70)
_MLC_INT1 = const(0x0D)
_TAP_CFG0 = const(0x56)

_EMB_FUNC_EN_A = const(0x04)
_EMB_FUNC_EN_B = const(0x05)

class LSM6DSOX:


    def __init__(
        self,
        i2c,
        address=_DEFAULT_ADDR,
        gyro_odr=104,
        accel_odr=104,
        gyro_scale=2000,
        accel_scale=4,
        ucf=None,
    ):
        self.i2c = i2c
        self.address = address

        # allocate scratch buffer for efficient conversions and memread op's
        self.scratch_int = array.array("h", [0, 0, 0])

        SCALE_GYRO = {250: 0, 500: 1, 1000: 2, 2000: 3}
        SCALE_ACCEL = {2: 0, 4: 2, 8: 3, 16: 1}
        # XL_HM_MODE = 0 by default. G_HM_MODE = 0 by default.
        ODR = {
            0: 0x00,
            1.6: 0x08,
            3.33: 0x09,
            6.66: 0x0A,
            12.5: 0x01,
            26: 0x02,
            52: 0x03,
            104: 0x04,
            208: 0x05,
            416: 0x06,
            888: 0x07,
        }

        gyro_odr = round(gyro_odr, 2)
        accel_odr = round(accel_odr, 2)

        # Soft-reset the device.
        self.reset()

        # Set Gyroscope datarate and scale.
        # Note output from LPF2 second filtering stage is selected. See Figure 18.
        self.__write_reg(_CTRL1_XL, (ODR[accel_odr] << 4) | (SCALE_ACCEL[accel_scale] << 2) | 2)

        # Enable LPF2 and HPF fast-settling mode, ODR/4
        self.__write_reg(_CTRL8_XL, 0x09)

        # Set Gyroscope datarate and scale.
        self.__write_reg(_CTRL2_G, (ODR[gyro_odr] << 4) | (SCALE_GYRO[gyro_scale] << 2) | 0)

        self.gyro_scale = 32768 / gyro_scale
        self.accel_scale = 32768 / accel_scale

    def __read_reg(self, reg, size=1):
        self.i2c.write(self.address, bytes(reg))
        buf = self.i2c.read(self.address, size)
        if size == 1:
            return int(buf[0])
        return [int(x) for x in buf]

    def __write_reg(self, reg, val):
        self.i2c.write(self.address, bytes(reg))
        self.i2c.write(self.address,  bytes([val]))

    def reset(self):
        self.__write_reg(_CTRL3_C, self.__read_reg(_CTRL3_C) | 0x1)
        for i in range(0, 10):
            if (self.__read_reg(_CTRL3_C) & 0x01) == 0:
                return
            time.sleep_ms(10)
        raise OSError("Failed to reset LSM6DS device.")

    def set_mem_bank(self, bank):
        cfg = self.__read_reg(_FUNC_CFG_ACCESS) & 0x3F
        self.__write_reg(_FUNC_CFG_ACCESS, cfg | (bank << 6))

    def set_embedded_functions(self, enable, emb_ab=None):
        self.set_mem_bank(_FUNC_CFG_BANK_EMBED)
        if enable:
            self.__write_reg(_EMB_FUNC_EN_A, emb_ab[0])
            self.__write_reg(_EMB_FUNC_EN_B, emb_ab[1])
        else:
            emb_a = self.__read_reg(_EMB_FUNC_EN_A)
            emb_b = self.__read_reg(_EMB_FUNC_EN_B)
            self.__write_reg(_EMB_FUNC_EN_A, (emb_a & 0xC7))
            self.__write_reg(_EMB_FUNC_EN_B, (emb_b & 0xE6))
            emb_ab = (emb_a, emb_b)

        self.set_mem_bank(_FUNC_CFG_BANK_USER)
        return emb_ab


    def read_gyro(self):
        """Returns gyroscope vector in degrees/sec."""
        mv = memoryview(self.scratch_int)
        f = self.gyro_scale
        self.i2c.readfrom_mem_into(self.address, _OUTX_L_G, mv)
        return (mv[0] / f, mv[1] / f, mv[2] / f)

    def read_accel(self):
        """Returns acceleration vector in gravity units (9.81m/s^2)."""
        mv = memoryview(self.scratch_int)
        f = self.accel_scale
        self.i2c.readfrom_mem_into(self.address, _OUTX_L_XL, mv)
        return (mv[0] / f, mv[1] / f, mv[2] / f)