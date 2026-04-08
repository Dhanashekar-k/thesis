
<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Description</td><td style='text-align: center; word-wrap: break-word;'>Length (Byte)</td><td style='text-align: center; word-wrap: break-word;'>Example</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>RFU (proprietary use)</td><td style='text-align: center; word-wrap: break-word;'>3</td><td style='text-align: center; word-wrap: break-word;'>XX XX XX</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>CRC16</td><td style='text-align: center; word-wrap: break-word;'>2</td><td style='text-align: center; word-wrap: break-word;'>a6 09</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Summary</td><td style='text-align: center; word-wrap: break-word;'>8</td><td style='text-align: center; word-wrap: break-word;'>510403XXXXXXa609</td></tr></table>

The EV ID is stored in the user memory of the tag from address 0 and comprises 18 bytes of data (ASCII format) + 2 bytes of CRC16. If the EV ID is shorter than 8 bytes, the remaining bytes are filled with 0x00.

The nominal height of the tags above the road surface is provided so that the infrastructure mounted RFID reader can adjust to different height vehicles, e.g. double deck buses versus single deck buses.

The Salt is an optional pre-shared value for additional security. For example, it could be only known to vehicles and chargers belonging to a particular fleet operator to prevent others from using one of the operator’s chargers.

The hash value is stored from address 20 and comprises 20 bytes of data. The hash is formed from sha1 (EPC-ID + EVID + TagID + Salt) and is used for the validation and copy protection of a tag. The TagID is unique and write-protected ex works for each tag.

<div style="text-align: center;">Table E.2 — User memory</div>



<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Description</td><td style='text-align: center; word-wrap: break-word;'>Length(Byte)</td><td style='text-align: center; word-wrap: break-word;'>Example</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>EV ID</td><td style='text-align: center; word-wrap: break-word;'>18</td><td style='text-align: center; word-wrap: break-word;'>ABCDEFGHIJKLMNOPQR</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Nominal height of tag against top of road. [mm]</td><td style='text-align: center; word-wrap: break-word;'>2</td><td style='text-align: center; word-wrap: break-word;'>0c80 (3200 mm)</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>CRC16</td><td style='text-align: center; word-wrap: break-word;'>2</td><td style='text-align: center; word-wrap: break-word;'></td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Hash</td><td style='text-align: center; word-wrap: break-word;'>20</td><td style='text-align: center; word-wrap: break-word;'>sha1(EPC-ID + EVID + TagID + Salt)</td></tr></table>

##### E.2.1.3 Specific requirements for the basic RFID PPD

[V2G20-4076]

In case more than 1 tag is used, the RFID reader PPD shall indicate sufficient positional accuracy information to support pairing during the wireless SDP process when it can correctly read at least n (number of tags) - 1 tags on the vehicle.



[V2G20-4077] In case more than 1 tag is used, The RFID reader PPD shall indicate sufficient positional accuracy information to support partitioning during the positioning process when it can correctly read at least n (number of tags) - 1 tags on the vehicle.

Copied with the permission of ANSI on behalf of ISO in connection with USDOT National Electric Vehicle Infrastructure (NEVI) Formula Program. Copying not permitted. ©ISO. All rights reserved.