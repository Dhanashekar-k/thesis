## BC

## charging based on PWM

Note 1 to entry: According to ISO/IEC 11889-1:2015, Annex A.

### 3.5 

## certificate

electronic document which uses a digital signature to bind a public key with an identity

Note 1 to entry: The ISO 15118 series describe several certificates covering different purposes [e.g. contract certificate including the EMAID (3.19) and OEM (3.36) provisioning certificates].

### 3.6 

## charging limit

set of physical constraints that is negotiated during a service session (3.50)

EXAMPLE Voltage, current, energy, power, etc.

### 3.7 

## charging session

collection of charging transactions at a charge point related only to the charging of an electric vehicle assigned to a specific customer in a specific timeframe with a unique identifier

Note 1 to entry: The charging session is a subset of the service session (3.50).

### 3.8 

## charging station operator

## CSO

secondary actor responsible for the installation and operation of a charging infrastructure (including charging sites), and the management of electricity to provide the requested energy transfer services

Note 1 to entry: The term CSO for charge point operator is also used in other ISO 15118 documents. This term is not recommended for trademark reasons.

### 3.9 

## communication session

sequence of time where EVCC (3.21) and SECC (3.47) interactively exchange digital information in order to manage charging or discharging the EV battery

Note 1 to entry: A communication session can be paused and resumed later several times. The communication session encapsulates zero or more energy transfer periods.

### 3.10 

## communication setup timer

timer (3.61) monitoring the time between establishment of TLS connection and reception of SessionSetupRes by EVCC (3.21)

### 3.11 

## contract certificate

certificate (3.5) issued for the EVCC (3.21) by an eMSP (3.20) sub-CA (3.57), which is used in XML signatures on application layer so that the SECC (3.47) or secondary actor can verify the signature created by the EVCC with the contract certificate issued for that EV

Note1 to entry: The secondary actor uses the EMAID (3.19), which is part of the contract certificate's subject field, to authorize the EV for charging based on the eMSP's associated e-mobility contract.