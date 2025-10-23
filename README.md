# pcb-test


High-voltage or noisy source
       │
       ▼
 ┌────────────────┐
 │   AMC3311      │   ← isolation barrier
 │ (Isolated amp) │
 └────────────────┘
       │ (low-voltage analog output)
       ▼
 ┌────────────────┐
 │   ADS7138      │   ← ADC converts analog → digital
 │ (I²C ADC)      │
 └────────────────┘
       │ (I²C digital data)
       ▼
 Raspberry Pi

<img width="1078" height="811" alt="Screenshot from 2025-10-22 17-59-13" src="https://github.com/user-attachments/assets/42708524-bab2-490e-be04-f5f5fbb0c32a" />


## Detect the ADC devices (two)

```
$ dmesg | grep ads
[    1.561214] ti_ads7138: loading out-of-tree module taints kernel.
[    1.854918] ads7138 1-0010: error -EREMOTEIO: Failed to initialize device
[    1.855000] ads7138 1-0010: probe with driver ads7138 failed with error -121
rivieh@raspberrypi:~ $ sudo i2cdetect -y 1
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:                         -- -- -- -- -- -- -- -- 
10: 10 -- -- -- -- UU -- -- -- -- -- -- -- -- -- -- 
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
```

### Change Overlay to initiate two addresses 

```
            ads7138_1: ads7138@10 {
                compatible = "ti,ads7138";
                reg = <0x10>;
                status = "okay";
                avdd-supply = <&vdd_3v3_reg>;
            };

            ads7138_2: ads7138@15 {
                compatible = "ti,ads7138";
                reg = <0x15>;
                status = "okay";
                avdd-supply = <&vdd_3v3_reg>;
            };

```
### Some people said need to add two addresses into config.txt
### but I didn't. It works after several reboot.

```
$ sudo i2cdetect -y 1
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:                         -- -- -- -- -- -- -- -- 
10: UU -- -- -- -- UU -- -- -- -- -- -- -- -- -- -- 
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
70: -- -- -- -- -- -- -- --                         
:~ $ dmesg | grep ads
[    1.504691] ti_ads7138: loading out-of-tree module taints kernel.
```

### Now I have two devices under iio devices
```
~ $ ls /sys/bus/iio/devices/iio\:device
iio:device0/ iio:device1/ 
```


