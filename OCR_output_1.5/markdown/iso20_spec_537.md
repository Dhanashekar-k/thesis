
<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>#</td><td style='text-align: center; word-wrap: break-word;'>Challenge</td><td style='text-align: center; word-wrap: break-word;'>Trust</td><td style='text-align: center; word-wrap: break-word;'>Private SECC</td><td style='text-align: center; word-wrap: break-word;'>EV</td><td style='text-align: center; word-wrap: break-word;'>Usability</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>2</td><td style='text-align: center; word-wrap: break-word;'>The manufacturer initially only installs its own trust anchor, but not that of others. The user should manage the trust anchors.</td><td style='text-align: center; word-wrap: break-word;'>high through push button or other similar methods requiring explicit user interaction</td><td style='text-align: center; word-wrap: break-word;'>The private SECC only transmits the trust anchor of its PE certificate chain when it is in CPM4PE. The private SECC additionally installs new trust anchors when it is in CPM4PE. Other than that, the charging process does not change compared to charging in public. Refer to H.2.2.3 for details of CPM4PE.</td><td style='text-align: center; word-wrap: break-word;'>The EV only transmits the trust anchor of its vehicle certificate chain when it is in CPM4PE. The EV additionally installs new trust anchors when it is in CPM4PE. Other than that, the charging process does not change compared to charging in public. Refer to H.2.2.3 for details of CPM4PE.</td><td style='text-align: center; word-wrap: break-word;'>The user will need to add or update required certificates from time to time. The manufacturer of the devices does not manage the certificates for the user.</td></tr></table>

These are just some examples. Exceptions in the implementations of PE are possible.

In these private environments the certificate infrastructure can be simplified by certificates with shorter certificate chains and long validities. These are derived from a private root certificate which can be validated offline. Nevertheless encryption should be applied. In order to keep the production and operation costs of a private PE EVSE low, the following special characteristics should be considered:

There may be no connection to a backend (except, for example, a setup phase upon installation).

Maintenance needs to be minimized, i.e. on regular operation there is no human intervention necessary at all.

– No secondary actor is involved. In particular, a private SECC does not need to communicate any bills to a backend, because no special accounting for energy is done.

This means, OCSP and short lived certificates cannot be applied here. But even in a private environment, the communication between private SECC and EVCC is required; e.g. to enable the transmission of charge profiles (which may contain data with the preferred charging time, which is at night from 0:30 am to 6:00 am when lot of energy is available). In order to explicitly enable this use case regardless, this document provides tailored exceptions.

#### H.2.2 Solution for private environments

##### H.2.2.1 General

What both challenges have in common is that PE EVSE manufacturers and OEMs initially provide the certificate chains for the leaf certificates for their devices/EVs. The chains include the root CA certificate(s).

For challenge 1, PE EVSE manufacturers and OEMs are also installing and maintaining the trust anchors for the leaf certificates that their devices/EVs are allowed to work with and limiting the usage to those certificates.