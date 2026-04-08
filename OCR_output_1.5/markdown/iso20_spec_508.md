- All separators and leading zeros are removed before calculating the check digit.
- While the numbers (DIGIT) keep their value, the letters (ALPHA) are mapped to values from A=10 to Z=35.
; The mapping is case-insensitive, i.e. "D" as well as "d" maps to the value 13.
- In the resulting <value string>, each digit is multiplied with the weight  $ 2^{(<pos> \text{modulo } 28))} $ ("2 to the power of (<pos> \text{modulo } 28)"), where <pos> represents the position of the digit in the <value string> and <pos> starts on the left with number zero. The resulting products are summed up to <CHECKSUM>.
; The modulo 28 method was introduced to allow calculating the check digit within 32-bit integers.
- Finally, <CHECKSUM> is taken "modulo 11". The result of this modulo computation is a number between "0" and "10". The numbers between "0" and "9" are taken as <Check Digit>, the <Check Digit> for "10" is the letter "X" (or case-insensitive "x", like the Latin numeral for "10").

NOTE This algorithm is able to identify single typing errors as well as single transposed characters.

EXAMPLE For the <EMAID> "DE-0008AA-1A2B3C4D5" first all leading zeros within the elements and separators are removed, resulting in the significant characters "DE8AA1A2B3C4D5". The 14 characters of "DE8AA1A2B3C4D5" are transcoded to values, resulting in the <value string> "1314810101102113124135" and the <CHECKSUM> "15664971". The modulo-11 computation results in the <Check Digit> "3" which is appended to the <EMAID> to form the correct string "DE-8AA-1A2B3C4D5-3".