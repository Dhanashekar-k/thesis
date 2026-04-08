NOTE 2 When pausing a V2G communication session, the EVCC turns OFF its transport layer connection which induces a phase of no active communication and no power transfer, therefore no value added services are usable during a pause either.

[V2G20-2099]

During a pause period with conductive charging and communication via PLC, the physical connection shall be maintained throughout the entire service session.



NOTE 3 Any physical disconnection, for example, removal of the connector, will result in abortion of the service session.

###### 8.3.4.1.4 V2G session resumption

[V2G20-1199] In scheduled control mode, the EVCC shall ensure it is resuming the communication session according to [V2G20-1541], while the applied EVPowerProfileEntry is still equal to 0 kW.

During V2G communication session resumption, the SECC compares the SessionID (received in the current SessionSetupReq) and the vehicle certificate (received during the TLS handshake for the currently active TLS session in which the SessionSetupReq for V2G communication session resumption is received) with the SessionID and the vehicle certificate data that was stored when the corresponding V2G communication session was initially setup. If the data does not match, V2G communication session resumption will fail. For example, if the vehicle certificate provided during initial V2G communication session setup is different than the vehicle certificate provided during V2G communication session resumption because the vehicle certificate was updated as it was about to expire, the SECC will detect this as a request to initiate a new V2G communication session, not to resume the previously paused V2G communication session.

Similarly, during V2G communication session resumption, the EVCC compares the SessionID (received in the current SessionSetupRes) and the SECC certificate (received during the TLS handshake for the currently active TLS session in which the SessionSetupRes for V2G communication session resumption is received) with the SessionID and the SECC certificate data that was stored when the corresponding V2G communication session was initially setup. If the data does not match, V2G communication session resumption will fail. For example, if the SECC certificate provided during initial V2G communication session setup is different than the SECC certificate provided during V2G communication session resumption because the SECC certificate was updated as it was about to expire, the EVCC will detect this as an issue and terminate the V2G communication session. It will then setup a new V2G communication session.

Since setting up a new V2G communication session (i.e. a V2G communication session with new SessionID) means that the previous authorizations are no longer valid. This requires the EVCC requesting authorization of the session once again. This can become an issue, especially in cases where user interaction is required for authorization (e.g. in EIM). Hence, the EVCC should be careful about pausing the V2G session close to SECC certificate's expiration and its own vehicle certificate's expiration.

The EVCC receives the SECC certificate in the TLS handshake and can get the SECC certificate’s expiration date/time stamp from the SECC certificate. The EVCC contains its own vehicle certificate and can get the vehicle certificate’s expiration date/time stamp from the vehicle certificate.

Before EVCC can resume a paused V2G session, it needs to start a new TLS session.

[V2G20-2073]

When the EVCC wants to resume the previously paused V2G communication session, the EVCC shall follow 7.7.3.3, 7.7.3.4 and 7.7.3.5 to set up a new TLS session that can be used for V2G session resumption.

