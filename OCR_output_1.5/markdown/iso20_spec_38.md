d Upon OEM's discretion the vehicle certificate and OEM provisioning certificate chain may originate from V2G root CA certificate. This type of arrow shows when the sub-CA1 is signed by the V2G root CA.

Upon OEM's discretion the vehicle certificate and OEM provisioning certificate chain may originate from V2G root CA certificate. This type of arrow shows when the sub-CA1 is not used and sub-CA2 is signed by the V2G root CA.

## Figure 7 — Certificate structure originating from OEM root CA certificate

## [V2G20-2335]

A PE certificate shall be generated using a certificate chain that uses a PE private root CA certificate as the trust anchor. Refer to Annex H for further details. Refer to H.1.6 for examples of certificate structure. Refer to Annex B for details of the certificate profile.

[V2G20-2336] A PE certificate chain shall not be signed or cross-signed by any CA under a V2G root CA or an eMSP root CA or an OEM root CA. Similarly, PE certificate chain shall not be signed or cross-signed by any V2G root CA or eMSP root CA or OEM root CA.

NOTE 13 A PE certificate chain can, however, be cross-signed by a CA in another PE certificate chain.

###### 7.3.2.1.1 Minimum required/mandatory certificates

Some certificates are needed for the functioning of this document. This subclause defines the minimum certificates required both in the SECC and the EVCC that allows basic communication to function. The basic function is defined as being able to setup the communication and utilize EIM for authorization of services. This subclause does not cover requirements for the private SECC.

The SECC shall contain an SECC certificate. This certificate is necessary to establish a TLS session. Refer to 7.3.2.1 for SECC certificate requirements.

NOTE 1 In case of cross-signing the SECC certificate chain, the SECC can actually contain multiple sub-CA certificates and cross certificates.

[V2G20-2338] Each SECC shall possess at least one of either of the following root certificates:

- V2G root CA certificate;

– OEM root CA certificate.

NOTE 2 This means that at any given time, the SECC can have at least one of the above valid root certificates. Since the vehicle certificate used during TLS session setup is based on at least one, if not both, of the root certificates mentioned here, an SECC cannot support communication without at least one of these roots.

NOTE 3 The SECC can possess more than one V2G root CA certificates.

NOTE 4 The SECC can possess more than one OEM root CA certificates.

NOTE 5 The SECC can possess both V2G root CA certificates and OEM root CA certificates.

[V2G20-2339] The EVCC shall contain a vehicle certificate. This certificate is necessary to establish a TLS session. Refer to 7.3.2.1 for vehicle certificate requirements.

NOTE 6 In case of cross-signing the vehicle certificate chain in the EVCC can actually contain multiple sub-CA certificates and cross certificates.

[V2G20-2340] The EVCC shall possess at least one V2G root CA certificate. This certificate is necessary to verify SECC certificates to establish TLS session. Refer to 7.3.2.1 for V2G root CA certificate requirements.

NOTE 7 The EVCC can possess more than one V2G root CA certificates.