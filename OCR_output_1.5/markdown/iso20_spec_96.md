binary encryption provides a confidentiality protected way for private key provisioning to the EVCC without having intermediaries access to this private key. Both approaches require asymmetric key material. The credentials for EVCC signing are provided by the private key associated with the contract certificate and credentials for EVCC receiving encrypted data are provided by an ECDH key exchange as described in 7.9.2.5.4.

An OEM provisioning certificate enables an EVCC to request a valid contract certificate for PnC.

Refer to 7.3.6 and is subclauses for further details of securing the private keys in EVCC.

##### 7.9.2.3 Contract certificates as XML signature credentials

Contract certificate is bound to an EMAID and used in XML signature to authorize the EV for charging. The contract certificate's attributes, like signature and validity period, can be verified even if the SECC is offline, given that the corresponding root CA certificate is stored locally on the SECC. For checking the revocation status via OCSP, the SECC needs to be online. The contract binding is handled as follows.

[V2G20-108] The EMAID shall be encoded in the subject of the certificate.

NOTE The EVCC is sending the sub-CA certificates within its authentication request so that the SECC can check the certificate chain up to the root certificate which it has stored itself.

##### 7.9.2.4 XML security specifics for "PnC" message set(s)

###### 7.9.2.4.1 XML data structures for application layer security

Security on application layer is provided using signature and encryption of messages. Information targeted for SA services is exchanged using XML data structures. Consequently, this information can be protected end-to-end using XML security.

###### 7.9.2.4.2 XML signature mechanism

This subclause is intended as an introduction to XML signatures. For an overview on XML signatures see ISO 15118-2:2014.

NOTE 1 This document uses different ECC algorithms, signature algorithms, hash algorithms, etc. as compared to the examples in ISO 15118-2:2014. Hence the examples in ISO 15118-2:2014, do not directly apply to this document, but are very close.

XML signatures as defined in W3C XML can be applied to arbitrary digital content (data objects) in the same way as digital signatures are calculated. When applying a digital signature to data objects, the data objects are first digested (hashed) and the result is then signed using an asymmetric algorithm like ECDSA or EdDSA. In the case of XML, the digest is placed in an XML element, together with additional information. This element is then hashed and cryptographically signed. This document uses detached XML signatures according to W3C XML. That means the signature and data can be in separate (externally detached) or in the same XML document (internally detached) as sibling elements. The signature may comprise only a part of the XML document referenced by an ObjectID.

Figure 13 shows the schema diagram of the XML signature element included in the V2G message header.