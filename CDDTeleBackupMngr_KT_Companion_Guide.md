# Knowledge Transfer (KT) Companion Guide: CDDTeleBackupMngr
**Component Name:** `CDDTeleBackupMngr` (Complex Device Driver Telematics Backup Manager)  
**System Architecture:** Cummins AUTOSAR (CSAR) Basic Software (BSW)  
**Requirement Specification (Integrity ID):** `9167284`  
**Software Design Specification (SDD):** `CSAR_SDD_CddTeleBackupMngr`  
**Target Hardware / ECUs:** Cummins CM3550 & CM3580 (Infineon AURIX TC3xx TriCore Microcontroller)  
**Deliverable PPT Presentation:** `CDDTeleBackupMngr_KT_Presentation.pptx` (22 Slides)

---

## 1. Executive Summary & Purpose

The `CDDTeleBackupMngr` component is a dedicated Basic Software (BSW) Complex Device Driver designed under the Cummins AUTOSAR (CSAR) architecture to manage the secure, autonomous backup of internal Program Flash (PF) calibration data into external Serial Flash (SF) memory.

### Why is this Component Needed?
During **Telematics Remote Calibration Download (CSU)**, new engine and vehicle calibrations are flashed Over-The-Air (OTA) into ECM internal Program Flash. In the event of a system disruption, software instability, or communication failure during field deployment, the ECM requires a guaranteed, verified, and secure copy of the previously running calibration to execute an autonomous rollback.

### Key Functional Responsibilities:
1. **Autonomous Operation:** Encapsulates the entire backup process within a non-blocking, state-machine-driven architecture without impacting real-time engine control loops.
2. **Cryptographic Protection:** Ensures **confidentiality** via AES-128-CBC encryption and **authenticity/integrity** via Cipher-based Message Authentication Code (CMAC) using the AUTOSAR Crypto Service Manager (CSM).
3. **Hardware Read-Back Verification:** Performs an immediate byte-by-byte comparison of every 256-byte page written to external Serial Flash against the encrypted buffer before proceeding.
4. **Resilient Retry Loop:** Automatically executes up to 3 complete retries (including chip full erase) if any flash or crypto operation fails.
5. **Cybersecurity Event Logging:** Upon exhaustion of retries, logs a formal Cybersecurity Event (`ppLogCSEvent_LogEvent` with reason codes `{13, 67}`) complying with UNECE R155 and ISO/SAE 21434.
6. **Non-Volatile Persistence:** Tracks status across ignition cycles via the AUTOSAR Non-Volatile Memory (NvM) manager.

---

## 2. Hardware Topology & Memory Partitioning

| Parameter | Specification | Details |
| :--- | :--- | :--- |
| **Microcontroller** | Infineon AURIX TC3xx (TriCore) | Hosts primary code execution and on-chip Program Flash (PF). |
| **External Memory** | 512 Mbit (64 MB) SPI NOR Flash | Cypress S25FL512S or Micron 25QL512. |
| **Serial Flash Buffer Region** | Base Address: `0x0200_0000` (32 MB) | Staging area for incoming calibration downloads over telematics. |
| **Serial Flash Backup Region** | Base Address: `0x0300_0000` (48 MB) | Dedicated vault managed by `CDDTeleBackupMngr`. |
| **Transfer Granularity** | `SF_PAGE_SIZE` = 256 Bytes | Page-aligned read, write, and verify operations. |
| **Cipher IV Length** | `Cipher_IV_LENGTH` = 16 Bytes | Session-unique random initialization vector for AES-128-CBC. |
| **CMAC Generation Length** | `CMAC_GEN_LENGTH` = 16 Bytes | 128-bit MAC tag generated for each block and the metadata trailer. |

---

## 3. AUTOSAR Interfaces & RTE Ports

### Explicit Sender / Receiver Ports
* **`nvrBackupStatus_nvdVal` / `nvwBackupStatus_nvdVal`** (uint8):
  * `0`: Uninitialized
  * `1` (`BACKUP_IN_PROGRESS`): Scheduler active
  * `2` (`BACKUP_COMPLT_VALID`): Successful completion and verification
  * `3` (`BACKUP_FAILED`): Permanent failure after 3 retries
  * `4` (`CSU_FEATURE_DISABLE`): Feature disabled via trim
* **`nvrRollBackTimerStatus_nvdVal` / `nvwRollBackTimerStatus_nvdVal`** (uint8/32):
  * Indicates whether the 5-second rollback countdown monitor is running.
* **`nvrTeleRollBackTimeOut_nvdVal` / `nvwTeleRollBackTimeOut_nvdVal`** (uint32):
  * Tracks elapsed seconds since portover completion.
* **`nvrPortOverstatus_nvdVal` / `nvwPortOverstatus_nvdVal`** (uint8):
  * Signals portover state (`PORTOVER_COMPLETE` vs `PORTOVER_DEFAULT`).
* **`ppCSUFeatureEnbl_deVal`** (boolean):
  * Master enable trim calibration (CR#18134205).
* **`ppToolConnectedProg_deVal`** (boolean):
  * Flag indicating a new calibration download event (`0x01`).

### Client / Server Ports & BSW Services
* **`ppLogCSEvent_LogEvent`**:
  * Called on permanent failure: `Rte_Call_ppLogCSEvent_LogEvent(UPDATE_FAILURE, &Update_Failure_ReasonCode[0], 0xFFu, 0xFFu)` where `Update_Failure_ReasonCode = {13, 67}`.
* **`NvM_WriteBlock` / `NvM_GetErrorStatus`**:
  * Persistent storage targeting descriptor `NvMConf_NvMBlockDescriptor_NvbswcBootSharedBootSharedFBLGeneral`.
* **`Csm_RandomGenerate`, `Csm_KeyElementSet`, `Csm_KeySetValid`, `Csm_Encrypt`, `Csm_MacGenerate`**:
  * Standardized AUTOSAR 4.x Crypto Service Manager interfaces.
* **`SerialFlashGetServ` / `GetSerialFlashState`**:
  * Memory access driver interfaces for Serial Flash commands (`SF_FULL_ERASE`, `SF_DATA_TRANSFER`, `SF_READ_DATA`).

---

## 4. Software Entity Architecture

The component consists of **3 Runnables** and **1 Static Internal Function**:

```
+-----------------------------------------------------------------------------------+
|                                 CDDTeleBackupMngr                                 |
+-----------------------------------------+-----------------------------------------+
| reInitCDDTeleBackupMngr()               | Executed once at boot after RTE start   |
| reTeleRollBackTimeCheck()               | Executed periodically every 5000 ms     |
| reCddTeleBackupSchdlr()                 | Executed periodically every 10 ms       |
| metadata_extract()                      | Internal synchronous helper function    |
+-----------------------------------------+-----------------------------------------+
```

---

## 5. Master State Machine Pipeline (`reCddTeleBackupSchdlr`)

### Tier 1: Primary Data State Machine (`backup_flag`)
1. **`NO_REQUEST` (Line 292):** Idle state. Awaits `BACKUP_IN_PROGRESS`.
2. **`BACKUP_FULL_ERASE` (Line 299):** Issues `SF_FULL_ERASE` on `BACKUP_REGION`. Calls `metadata_extract()`. Sets initial Program Flash address.
3. **`PF_ADDR_HANDLE` (Line 342):** Computes segment/block boundaries. If at segment start, generates a 16-byte random IV via `Csm_RandomGenerate()`. Copies 256 bytes from Program Flash into `Mem_Read_Buff`.
4. **`SET_KEYS` (Line 416):** Loads key material and IV into CSM via `Csm_KeyElementSet()` and validates keys with `Csm_KeySetValid()`.
5. **`ENCRYPT_START` (Line 482):** Initializes AES-128-CBC encryption (`CRYPTO_OPERATIONMODE_START`).
6. **`CMAC_START` (Line 521):** Initializes CMAC calculation (`CRYPTO_OPERATIONMODE_START`).
7. **`SEG_START_HANDLE` (Line 549):** Formats 8-byte Big-Endian segment header `[source_start_address_pf (4B) | uncompress_size (4B)]` and hashes it into CMAC via `Csm_MacGenerate(UPDATE)`.
8. **`CYBER_UPDATE` (Line 581):** Encrypts 256-byte chunk into `backup_encrypt_data` and hashes plaintext into CMAC via `Csm_MacGenerate(UPDATE)`.
9. **`ENCRYPT_FINISH` (Line 631):** Finalizes AES stream on segment end (`CRYPTO_OPERATIONMODE_FINISH`).
10. **`WRITE_TO_SF` (Line 697):** Dispatches `SF_DATA_TRANSFER` (page write) of 256 encrypted bytes to Serial Flash at `PF2SF_translate_addr`.
11. **`BACKUP_READ_SF_DATA` (Line 740):** **Hardware Read-Back Verification:** Dispatches `SF_READ_DATA`. Compares read-back data byte-by-byte with `backup_encrypt_data`. If mismatch -> `BACKUP_RETRY`. If match -> advances address. If block finished -> `CMAC_FINISH`.
12. **`CMAC_FINISH` (Line 676):** Calls `Csm_MacGenerate(FINISH)` to yield 16-byte block MAC.
13. **`CMAC_WRITE` (Line 826):** Writes 16-byte block CMAC to `block_cmac_addr_reference`. If more blocks remain -> loops back to `PF_ADDR_HANDLE`. If last block finished -> triggers Metadata Pipeline!
14. **`BACKUP_RETRY` (Line 881):** Increments `backup_attempts`. If $\le 3$ -> loops to `BACKUP_FULL_ERASE`. If $> 3$ -> sets `BACKUP_FAILED`, logs `ppLogCSEvent_LogEvent`, and sets `NvM_backup_update = TRUE`.
15. **`BACKUP_COMPLETE` (Line 905):** Sets `NVM_Back_up_status = BACKUP_COMPLT_VALID`, resets `nvrPortOverstatus` to default, and sets `NvM_backup_update = TRUE`.

### Tier 2: Metadata Sub-State Machine (`backup_metadata_flag`)
1. **`METADATA_NO_REQUEST` (Line 942):** Idle state.
2. **`METADATA_CMAC_START` (Line 1082):** Initializes CSM MAC generation for the metadata structure.
3. **`METADATA_ARRAY_HANDLING` (Line 947):** Populates `backup_matadata_array` with fixed header (0x17 B), block headers, and segment descriptors.
4. **`METADATA_CMAC_UPDATE` (Line 1126):** Hashes metadata array bytes into the CMAC generator.
5. **`METADATA_CMAC_FINISH` (Line 1225):** Finalizes 16-byte metadata CMAC and appends it to the trailer.
6. **`METADATA_WRITE` (Line 1160):** Writes complete metadata header and CMAC to `SF_BACKUP_CSU_METADATA_STRUCTURE_START`. On completion, triggers `backup_flag = BACKUP_COMPLETE`.

---

## 6. Slide-by-Slide Presentation Structure

| Slide | Title | Focus Area | Embedded Visual Asset |
| :---: | :--- | :--- | :--- |
| **01** | **CDDTeleBackupMngr Knowledge Transfer** | Title, Scope, Document References | Styled Widescreen Header Banner |
| **02** | **Executive Summary: Why CDDTeleBackupMngr?** | Business Context, Problem Statement, Value | 3 Strategic Comparison Cards |
| **03** | **CSAR System Architecture & Boundary Model** | Layered AUTOSAR Model & Interfaces | `diag_csar_architecture.png` |
| **04** | **Hardware Topology & Memory Partitioning** | Internal PF vs External 64MB SPI NOR Flash | `diag_data_layout.png` |
| **05** | **Software Component Boundary & RTE Interfaces** | S/R Ports, C/S Ports, NvM Descriptors | Matrix Table & Callout Cards |
| **06** | **Core Runnables & Execution Lifecycle** | 3 Runnables + 1 Helper, Rates, Roles | 4-Card Modular Layout |
| **07** | **Startup & Initialization Flow** | `reInitCDDTeleBackupMngr()` Logic | `diag_init_flowchart.png` |
| **08** | **Rollback Timer Management** | `reTeleRollBackTimeCheck()` 5s Cadence | `diag_rollback_flowchart.png` |
| **09** | **CSU Metadata & ODX-F Data Structures** | `telematics_csu_table` & Math | ODX-F Model & Formula Card |
| **10** | **Master Backup State Machine Architecture** | 2-Tier Architecture: 15 Data + 6 Meta | `diag_state_machine.png` |
| **11** | **Phase 1: Erase, Addressing & Key Loading** | `NO_REQUEST` to `SET_KEYS` | 4 Sequential State Cards |
| **12** | **Phase 2: Cryptographic Pipeline (AES & CMAC)**| Random IV, Big-Endian Seg CMAC | `diag_crypto_pipeline.png` |
| **13** | **Phase 3: Page Processing & Verification** | Chunk Encrypt, Flash Write, Read Verify | 4 Sequential State Cards |
| **14** | **Phase 4: Block CMAC Generation & Multi-Block**| Finalizing Block MAC & Offset Math | 2 Structured Detail Cards |
| **15** | **Phase 5: CSU Metadata Sub-State Machine** | Assembling, Signing & Writing Metadata | SDD Flowchart & State Breakdown |
| **16** | **Phase 6: Backup Completion & NVRAM Persistence**| `BACKUP_COMPLT_VALID` & Deferred NvM | Success Workflow & NvM Sync Cards |
| **17** | **Runtime Sequence Diagram** | Chronological Swimlanes across Modules | `diag_sequence.png` |
| **18** | **Fault Tolerance & Cybersecurity Event Logging**| 3-Attempt Retry Loop & Event Reason {13,67}| Warning Card & Regulatory Card |
| **19** | **Debug Instrumentation & Diagnostics Support** | `tele_dbg_backup_t` & Error Codes (0x01-0x1D)| Debug Struct & Error Code Matrix |
| **20** | **Requirements Traceability Matrix** | Integrity IDs 13584655 - 18134113 | Formal RTM Table |
| **21** | **Presenter's Code Walkthrough Guide** | Line-by-Line Navigation Guide for `code.txt`| 2 Navigation Index Cards |
| **22** | **Summary & Open Q&A Session** | Key Takeaways & Discussion Topics | Summary Card & Q&A Callout |

---

## 7. Line-by-Line Code Reference Guide for `code.txt`

When presenting the code line-by-line, use this guide to navigate:

* **Lines 1 - 35:** Header includes (`Rte_CDDTeleBackupMngr.h`, `Csm.h`, `NvM.h`, `telematics_csu_table.h`).
* **Lines 36 - 65:** Static memory buffers and crypto globals:
  * `Mem_Read_Buff[256]`: Plaintext buffer from Program Flash.
  * `backup_encrypt_data[256]`: Encrypted ciphertext buffer for Serial Flash.
  * `CMAC_array[16]`: Holds 128-bit block MAC.
  * `Backup_Cipher_IV[16]`: Holds random IV generated per session.
* **Lines 66 - 137:** Cybersecurity reason codes `{13, 67}` and NvM update flags.
* **Lines 138 - 248 (`reInitCDDTeleBackupMngr`):**
  * Lines 145-146: Sets default start addresses.
  * Lines 147-151: Reads NVM and port inputs.
  * Lines 152-167: Evaluates `PORTOVER_COMPLETE` to arm timer vs `new_cal_download` to start backup immediately.
  * Lines 170-176: Issues `NvM_WriteBlock` and handles failure flag.
* **Lines 249 - 938 (`reCddTeleBackupSchdlr` - Data Pipeline):**
  * Line 283: Feature enable gate (`NVM_Back_up_status != BACKUP_IN_PROGRESS || CSU_feature_enable == FALSE`).
  * Line 299: `case BACKUP_FULL_ERASE` - Erase command & calls `metadata_extract()`.
  * Line 342: `case PF_ADDR_HANDLE` - Calculates block/segment addresses, generates IV, reads Program Flash.
  * Line 416: `case SET_KEYS` - Loads IV and validates keys in CSM.
  * Line 482: `case ENCRYPT_START` - Initializes AES-128.
  * Line 521: `case CMAC_START` - Initializes CMAC generator.
  * Line 549: `case SEG_START_HANDLE` - Packs Big-Endian segment descriptor `seg_info[8]` and updates CMAC.
  * Line 581: `case CYBER_UPDATE` - Encrypts 256B chunk, updates CMAC.
  * Line 631: `case ENCRYPT_FINISH` - Finalizes AES encryption.
  * Line 697: `case WRITE_TO_SF` - Dispatches page write to Serial Flash.
  * Line 740: `case BACKUP_READ_SF_DATA` - Hardware read back & byte-by-byte comparison (`Mem_Read_Buff` vs `backup_encrypt_data`).
  * Line 826: `case CMAC_WRITE` - Writes 16-byte block CMAC to pre-calculated address.
  * Line 881: `case BACKUP_RETRY` - 3-attempt loop and cybersecurity audit event logging.
  * Line 905: `case BACKUP_COMPLETE` - Sets `BACKUP_COMPLT_VALID` and default portover status.
* **Lines 939 - 1250 (`reCddTeleBackupSchdlr` - Metadata Pipeline):**
  * Line 947: `case METADATA_ARRAY_HANDLING` - Packs CSU header structure.
  * Line 1082: `case METADATA_CMAC_START` - Starts metadata CMAC.
  * Line 1126: `case METADATA_CMAC_UPDATE` - Updates metadata CMAC.
  * Line 1160: `case METADATA_WRITE` - Writes metadata and CMAC to flash.
  * Line 1225: `case METADATA_CMAC_FINISH` - Finalizes metadata CMAC.
* **Lines 1251 - 1325:** Deferred NvM update check (`if (NvM_backup_update == TRUE)`).
* **Lines 1326 - 1376 (`reTeleRollBackTimeCheck`):**
  * Line 1335: Checks `Rollback_timer_status == TRUE`.
  * Line 1338: Compares against `Rte_CData_caTeleRollBackTimer()`.
  * Line 1342: Expiration sets `NVM_Back_up_status = BACKUP_IN_PROGRESS`.
  * Line 1349: Running timer increments by 5 seconds.
* **Lines 1377 - 1437 (`metadata_extract`):**
  * Traverses `telematics_csu_table`, calculates total metadata length, padding, and computes `block_cmac_addr_reference`.
