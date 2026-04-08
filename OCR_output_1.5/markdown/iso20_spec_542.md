Additionally, public CAs also provide certificate revocation services to revoke certificates in cases of compromise of private keys, entity no longer in service, etc. private CAs are not required to provide these services.

While in challenge 1 the OEM/PE EVSE manufacturer is installing the trust anchors and could potentially do some due diligence to ensure that those trust anchors are actually trust worthy and the certificate chains signed by those trust anchors are secure, in challenge 2 the user actually installs the trust anchors both in the EV and the PE EVSE. The user will likely neither be knowledgeable in PKI security nor be able to perform the necessary due diligence before installing the trust anchors.

Hence, the use of private environment should be weighed against the security risks that it presents.

### H.3 Solution for emergency and disaster situations

In case of big infrastructure failures (regional communication outage, etc.) or major natural disasters (tsunami, earth quake, flooding due to heavy rain, etc.) a functioning transport system is of big importance in order to resolve the crisis and to provide urgent relief.

With EVs another important service can be provided in the form of mobile energy delivery to critical places. This is commonly encapsulated in the categories of vehicle-to-grid (V2G), vehicle-to-home (V2H), vehicle-to-infrastructure (V2I) or vehicle-to-vehicle (V2V). The ISO 15118 series provides the technical foundation to solve those problems.

Since in some disaster situations a reliable communication infrastructure cannot be guaranteed ISO 15118 has made the following key design decision:

Certificates are validated on a peer-to-peer basis between the EVCC and the SECC.

Certificates are used to ensure trusted business relations in day to day life. In order to ensure the highest level of disaster resilience it is recommended that all equipment (EVSEs and EVs) have a documented switch or mode setting, which disables the certificate and business level of the protocol and falls back to only the safety related parts (e.g. voltage negotiation). If both sides of the charging cable signal, that they are willing to work with "uncertified" messages then this type of operation should be permitted.

Additionally, during such events it should be possible to bypass certificate revocations checks, etc.

For EVSEs this mode should only be accessible after physically opening the housing of the system and it should only be "obvious" to a trained technician how to enable it. However, it should not require highly sophisticated configuration tools, as those might not be at hand during those types of events, as disasters from the past have shown.

Any misuse of the emergency/disaster feature can easily be handled after the fact by the legal system. The rational here is that if someone has the will and the means to open an EVSE and gain physical access to the power cables he most likely has a valid reason for this type of action. It typically will only happen in emergency and disaster situations.

### H.4 Use of OEM provisioning certificates

The difficulty with the handling of contract certificates (as defined in this document) for the OEM is to bring such a certificate into an EV. This becomes necessary in many situations as, for example, EV handover to customer, energy contract conclusion, changing the mobility provider, exchanging the component containing the contract certificate at EV repair, expired contract certificates, etc.

Using a diagnosis tool to write a file containing a contract certificate (that the customer received from the mobility provider at contract conclusion) into the EV is impractical, since such a manual procedure in a