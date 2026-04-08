- every mandatory parameter, as defined for that certificate's profile in Annex B, exists;

– all BasicConstraints attributes are set as defined for that certificate's profile in Annex B;

- DomainComponent value matches the definition of that certificate’s profile in Annex B;

- the subjectID of the leaf certificate is acceptable [e.g. if the CN (common name) of the certificate is accepted by the V2G entity];

– the subjectID of the leaf certificate is acceptable [e.g. if the CN (common name) of the certificate is accepted by the V2G entity].

e) All critical parameters are processed.

f) All non-critical parameters that are recognized by the relying party are processed.

<div style="text-align: center;">NOTE 21 A V2G entity can use the services of a secondary actor to carry out one or more of these validation steps. For example, the SECC can use the service of a secondary actor to receive revocation information for each certificate in the certificate chain the EVCC provided.</div>


NOTE 22 IETF RFC 5280 has been updated by IETF RFC 6818, IETF RFC 8398 and IETF RFC 8399. These updates are considered to be included in this document.

[V2G20-2324] When the configurable mechanism as defined by [V2G20-2320] indicates that the curve as defined by [V2G20-2319] needs to be used, certificates and certificate profiles as defined in Table B.4, Table B.6, Table B.8, Table B.10, Table B.12, Table B.14, Table B.16 and Table B.18 for that particular certificate type shall be used during certificate validation (as defined by [V2G20-1001]).

[V2G20-2325] When the configurable mechanism as defined by [V2G20-2320] indicates that the curve as defined by [V2G20-2674] needs to be used, certificates and certificate profiles as defined in Table B.3, Table B.5, Table B.7, Table B.9, Table B.11, Table B.13, Table B.15 and Table B.17 for that particular certificate type shall be used during certificate validation (as defined by [V2G20-1001]).

##### 7.3.2.1 Certificate structure

This document does not provide any mandatory PKI for implementations. It, however, defines a minimum required certificate structure that should be followed ensuring that the system as a whole is functioning. The details of the PKI, though, are left to the industry and implementers to define. For examples of the possible certificate structures/PKI, see H.1.6.

2581] When using the curve as defined by [V2G20-2674], each certificate used in this document shall comply to the appropriate profile as specified in Annex B, Table B.3, Table B.5, Table B.7, Table B.9, Table B.11, Table B.13, Table B.15 and Table B.17. When using the curve as defined by [V2G20-2319], each certificate used in this document shall comply to the appropriate profile as specified in Annex B, Table B.4, Table B.6, Table B.8, Table B.10, Table B.12, Table B.14, Table B.16 and Table B.18.

NOTE 1 Although Annex B defines certificate profiles with the two different curves, as defined by [V2G20-2674] and [V2G20-2319], it is not mandatory for a V2G entity to have certificates with both curves available at the same time. It is up to the V2G entity's discretion whether to store certificate chains with both curves at the same time or just the ones as required to be used per the configurable mechanism as defined by [V2G20-2320]. If the V2G entity chooses to store certificate chains based on just one curve, the V2G entity will need a capability to replace those certificate chains with different ones when the configurable mechanism as defined by [V2G20-2320] is updated to use the secondary curve.