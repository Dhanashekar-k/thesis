[V2G20-099]

The EXI coder for encoding and decoding of the ISO 15118 communication shall use the default EXI coding options according to W3C EXI 1.0, subclause "EXI options" with the exception of the options listed in Table 15.



<div style="text-align: center;">Table 15 — EXI option settings</div>



<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>EXI Option</td><td style='text-align: center; word-wrap: break-word;'>Description</td><td style='text-align: center; word-wrap: break-word;'>Value defined by this document</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>valuePartitionCapacity</td><td style='text-align: center; word-wrap: break-word;'>Specifies the total capacity of value partitions in a string table</td><td style='text-align: center; word-wrap: break-word;'>0</td></tr></table>

[V2G20-100] The EXI header (refer to W3C EXI 1.0, clause "Header") shall be used in a way that fulfils the ISO 15118 needs. That means, the optional EXI cookie ($EXI) shall never be used and the presence bit for EXI options shall be always set to 0 (=false). As a consequence the optional EXI options shall never be part of an EXI message defined by this document. Each EXI implementation (on EVCC or SECC side) shall discard messages that do not respect the EXI header options defined by this document.

[V2G20-2310] An element/attribute which is not defined in Annex A shall be encoded and decoded as schema deviation case according to W3C EXI 1.0.

[V2G20-600] The EXI coder for encoding and decoding of the ISO 15118 communication shall use the EXI profile settings (Reference [105]) according to Table 16.

NOTE For details describing the EXI profile refer to Reference [105].

<div style="text-align: center;">Table 16 — EXI profile settings</div>



<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>EXI profile parameter</td><td style='text-align: center; word-wrap: break-word;'>Description</td><td style='text-align: center; word-wrap: break-word;'>Value defined by this document</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>maximumNumberOfBuiltInElementGrammars</td><td style='text-align: center; word-wrap: break-word;'>This option is the maximum number of built-in element grammars for which dynamically productions other than AT (xsi:type) productions have been added.</td><td style='text-align: center; word-wrap: break-word;'>0</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>maximumNumberOfBuiltInProductions</td><td style='text-align: center; word-wrap: break-word;'>This option is the maximum number of top-level productions that can be dynamically inserted in built-in element grammars excluding AT (xsi:type) productions.</td><td style='text-align: center; word-wrap: break-word;'>0</td></tr></table>

[V2G20-2311] A simple type/value of an element/attribute which is not defined in Annex A shall be encoded and decoded type-aware.

#### 7.9.2 Message security

##### 7.9.2.1 Overview

XML signature is a W3C recommendation that addresses the authenticity requirements of some data fragments (e.g. metering information) of the XML-based V2G communications. XML signature defines a mechanism by which messages and message parts can be digitally signed to provide integrity, to ensure that the data is not tampered with and is authentic and to verify the identity of the message producer. For protecting confidentiality, a hybrid encryption scheme based on the Diffie-Hellman-Protocol is applied.

##### 7.9.2.2 Application layer credentials and cipher suites

Credentials to be applied on application layer shall be suitable for the targeted XML security. Here, XML signature is chosen to protect billing relevant information between EVCC, SECC and/or SA. Moreover,