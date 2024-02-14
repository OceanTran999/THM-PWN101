def big_to_little(value):
    to_left1 = (value & 0x00000000000000ff) << 56
    to_left2 = (value & 0x000000000000ff00) << 40
    to_left3 = (value & 0x0000000000ff0000) << 24
    to_left4 = (value & 0x00000000ff000000) << 8

    to_right4 = (value & 0xff00000000000000) >> 56
    to_right3 = (value & 0x00ff000000000000) >> 40
    to_right2 = (value & 0x0000ff0000000000) >> 24
    to_right1 = (value & 0x000000ff00000000) >> 8

    return to_left1 | to_left2 | to_left3 | to_left4 | to_right1 | to_right2 | to_right3 | to_right4

list1 = [0x5b5858587b4d4854, 0x6465725f67616c66, 0x58585d6465746361, 0x7d58]
list2 = [0x7fc4c7cda4c0, 0x5f5530797b4d4854, 0x5f3368745f6e3077, 0x5961774133766947, 0x3168745f446e615f, 0x756f595f73315f73, 0x7d47346c665f52]
for element in list2:
    print(hex(big_to_little(element)).replace('0x', ''))