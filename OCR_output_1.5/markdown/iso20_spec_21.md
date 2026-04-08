- "xxxx" represents the unique requirement number consisting of four digits starting from 1 000;

– "requirement text" defines the actual text of the requirement.

EXAMPLE [V2G20-1000] This is an example requirement introduced in this document.

The format below is applied to the handed over requirements from ISO 15118-2:

[V2G20-yyy] requirement text, where:

- "V2G20" represents this document;

- "yyy" represents the unique requirement number same as already defined in ISO 15118-2;

- "requirement text" is the same text as defined in first edition.

EXAMPLE [V2G20-000] This is an example requirement originally defined in ISO 15118-2.

### 5.3 Usage of references

[V2G20-1230] All published updates and error corrections (errata) shall be applied to the referred documents.

NOTE This does not include updated RFC or other requirement numbers not referenced in Clause 2 or Bibliography. This additionally does not include requirements published after publication of this document.

EXAMPLE If an errata to IETF RFC 8446 for TLS 1.3 is published 2 months after publication of this document and simply provides correction to an existing spec without which TLS 1.3 could not be implemented, that errata can be considered during implementation of this document. But if an IETF RFC is published 2 months after publication of this document and updates TLS 1.3 to TLS 1.4 due to some major issues in the protocol, this IETF RFC cannot be considered for implementation of this document as it can result in unforeseen issues.

### 5.4 Notation used for XML schema diagrams

This document makes use of XML as a description format for V2G messages. For details with regards to the XML schema diagram notation used in this document refer to Reference [96].

Allowing for an easy way to distinguish the types used for the XML schema definitions in this document, the following naming conventions apply:

- complex type use capitalized first letters,

– simple types use non capitalized first letters.

## 6 Document overview

Figure 2 describes the organization of the different documents in the ISO 15118 series and the usage of the subclauses, according to the OSI layered architecture.

As indicated by the bold framed shapes, this document defines requirements applicable to layers 3 – 7 according to the OSI layered architecture. Layer 1 and layer 2 requirements including the V2G standardized service primitive interface are specified in ISO 15118-3 and ISO 15118-8.

Copied with the permission of ANSI on behalf of ISO in connection with USDOT National Electric Vehicle Infrastructure (NEVI) Formula Program. Copying not permitted. ©ISO. All rights reserved.