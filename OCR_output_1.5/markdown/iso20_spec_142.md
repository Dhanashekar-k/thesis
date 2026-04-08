and common issues like hardware clock drift, this document needs to support use cases where the SECC and/or the EVCC do not have a buffered real time clock and the coordination of the entire energy transfer process should also work reliably when there is no internet connection or if the backend networks are temporarily unreachable.

The management of (scheduled) events with a time resolution shorter than 1 s is considered not in scope for ISO 15118 communication and they are typically handled by safety standards, power inverter hardware designs or similar solutions. However, for some purposes a very fine-grained time notation is necessary after all.

To address all those requirements this document is introducing the concept of "SECC time".

##### 8.3.3.3 The definition of SECC time

[V2G20-1529] Unless noted otherwise, all time stamps and time anchors (e.g. as used in schedules) are values that shall be interpreted in the context of SECC time.

NOTE 1 SECC time is modeled after UNIX time (also known as POSIX time or epoch time) to simplify its implementation and it therefore shares many, but not all characteristics. This means that if an SECC is based on a system that works with UNIX time and uses some common form of clock synchronization (e.g. via NTP), then the system's time can be used directly to fulfill all possible SECC time requirements. On the EVCC side implementation requirements are slightly different, as is outlined further below.

NOTE 2 SECC time is a system for describing a point in time, defined as the number of seconds that have elapsed since the beginning of the local SECC epoch minus the number of leap seconds that have taken place since then.

NOTE 3 Leap seconds are intentionally omitted in SECC time, just like in UNIX time, so every day has precisely 86 400 s. This makes calculations into the future predictable but has the consequence that SECC time, in the context of UTC, is neither a truly linear measure of time nor a true representation of UTC.

[V2G20-1531] If coordination with external secondary actors is necessary, than SECC time shall use an SECC epoch starting at 00:00:00 (hh:mm:ss) Coordinated Universal Time (UTC), Thursday, 1 January 1970.

NOTE 4 The coordination with external secondary actors implies that some form of backend communication is possible, meaning that the SECC has some technical capability to synchronize with UTC. This automatically places SECC time into the UTC time zone.

[V2G20-1532] For situations where UTC synchronization is not necessary or no internet connection is possible any other SECC epoch start time shall be allowed.

NOTE 5 Typically this is the point in time where the system was powered on.

NOTE 6 The charging systems, for example, designed as PV-battery buffered power islands or vehicle-to-vehicle charging solutions, with EIM access control can properly work in scheduled or dynamic control modes even without SECC time being in sync with UTC. Refer to 8.4.2 for description of scheduled and dynamic control modes.

[V2G20-1533] SECC time shall never be used as the reference time for the purpose of certificate expiration validation.

NOTE 7 The SECC and EVCC can perform certificate expiration validation with the help of time sources which they individually consider as trustworthy. From the EVCCs perspective SECC time cannot be guaranteed to meet any well-defined security criteria.

##### 8.3.3.4 TimeStamp within MessageHeaderType