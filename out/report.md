# VistA corpus template & boilerplate induction

Analyzed **469** documents across **24** doc_types (min-docs threshold = 3).

`status`: **strong** = ≥5 required sections (clean template); **weak** = 1–4 required; **noisy** = sections found but none recurring enough to be required; **sparse** = too few docs to induce.

| doc_type | docs | sections | required | boilerplate | status |
|---|---:|---:|---:|---:|---|
| DIBR | 120 | 39 | 39 | 1122 | strong |
| IG | 108 | 0 | 0 | 430 | noisy |
| RN | 83 | 2 | 0 | 54 | noisy |
| TM | 42 | 5 | 0 | 768 | noisy |
| UM | 25 | 2 | 0 | 66 | noisy |
| UG | 14 | 18 | 0 | 4 | noisy |
| DG | 12 | 87 | 0 | 393 | noisy |
| API | 8 | 256 | 247 | 1538 | strong |
| CFG | 8 | 7 | 6 | 17 | strong |
| INT | 6 | 0 | 0 | 3 | noisy |
| POM | 5 | 33 | 33 | 156 | strong |
| AG | 4 | 37 | 37 | 57 | strong |
| QRG | 4 | 0 | 0 | 0 | noisy |
| SG | 4 | 0 | 0 | 0 | noisy |
| SG-SET | 4 | 0 | 0 | 269 | noisy |
| IG-IMP | 3 | 0 | 0 | 0 | noisy |
| PDD | 3 | 1 | 1 | 10 | weak |
| REF | 3 | 0 | 0 | 0 | noisy |
| SM | 3 | 0 | 0 | 0 | noisy |
| SUP | 3 | 0 | 0 | 0 | noisy |
| APX | 2 | 0 | 0 | 0 | sparse |
| DESC | 2 | 0 | 0 | 0 | sparse |
| FAQ | 2 | 0 | 0 | 0 | sparse |
| CVG | 1 | 0 | 0 | 0 | sparse |

## Notes for curators

- **Promote with confidence:** `DIBR` — corpus-wide standardized template (many docs, high coverage).
- **Small-cohort 'strong' (verify before promoting):** `API`, `CFG`, `POM`, `AG` — < 10 docs, so a near-duplicate handful can manufacture a 'template' that won't generalize.
- **Heterogeneous (sections found, none required):** `RN`, `TM`, `UM`, `UG`, `DG` — exact-anchor alignment is defeated by numbered/renamed headings; would need fuzzy heading alignment to induce a skeleton.
- Boilerplate blocks are exact/near-duplicate prose recurring across ≥ min-docs of a type, sorted by evidence; the top entries per type are the curation-worthy ones (the long tail is short fragments).

## DIBR — 120 docs (strong)

**Template** `DIBR:bffd790e` — 39 sections, 39 required

| level | section | required | evidence |
|---:|---|:--:|---:|
| 2 | Purpose | ✓ | 94/120 |
| 2 | Dependencies | ✓ | 88/120 |
| 2 | Constraints | ✓ | 89/120 |
| 2 | Timeline | ✓ | 85/120 |
| 2 | Site Readiness Assessment | ✓ | 86/120 |
| 3 | &nbsp;&nbsp;Deployment Topology (Targeted Architecture) | ✓ | 84/120 |
| 3 | &nbsp;&nbsp;Site Information (Locations, Deployment Recipients) | ✓ | 72/120 |
| 3 | &nbsp;&nbsp;Site Preparation | ✓ | 81/120 |
| 2 | Resources | ✓ | 84/120 |
| 3 | &nbsp;&nbsp;Facility Specifics | ✓ | 61/120 |
| 3 | &nbsp;&nbsp;Hardware | ✓ | 80/120 |
| 3 | &nbsp;&nbsp;Software | ✓ | 88/120 |
| 3 | &nbsp;&nbsp;Communications | ✓ | 84/120 |
| 2 | Pre-Installation and System Requirements | ✓ | 79/120 |
| 2 | Platform Installation and Preparation | ✓ | 94/120 |
| 2 | Download and Extract Files | ✓ | 84/120 |
| 2 | Database Creation | ✓ | 82/120 |
| 2 | Installation Scripts | ✓ | 90/120 |
| 2 | Cron Scripts | ✓ | 89/120 |
| 2 | Access Requirements and Skills Needed for the Installation | ✓ | 85/120 |
| 2 | Installation Procedure | ✓ | 74/120 |
| 2 | Installation Verification Procedure | ✓ | 77/120 |
| 2 | System Configuration | ✓ | 83/120 |
| 2 | Database Tuning | ✓ | 82/120 |
| 2 | Back-Out Strategy | ✓ | 86/120 |
| 2 | Back-Out Considerations | ✓ | 83/120 |
| 3 | &nbsp;&nbsp;Load Testing | ✓ | 88/120 |
| 3 | &nbsp;&nbsp;User Acceptance Testing | ✓ | 81/120 |
| 2 | Back-Out Criteria | ✓ | 86/120 |
| 2 | Back-Out Risks | ✓ | 88/120 |
| 2 | Authority for Back-Out | ✓ | 88/120 |
| 2 | Back-Out Procedure | ✓ | 81/120 |
| 2 | Rollback Considerations | ✓ | 86/120 |
| 2 | Back-Out Verification Procedure | ✓ | 80/120 |
| 2 | Rollback Criteria | ✓ | 87/120 |
| 2 | Rollback Risks | ✓ | 87/120 |
| 2 | Authority for Rollback | ✓ | 87/120 |
| 2 | Rollback Procedure | ✓ | 80/120 |
| 2 | Rollback Verification Procedure | ✓ | 71/120 |

**Boilerplate** — 1122 recurring blocks

- `57×` Department of Veterans Affairs
- `48×` Office of Information and Technology (OIT)
- `41×` **Revision History**
- `39×` Department of Veterans Affairs (VA)
- `30×` Office of Information and Technology (OI&T)
- `30×` The following table describes software specifications required at each site prior to deplo…
- `28×` Per the Veteran-focused Integrated Process (VIP) Guide, the Deployment, Installation, Back…
- `27×` The following table describes preparation required by the site prior to deployment.
- `27×` **Artifact Rationale**
- `24×` Back-out pertains to a return to the last known good operational state of the software and…
- `21×` 4.  Select the Install Package(s) option and choose the patch to install.
- `21×` **Table 1: Deployment, Installation, Back-out, and Rollback Roles and Responsibilities**
- `21×` 3.  You may also elect to use the following options:
- `21×` This document describes the Deployment, Installation, Back-out, and Rollback Guide for new…
- `20×` The following table lists facility-specific features required for deployment.
- _… and 1107 more_

## IG — 108 docs (noisy)

**Template** `IG:e3b0c442` — 0 sections, 0 required

_No consistent section structure induced (noisy)._

**Boilerplate** — 430 recurring blocks

- `59×` Department of Veterans Affairs
- `32×` Installing Routines:
- `32×` Updating KIDS files...
- `32×` Updating Routine file...
- `32×` Installing PACKAGE COMPONENTS:
- `31×` You can queue the install by enter a 'Q' at the device prompt.
- `31×` Enter a '^' to abort the install.
- `31×` Enter the Device you want to print the Install messages.
- `30×` It consisted of the following Install(s):
- `26×` I will OVERWRITE your data with mine.
- `24×` **INSTALLATION GUIDE**
- `23×` Installing Data Dictionaries:
- `22×` Unload a Distribution
- `22×` Restart Install of Package(s)
- `20×` 4 Compare Transport Global to Current System
- _… and 415 more_

## RN — 83 docs (noisy)

**Template** `RN:99af6ca2` — 2 sections, 0 required

| level | section | required | evidence |
|---:|---|:--:|---:|
| 2 | Purpose | · | 23/83 |
| 2 | Required Patches | · | 18/83 |

**Boilerplate** — 54 recurring blocks

- `53×` Department of Veterans Affairs
- `16×` The following documents apply to this release:
- `14×` **<span class="smallcaps">Release Notes</span>**
- `11×` ![](bef32da019e17b7948fcf61d05ff68558fa625ac25a40e8e8a8b7584f44959d6.jpeg)
- `9×` Office of Information and Technology (OI&T)
- `9×` Computerized Patient Record System Product Line
- `8×` The most recent entries in this list are linked to the location in the manual they describ…
- `7×` Product Development (PD)
- `7×` Office of Information and Technology (OIT)
- `7×` Office of Information & Technology (OI&T)
- `7×` Department of Veterans Affairs (VA)
- `7×` Office of Enterprise Development
- `5×` Office of Information and Technology
- `5×` Select one of the following:
- `5×` **Table of Contents**
- _… and 39 more_

## TM — 42 docs (noisy)

**Template** `TM:6a0e39ae` — 5 sections, 0 required

| level | section | required | evidence |
|---:|---|:--:|---:|
| 2 | Templates | · | 9/42 |
| 2 | XINDEX | · | 9/42 |
| 2 | File Security | · | 13/42 |
| 2 | Electronic Signatures | · | 10/42 |
| 2 | Security Keys | · | 12/42 |

**Boilerplate** — 768 recurring blocks

- `25×` Department of Veterans Affairs
- `11×` **Technical Manual**
- `8×` This manual uses several methods to highlight different aspects of the material:
- `8×` - Descriptive text is presented in a proportional font (as represented by this font).
- `7×` Office of Information and Technology (OI&T)
- `7×` This manual is written with the assumption that the reader is familiar with the following:
- `7×` - M programming language
- `7×` This software was developed at the Department of Veterans Affairs (VA) by employees of the…
- `7×` ------------------------------------------------------------------------------
- `6×` \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*…
- `6×` Select Systems Manager Menu Option: **programmer** Options
- `6×` -------------------------------------------------------------------------------
- `6×` Select Programmer Options Option: **routine Tools**
- `6×` The first line of each routine contains a brief description of the general function of the…
- `6×` XINDEX is invoked from programmer mode: D ^XINDEX.
- _… and 753 more_

## UM — 25 docs (noisy)

**Template** `UM:a9e559da` — 2 sections, 0 required

| level | section | required | evidence |
|---:|---|:--:|---:|
| 2 | Recommended Users | · | 5/25 |
| 2 | Related Manuals | · | 6/25 |

**Boilerplate** — 66 recurring blocks

- `13×` Department of Veterans Affairs
- `6×` Office of Information and Technology (OIT)
- `6×` This manual uses several methods to highlight different aspects of the material:
- `6×` - Descriptive text is presented in a proportional font (as represented by this font).
- `6×` **Table of Contents**
- `5×` - Patient and user names are formatted as follows:
- `5×` -------------------------------------------------------------------------------
- `5×` This manual is written with the assumption that the reader is familiar with the following:
- `5×` Enter RETURN to continue or '^' to exit:
- `5×` Select one of the following:
- `5×` - Conventions for displaying TEST data in this document are as follows:
- `5×` - M programming language
- `5×` VistA M Server-based software provides online help and commonly used system default prompt…
- `5×` Department of Veterans Affairs (VA)
- `4×` Documentation Conventions
- _… and 51 more_

## UG — 14 docs (noisy)

**Template** `UG:33315666` — 18 sections, 0 required

| level | section | required | evidence |
|---:|---|:--:|---:|
| 2 | Revision History | · | 3/14 |
| 2 | Purpose | · | 5/14 |
| 3 | &nbsp;&nbsp;Assumptions | · | 4/14 |
| 3 | &nbsp;&nbsp;Disclaimers | · | 3/14 |
| 3 | &nbsp;&nbsp;Coordination | · | 3/14 |
| 3 | &nbsp;&nbsp;Documentation Conventions | · | 3/14 |
| 3 | &nbsp;&nbsp;References and Resources | · | 4/14 |
| 2 | National Service Desk and Organizational Contacts | · | 3/14 |
| 2 | System Configuration | · | 4/14 |
| 2 | Data Flows | · | 4/14 |
| 2 | User Access Levels | · | 3/14 |
| 2 | Continuity of Operation | · | 3/14 |
| 2 | Logging On | · | 4/14 |
| 2 | System Menu | · | 4/14 |
| 2 | Changing User ID and Password | · | 3/14 |
| 2 | Exit System | · | 4/14 |
| 2 | Caveats and Exceptions | · | 3/14 |
| 2 | Special Instructions for Error Correction | · | 3/14 |

**Boilerplate** — 4 recurring blocks

- `5×` Department of Veterans Affairs
- `4×` Per the Veteran-focused Integrated Process (VIP) Guide, the User’s Guide is required to be…
- `3×` **How to use this manual**
- `3×` Select one of the following:

## DG — 12 docs (noisy)

**Template** `DG:38de0b54` — 87 sections, 0 required

| level | section | required | evidence |
|---:|---|:--:|---:|
| 2 | About this Guide | · | 3/12 |
| 2 | About J2EE Connectors | · | 3/12 |
| 2 | Public VistALink APIs Documentation | · | 3/12 |
| 2 | Sample Applications for J2EE Server | · | 3/12 |
| 2 | J2EE Development | · | 3/12 |
| 3 | &nbsp;&nbsp;IDE | · | 3/12 |
| 3 | &nbsp;&nbsp;J2EE Runtime | · | 3/12 |
| 2 | J2SE Development | · | 3/12 |
| 3 | &nbsp;&nbsp;IDE | · | 3/12 |
| 3 | &nbsp;&nbsp;J2SE Runtime | · | 3/12 |
| 3 | &nbsp;&nbsp;System Locator: Institution-Connector Mapping | · | 3/12 |
| 3 | &nbsp;&nbsp;Multidivision-Aware Application Code: ConnectionSpec Credentials | · | 3/12 |
| 3 | &nbsp;&nbsp;Example | · | 3/12 |
| 2 | Request Cycle | · | 3/12 |
| 3 | &nbsp;&nbsp;Retrieving the Connection Factory | · | 3/12 |
| 3 | &nbsp;&nbsp;Instantiating a Connection Spec for Re-authentication | · | 3/12 |
| 3 | &nbsp;&nbsp;Getting a Connection (Connection Spec) | · | 3/12 |
| 3 | &nbsp;&nbsp;Executing a Request | · | 3/12 |
| 3 | &nbsp;&nbsp;Closing the Connection | · | 3/12 |
| 3 | &nbsp;&nbsp;Connectivity Failures and Retry Strategies | · | 3/12 |
| 2 | More about Re-authentication | · | 3/12 |
| 3 | &nbsp;&nbsp;Overview | · | 5/12 |
| 3 | &nbsp;&nbsp;Connection Specification Classes | · | 3/12 |
| 3 | &nbsp;&nbsp;Institution/Division Rules for Re-authentication | · | 3/12 |
| 3 | &nbsp;&nbsp;Application Proxy User | · | 3/12 |
| 2 | Timeouts | · | 3/12 |
| 3 | &nbsp;&nbsp;Socket-Level Forced Timeout | · | 3/12 |
| 3 | &nbsp;&nbsp;Graceful (Request-Level) Timeout | · | 3/12 |
| 2 | Institution Mapping | · | 3/12 |
| 3 | &nbsp;&nbsp;How to Configure Mappings | · | 3/12 |
| 3 | &nbsp;&nbsp;How to View the Currently Loaded Mappings | · | 3/12 |
| 3 | &nbsp;&nbsp;Retrieving Mappings for Applications | · | 3/12 |
| 3 | &nbsp;&nbsp;Subdivisions | · | 3/12 |
| 2 | VistALink Java API Reference | · | 3/12 |
| 2 | Remote Procedure Calls | · | 3/12 |
| 3 | &nbsp;&nbsp;RPC Security (“B”-Type Option) | · | 3/12 |
| 3 | &nbsp;&nbsp;RPCs for Use by Application Proxy Users | · | 3/12 |
| 2 | Request Processing | · | 3/12 |
| 3 | &nbsp;&nbsp;Get an RpcRequest Object: RpcRequestFactory Class | · | 3/12 |
| 3 | &nbsp;&nbsp;Set RpcRequest Parameters: “Explicit” Style | · | 3/12 |
| 3 | &nbsp;&nbsp;Set RpcRequest Parameters: “setParams” Style | · | 3/12 |
| 3 | &nbsp;&nbsp;Specifying Indices for List-Type RPC Parameters | · | 3/12 |
| 3 | &nbsp;&nbsp;Other Useful RpcRequest Methods | · | 3/12 |
| 2 | Response Processing | · | 3/12 |
| 3 | &nbsp;&nbsp;RpcResponse Class | · | 3/12 |
| | _… and 42 more (low-evidence tail)_ | | |

**Boilerplate** — 393 recurring blocks

- `7×` - M programming language
- `6×` - Author’s comments are displayed in italics or as “callout” boxes.
- `6×` - Information Security Officers (ISOs)—Personnel at VA sites responsible for system securi…
- `6×` - Descriptive text is presented in a proportional font (as represented by this font).
- `6×` <img src="27daafb47980ab9024dc7a4473402b34b67543437b40b475e4369ba39619bb05.png" style="wid…
- `6×` - VistA computing environment:
- `6×` - References to “**\<Enter\>**” within these snapshots indicate that the user should press…
- `6×` VistA M Server-based software provides online help and commonly used system default prompt…
- `6×` Department of Veterans Affairs (VA)
- `6×` This software was developed at the Department of Veterans Affairs (VA) by employees of the…
- `5×` Documentation Conventions
- `5×` <img src="27daafb47980ab9024dc7a4473402b34b67543437b40b475e4369ba39619bb05.png" style="wid…
- `5×` Obtaining Data Dictionary Listings
- `5×` - Patient and user names are formatted as follows:
- `5×` How to Obtain Technical Information Online
- _… and 378 more_

## API — 8 docs (strong)

**Template** `API:00ff282f` — 256 sections, 247 required

| level | section | required | evidence |
|---:|---|:--:|---:|
| 2 | Intended Audience | ✓ | 4/8 |
| 2 | Document Conventions | ✓ | 4/8 |
| 2 | Acronyms and Definitions | ✓ | 4/8 |
| 3 | &nbsp;&nbsp;Acronyms | ✓ | 4/8 |
| 3 | &nbsp;&nbsp;Definitions | ✓ | 4/8 |
| 2 | User Interfaces | ✓ | 4/8 |
| 2 | Software Interfaces | ✓ | 4/8 |
| 2 | Hardware Interfaces | ✓ | 4/8 |
| 2 | PSN50612 API – NATIONAL DRUG TRANSLATION file (#50.612) | ✓ | 4/8 |
| 3 | &nbsp;&nbsp;Component: DATA | ✓ | 4/8 |
| 2 | PSN50625 API – WARNING LABEL – ENGLISH file (#50.625) | ✓ | 4/8 |
| 3 | &nbsp;&nbsp;Component: DATA | ✓ | 4/8 |
| 2 | PSN50626 API – WARNING LABEL – SPANISH file (#50.626) | ✓ | 4/8 |
| 3 | &nbsp;&nbsp;Component: DATA | ✓ | 4/8 |
| 2 | PSN50627 API – WARNING LABEL MAP file (#50.627) | ✓ | 4/8 |
| 3 | &nbsp;&nbsp;Component: DATA | ✓ | 4/8 |
| 2 | PSN5067 API – NDC/UPN file (#50.67) | ✓ | 4/8 |
| 3 | &nbsp;&nbsp;Component: ALL | ✓ | 4/8 |
| 2 | PSN50P41 API – DRUG INGREDIENTS file (#50.416) | ✓ | 4/8 |
| 3 | &nbsp;&nbsp;Component: APD | ✓ | 4/8 |
| 3 | &nbsp;&nbsp;Component: APS | ✓ | 4/8 |
| 3 | &nbsp;&nbsp;Component: B | ✓ | 4/8 |
| 3 | &nbsp;&nbsp;Component: ID | ✓ | 4/8 |
| 3 | &nbsp;&nbsp;Component: NAME | ✓ | 4/8 |
| 3 | &nbsp;&nbsp;Component: ZERO | ✓ | 4/8 |
| 2 | PSN50P6 API - VA GENERIC file (#50.6) | ✓ | 4/8 |
| 3 | &nbsp;&nbsp;Component: ROOT | ✓ | 4/8 |
| 3 | &nbsp;&nbsp;Component: ZERO | ✓ | 4/8 |
| 2 | PSN50P65 API - VA DRUG CLASS file (#50.605) | ✓ | 4/8 |
| 3 | &nbsp;&nbsp;Component: C | ✓ | 4/8 |
| 3 | &nbsp;&nbsp;Component: IEN | ✓ | 4/8 |
| 3 | &nbsp;&nbsp;Component: ROOT | ✓ | 4/8 |
| 2 | PSN50P67 API – DRUG UNITS file (#50.607) | ✓ | 4/8 |
| 3 | &nbsp;&nbsp;Component: ALL | ✓ | 4/8 |
| 2 | PSN50P68 API – VA PRODUCT file (#50.68) | ✓ | 4/8 |
| 3 | &nbsp;&nbsp;Component: DATA | ✓ | 4/8 |
| 3 | &nbsp;&nbsp;Component: FORM | ✓ | 4/8 |
| 2 | PSN56 API – DRUG INTERACTION file (#56) | ✓ | 4/8 |
| 3 | &nbsp;&nbsp;Component: ALL | ✓ | 4/8 |
| 3 | &nbsp;&nbsp;Component: IEN | ✓ | 4/8 |
| 2 | PSNAPIS API – API for NDF files | ✓ | 4/8 |
| 3 | &nbsp;&nbsp;Component: B | ✓ | 4/8 |
| 3 | &nbsp;&nbsp;Component: CIRN | ✓ | 4/8 |
| 3 | &nbsp;&nbsp;Component: CIRN2 | ✓ | 4/8 |
| 3 | &nbsp;&nbsp;Component: CLASS | ✓ | 4/8 |
| | _… and 211 more (low-evidence tail)_ | | |

**Boilerplate** — 1538 recurring blocks

- `4×` DRCT = Drug Cost of Refill
- `4×` CLN = Clinic; variable format A;B where:
- `4×` 0 = No, do not override the value in the EXCLUDE FROM DOSAGE CHECKS field (#11) of the DOS…
- `4×` ^TMP(\$J,LIST,PSSIEN,"QCODE",PSS(1),5) = ADMINISTRATION TIMES (52.61,5)
- `4×` ^TMP(\$J,LIST,DFN,IEN,"RF",n,8)=DIVISION (52.1,8) ^NAME (59,.01)
- `4×` ^TMP(\$J,LIST,PSSIEN,"AL",PSS(1),2) = INITIATOR OF ACTIVITY (50.0214,2)^ NAME(200,.01)
- `4×` VA PRODUCT IDENTIFIER = 5-character CMOP ID
- `4×` n = the IEN of entry in the Medication Instruction (SIG) multiple
- `4×` \#50.68 *See* VA PRODUCT file
- `4×` - Inpatient Pharmacy Automatic Replenishment/Ward Stock (AR/WS)
- `4×` 0 = not a valid VA Generic Name or Valid Trade name
- `4×` ^TMP(\$J,LIST,PSSIEN,24) = PACKAGE TYPE (50,24)^NAME (50.608,.01)
- `4×` ^TMP(\$J,LIST,PSSIEN,"SYN",PSS(1),404) = PRICE PER DISPENSE UNIT (50.1,404)
- `4×` PSSFT = NAME field (#.01) of the ADMINISTRATION SCHEDULE file (#51.1) (a value of "??" may…
- `4×` Returns the set of codes as defined by VA FileMan Data Retrieval call FIELD^DID to the arr…
- _… and 1523 more_

## CFG — 8 docs (strong)

**Template** `CFG:a314b964` — 7 sections, 6 required

| level | section | required | evidence |
|---:|---|:--:|---:|
| 2 | Overview | ✓ | 4/8 |
| 2 | Recommended Audience | ✓ | 5/8 |
| 2 | About this Guide | ✓ | 5/8 |
| 2 | Document Conventions | ✓ | 4/8 |
| 2 | Related Documents | ✓ | 4/8 |
| 2 | Pre-requisite Patches | ✓ | 4/8 |
| 2 | Install Reminder Content | · | 3/8 |

**Boilerplate** — 17 recurring blocks

- `6×` Department of Veterans Affairs
- `5×` Enterprise Program Management Office (EPMO)
- `5×` Office of Information & Technology (OI&T)
- `4×` Edit Parameter Values
- `4×` The following documents, in addition to this document, will be available on the VA Softwar…
- `4×` Examples of VistA “Roll and Scroll” interface actions will be shown in a box such as this:
- `4×` Select OPTION NAME: XPAR EDIT PARAMETER Edit Parameter Values
- `3×` Emphasis of important points may be displayed in this manner:
- `3×` Select OPTION: ENTER OR EDIT FILE ENTRIES
- `3×` This set up/configuration guide provides instructions for:
- `3×` - *CPRS Technical Manual: GUI Version*
- `3×` > **NOTE:** This is an important point and must not be omitted.
- `3×` The Computerized Patient Record System (CPRS) is a Veterans Health Information Systems and…
- `3×` -----------------------------------------------------------------------------
- `3×` ----------------------------------------------------------------------------
- _… and 2 more_

## INT — 6 docs (noisy)

**Template** `INT:e3b0c442` — 0 sections, 0 required

_No consistent section structure induced (noisy)._

**Boilerplate** — 3 recurring blocks

- `4×` Department of Veterans Affairs
- `3×` The MSA segment contains information sent while acknowledging another message.
- `3×` The MSH segment defines the intent, source, destination, and some specifics of the syntax…

## POM — 5 docs (strong)

**Template** `POM:33e031ff` — 33 sections, 33 required

| level | section | required | evidence |
|---:|---|:--:|---:|
| 2 | Administrative Procedures | ✓ | 4/5 |
| 3 | &nbsp;&nbsp;System Startup | ✓ | 3/5 |
| 3 | &nbsp;&nbsp;System Shutdown | ✓ | 3/5 |
| 3 | &nbsp;&nbsp;Backup and Restore | ✓ | 3/5 |
| 2 | Security/Identity Management | ✓ | 3/5 |
| 3 | &nbsp;&nbsp;Identity Management | ✓ | 4/5 |
| 3 | &nbsp;&nbsp;Access control | ✓ | 4/5 |
| 2 | User Notifications | ✓ | 4/5 |
| 3 | &nbsp;&nbsp;User Notification Points of Contact | ✓ | 3/5 |
| 2 | System Monitoring, Reporting and Tools | ✓ | 3/5 |
| 3 | &nbsp;&nbsp;Dataflow Diagram | ✓ | 3/5 |
| 3 | &nbsp;&nbsp;Availability Monitoring | ✓ | 4/5 |
| 3 | &nbsp;&nbsp;Performance/Capacity Monitoring | ✓ | 4/5 |
| 3 | &nbsp;&nbsp;Critical Metrics | ✓ | 4/5 |
| 2 | Routine Updates, Extracts and Purges | ✓ | 4/5 |
| 2 | Scheduled Maintenance | ✓ | 4/5 |
| 2 | Capacity Planning | ✓ | 4/5 |
| 3 | &nbsp;&nbsp;Initial Capacity Plan | ✓ | 3/5 |
| 2 | Routine Errors | ✓ | 4/5 |
| 3 | &nbsp;&nbsp;Security Errors | ✓ | 3/5 |
| 3 | &nbsp;&nbsp;Time-outs | ✓ | 4/5 |
| 3 | &nbsp;&nbsp;Concurrency | ✓ | 4/5 |
| 2 | Significant Errors | ✓ | 4/5 |
| 3 | &nbsp;&nbsp;Application Error Logs | ✓ | 4/5 |
| 3 | &nbsp;&nbsp;Application Error Codes and Descriptions | ✓ | 4/5 |
| 3 | &nbsp;&nbsp;Infrastructure Errors | ✓ | 4/5 |
| 2 | Dependent Systems | ✓ | 4/5 |
| 2 | Troubleshooting | ✓ | 3/5 |
| 2 | System Recovery | ✓ | 4/5 |
| 3 | &nbsp;&nbsp;Restart after Non-Scheduled System Interruption | ✓ | 4/5 |
| 3 | &nbsp;&nbsp;Restart after Database Restore | ✓ | 4/5 |
| 3 | &nbsp;&nbsp;Back-out Procedures | ✓ | 3/5 |
| 3 | &nbsp;&nbsp;Rollback Procedures | ✓ | 3/5 |

**Boilerplate** — 156 recurring blocks

- `3×` - WebLogic JMS queues response time
- `3×` 17. Contact Tier 3 support.
- `3×` You need to be in the CA APM Application Environment Tool in order to access Introscope an…
- `3×` The following is an example of a message in a log file:
- `3×` This section provides information regarding the logging capabilities of the system.
- `3×` The ES Physical view in Figure 7 represents the deployed environment and the relationship…
- `3×` In this example, the message attributes are: Timestamp, Severity, Subsystem, Message ID, a…
- `3×` 1.  Find the batch process’ execution in esr.log.
- `3×` - EE Supervisor/Report Manager – DQM/Report Viewer – SSN
- `3×` 1.  Verify a Z11 was transmitted from ES to the sites; Verify the Z11 contains the ZHP seg…
- `3×` This scenario assumes that a Veteran record was already identified.
- `3×` Signed: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_…
- `3×` **Scenario 5: eMIS Query Status in “Queried – Pending Response”**
- `3×` - Look for the batch process’ execution in the esr.log file.
- `3×` > If the message is not found in the database then either ES has not received it, or it is…
- _… and 141 more_

## AG — 4 docs (strong)

**Template** `AG:84a6ee21` — 37 sections, 37 required

| level | section | required | evidence |
|---:|---|:--:|---:|
| 2 | Intended Audience | ✓ | 4/4 |
| 2 | Terms of Use | ✓ | 3/4 |
| 2 | Document Conventions | ✓ | 3/4 |
| 2 | Related Information | ✓ | 3/4 |
| 2 | CVIX Major Functions | ✓ | 3/4 |
| 2 | CVIX Physical and Logical Description | ✓ | 3/4 |
| 2 | CVIX Operational Priority | ✓ | 3/4 |
| 2 | CVIX Dependencies | ✓ | 3/4 |
| 2 | The CVIX, VIXes, and Multidivisional VA Sites | ✓ | 3/4 |
| 2 | CVIX Connection Security | ✓ | 3/4 |
| 2 | CVIX Monitoring | ✓ | 3/4 |
| 2 | Using the CVIX Transaction Log | ✓ | 3/4 |
| 2 | Using the Cache Manager | ✓ | 3/4 |
| 2 | User Notifications | ✓ | 3/4 |
| 2 | Cluster-related Activities | ✓ | 3/4 |
| 2 | CVIX Planned Startup and Shutdown | ✓ | 3/4 |
| 2 | CVIX Data Retention and Purges | ✓ | 3/4 |
| 2 | CVIX and Backups | ✓ | 3/4 |
| 2 | CVIX and User Management | ✓ | 3/4 |
| 2 | VistA Site Service Overview | ✓ | 3/4 |
| 2 | Checking the Site Service | ✓ | 3/4 |
| 2 | Updating Site Service Data | ✓ | 3/4 |
| 2 | Remote Metadata Retrieval | ✓ | 3/4 |
| 2 | Remote Image Retrieval | ✓ | 3/4 |
| 2 | Caching of Metadata and Images | ✓ | 3/4 |
| 2 | Image Sharing and CVIX Timeouts | ✓ | 3/4 |
| 2 | VIX Log Collector Overview | ✓ | 3/4 |
| 2 | Log Collector Automatic Emails | ✓ | 3/4 |
| 2 | Archived Transaction Log Storage Area | ✓ | 3/4 |
| 2 | Excluding a VIX from Log Collection | ✓ | 3/4 |
| 2 | Routine Errors | ✓ | 3/4 |
| 2 | Significant Errors | ✓ | 3/4 |
| 2 | Unplanned Shutdowns | ✓ | 3/4 |
| 2 | CVIX Support | ✓ | 3/4 |
| 2 | CVIX Java Components | ✓ | 3/4 |
| 2 | VistA/M Information | ✓ | 3/4 |
| 2 | Other VIX Components | ✓ | 3/4 |

**Boilerplate** — 57 recurring blocks

- `3×` - For a site VIX, this is the STATION NUMBER (field (#99) of the INSTITUTION file (#4) of…
- `3×` 10. Click **Save as CSV** for comma-separated values or **Save as TSV** for tab-separated…
- `3×` Department of Veterans Affairs
- `3×` - For the CVIX, this value will be 2001.
- `3×` - Once a day, access the transaction log on each CVIX node to verify that the CVIX is runn…
- `3×` - Repository (VA site or DoD facility)
- `3×` - CVIX-to-VIX communications require a valid security certificate.
- `3×` 65. Open the Services window (click **Start \| All Programs \| Administrative Tools \| Ser…
- `3×` If the connection information in the site service needs to be changed, do the following.
- `3×` - If the image originates from the DoD, the CVIX does not perform any compression before s…
- `3×` 4.  To view different parts of the log, use the paging buttons near the top and at the bot…
- `3×` 3.  The CVIX Transaction Log page will display.
- `3×` - Host the VIX log collector.
- `3×` - Study (group) identifier
- `3×` 4.  The CVIX caches the image in its local cache. If the CVIX compressed the image, the co…
- _… and 42 more_

## QRG — 4 docs (noisy)

**Template** `QRG:e3b0c442` — 0 sections, 0 required

_No consistent section structure induced (noisy)._

**Boilerplate** — 0 recurring blocks

_No recurring verbatim blocks above threshold._

## SG — 4 docs (noisy)

**Template** `SG:e3b0c442` — 0 sections, 0 required

_No consistent section structure induced (noisy)._

**Boilerplate** — 0 recurring blocks

_No recurring verbatim blocks above threshold._

## SG-SET — 4 docs (noisy)

**Template** `SG-SET:e3b0c442` — 0 sections, 0 required

_No consistent section structure induced (noisy)._

**Boilerplate** — 269 recurring blocks

- `3×` The NUMI website basic and advanced settings are shown in Figure 23: NUMI Exchange Basic S…
- `3×` e.g., InstallUtil.exe /i D:\NUMI\\install_dir\>\bin\NumiWebApp.dll
- `3×` The NUMI application pool setup is shown in Figure 39: Application Pool Window.
- `3×` **NOTE**: With this command, we are changing the key password to “reallysecret” for this e…
- `3×` 5.  Install / restore the database components according to the instructions in section 4.1…
- `3×` Restoring the Appropriate Databases for the NUMI Application applies to the database serve…
- `3×` The NUMI Exchange web site authentication settings are shown in Figure 26: NUMI Exchange A…
- `3×` The average amount of time required to complete the NUMI installation is 2 days.
- `3×` 49. Now follow the steps below to update CERMe to CERMe 21.0.1.
- `3×` Add the content below to the end of the \< Config \> element
- `3×` \<Call name="addRule"\>
- `3×` **\<IntegratedLogin Enabled="true" CookieName="unifiedkey" UnifiedKey="8rzVNfLwjHWHvPctaen…
- `3×` To make any future changes to the src\\main\\resources\\xml\\deployment\\NumiWebApp.config…
- `3×` 4.  Optional – Reuse this file if another web server requires this STS endpoint’s certific…
- `3×` AuthenticationFailUrl="/iqm/html/rm_integrated_authentication_failed.htm" GuidUserCid="IQ_…
- _… and 254 more_

## IG-IMP — 3 docs (noisy)

**Template** `IG-IMP:e3b0c442` — 0 sections, 0 required

_No consistent section structure induced (noisy)._

**Boilerplate** — 0 recurring blocks

_No recurring verbatim blocks above threshold._

## PDD — 3 docs (weak)

**Template** `PDD:d3db5338` — 1 sections, 1 required

| level | section | required | evidence |
|---:|---|:--:|---:|
| 2 | Introduction | ✓ | 3/3 |

**Boilerplate** — 10 recurring blocks

- `3×` This manual is written with the assumption that the reader is familiar with the following:
- `3×` **Assumptions About the Reader**
- `3×` **How to Use this Manual**
- `3×` This manual uses several methods to highlight different aspects of the material:
- `3×` - Descriptive text is presented in a proportional font (as represented by this font).
- `3×` - Conventions for displaying TEST data in this document are as follows:
- `3×` **Reference Materials**
- `3×` - The first three digits (prefix) of any Social Security Numbers (SSN) will begin with eit…
- `3×` - M programming language
- `3×` - Various symbols are used throughout the documentation to alert the reader to special inf…

## REF — 3 docs (noisy)

**Template** `REF:e3b0c442` — 0 sections, 0 required

_No consistent section structure induced (noisy)._

**Boilerplate** — 0 recurring blocks

_No recurring verbatim blocks above threshold._

## SM — 3 docs (noisy)

**Template** `SM:e3b0c442` — 0 sections, 0 required

_No consistent section structure induced (noisy)._

**Boilerplate** — 0 recurring blocks

_No recurring verbatim blocks above threshold._

## SUP — 3 docs (noisy)

**Template** `SUP:e3b0c442` — 0 sections, 0 required

_No consistent section structure induced (noisy)._

**Boilerplate** — 0 recurring blocks

_No recurring verbatim blocks above threshold._

## APX — 2 docs (sparse)

_Too sparse (2 < 3) to induce a reliable template or boilerplate set._

## DESC — 2 docs (sparse)

_Too sparse (2 < 3) to induce a reliable template or boilerplate set._

## FAQ — 2 docs (sparse)

_Too sparse (2 < 3) to induce a reliable template or boilerplate set._

## CVG — 1 docs (sparse)

_Too sparse (1 < 3) to induce a reliable template or boilerplate set._

