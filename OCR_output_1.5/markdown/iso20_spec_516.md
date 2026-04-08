## Annex G (informative)

# Association of VAS client to V2G session

Security of VAS has not been fully defined in this document. It will be improved upon in the next edition. The implementers should be careful about security pitfalls and risks when designing VAS systems relying on VAS security architecture specified here.

This annex has not been fully reviewed and updated in this document. It will be improved upon in the next edition. The implementers should be careful when reading and designing systems relying on information mentioned here.

In addition to the cryptographic binding in TLS layer achieved by TLS resumption ticket as described in 7.7.3.7, the application-layer association of a connecting VAS client to existing V2G session in the SECC may be accomplished as follows.

– Comparing fingerprints of the TLS master key contained in the session ticket.

- Export hash of master secret from running TLS sessions to VAS process for comparison.

- Export hash of master secret from session ticket received to VAS process for comparison.

– The implementation can be achieved for example by inter-process-communication between the VAS and V2G process or an intermediary database.

– Pre-shared credentials keys based on exported key material from TLS (refer to IETF RFC 5705 as updated by IETF RFC 8446 and IETF RFC 8447).

– The key export shall use the label EXPORTER_V2G_VAS.

– The EVCC authenticates against the VAS using digest authentication (refer to IETF RFC 7235, IETF RFC 7615, IETF 7616 and IETF RFC 7617) with a username password combination derived from the V2G session:

- § Username: V2G session ID,

- § Password: Exported key material.

The V2G process exports the login information to the VAS process.