This document does not provide a specific methodology to put the PE SECC or the EVCC in CPM4PE. It leaves those methodologies on the PE EVSE manufacturers/OEMs to define and describe in appropriate user/owner's manuals.

The PE EVSE manufacturers/OEMs should include basic constraints necessary to install these trust anchors. For example, "The user presses the button on the PE EVSE and the EV before connecting the charging cable," etc.

A push button or other similar methods requiring explicit user interaction could be used on both the PE SECC and the EVCC to install new trust anchors. Figure H.12 provides an example of how the flow could work.

In summary, it can be said that the manufacturers of a PE EVSE or an EV should therefore carefully consider how they want to offer PE charging to the user. They need to make a business decision:

- Whether they are facing challenge 1:

Have high security with advanced and intelligent charging functions with advantages like:

– simplified PE with no need for PE owner to manage the necessary trust anchors (PE private root CA certificate(s) and OEM root CA certificate(s)) for mutual authentication.

While accepting disadvantages like:

pre-installing and managing (e.g. securely reinstalling, renewing, etc.) the necessary trust anchors (PE private root CA certificate(s) and OEM root CA certificate(s)) for mutual authentication so that the TLS connection is not rejected;

this will additionally limit the availability and use or PE. For example, the EV user will not be able to charge using ISO 15118-20 based communications at a PE EVSE not approved by the OEM (DIN SPEC 70121, Table 5 based charging is still allowed).

## OR

- Whether they are facing challenge 2:

Reduced security and possibly limit the scope of their charging functions with advantages like:

– expanded availability and use of PE with the user able to charge using ISO 15118-20 based communications at any PE EVSE;

While accepting disadvantages like:

- requires PE owner to manage the necessary trust anchors (PE private root CA certificate(s) and OEM root CA certificate(s)) for mutual authentication;

- requires EV owner to manage the necessary trust anchors (PE private root CA certificate(s)) for mutual authentication;

– user interaction necessary to provision the necessary trust anchors (PE private root CA certificate(s) and OEM root CA certificate(s)) in the private SECC and the EVCC for mutual authentication so that the TLS connection is not rejected. CPM4PE could be used for this purpose (refer to H.2.2.3 for details of CPM4PE).

Trust anchor (certificate) installation could also be done by using any other communication channel to the EV the OEM offers for this purpose. This communication channels may include an OEM online service, a diagnostic interface of the EV used at a garage, an USB interface contained in the EV, etc.

The PE EVSE manufacturers and OEMs could support both challenge 1 and challenge 2 at the same time. They could install and maintain some of the trust anchors used in PE while allowing users to install and