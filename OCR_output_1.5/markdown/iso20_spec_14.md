## OEM provisioning certificate

certificate (3.5) issued to the EVCC (3.21) by the OEM (3.36) to enable the provisioning of a contract certificate (3.11)

Note 1 to entry: It is securely requested and received from a secondary actor to uniquely identify the EVCC.

### 3.38 

## PE certificate

leaf certificate (3.5) issued in PE (3.42) to a private SECC (3.43) by a PE private root CA or optionally by a PE sub CA, which is used in TLS so that the EVCC (3.21) can verify the authenticity of the private SECC

### 3.39 

## PE EVSE

EVSE that is operating in a private environment (3.42) and is containing or being controlled by a private SECC (3.43)

### 3.40 

## performance time

non-functional timing requirement defining the time a V2G entity (3.65) should not exceed when executing or processing certain functionality

Note 1 to entry: This is a fixed time value.

### 3.41 

## park and charge

## PnC

authorization mechanism using certificates (3.5) stored in the EV which does not require any user interaction

### 3.42 

## private environment

## PE

area of private responsibility with physical access limited to a small number of vehicles

### 3.43 

## private SECC

SECC (3.47) operating in a private environment (3.42) that uses a PE certificate (3.38)

Note 1 to entry: PE (3.42) usually implies lower security. In most cases SECC requirements will also apply to a private SECC. In some specific cases, the SECC and private SECC requirements can be distinct. Those cases and requirements will be called out as such.

### 3.44 

## public SECC

SECC (3.47) operating in a public environment that uses a PE certificate (3.38)

### 3.45 

## request-response message pair

request message and the corresponding response message

### 3.46 

## request-response message sequence

predefined sequence of request-response message pairs (3.45)

### 3.47 