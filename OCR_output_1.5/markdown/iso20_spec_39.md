###### 7.3.2.1.2 Certificates required for PnC

Support for PnC is not mandatory for EVCC/SECC. It is up to the OEM/CSO to decide whether to support PnC or not. If the EVCC wants to support PnC, requirements defined in this subclause are mandatory.

[V2G20-2341] The EVCC shall contain at least one contract certificate or, in case the EVCC supports contract certificate installation via EVSE, storage space for at least one contract certificate. This certificate is necessary for PnC authorization. Refer to 7.3.2.1 for contract certificate requirements.

NOTE 1 EVCC can contain more than one contract certificate.

NOTE 2 This requirement does not provide details of how the contract certificate was installed. This document provides a methodology to install these certificates via EVSE but the OEM can choose to install contract certificates in another manner as suitable for their design.

###### 7.3.2.1.3 Certificates required for installation of contract certificates via EVSE

Support for contract certificate installation via EVSE is not mandatory. It is up to the OEM to decide whether to support contract certificate installation via EVSE or not. If the EVCC wants to support contract certificate installation via EVSE, requirements defined in this subclause are mandatory.

[V2G20-2342] The EVCC shall contain one OEM provisioning certificate. This certificate is necessary for contract certificate installation via EVSE. Refer to 7.3.2.1 for OEM provisioning certificate requirements.

NOTE If the EVCC does not want to install contract certificates via EVSE, this requirement can be skipped.

[V2G20-2343] If the EVCC does not contain an OEM provisioning certificate, it shall not send CertificateInstallationReq message. Refer to 8.3.4.3.9.2 for details of CertificateInstallationReq message. Refer to 7.9.2.5 and its subclauses for details of contract certificate installation via the EVSE.

###### 7.3.2.1.4 Minimum certificates required for PE

This subclause covers both the SECC and the private SECC.

[V2G20-2344] The SECC shall not contain any PE private root CA certificates.

NOTE 1 The SECC is assumed to always operate in public environment.

[V2G20-2345] The SECC operating in public environment shall not contain any PE certificate.

NOTE 2 The SECC is assumed to always operate in public environment.

[V2G20-2346] The private SECC shall not contain any SECC certificate.

[V2G20-2347] The private SECC shall possess a PE private root CA certificate. This certificate is necessary to establish a TLS session. Refer to 7.3.2.1 for PE private root CA certificate requirements.

[V2G20-2348] The private SECC shall contain a PE certificate. This certificate is necessary to establish a TLS session. Refer to 7.3.2.1 for PE certificate requirements.

7.3.2.2 Certificate governance

Copied with the permission of ANSI on behalf of ISO in connection with USDOT National Electric Vehicle Infrastructure (NEVI) Formula Program. Copying not permitted. ©ISO. All rights reserved.