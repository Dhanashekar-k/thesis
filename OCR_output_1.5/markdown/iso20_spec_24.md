a) whereas [initial of layer] is one out of the following seven:

- physical, data link, network, transport, session, presentation, application;

b) whereas [NAME] is the name of the primitive;

EXAMPLE Typical examples for [Name] are CONNECT, DISCONNECT, DATA; other names are used in this document and ISO 15118-3.

c) whereas [primitive type] is one out of the following four:

request, indication, response, confirmation;

d) whereas (parameter list) includes a list of parameters separated by comma the user of the service is supposed to provide when using the respective service primitive; optional parameters are marked with brackets "[..]".

NOTE In this document, the primitive type ".indication" always indicates an event asynchronously to the upper layer.

### 7.3 Security concept

#### 7.3.1 General

This subclauses provide specific and separate requirements for the private SECC and the SECC. Thus, unless otherwise specified, private SECC and SECC are not considered interchangeable.

In ISO 15118-2, transport layer security (TLS) was only required for PnC or VAS. In this document, TLS is always mandatory. For backward compatibility, connection setup processes will accept both ISO 15118-2 handling and the handling defined in this document. This means the connection setup processes will not change.

If an application still requires optional TLS, ISO 15118-2 shall be used. Refer to 7.7.3.10 for further details.

Figure 4 depicts the principal approach for various cases from a security point of view, showing the necessary security services applied as well as an abstract view on the different data flows necessary for the operation.

The data flow/sequence diagrams can be found in 8.6.6. In Figure 4, only the security relevant information is highlighted.

The security concept provides a basic transport based protection mechanism. For all scenarios described in this document, the usage of TLS for the transport communication between the EVCC and SECC is mandatory. In case data should be protected to or from a secondary actor or if the protection should last longer than the existence of the TLS channel, specific messages could be protected on application layer (XML-based signatures).

Figure 4 shows an example sequence for a PnC scenario. As described in Figure 4, all TCP/IP based communication is protected using a mutually authenticated TLS channel between the two peers.

Some of the information provided by the EVCC may need to be sent to the SA for further processing. The EVCC calculates a power profile (refer to 8.3.4.3.8.2) and sends it to the SECC. The SECC may send it to SA systems like energy management system or demand clearing house. Further process is similar to the semi-online case with the exception that the final charging data can be directly submitted to the SA. It is assumed that the SECC will also use a secure transport connection to the SA.