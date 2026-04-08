certificate provisioning process (see also H.4 for contract certificate provisioning). OEM provisioning certificates are derived from the OEM root CA certificates mentioned below or V2G root CA certificates mentioned above. If derived from OEM root CA certificates, OEM provisioning certificates may optionally be cross signed by V2G root CA certificates.

– OEM root CA certificate: OEM root CA certificate is used to sign (via a chain of sub-CAs) OEM provisioning certificates mentioned above. Each OEM may create a (top level) root certificate and distribute it to the secondary actors. The root certificate of an OEM is not part of the global PKI; i.e. it is not necessarily signed by a V2G root CA certificate.

Vehicle certificate: This kind of certificate is individual for each EVCC (installed, e.g. at EV production) and is used to verify the identity of an EVCC during TLS handshake. Vehicle certificates are derived from the OEM root CA certificates mentioned above or V2G root CA certificates mentioned above. If derived from OEM root CA certificates, vehicle certificates may be cross signed by V2G root CA certificates.

– Cross certificate: A cross certificate issued by one CA for another CA to enable cross certification so that a V2G entity holding the former CA certificate can validate a certificate chain of a V2G entity that is issued by the latter V2G RootCA. See H.1.5 for detailed description of cross certificates.

In the following the general demands and restrictions caused by the OEMs (refer to H.1.2) and the secondary actors (refer to H.1.3) with respect to these kinds of certificates are explained. Based on this, the argumentation for why the certificate/security decisions made in this document are necessary or at least meaningful is described (refer to H.1.4). Finally, a visual overview of the resulting certificate structure and usage is given (refer to H.1.5.4).

#### H.1.2 Demands of the OEM

An OEM typically has the following general demands that result from their desire to keep control units (here the EVCC) from becoming very expensive. For the same reasons, manual treatment of a control unit (e.g. in a garage) causes much effort and should be avoided.

R1 Installing a certificate into an EV is only simple at EV production. Later, installation actions result in much effort in a garage. To enable certificate installation only at EV production, a certificate should be "static". That means, the certificate needs a very long validity. Since EVs are used for 20 years or longer, the certificate needs an even longer validity. Such static certificates for instance may be the root certificates (of the PKI) that are stored in the EV.

R2 Static certificates cannot be used for all purposes: The validity of a contract certificate (used for PnC) typically is only as long as the validity of the contract. Furthermore, the contract may not exist at EV production time and, therefore, the contract certificate then still does not exist. It is possible to install "non-static" certificates into an EV in an acceptable manner: Ideally, the certificate installation happens automatically via the charge protocol. If this is not possible for any reason, the certificate may be sent from the secondary actor to the customer as a file and is installed into the EV by using an online connection or the diagnosis interface (in a garage), format transformations should be avoided to reduce costs and guarantee compatibility with all secondary actors. Therefore, a standardized file format is required for certificate files (especially for contract certificates because they cannot be of static manner).

R3 Control units with much (persistent) storage are expensive, especially if the storage allows a large number of write cycles. In order to reduce the amount of storage (e.g. flash), memory required for certificates should be kept small. This results in the following sub-demands:

— the size of a single certificate should be small;