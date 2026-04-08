authorization methods could be required. Regardless of the methodology used, CPM4PE on private SECC can only be activated by explicit user interaction.

[V2G20-2377] The CPM4PE shall expire on the private SECC at least 120 s after the user activates the mode. Refer to H.2.2.3 for details of CPM4PE.

NOTE 14 Longer times can result in user experience issues.

[V2G20-1007] A public SECC shall send in the "ServerHello" message its own certificate chain (SECC certificate chain) including any necessary cross-certificates up to a root (excluding the root certificate itself), which shall be one of those roots previously indicated by the EVCC as being present in the EVCC.

[V2G20-2378] If the EVCC did not provide any indication of the available roots (i.e. the "authorities" element of "certificate_authorities" extension in the "ClientHello" message is empty), a public SECC shall send in the "ServerHello" message its own certificate chain (SECC certificate chain) including any necessary cross certificates up to a root (excluding the root certificate itself) of its own choosing.

[V2G20-2379] If the EVCC provides a list of the available roots (i.e. the "authorities" element of "certificate_authorities" extension in the "ClientHello" message is not empty), the public SECC shall follow IETF RFC 5280:2008, 7.1, as updated by IETF RFC 6818, IETF RFC 8398 and IETF RFC 8399, to utilize the received "DistinguishedNames" (see [V2G20-1006]) to choose an SECC certificate chain originating from one of the received "DistinguishedNames" and provide it to the EVCC in "ServerHello" message as defined in IETF RFC 8446.

[V2G20-2380] If the EVCC offers and the public SECC chooses a named group and signature algorithm based on curves as defined by [V2G20-2674] (as per the configurable mechanism as defined by [V2G20-2320]), the SECC certificate chain provided by the public SECC in the "ServerHello" message shall be based on profiles as defined in B.4.1.

[V2G20-2381] If the EVCC offers and the public SECC chooses a named group and signature algorithm based on curves as defined by [V2G20-2319] (as per the configurable mechanism as defined by [V2G20-2320]), the SECC certificate chain provided by the public SECC in the "ServerHello" message shall be based on profiles as defined in B.4.2.

[V2G20-2382] A private SECC not in CPM4PE shall send the "ServerHello" message containing its own certificate chain (PE certificate chain) including any necessary cross-certificates up to a root (excluding the root certificate itself), which shall be one of those roots previously indicated by the EVCC as being present in the EVCC. Refer to H.2.2.3 for details of CPM4PE.

[V2G20-2383] If the EVCC provides a list of the available roots (i.e. the "authorities" element of "certificate_authorities" extension in the "ClientHello" message is not empty), the private SECC shall follow IETF RFC 5280:2008, 7.1 as updated by IETF RFC 6818, IETF RFC 8398 and IETF RFC 8399, to utilize the received "DistinguishedNames" (see [V2G20-1006]) to choose a PE certificate chain originating from one of the received "DistinguishedNames" and provide it to the EVCC in "ServerHello" message as defined in IETF RFC 8446.

[V2G20-2384] If the EVCC did not provide any indication of the available roots (i.e. the EVCC the "authorities" element of "certificate_authorities" extension in the "ClientHello"