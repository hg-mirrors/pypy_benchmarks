from warnings import warnpy3k
warnpy3k("the DEVICE module has been removed in Python 3.0", stacklevel=2)
del warnpy3k

NULLDEV = 0
BUTOFFSET = 1
VALOFFSET = 256
PSEUDOFFSET = 512
BUT2OFFSET = 3840
TIMOFFSET = 515
XKBDOFFSET = 143
BUTCOUNT = 255
VALCOUNT = 256
TIMCOUNT = 4
XKBDCOUNT = 28
USERBUTOFFSET = 4096
USERVALOFFSET = 12288
USERPSEUDOFFSET = 16384
BUT0 = 1
BUT1 = 2
BUT2 = 3
BUT3 = 4
BUT4 = 5
BUT5 = 6
BUT6 = 7
BUT7 = 8
BUT8 = 9
BUT9 = 10
BUT10 = 11
BUT11 = 12
BUT12 = 13
BUT13 = 14
BUT14 = 15
BUT15 = 16
BUT16 = 17
BUT17 = 18
BUT18 = 19
BUT19 = 20
BUT20 = 21
BUT21 = 22
BUT22 = 23
BUT23 = 24
BUT24 = 25
BUT25 = 26
BUT26 = 27
BUT27 = 28
BUT28 = 29
BUT29 = 30
BUT30 = 31
BUT31 = 32
BUT32 = 33
BUT33 = 34
BUT34 = 35
BUT35 = 36
BUT36 = 37
BUT37 = 38
BUT38 = 39
BUT39 = 40
BUT40 = 41
BUT41 = 42
BUT42 = 43
BUT43 = 44
BUT44 = 45
BUT45 = 46
BUT46 = 47
BUT47 = 48
BUT48 = 49
BUT49 = 50
BUT50 = 51
BUT51 = 52
BUT52 = 53
BUT53 = 54
BUT54 = 55
BUT55 = 56
BUT56 = 57
BUT57 = 58
BUT58 = 59
BUT59 = 60
BUT60 = 61
BUT61 = 62
BUT62 = 63
BUT63 = 64
BUT64 = 65
BUT65 = 66
BUT66 = 67
BUT67 = 68
BUT68 = 69
BUT69 = 70
BUT70 = 71
BUT71 = 72
BUT72 = 73
BUT73 = 74
BUT74 = 75
BUT75 = 76
BUT76 = 77
BUT77 = 78
BUT78 = 79
BUT79 = 80
BUT80 = 81
BUT81 = 82
BUT82 = 83
MAXKBDBUT = 83
BUT100 = 101
BUT101 = 102
BUT102 = 103
BUT103 = 104
BUT104 = 105
BUT105 = 106
BUT106 = 107
BUT107 = 108
BUT108 = 109
BUT109 = 110
BUT110 = 111
BUT111 = 112
BUT112 = 113
BUT113 = 114
BUT114 = 115
BUT115 = 116
BUT116 = 117
BUT117 = 118
BUT118 = 119
BUT119 = 120
BUT120 = 121
BUT121 = 122
BUT122 = 123
BUT123 = 124
BUT124 = 125
BUT125 = 126
BUT126 = 127
BUT127 = 128
BUT128 = 129
BUT129 = 130
BUT130 = 131
BUT131 = 132
BUT132 = 133
BUT133 = 134
BUT134 = 135
BUT135 = 136
BUT136 = 137
BUT137 = 138
BUT138 = 139
BUT139 = 140
BUT140 = 141
BUT141 = 142
BUT142 = 143
BUT143 = 144
BUT144 = 145
BUT145 = 146
BUT146 = 147
BUT147 = 148
BUT148 = 149
BUT149 = 150
BUT150 = 151
BUT151 = 152
BUT152 = 153
BUT153 = 154
BUT154 = 155
BUT155 = 156
BUT156 = 157
BUT157 = 158
BUT158 = 159
BUT159 = 160
BUT160 = 161
BUT161 = 162
BUT162 = 163
BUT163 = 164
BUT164 = 165
BUT165 = 166
BUT166 = 167
BUT167 = 168
BUT168 = 169
BUT181 = 182
BUT182 = 183
BUT183 = 184
BUT184 = 185
BUT185 = 186
BUT186 = 187
BUT187 = 188
BUT188 = 189
BUT189 = 190
MOUSE1 = 101
MOUSE2 = 102
MOUSE3 = 103
LEFTMOUSE = 103
MIDDLEMOUSE = 102
RIGHTMOUSE = 101
LPENBUT = 104
BPAD0 = 105
BPAD1 = 106
BPAD2 = 107
BPAD3 = 108
LPENVALID = 109
SWBASE = 111
SW0 = 111
SW1 = 112
SW2 = 113
SW3 = 114
SW4 = 115
SW5 = 116
SW6 = 117
SW7 = 118
SW8 = 119
SW9 = 120
SW10 = 121
SW11 = 122
SW12 = 123
SW13 = 124
SW14 = 125
SW15 = 126
SW16 = 127
SW17 = 128
SW18 = 129
SW19 = 130
SW20 = 131
SW21 = 132
SW22 = 133
SW23 = 134
SW24 = 135
SW25 = 136
SW26 = 137
SW27 = 138
SW28 = 139
SW29 = 140
SW30 = 141
SW31 = 142
SBBASE = 182
SBPICK = 182
SBBUT1 = 183
SBBUT2 = 184
SBBUT3 = 185
SBBUT4 = 186
SBBUT5 = 187
SBBUT6 = 188
SBBUT7 = 189
SBBUT8 = 190
AKEY = 11
BKEY = 36
CKEY = 28
DKEY = 18
EKEY = 17
FKEY = 19
GKEY = 26
HKEY = 27
IKEY = 40
JKEY = 34
KKEY = 35
LKEY = 42
MKEY = 44
NKEY = 37
OKEY = 41
PKEY = 48
QKEY = 10
RKEY = 24
SKEY = 12
TKEY = 25
UKEY = 33
VKEY = 29
WKEY = 16
XKEY = 21
YKEY = 32
ZKEY = 20
ZEROKEY = 46
ONEKEY = 8
TWOKEY = 14
THREEKEY = 15
FOURKEY = 22
FIVEKEY = 23
SIXKEY = 30
SEVENKEY = 31
EIGHTKEY = 38
NINEKEY = 39
BREAKKEY = 1
SETUPKEY = 2
CTRLKEY = 3
LEFTCTRLKEY = CTRLKEY
CAPSLOCKKEY = 4
RIGHTSHIFTKEY = 5
LEFTSHIFTKEY = 6
NOSCRLKEY = 13
ESCKEY = 7
TABKEY = 9
RETKEY = 51
SPACEKEY = 83
LINEFEEDKEY = 60
BACKSPACEKEY = 61
DELKEY = 62
SEMICOLONKEY = 43
PERIODKEY = 52
COMMAKEY = 45
QUOTEKEY = 50
ACCENTGRAVEKEY = 55
MINUSKEY = 47
VIRGULEKEY = 53
BACKSLASHKEY = 57
EQUALKEY = 54
LEFTBRACKETKEY = 49
RIGHTBRACKETKEY = 56
LEFTARROWKEY = 73
DOWNARROWKEY = 74
RIGHTARROWKEY = 80
UPARROWKEY = 81
PAD0 = 59
PAD1 = 58
PAD2 = 64
PAD3 = 65
PAD4 = 63
PAD5 = 69
PAD6 = 70
PAD7 = 67
PAD8 = 68
PAD9 = 75
PADPF1 = 72
PADPF2 = 71
PADPF3 = 79
PADPF4 = 78
PADPERIOD = 66
PADMINUS = 76
PADCOMMA = 77
PADENTER = 82
LEFTALTKEY = 143
RIGHTALTKEY = 144
RIGHTCTRLKEY = 145
F1KEY = 146
F2KEY = 147
F3KEY = 148
F4KEY = 149
F5KEY = 150
F6KEY = 151
F7KEY = 152
F8KEY = 153
F9KEY = 154
F10KEY = 155
F11KEY = 156
F12KEY = 157
PRINTSCREENKEY = 158
SCROLLLOCKKEY = 159
PAUSEKEY = 160
INSERTKEY = 161
HOMEKEY = 162
PAGEUPKEY = 163
ENDKEY = 164
PAGEDOWNKEY = 165
NUMLOCKKEY = 166
PADVIRGULEKEY = 167
PADASTERKEY = 168
PADPLUSKEY = 169
SGIRESERVED = 256
DIAL0 = 257
DIAL1 = 258
DIAL2 = 259
DIAL3 = 260
DIAL4 = 261
DIAL5 = 262
DIAL6 = 263
DIAL7 = 264
DIAL8 = 265
MOUSEX = 266
MOUSEY = 267
LPENX = 268
LPENY = 269
BPADX = 270
BPADY = 271
CURSORX = 272
CURSORY = 273
GHOSTX = 274
GHOSTY = 275
SBTX = 276
SBTY = 277
SBTZ = 278
SBRX = 279
SBRY = 280
SBRZ = 281
SBPERIOD = 282
TIMER0 = 515
TIMER1 = 516
TIMER2 = 517
TIMER3 = 518
KEYBD = 513
RAWKEYBD = 514
VALMARK = 523
REDRAW = 528
INPUTCHANGE = 534
QFULL = 535
QREADERROR = 538
WINFREEZE = 539
WINTHAW = 540
REDRAWICONIC = 541
WINQUIT = 542
DEPTHCHANGE = 543
WINSHUT = 546
DRAWOVERLAY = 547
VIDEO = 548
MENUBUTTON = RIGHTMOUSE
WINCLOSE = 537
KEYBDFNAMES = 544
KEYBDFSTRINGS = 545
MAXSGIDEVICE = 20000
GERROR = 524
WMSEND = 529
WMREPLY = 530
WMGFCLOSE = 531
WMTXCLOSE = 532
MODECHANGE = 533
PIECECHANGE = 536
