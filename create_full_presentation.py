import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor

# Color Palette Definitions
C_NAVY_DARK    = RGBColor(11, 37, 69)      # #0B2545 Primary Dark
C_NAVY_MED     = RGBColor(19, 64, 116)     # #134074 Secondary Header
C_TEAL         = RGBColor(0, 168, 150)     # #00A896 Brand Accent
C_TEAL_LIGHT   = RGBColor(230, 255, 250)   # #E6FFFA Card Accent
C_BLUE_ACCENT  = RGBColor(37, 99, 235)     # #2563EB Link/Info Blue
C_BLUE_LIGHT   = RGBColor(239, 246, 255)   # #EFF6FF
C_RED_ACCENT   = RGBColor(220, 38, 38)     # #DC2626 Warning / Error
C_RED_LIGHT    = RGBColor(254, 226, 226)   # #FEE2E2 Warning Card
C_AMBER        = RGBColor(217, 119, 6)     # #D97706 Caution / Timer
C_AMBER_LIGHT  = RGBColor(254, 243, 199)   # #FEF3C7
C_GREEN        = RGBColor(22, 163, 74)     # #16A34A Success
C_GREEN_LIGHT  = RGBColor(220, 252, 231)   # #DCFCE7 Success Card
C_PURPLE       = RGBColor(124, 58, 237)    # #7C3AED Crypto / Logic
C_PURPLE_LIGHT = RGBColor(237, 233, 254)   # #EDE9FE Crypto Card
C_TEXT_DARK    = RGBColor(30, 41, 59)      # #1E293B Text Dark
C_TEXT_MUTED   = RGBColor(100, 116, 139)   # #64748B Secondary Text
C_BG_CARD      = RGBColor(248, 250, 252)   # #F8FAFC Card Fill
C_BORDER_CARD  = RGBColor(226, 232, 240)   # #E2E8F0 Card Border
C_WHITE        = RGBColor(255, 255, 255)   # #FFFFFF Clean White

def init_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    return prs

def add_header(slide, title, category, subtitle=""):
    # Category Tag / Pill
    cat_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.38), Inches(2.6), Inches(0.28))
    cat_box.fill.solid()
    cat_box.fill.fore_color.rgb = C_NAVY_DARK
    cat_box.line.color.rgb = C_TEAL
    cat_box.line.width = Pt(1)
    tf_c = cat_box.text_frame
    tf_c.word_wrap = False
    p_c = tf_c.paragraphs[0]
    p_c.text = category.upper()
    p_c.font.size = Pt(8.5)
    p_c.font.bold = True
    p_c.font.color.rgb = C_WHITE
    p_c.alignment = PP_ALIGN.CENTER

    # Title Box
    t_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.70), Inches(11.733), Inches(0.68))
    tf_t = t_box.text_frame
    tf_t.word_wrap = True
    p_t = tf_t.paragraphs[0]
    p_t.text = title
    p_t.font.size = Pt(19)
    p_t.font.bold = True
    p_t.font.color.rgb = C_NAVY_DARK

    if subtitle:
        p_sub = tf_t.add_paragraph()
        p_sub.text = subtitle
        p_sub.font.size = Pt(10.5)
        p_sub.font.color.rgb = C_TEXT_MUTED
        p_sub.space_before = Pt(2)

    # Divider Line
    rule = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.44), Inches(11.733), Inches(0.015))
    rule.fill.solid()
    rule.fill.fore_color.rgb = C_BORDER_CARD
    rule.line.fill.background()

def add_footer(slide, current_page, total_pages=22):
    rule = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(7.05), Inches(11.733), Inches(0.015))
    rule.fill.solid()
    rule.fill.fore_color.rgb = C_BORDER_CARD
    rule.line.fill.background()

    f_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.08), Inches(8.5), Inches(0.3))
    tf = f_box.text_frame
    p = tf.paragraphs[0]
    p.text = "CDDTeleBackupMngr Knowledge Transfer  |  Cummins CSAR Architecture  |  Req ID: 9167284"
    p.font.size = Pt(8.5)
    p.font.color.rgb = C_TEXT_MUTED

    p_box = slide.shapes.add_textbox(Inches(10.5), Inches(7.08), Inches(2.0), Inches(0.3))
    tf_p = p_box.text_frame
    p_pg = tf_p.paragraphs[0]
    p_pg.text = f"Slide {current_page} of {total_pages}"
    p_pg.alignment = PP_ALIGN.RIGHT
    p_pg.font.size = Pt(8.5)
    p_pg.font.bold = True
    p_pg.font.color.rgb = C_NAVY_MED

def create_card(slide, left, top, width, height, bg_color=C_BG_CARD, border_color=C_BORDER_CARD, border_width=1.0):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    card.line.color.rgb = border_color
    card.line.width = Pt(border_width)
    return card

def add_bullet_list(text_frame, items, font_size=9.5, space_after=4, bullet_char="•"):
    for idx, item in enumerate(items):
        if idx == 0 and len(text_frame.paragraphs[0].text) == 0:
            p = text_frame.paragraphs[0]
        else:
            p = text_frame.add_paragraph()
        p.space_after = Pt(space_after)
        if isinstance(item, tuple):
            if len(item) == 2:
                title, desc = item
                run_b = p.add_run()
                run_b.text = f"{bullet_char} {title}: "
                run_b.font.bold = True
                run_b.font.size = Pt(font_size)
                run_b.font.color.rgb = C_TEXT_DARK
                run_d = p.add_run()
                run_d.text = desc
                run_d.font.size = Pt(font_size)
                run_d.font.color.rgb = C_TEXT_DARK
            elif len(item) == 3:
                title, desc, detail = item
                run_b = p.add_run()
                run_b.text = f"{bullet_char} {title} — "
                run_b.font.bold = True
                run_b.font.size = Pt(font_size)
                run_b.font.color.rgb = C_NAVY_MED
                run_d = p.add_run()
                run_d.text = f"{desc}  "
                run_d.font.size = Pt(font_size)
                run_d.font.color.rgb = C_TEXT_DARK
                run_t = p.add_run()
                run_t.text = f"[{detail}]"
                run_t.font.bold = True
                run_t.font.size = Pt(font_size)
                run_t.font.color.rgb = C_TEAL
        else:
            run = p.add_run()
            run.text = f"{bullet_char} {item}"
            run.font.size = Pt(font_size)
            run.font.color.rgb = C_TEXT_DARK

def set_speaker_notes(slide, notes_text):
    notes_slide = slide.notes_slide
    text_frame = notes_slide.notes_text_frame
    text_frame.text = notes_text

prs = init_presentation()
blank_layout = prs.slide_layouts[6]
TOTAL_SLIDES = 22

# ==============================================================================
# SLIDE 1: TITLE SLIDE
# ==============================================================================
slide1 = prs.slides.add_slide(blank_layout)

bg_banner = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
bg_banner.fill.solid()
bg_banner.fill.fore_color.rgb = C_NAVY_DARK
bg_banner.line.fill.background()

acc1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(0.4), Inches(7.5))
acc1.fill.solid()
acc1.fill.fore_color.rgb = C_TEAL
acc1.line.fill.background()

acc2 = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(9.8), Inches(-1.5), Inches(5.0), Inches(10.5))
acc2.fill.solid()
acc2.fill.fore_color.rgb = RGBColor(19, 64, 116)
acc2.line.color.rgb = C_TEAL
acc2.line.width = Pt(1.5)

tag1 = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(1.5), Inches(3.8), Inches(0.45))
tag1.fill.solid()
tag1.fill.fore_color.rgb = RGBColor(19, 64, 116)
tag1.line.color.rgb = C_TEAL
tf1 = tag1.text_frame
p1 = tf1.paragraphs[0]
p1.text = "CUMMINS AUTOSAR (CSAR) BSW"
p1.font.size = Pt(11)
p1.font.bold = True
p1.font.color.rgb = C_WHITE
p1.alignment = PP_ALIGN.CENTER

title_box = slide1.shapes.add_textbox(Inches(1.2), Inches(2.2), Inches(8.5), Inches(2.2))
tf_main = title_box.text_frame
tf_main.word_wrap = True
p_m = tf_main.paragraphs[0]
p_m.text = "CDDTeleBackupMngr"
p_m.font.size = Pt(38)
p_m.font.bold = True
p_m.font.color.rgb = C_WHITE

p_m2 = tf_main.add_paragraph()
p_m2.text = "Complex Device Driver Telematics Backup Manager"
p_m2.font.size = Pt(20)
p_m2.font.color.rgb = RGBColor(153, 246, 228)
p_m2.space_before = Pt(8)

p_m3 = tf_main.add_paragraph()
p_m3.text = "Comprehensive Technical Knowledge Transfer (KT) & Architecture Walkthrough"
p_m3.font.size = Pt(13)
p_m3.font.color.rgb = RGBColor(203, 213, 225)
p_m3.space_before = Pt(8)

meta_card = create_card(slide1, Inches(1.2), Inches(4.9), Inches(8.2), Inches(1.7), bg_color=RGBColor(15, 23, 42), border_color=C_TEAL, border_width=1.5)
tf_mc = meta_card.text_frame
tf_mc.vertical_anchor = MSO_ANCHOR.MIDDLE

p_row1 = tf_mc.paragraphs[0]
p_row1.text = "Document & Implementation References:"
p_row1.font.size = Pt(10)
p_row1.font.bold = True
p_row1.font.color.rgb = RGBColor(153, 246, 228)

items_meta = [
    ("Software Design Doc", "CSAR_SDD_CddTeleBackupMngr (Integrity ID: 9167284)"),
    ("Target Platforms", "CM3550 & CM3580 (TriCore AURIX TC3xx Microcontroller)"),
    ("Key Technologies", "AUTOSAR 4.x CDD, CSM AES-128 Encryption & CMAC, NvM, Serial Flash SPI"),
    ("Scope", "Architecture, Flowcharts, State Machine, Sequence, Error Recovery, Code Guide")
]
add_bullet_list(tf_mc, items_meta, font_size=9, space_after=2)

set_speaker_notes(slide1, 
"""WELCOME & SESSION OBJECTIVE:
Welcome everyone to this technical Knowledge Transfer (KT) session on the CDDTeleBackupMngr component.
- CDDTeleBackupMngr is a core Basic Software (BSW) Complex Device Driver developed under the Cummins AUTOSAR (CSAR) framework.
- Document Reference: CSAR_SDD_CddTeleBackupMngr (Integrity ID: 9167284).
- Target Electronic Control Modules: CM3550 and CM3580 ECU platforms powered by Infineon AURIX TC3xx TriCore microcontrollers.
- Purpose of this KT: In this presentation, we will walk through the theory of operation, CSAR architectural integration, RTE ports, the 3 runnables, the master state machine, the cryptographic pipeline (AES-128-CBC encryption and CMAC authentication), serial flash read-back verification, and error recovery.
- Following this architectural overview, I will walk you through the source code (CDDTeleBackupMngr.c) line-by-line.""")

# ==============================================================================
# SLIDE 2: EXECUTIVE SUMMARY & COMPONENT CONTEXT
# ==============================================================================
slide2 = prs.slides.add_slide(blank_layout)
add_header(slide2, "Executive Summary: Why CDDTeleBackupMngr?", "1. Overview & Context", "Mission-critical failsafe protection for Telematics Remote Calibration Download (CSU)")
add_footer(slide2, 2, TOTAL_SLIDES)

c1 = create_card(slide2, Inches(0.8), Inches(1.7), Inches(3.7), Inches(4.9), C_BG_CARD, C_BORDER_CARD)
tf_c1 = c1.text_frame
tf_c1.word_wrap = True
p = tf_c1.paragraphs[0]
p.text = "THE PROBLEM & NEED"
p.font.size = Pt(12)
p.font.bold = True
p.font.color.rgb = C_RED_ACCENT
p.space_after = Pt(8)
items_c1 = [
    ("Over-The-Air Flashing", "Remote Calibration Download (CSU) updates engine ECU calibrations in the field over telematics."),
    ("Flash Corruption Risk", "Power disruptions, battery disconnects, or bad network transfers during calibration updates can brick an ECM."),
    ("Rollback Guarantee", "Automotive functional safety requires a guaranteed rollback copy of known good calibration if newly flashed software fails.")
]
add_bullet_list(tf_c1, items_c1, font_size=9, space_after=6)

c2 = create_card(slide2, Inches(4.8), Inches(1.7), Inches(3.7), Inches(4.9), C_BG_CARD, C_TEAL, border_width=1.5)
tf_c2 = c2.text_frame
tf_c2.word_wrap = True
p = tf_c2.paragraphs[0]
p.text = "CORE RESPONSIBILITY"
p.font.size = Pt(12)
p.font.bold = True
p.font.color.rgb = C_NAVY_DARK
p.space_after = Pt(8)
items_c2 = [
    ("Autonomous Execution", "Encapsulates the complete backup lifecycle as an autonomous state-machine-driven BSW CDD."),
    ("Secure Data Pipeline", "Reads raw Program Flash (PF) data, encrypts via AES-128, and signs with CMAC via CSM."),
    ("Storage on Serial Flash", "Transfers encrypted blocks to external SPI Serial Flash with byte-by-byte read verification."),
    ("Persistent NvM Tracking", "Maintains calibration states, rollback countdowns, and portover statuses across key cycles.")
]
add_bullet_list(tf_c2, items_c2, font_size=9, space_after=6)

c3 = create_card(slide2, Inches(8.8), Inches(1.7), Inches(3.7), Inches(4.9), C_BG_CARD, C_BORDER_CARD)
tf_c3 = c3.text_frame
tf_c3.word_wrap = True
p = tf_c3.paragraphs[0]
p.text = "KEY CAPABILITIES"
p.font.size = Pt(12)
p.font.bold = True
p.font.color.rgb = C_NAVY_DARK
p.space_after = Pt(8)
items_c3 = [
    ("Tri-Attempt Retry Loop", "If flash write or crypto verification fails, ECM retries up to 3 times before setting BACKUP_FAILED."),
    ("Cybersecurity Logging", "Exhaustion of retries immediately logs a Cybersecurity Security Event (Reason codes: 13, 67)."),
    ("Configurable Rollback Timer", "Calibratable rollback window (caTeleRollBackTimer) before committing the backup."),
    ("Zero Application Overhead", "Runs asynchronously on 10ms timing events without stalling engine control loops.")
]
add_bullet_list(tf_c3, items_c3, font_size=9, space_after=6)

set_speaker_notes(slide2,
"""KEY TALKING POINTS FOR SLIDE 2:
1. Business Context: Telematics Remote Calibration Download allows Cummins fleets to update engine calibrations Over-The-Air (OTA) without visiting a service bay.
2. The Safety Imperative: If a new calibration is downloaded and portover completes, the vehicle must test run. If something goes wrong, or if rollback is requested, the ECU needs a complete, trusted, encrypted backup of the previous calibration.
3. Why Serial Flash? Microcontroller internal Program Flash is limited. We back up the entire calibration footprint to an external 64MB SPI Serial Flash.
4. Security: The backup cannot be stored in plain text. It must be encrypted (AES-128-CBC) and authenticated (CMAC) to prevent unauthorized tampering or intellectual property extraction.
5. In summary, CDDTeleBackupMngr is the autonomous engine that coordinates memory erasure, reading, crypto operations, serial flash programming, hardware read-back verification, and non-volatile status updates.""")

# ==============================================================================
# SLIDE 3: SYSTEM ARCHITECTURE & CSAR LAYER MODEL
# ==============================================================================
slide3 = prs.slides.add_slide(blank_layout)
add_header(slide3, "CSAR System Architecture & Boundary Model", "2. Architecture", "Layered AUTOSAR integration across Application SWCs, BSW Services, and Hardware")
add_footer(slide3, 3, TOTAL_SLIDES)

slide3.shapes.add_picture('diag_csar_architecture.png', Inches(0.8), Inches(1.65), width=Inches(6.8))

c_arch = create_card(slide3, Inches(7.8), Inches(1.65), Inches(4.7), Inches(5.1), C_BG_CARD, C_BORDER_CARD)
tf_a = c_arch.text_frame
tf_a.word_wrap = True
p = tf_a.paragraphs[0]
p.text = "ARCHITECTURAL INTEGRATION POINTS"
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = C_NAVY_DARK
p.space_after = Pt(6)

items_a = [
    ("Complex Device Driver (CDD)", "Resides in the BSW layer with direct access to hardware buffers and low-level memory services while exposing standard AUTOSAR ports to the RTE."),
    ("Crypto Service Manager (CSM)", "Interfaced for AES-128-CBC encryption, CMAC message authentication, and hardware-backed random IV generation."),
    ("Non-Volatile Memory (NvM)", "Stores backup execution state, rollback timer status, and triggers asynchronous block writes to FBLGeneral descriptor."),
    ("Virtual Memory Access Manager", "Interacts with vMemAccM and SPI drivers via SerialFlashGetServ() and GetSerialFlashState()."),
    ("Program Flash (PF)", "Directly reads uncompressed calibration blocks and segments from TriCore AURIX internal flash memory."),
    ("External Serial Flash (SF)", "Erases, programs, and verifies 256-byte pages in dedicated Backup memory regions.")
]
add_bullet_list(tf_a, items_a, font_size=8.5, space_after=4)

set_speaker_notes(slide3,
"""KEY TALKING POINTS FOR SLIDE 3:
- Refer to Figure 1 and the boundary diagram from Section 4.2 of the SDD.
- Notice the position of CDDTeleBackupMngr: It sits in the BSW layer as a Complex Device Driver.
- Why is it a CDD rather than a standard SWC?
  Because it requires tight integration with raw memory pointers in Program Flash, high-throughput buffer transfers, and custom synchronization with the Serial Flash SPI driver.
- It interfaces with three major BSW modules:
  1. CSM (Crypto Service Manager): Provides standardized cryptographic primitives (AES encryption and CMAC MAC generation).
  2. NvM (Non-Volatile RAM Manager): Manages persistence of backup status across ECU power resets.
  3. vMemAccM / SPI Driver: Handles the external Serial Flash memory access commands.
- On the hardware level, we interface between Infineon AURIX TC3xx internal Program Flash and Cypress/Micron external Serial Flash.""")

# ==============================================================================
# SLIDE 4: HARDWARE TOPOLOGY & SERIAL FLASH PARTITIONING
# ==============================================================================
slide4 = prs.slides.add_slide(blank_layout)
add_header(slide4, "Hardware Topology & Memory Partitioning", "2. Architecture", "Physical flash separation: Internal TriCore Flash vs. External SPI Serial Flash")
add_footer(slide4, 4, TOTAL_SLIDES)

slide4.shapes.add_picture('diag_data_layout.png', Inches(0.8), Inches(1.65), width=Inches(7.2))

c_mem = create_card(slide4, Inches(8.2), Inches(1.65), Inches(4.3), Inches(5.1), C_BG_CARD, C_BORDER_CARD)
tf_m = c_mem.text_frame
tf_m.word_wrap = True
p = tf_m.paragraphs[0]
p.text = "MEMORY MAP SPECIFICATION"
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = C_NAVY_DARK
p.space_after = Pt(6)

items_m = [
    ("Serial Flash Device", "512 Mbit (64 MByte) SPI NOR Flash (Cypress S25FL512S or Micron 25QL512)."),
    ("Buffer Region (0x0200_0000)", "Base Address: 33,554,432 (32 MB). Staging area for incoming calibration downloads over telematics."),
    ("Backup Region (0x0300_0000)", "Base Address: 50,331,648 (48 MB). Dedicated non-volatile rollback vault managed by CDDTeleBackupMngr."),
    ("CSU Metadata Header", "Located at the start of Backup Region. Stores block counts, segment sizes, and header CMAC."),
    ("256-Byte Page Granularity", "All serial flash writes and read-backs operate in SF_PAGE_SIZE chunks (256 bytes)."),
    ("Hardware Independence", "vMemAccM driver layer abstracts physical chip commands (sector erase, page program).")
]
add_bullet_list(tf_m, items_m, font_size=8.5, space_after=4)

set_speaker_notes(slide4,
"""KEY TALKING POINTS FOR SLIDE 4:
- Let's look at the physical memory layout (Section 4 and 10 of the SDD):
- The ECU features an external 64 MB Serial Flash connected via High-Speed SPI.
- Memory Partitioning:
  1. Buffer Region starting at 0x02000000 (32 MB): Used by Telematics Processing to download and verify new incoming calibrations before flashing.
  2. Backup Region starting at 0x03000000 (48 MB): This is the exact area managed by CDDTeleBackupMngr.
- Inside the Backup Region:
  - The CSU Metadata Header sits at the start address (SF_BACKUP_CSU_METADATA_STRUCTURE_START).
  - Following the metadata, we store encrypted block pages.
  - At the end of each block, we store a 16-byte Block CMAC at a pre-calculated reference address.
- Notice that all operations are page-aligned to 256 bytes (SF_PAGE_SIZE).""")

# ==============================================================================
# SLIDE 5: COMPONENT INTERFACES & AUTOSAR PORTS
# ==============================================================================
slide5 = prs.slides.add_slide(blank_layout)
add_header(slide5, "Software Component Boundary & RTE Interfaces", "3. Interfaces", "Standardized AUTOSAR Sender/Receiver and Client/Server port specifications")
add_footer(slide5, 5, TOTAL_SLIDES)

c_ports = create_card(slide5, Inches(0.8), Inches(1.65), Inches(7.5), Inches(5.1), C_BG_CARD, C_BORDER_CARD)
tf_p = c_ports.text_frame
tf_p.word_wrap = True
p = tf_p.paragraphs[0]
p.text = "AUTOSAR PORT INTERFACE MATRIX"
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = C_NAVY_DARK
p.space_after = Pt(4)

port_items = [
    ("nvrBackupStatus / nvwBackupStatus", "S/R Port (uint8): Reads and updates current backup state (0: UNINITIALIZED, 1: IN_PROGRESS, 2: COMPLT_VALID, 3: FAILED, 4: CSU_FEATURE_DISABLE)."),
    ("nvrRollBackTimerStatus / nvwRollBackTimerStatus", "S/R Port (uint8/32): Tracks whether the automatic rollback countdown timer is active (1) or inactive (0)."),
    ("nvrTeleRollBackTimeOut / nvwTeleRollBackTimeOut", "S/R Port (uint32): Current elapsed seconds since portover completion. Incremented every 5s."),
    ("nvrPortOverstatus / nvwPortOverstatus", "S/R Port (uint8): Checks if calibration transfer to flash is finished (PORTOVER_COMPLETE). Resets to PORTOVER_DEFAULT on completion."),
    ("ppCSUFeatureEnbl", "S/R Port (boolean): Master enable trim calibration. If FALSE, backup is disabled."),
    ("ppToolConnectedProg", "S/R Port (boolean): Detects new cal download (0x01) triggering immediate backup."),
    ("ppLogCSEvent_LogEvent", "C/S Port (Client): Invoked on 3-attempt failure to record cybersecurity audit events.")
]
add_bullet_list(tf_p, port_items, font_size=8, space_after=3)

c_nvm = create_card(slide5, Inches(8.5), Inches(1.65), Inches(4.0), Inches(5.1), C_PURPLE_LIGHT, C_PURPLE, border_width=1.5)
tf_n = c_nvm.text_frame
tf_n.word_wrap = True
p = tf_n.paragraphs[0]
p.text = "NVRAM & BSW SERVICES"
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = C_PURPLE
p.space_after = Pt(6)

items_n = [
    ("NvM Block Descriptor", "NvMConf_NvMBlockDescriptor_NvbswcBootSharedBootSharedFBLGeneral: Stores boot shared flags persistently across resets."),
    ("Asynchronous NvM Write", "Calls NvM_WriteBlock(Descriptor, NULL_PTR). If write returns E_NOT_OK, sets NvM_backup_update = TRUE to retry in scheduler."),
    ("CSM Service IDs", "CSM_AES_128_CBC_ENCRYPT_SERVICE_ID and CSM_MAC_GEN_SERVICE_ID."),
    ("Serial Flash Service", "SerialFlashGetServ() dispatches SF_FULL_ERASE, SF_DATA_TRANSFER, and SF_READ_DATA.")
]
add_bullet_list(tf_n, items_n, font_size=8.5, space_after=4)

set_speaker_notes(slide5,
"""KEY TALKING POINTS FOR SLIDE 5:
- Refer to Section 5 of the SDD.
- The component exposes explicit Sender/Receiver (S/R) ports and one Client/Server (C/S) port:
  1. nvrBackupStatus / nvwBackupStatus: Holds the state of the backup lifecycle.
  2. nvrRollBackTimerStatus / nvwRollBackTimerStatus: Controls whether the 5-second timer runnable is actively incrementing the timeout.
  3. nvrPortOverstatus: Signals that the bootloader/tool has finished porting over the new calibration.
  4. ppCSUFeatureEnbl: This was added under CR#18134205 (CSU Master Enable). If this trim is disabled, the module sets status to CSU_FEATURE_DISABLE and takes no action.
  5. ppLogCSEvent_LogEvent: Cybersecurity event logging port. If backup fails after 3 retries, an event is logged with reason codes {13, 67}.
- For NVRAM, notice the use of NvM_WriteBlock for NvbswcBootSharedBootSharedFBLGeneral.""")

# ==============================================================================
# SLIDE 6: CORE RUNNABLES & EXECUTION LIFECYCLE
# ==============================================================================
slide6 = prs.slides.add_slide(blank_layout)
add_header(slide6, "Core Runnables & Execution Lifecycle", "4. Runnables", "Four software entities orchestrating boot initialization, timing, and state execution")
add_footer(slide6, 6, TOTAL_SLIDES)

entities = [
    ("reInitCDDTeleBackupMngr", "ECU Boot / RTE Start", "One-Shot Init Runnable", C_BLUE_LIGHT, C_BLUE_ACCENT, [
        "Invoked once immediately after RTE initialization.",
        "Reads non-volatile backup states and portover status.",
        "Arms rollback timer or triggers immediate backup.",
        "Checks CSU master feature enable gate."
    ]),
    ("reTeleRollBackTimeCheck", "TimingEvent: Every 5s", "Rollback Timer Monitor", C_AMBER_LIGHT, C_AMBER, [
        "Executes periodically every 5 seconds.",
        "Increments TeleRollBackTimeOut counter by 5.",
        "Compares timeout against caTeleRollBackTimer calibration.",
        "When expired: sets status to BACKUP_IN_PROGRESS."
    ]),
    ("reCddTeleBackupSchdlr", "TimingEvent: Every 10ms", "Master State Scheduler", C_TEAL_LIGHT, C_TEAL, [
        "Executes periodically every 10 milliseconds.",
        "Active only if status == BACKUP_IN_PROGRESS.",
        "Drives the 15-state primary data pipeline.",
        "Coordinates crypto, flash write, verify & metadata."
    ]),
    ("metadata_extract", "Synchronous Helper Call", "Internal Data Parser", C_PURPLE_LIGHT, C_PURPLE, [
        "Called internally from reCddTeleBackupSchdlr.",
        "Parses telematics_csu_table block/segment data.",
        "Computes exact metadata length & padding.",
        "Pre-calculates block_cmac_addr_reference."
    ])
]

for idx, (title, trigger, tag, bg, border, pts) in enumerate(entities):
    col = idx % 2
    row = idx // 2
    x = Inches(0.8 + col * 5.95)
    y = Inches(1.65 + row * 2.55)
    card = create_card(slide6, x, y, Inches(5.8), Inches(2.35), bg, border, border_width=1.5)
    tf = card.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = f"{title}()"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = border

    p_tag = tf.add_paragraph()
    p_tag.text = f"Trigger: {trigger}  |  Role: {tag}"
    p_tag.font.size = Pt(8.5)
    p_tag.font.bold = True
    p_tag.font.color.rgb = C_NAVY_DARK
    p_tag.space_after = Pt(4)

    add_bullet_list(tf, pts, font_size=8, space_after=2)

set_speaker_notes(slide6,
"""KEY TALKING POINTS FOR SLIDE 6:
- Section 8.1 of the SDD lists the API functions.
- The component is comprised of 3 RTE runnables and 1 internal static function:
  1. reInitCDDTeleBackupMngr: The boot initializer. Runs once when the RTE starts up.
  2. reTeleRollBackTimeCheck: Runs every 5 seconds. Manages the countdown timer before backup triggers.
  3. reCddTeleBackupSchdlr: The workhorse of the module. Runs every 10 milliseconds. Implements the complete state machine.
  4. metadata_extract: Internal helper called at the beginning of the scheduler to parse the CSU structure table.
- Notice the clear separation of concerns:
  The 5s runnable handles slow timing events without loading the CPU.
  The 10ms runnable handles the high-speed state machine for flash reading, encryption, and writing.""")

# ==============================================================================
# SLIDE 7: STARTUP & INITIALIZATION FLOW (reInitCDDTeleBackupMngr)
# ==============================================================================
slide7 = prs.slides.add_slide(blank_layout)
add_header(slide7, "Startup & Initialization: reInitCDDTeleBackupMngr()", "5. Execution Flow", "Restoring state, checking calibration flags, and configuring initial triggers")
add_footer(slide7, 7, TOTAL_SLIDES)

slide7.shapes.add_picture('diag_init_flowchart.png', Inches(0.8), Inches(1.65), width=Inches(6.6))

c_init = create_card(slide7, Inches(7.6), Inches(1.65), Inches(4.9), Inches(5.1), C_BG_CARD, C_BORDER_CARD)
tf_i = c_init.text_frame
tf_i.word_wrap = True
p = tf_i.paragraphs[0]
p.text = "INITIALIZATION LOGIC WALKTHROUGH"
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = C_NAVY_DARK
p.space_after = Pt(6)

items_i = [
    ("Set Flash Start Addresses", "Initializes nvwBackupSfStartAddr (0x0300_0000) and nvwBufferSfStartAddr (0x0200_0000)."),
    ("Read NVRAM & Ports", "Reads NVM_portover_status, new_cal_download, NVM_Back_up_status, Rollback_timer_status, and CSU_feature_enable."),
    ("Feature Enable Gate", "If CSU_feature_enable == FALSE: sets status to CSU_FEATURE_DISABLE and bypasses backup logic."),
    ("Condition A: Arm Rollback Timer", "If portover is COMPLETE, timer is inactive, and backup is not already in progress:\n-> Sets Rollback_timer_status = 1, TeleRollBackTimeOut = 0."),
    ("Condition B: Immediate Backup", "If new_cal_download == 0x01 OR NVM_Back_up_status == BACKUP_FAILED:\n-> Sets NVM_Back_up_status = BACKUP_IN_PROGRESS immediately."),
    ("NVRAM Persistence", "Calls NvM_WriteBlock() for FBLGeneral block. If write returns E_NOT_OK, sets NvM_backup_update = TRUE to retry in the 10ms scheduler.")
]
add_bullet_list(tf_i, items_i, font_size=8.5, space_after=4)

set_speaker_notes(slide7,
"""KEY TALKING POINTS FOR SLIDE 7:
- Open code.txt at line 138: FUNC(void, CDDTeleBackupMngr_CODE) reInitCDDTeleBackupMngr(void).
- Step 1: Default serial flash addresses are written out to RTE ports.
- Step 2: The runnable reads five critical status variables.
- Step 3: Checks CSU_feature_enable. If FALSE, sets CSU_FEATURE_DISABLE. This satisfies requirement 18134113.
- Step 4: Evaluates two distinct triggers:
  - Branch A (Rollback Timer Arming):
    If NVM_portover_status == PORTOVER_COMPLETE and timer is not yet active, it arms the 5s timer: Rollback_timer_status = 1, TeleRollBackTimeOut = 0.
  - Branch B (Immediate Backup):
    If new_cal_download == 1 (from tool) or if previous backup was BACKUP_FAILED, it starts immediately by setting BACKUP_IN_PROGRESS.
- Step 5: Commits the new backup status to NvM via NvM_WriteBlock. If E_NOT_OK, it flags NvM_backup_update = TRUE for deferred retry.""")

# ==============================================================================
# SLIDE 8: ROLLBACK TIMER MANAGEMENT (reTeleRollBackTimeCheck)
# ==============================================================================
slide8 = prs.slides.add_slide(blank_layout)
add_header(slide8, "Rollback Timer Management: reTeleRollBackTimeCheck()", "5. Execution Flow", "Managing the configurable pre-backup rollback evaluation window")
add_footer(slide8, 8, TOTAL_SLIDES)

slide8.shapes.add_picture('diag_rollback_flowchart.png', Inches(0.8), Inches(1.65), width=Inches(6.4))

c_rb = create_card(slide8, Inches(7.4), Inches(1.65), Inches(5.1), Inches(5.1), C_BG_CARD, C_BORDER_CARD)
tf_rb = c_rb.text_frame
tf_rb.word_wrap = True
p = tf_rb.paragraphs[0]
p.text = "ROLLBACK TIMER OPERATIONAL MECHANISM"
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = C_NAVY_DARK
p.space_after = Pt(6)

items_rb = [
    ("5-Second Cadence", "Triggered every 5000ms via RTE timing event, minimizing CPU runtime impact during normal engine operation."),
    ("Gate Condition", "Executes only if Rollback_timer_status == TRUE AND CSU_feature_enable == TRUE. Otherwise exits immediately."),
    ("Timeout Comparison", "Compares current elapsed timeout against calibration caTeleRollBackTimer (via Rte_CData_caTeleRollBackTimer())."),
    ("Timer Running Path", "If TeleRollBackTimeOut < calibration limit, increments counter by 5 seconds (TeleRollBackTimeOut += 5)."),
    ("Timer Expiration Path", "If TeleRollBackTimeOut >= caTeleRollBackTimer:\n• Sets NVM_Back_up_status = BACKUP_IN_PROGRESS\n• Sets Rollback_timer_status = 0 (Deactivates timer)"),
    ("Atomic NvM Persistence", "Writes updated timeout & status to NVRAM descriptor. Tracks write result via Rollback_NvM_WriteBlock_rtn.")
]
add_bullet_list(tf_rb, items_rb, font_size=8.5, space_after=4)

set_speaker_notes(slide8,
"""KEY TALKING POINTS FOR SLIDE 8:
- Open code.txt at line 1326: FUNC(void, CDDTeleBackupMngr_CODE) reTeleRollBackTimeCheck(void).
- Why does the rollback timer exist?
  After a remote calibration download completes, the vehicle needs a grace period (the rollback window) to verify that the vehicle operates normally with the new calibration.
  During this window, the operator or telematics system can still trigger a rollback.
  Once this window expires without error, the ECU declares the new software solid and starts backing it up!
- How it works:
  - Runs every 5 seconds.
  - Reads TeleRollBackTimeOut from NVM.
  - Compares it to calibration parameter caTeleRollBackTimer.
  - If timeout is reached:
    NVM_Back_up_status = BACKUP_IN_PROGRESS
    Rollback_timer_status = 0 (stops timer).
  - This immediately activates reCddTeleBackupSchdlr on its next 10ms tick!""")

# ==============================================================================
# SLIDE 9: CSU METADATA & ODX-F DATA STRUCTURES
# ==============================================================================
slide9 = prs.slides.add_slide(blank_layout)
add_header(slide9, "CSU Metadata & ODX-F Data Structures", "6. Data Structures", "ODX-F block/segment hierarchies and dynamic serial flash address translation")
add_footer(slide9, 9, TOTAL_SLIDES)

c_ds = create_card(slide9, Inches(0.8), Inches(1.65), Inches(6.0), Inches(5.1), C_BG_CARD, C_BORDER_CARD)
tf_ds = c_ds.text_frame
tf_ds.word_wrap = True
p = tf_ds.paragraphs[0]
p.text = "ODX-F DATA MODEL (telematics_csu_table)"
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = C_NAVY_DARK
p.space_after = Pt(6)

items_ds = [
    ("Hierarchical Model", "Calibration is structured as N Blocks -> each Block contains M Segments -> each Segment contains raw Program Flash memory."),
    ("telematics_csu_block_count", "Specifies total number of ODX-F blocks to be backed up (e.g., Engine Cal, Transmission Cal, Diagnostics)."),
    ("Segment Descriptor (8 Bytes)", "Struct containing: uint32 source_start_address_pf (4B) and uint32 uncompress_size (4B)."),
    ("Big-Endian Conversion", "Segment address & size are converted to Big-Endian network byte order before hashing into CMAC (Req 13738945)."),
    ("tele_sf_request_data_t", "Buffer structure passed to SerialFlashGetServ() containing source address, data pointer, length, and transfer mode.")
]
add_bullet_list(tf_ds, items_ds, font_size=8.5, space_after=4)

c_math = create_card(slide9, Inches(7.1), Inches(1.65), Inches(5.4), Inches(5.1), C_PURPLE_LIGHT, C_PURPLE, border_width=1.5)
tf_m = c_math.text_frame
tf_m.word_wrap = True
p = tf_m.paragraphs[0]
p.text = "METADATA LENGTH & CMAC REFERENCE MATH"
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = C_PURPLE
p.space_after = Pt(6)

items_math = [
    ("Function metadata_extract()", "Executed in BACKUP_FULL_ERASE state to populate csu_header_backup from telematics_csu_table."),
    ("Metadata Length Formula", "metadata_length = CSU_METADATA_STRUCT_FIX_LENGTH (0x17)\n+ (num_blocks * (BLOCK_CYBER_HEADER_LENGTH (0x188) + 1))\n+ (total_segments * SEGMENT_DATA_STRUCT_LENGTH (0xC))\n+ CMAC_GEN_LENGTH (16 bytes)"),
    ("Page Alignment Padding", "cmac_padding = SF_PAGE_SIZE - (metadata_length % SF_PAGE_SIZE)"),
    ("Block CMAC Reference Address", "block_cmac_addr_reference = METADATA_REF_ADDRESS + cmac_padding + metadata_length"),
    ("Key Benefit", "Guarantees that block-level CMAC storage locations never collide with metadata headers or encrypted payloads.")
]
add_bullet_list(tf_m, items_math, font_size=8.5, space_after=4)

set_speaker_notes(slide9,
"""KEY TALKING POINTS FOR SLIDE 9:
- Open code.txt at line 1377: static void metadata_extract(void).
- How is calibration organized in memory?
  It follows the ODX-F standard (Requirement 13584666):
  - A calibration update consists of multiple blocks (e.g. Code block, Calibration block).
  - Each block consists of multiple memory segments.
  - Each segment defines a starting address in internal Program Flash and an uncompressed length.
- Look at the calculation of block_cmac_addr_reference:
  The module calculates the exact byte length of the metadata header, pads it up to the next 256-byte serial flash page boundary, and calculates where block CMACs must be stored.
- Big-Endian Requirement (Req 13738945):
  Notice that during CMAC generation, the segment address and length are fed into the MAC generator in Big-Endian order. We will see how seg_info[8] is formatted in SEG_START_HANDLE.""")

# ==============================================================================
# SLIDE 10: MASTER BACKUP STATE MACHINE ARCHITECTURE
# ==============================================================================
slide10 = prs.slides.add_slide(blank_layout)
add_header(slide10, "Master Backup State Machine Architecture", "7. State Machine", "2-Tier state machine: 15-state Data Pipeline & 6-state Metadata Pipeline")
add_footer(slide10, 10, TOTAL_SLIDES)

slide10.shapes.add_picture('diag_state_machine.png', Inches(0.8), Inches(1.65), width=Inches(11.733))

set_speaker_notes(slide10,
"""KEY TALKING POINTS FOR SLIDE 10:
- This is the master architectural map of reCddTeleBackupSchdlr() (Lines 249-1325).
- Notice the two-tiered design:
  - TIER 1: Primary Data State Machine (backup_flag) - Consists of 15 states.
    It handles full chip erase, Program Flash address calculation, crypto initialization, page-by-page encryption, serial flash writes, read-back verification, and block CMAC storage.
  - TIER 2: Metadata Sub-State Machine (backup_metadata_flag) - Consists of 6 states.
    Triggered only after all blocks and their CMACs are completely written. It packs the CSU metadata header, computes a metadata CMAC, and writes the header to the beginning of Serial Flash.
- Let's break down each phase in detail over the next several slides.""")

# ==============================================================================
# SLIDE 11: DETAILED FLOW: PHASE 1 - ERASE, ADDRESSING & KEYS
# ==============================================================================
slide11 = prs.slides.add_slide(blank_layout)
add_header(slide11, "Phase 1: Erase, Addressing & Key Loading", "8. Detailed Flow", "States: NO_REQUEST -> BACKUP_FULL_ERASE -> PF_ADDR_HANDLE -> SET_KEYS")
add_footer(slide11, 11, TOTAL_SLIDES)

states_p1 = [
    ("State 0: NO_REQUEST", "Idle / Waiting State", C_BG_CARD, C_BORDER_CARD, [
        "Default resting state of the scheduler.",
        "Executes no operations.",
        "Exited when NVM_Back_up_status == BACKUP_IN_PROGRESS."
    ]),
    ("State 1: BACKUP_FULL_ERASE", "Erase SF Backup Region", C_RED_LIGHT, C_RED_ACCENT, [
        "Checks GetSerialFlashState() == SF_REQUEST_COMPLETE.",
        "Dispatches SF_FULL_ERASE on BACKUP_REGION via SerialFlashGetServ().",
        "Invokes metadata_extract() to parse CSU table.",
        "Initializes PF_Addr to Block[0].Segment[0] start.",
        "Transitions to PF_ADDR_HANDLE (or RETRY on fail)."
    ]),
    ("State 2: PF_ADDR_HANDLE", "Address & Boundary Logic", C_BLUE_LIGHT, C_BLUE_ACCENT, [
        "Calculates segment and block boundary endpoints.",
        "Detects start of segment: triggers 16B Random IV generation via Csm_RandomGenerate().",
        "Detects last page of segment: calculates remaining bytes and sets segment_last_page flag.",
        "Copies 256 bytes from Program Flash into Mem_Read_Buff.",
        "Transitions to SET_KEYS (start of seg) or CYBER_UPDATE."
    ]),
    ("State 3: SET_KEYS", "Load Keys into CSM", C_PURPLE_LIGHT, C_PURPLE, [
        "Configures AES encryption and CMAC keys in CSM.",
        "Calls Csm_KeyElementSet() with IV and key material.",
        "Calls Csm_KeySetValid() to activate keys.",
        "Transitions to CMAC_START or ENCRYPT_START."
    ])
]

for idx, (title, sub, bg, border, pts) in enumerate(states_p1):
    x = Inches(0.8 + (idx % 2) * 5.95)
    y = Inches(1.65 + (idx // 2) * 2.55)
    card = create_card(slide11, x, y, Inches(5.8), Inches(2.35), bg, border, border_width=1.5)
    tf = card.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = border

    p_sub = tf.add_paragraph()
    p_sub.text = sub
    p_sub.font.size = Pt(8.5)
    p_sub.font.bold = True
    p_sub.font.color.rgb = C_NAVY_DARK
    p_sub.space_after = Pt(4)

    add_bullet_list(tf, pts, font_size=8, space_after=2)

set_speaker_notes(slide11,
"""KEY TALKING POINTS FOR SLIDE 11:
- Open code.txt at line 290:
- NO_REQUEST (Line 292): Idle state.
- BACKUP_FULL_ERASE (Line 299):
  Before writing anything, the entire Backup Region in external serial flash must be erased.
  Notice the non-blocking polling: It checks GetSerialFlashState(). If busy, it yields and waits for the next 10ms tick.
  Once complete, it calls metadata_extract() and initializes PF_Addr.
- PF_ADDR_HANDLE (Line 342):
  Loops through blocks and segments to compute current and end addresses.
  If at segment start, generates a 16-byte random IV using Csm_RandomGenerate().
  Handles padding if the segment length is not an exact multiple of 256 bytes.
  Copies plaintext data from internal Program Flash into Mem_Read_Buff.
- SET_KEYS (Line 416):
  Loads keys into the CSM hardware abstraction layer via Csm_KeyElementSet() and sets them valid.""")

# ==============================================================================
# SLIDE 12: PHASE 2: CRYPTOGRAPHIC PIPELINE (AES-128 & CMAC)
# ==============================================================================
slide12 = prs.slides.add_slide(blank_layout)
add_header(slide12, "Phase 2: Cryptographic Pipeline (AES-128 & CMAC)", "8. Detailed Flow", "Confidentiality & Authentication via AUTOSAR Crypto Service Manager (CSM)")
add_footer(slide12, 12, TOTAL_SLIDES)

slide12.shapes.add_picture('diag_crypto_pipeline.png', Inches(0.8), Inches(1.65), width=Inches(6.8))

c_cry = create_card(slide12, Inches(7.8), Inches(1.65), Inches(4.7), Inches(5.1), C_BG_CARD, C_BORDER_CARD)
tf_c = c_cry.text_frame
tf_c.word_wrap = True
p = tf_c.paragraphs[0]
p.text = "CRYPTOGRAPHIC SECURITY SPECIFICATION"
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = C_NAVY_DARK
p.space_after = Pt(6)

items_cry = [
    ("AES-128-CBC Encryption", "Provides confidentiality. Program Flash data is encrypted into backup_encrypt_data[] using 128-bit AES in CBC mode."),
    ("Cipher IV Initialization", "A unique 16-byte IV is generated per session (Csm_RandomGenerate) and stored in the first page of the block."),
    ("CMAC Authentication", "Provides data integrity and origin authentication. Computed incrementally across all segment data."),
    ("Segment Header Binding", "State SEG_START_HANDLE formats [source_start_address_pf (4B) | uncompress_size (4B)] into Big-Endian and hashes it BEFORE payload data!"),
    ("Asynchronous CSM Polling", "Handles CRYPTO_E_BUSY gracefully: if CSM hardware is busy, scheduler stays in state until next 10ms cycle.")
]
add_bullet_list(tf_c, items_cry, font_size=8.5, space_after=4)

set_speaker_notes(slide12,
"""KEY TALKING POINTS FOR SLIDE 12:
- Open code.txt at line 482 (ENCRYPT_START), line 521 (CMAC_START), and line 549 (SEG_START_HANDLE).
- Security Architecture:
  1. Confidentiality: AES-128-CBC encryption prevents calibration intellectual property extraction from serial flash.
  2. Authenticity: CMAC (Cipher-based MAC) ensures that any bit-flip, tampering, or flash corruption is detected.
- Notice SEG_START_HANDLE (Line 549):
  Requirement 13738945 specifies that CMAC must cover the segment starting address and length in Big-Endian format.
  Look at the code: It creates seg_info[8], packs the 4-byte address and 4-byte size in network byte order, and calls Csm_MacGenerate(UPDATE) with this 8-byte header!
- Then it transitions to CYBER_UPDATE to process the actual payload data.""")

# ==============================================================================
# SLIDE 13: PHASE 3: PAGE PROCESSING & READ-BACK VERIFICATION
# ==============================================================================
slide13 = prs.slides.add_slide(blank_layout)
add_header(slide13, "Phase 3: Page Processing, Writing & Verification", "8. Detailed Flow", "States: CYBER_UPDATE -> ENCRYPT_FINISH -> WRITE_TO_SF -> BACKUP_READ_SF_DATA")
add_footer(slide13, 13, TOTAL_SLIDES)

states_p3 = [
    ("State 6: CYBER_UPDATE", "Chunk Encryption & MAC", C_GREEN_LIGHT, C_GREEN, [
        "Calls Csm_Encrypt(UPDATE) to encrypt 256 bytes from Mem_Read_Buff into backup_encrypt_data.",
        "Calls Csm_MacGenerate(UPDATE) to update block CMAC with plain data.",
        "If last page of segment: transitions to ENCRYPT_FINISH.",
        "Otherwise: transitions directly to WRITE_TO_SF."
    ]),
    ("State 7: ENCRYPT_FINISH", "Finalize AES Ciphertext", C_AMBER_LIGHT, C_AMBER, [
        "Calls Csm_Encrypt(FINISH) to finalize cipher stream and handle block cipher padding.",
        "Updates backup_result_len_encrypt with final ciphertext length.",
        "Transitions to WRITE_TO_SF."
    ]),
    ("State 8: WRITE_TO_SF", "Write Encrypted 256B Page", C_BLUE_LIGHT, C_BLUE_ACCENT, [
        "Dispatches SF_DATA_TRANSFER request via SerialFlashGetServ().",
        "Writes backup_encrypt_data[256] to Serial Flash at PF2SF_translate_addr.",
        "Polls GetSerialFlashState().",
        "On success: transitions to BACKUP_READ_SF_DATA."
    ]),
    ("State 9: BACKUP_READ_SF_DATA", "Byte-by-Byte Verification", C_TEAL_LIGHT, C_TEAL, [
        "CRITICAL SAFETY STEP: Reads written page back from Serial Flash into Mem_Read_Buff.",
        "Compares every byte: if Mem_Read_Buff[i] != backup_encrypt_data[i] -> triggers BACKUP_RETRY!",
        "If matched: advances PF_Addr by 256 bytes.",
        "If block end reached -> CMAC_FINISH; else -> PF_ADDR_HANDLE."
    ])
]

for idx, (title, sub, bg, border, pts) in enumerate(states_p3):
    x = Inches(0.8 + (idx % 2) * 5.95)
    y = Inches(1.65 + (idx // 2) * 2.55)
    card = create_card(slide13, x, y, Inches(5.8), Inches(2.35), bg, border, border_width=1.5)
    tf = card.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = border

    p_sub = tf.add_paragraph()
    p_sub.text = sub
    p_sub.font.size = Pt(8.5)
    p_sub.font.bold = True
    p_sub.font.color.rgb = C_NAVY_DARK
    p_sub.space_after = Pt(4)

    add_bullet_list(tf, pts, font_size=8, space_after=2)

set_speaker_notes(slide13,
"""KEY TALKING POINTS FOR SLIDE 13:
- Open code.txt at line 581 (CYBER_UPDATE), line 631 (ENCRYPT_FINISH), line 697 (WRITE_TO_SF), and line 740 (BACKUP_READ_SF_DATA).
- Let's highlight the Hardware Read-Back Verification in BACKUP_READ_SF_DATA (Line 740):
  Why is this step so critical?
  In automotive flash programming, write commands can report success at the SPI bus level while physical flash cells fail to retain charge or suffer from bad sectors.
  To prevent silent data corruption, CDDTeleBackupMngr immediately issues SF_READ_DATA, reads the 256 bytes back, and loops through:
  if(Mem_Read_Buff[read_index] != backup_encrypt_data[read_index])
  If even a single byte differs, it flags error 0x1D and immediately jumps to BACKUP_RETRY!
- If the comparison succeeds, it checks whether PF_Addr == block_end_addr. If yes, it moves to CMAC_FINISH.""")

# ==============================================================================
# SLIDE 14: PHASE 4: BLOCK CMAC GENERATION & MULTI-BLOCK LOOP
# ==============================================================================
slide14 = prs.slides.add_slide(blank_layout)
add_header(slide14, "Phase 4: Block CMAC Generation & Multi-Block Loop", "8. Detailed Flow", "States: CMAC_FINISH -> CMAC_WRITE -> Next Block Iteration")
add_footer(slide14, 14, TOTAL_SLIDES)

c_cmac = create_card(slide14, Inches(0.8), Inches(1.65), Inches(5.8), Inches(5.1), C_BG_CARD, C_BORDER_CARD)
tf_cmac = c_cmac.text_frame
tf_cmac.word_wrap = True
p = tf_cmac.paragraphs[0]
p.text = "BLOCK CMAC LIFECYCLE"
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = C_NAVY_DARK
p.space_after = Pt(6)

items_cmac = [
    ("State CMAC_FINISH (Line 676)", "Calls Csm_MacGenerate(FINISH) with NULL input to finalize the 16-byte MAC tag into CMAC_array[16]."),
    ("State CMAC_WRITE (Line 826)", "Dispatches SF_DATA_TRANSFER to write CMAC_array to serial flash at block_cmac_addr_reference."),
    ("Multi-Block Evaluation", "Checks last_block_cmac flag:\n• If more blocks exist: increments block_cmac_addr_reference by SF_PAGE_SIZE and returns to PF_ADDR_HANDLE for next block.\n• If last block complete: sets backup_flag = NO_REQUEST and triggers the Metadata State Machine!"),
    ("Error Trapping", "If serial flash state reports SF_REQUEST_FAIL during CMAC write, logs error 0x11/0x12 and jumps to BACKUP_RETRY.")
]
add_bullet_list(tf_cmac, items_cmac, font_size=8.5, space_after=4)

c_vis = create_card(slide14, Inches(6.9), Inches(1.65), Inches(5.6), Inches(5.1), C_PURPLE_LIGHT, C_PURPLE, border_width=1.5)
tf_v = c_vis.text_frame
tf_v.word_wrap = True
p = tf_v.paragraphs[0]
p.text = "BLOCK CMAC STORAGE ARCHITECTURE"
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = C_PURPLE
p.space_after = Pt(6)

items_v = [
    ("Independent Block MACs", "Each ODX-F block receives its own distinct 16-byte CMAC signature covering its segments and uncompressed data."),
    ("Reference Address Pre-calculation", "block_cmac_addr_reference was pre-computed during metadata_extract() to prevent memory overlaps."),
    ("Block Progression", "Block 0 CMAC -> Block 1 CMAC -> ... -> Block N CMAC."),
    ("Transition to Metadata Pipeline", "When last block CMAC is confirmed written to flash:\n• blk_index and seg_index reset to 0\n• backup_metadata_flag = METADATA_CMAC_START\n• data_transfer_info.source_address_pf = METADATA_REF_ADDRESS")
]
add_bullet_list(tf_v, items_v, font_size=8.5, space_after=4)

set_speaker_notes(slide14,
"""KEY TALKING POINTS FOR SLIDE 14:
- Open code.txt at line 676 (CMAC_FINISH) and line 826 (CMAC_WRITE).
- When the last page of a block has been written and verified:
  1. CMAC_FINISH calls Csm_MacGenerate with CRYPTO_OPERATIONMODE_FINISH. This completes the hash over all segment headers and chunk data for that entire block, producing a 16-byte MAC.
  2. In CMAC_WRITE, this 16-byte signature is written to serial flash at block_cmac_addr_reference.
- Multi-block iteration:
  If the calibration contains multiple blocks (e.g. Block 0, Block 1, Block 2), the scheduler increments block_cmac_addr_reference and returns to PF_ADDR_HANDLE to process the next block.
- Once all blocks are finished (last_block_cmac == 1):
  It resets blk_index = 0, seg_index = 0, and kicks off the Tier 2 Metadata State Machine:
  backup_metadata_flag = METADATA_CMAC_START.""")

# ==============================================================================
# SLIDE 15: PHASE 5: CSU METADATA STATE MACHINE
# ==============================================================================
slide15 = prs.slides.add_slide(blank_layout)
add_header(slide15, "Phase 5: CSU Metadata Sub-State Machine", "8. Detailed Flow", "Finalizing CSU table packaging, computing header CMAC, and flash writing")
add_footer(slide15, 15, TOTAL_SLIDES)

slide15.shapes.add_picture('trimmed_flow_schdlr_meta_p23.png', Inches(0.8), Inches(1.65), width=Inches(5.6))

c_meta = create_card(slide15, Inches(6.6), Inches(1.65), Inches(5.9), Inches(5.1), C_BG_CARD, C_BORDER_CARD)
tf_m = c_meta.text_frame
tf_m.word_wrap = True
p = tf_m.paragraphs[0]
p.text = "METADATA SUB-STATE MACHINE (backup_metadata_flag)"
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = C_NAVY_DARK
p.space_after = Pt(4)

items_meta_states = [
    ("METADATA_CMAC_START (Line 1082)", "Initializes CSM for metadata MAC generation (Csm_MacGenerate START). Transitions to METADATA_ARRAY_HANDLING."),
    ("METADATA_ARRAY_HANDLING (Line 947)", "Constructs backup_matadata_array[] by copying CSU fixed header, block count, segment counts, and addresses from csu_header_backup. Handles multi-page splitting."),
    ("METADATA_CMAC_UPDATE (Line 1126)", "Feeds populated metadata bytes into Csm_MacGenerate(UPDATE). Transitions to METADATA_WRITE or METADATA_CMAC_FINISH."),
    ("METADATA_CMAC_FINISH (Line 1225)", "Finalizes metadata CMAC tag and appends the 16-byte MAC to the metadata array. Transitions to METADATA_WRITE."),
    ("METADATA_WRITE (Line 1160)", "Dispatches SF_DATA_TRANSFER to write complete metadata + CMAC to SF_BACKUP_CSU_METADATA_STRUCTURE_START. On completion -> BACKUP_COMPLETE!")
]
add_bullet_list(tf_m, items_meta_states, font_size=8, space_after=3)

set_speaker_notes(slide15,
"""KEY TALKING POINTS FOR SLIDE 15:
- Open code.txt at line 939 (switch(backup_metadata_flag)).
- Refer to Figure 8.4.3-2 on page 23 of the SDD.
- Why does metadata have its own sub-state machine?
  Because the metadata header contains the master directory of all blocks, addresses, and sizes.
  If the metadata header is corrupted, the ECU cannot parse the backup.
  Therefore, the metadata itself must be assembled, signed with a dedicated CMAC, and written to the designated start of the backup region.
- Follow the sequence:
  1. METADATA_CMAC_START initializes the CSM MAC generator.
  2. METADATA_ARRAY_HANDLING populates backup_matadata_array from csu_header_backup.
  3. METADATA_CMAC_UPDATE hashes the metadata array.
  4. METADATA_CMAC_FINISH generates the final 16-byte MAC and appends it to the trailer.
  5. METADATA_WRITE programs the entire metadata array to serial flash.
- When write completes, it sets backup_flag = BACKUP_COMPLETE!""")

# ==============================================================================
# SLIDE 16: PHASE 6: BACKUP COMPLETION & NVRAM PERSISTENCE
# ==============================================================================
slide16 = prs.slides.add_slide(blank_layout)
add_header(slide16, "Phase 6: Completion & NVRAM Persistence", "8. Detailed Flow", "State: BACKUP_COMPLETE, Status updates, and NvM commit")
add_footer(slide16, 16, TOTAL_SLIDES)

c_comp = create_card(slide16, Inches(0.8), Inches(1.65), Inches(5.8), Inches(5.1), C_GREEN_LIGHT, C_GREEN, border_width=1.5)
tf_comp = c_comp.text_frame
tf_comp.word_wrap = True
p = tf_comp.paragraphs[0]
p.text = "STATE: BACKUP_COMPLETE (Line 905)"
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = C_GREEN
p.space_after = Pt(6)

items_comp = [
    ("Serial Flash Status Polling", "Verifies GetSerialFlashState() == SF_REQUEST_COMPLETE before committing final status."),
    ("Status Transition: BACKUP_COMPLT_VALID", "Updates NVM_Back_up_status = BACKUP_COMPLT_VALID (Satisfies Requirement 13738925)."),
    ("Portover Status Reset", "Resets nvrPortOverstatus to PORTOVER_DEFAULT to indicate that post-portover actions are finalized."),
    ("State Machine Reset", "Sets backup_flag = NO_REQUEST and clears internal counters."),
    ("Persistent Flag Trigger", "Sets NvM_backup_update = TRUE to trigger atomic NVRAM write.")
]
add_bullet_list(tf_comp, items_comp, font_size=8.5, space_after=4)

c_nvm_sync = create_card(slide16, Inches(6.9), Inches(1.65), Inches(5.6), Inches(5.1), C_BG_CARD, C_BORDER_CARD)
tf_ns = c_nvm_sync.text_frame
tf_ns.word_wrap = True
p = tf_ns.paragraphs[0]
p.text = "NVRAM COMMIT & ERROR RECOVERY (Line 1253)"
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = C_NAVY_DARK
p.space_after = Pt(6)

items_ns = [
    ("Deferred Write Mechanism", "To prevent blocking the 10ms scheduler, NvM writes are managed via the NvM_backup_update flag."),
    ("NvM_GetErrorStatus Check", "Scheduler polls NvM_GetErrorStatus(NvMConf_NvMBlockDescriptor_NvbswcBootSharedBootSharedFBLGeneral, &NvM_Error_status)."),
    ("NvM_WriteBlock Dispatch", "If NvM is idle (E_OK), dispatches NvM_WriteBlock and clears NvM_backup_update = FALSE."),
    ("Resilient across Power Cuts", "Because the status is persistently recorded in NVRAM, subsequent ECU key cycles know that a valid, verified backup exists.")
]
add_bullet_list(tf_ns, items_ns, font_size=8.5, space_after=4)

set_speaker_notes(slide16,
"""KEY TALKING POINTS FOR SLIDE 16:
- Open code.txt at line 905 (BACKUP_COMPLETE) and line 1253 (NvM update block).
- When the metadata write completes successfully:
  1. The scheduler transitions into BACKUP_COMPLETE.
  2. It checks GetSerialFlashState(). If complete, it sets:
     NVM_Back_up_status = BACKUP_COMPLT_VALID (Req 13738925).
  3. It resets portover status:
     Rte_Write_nvwPortOverstatus_nvdVal(PORTOVER_DEFAULT).
  4. It flags NvM_backup_update = TRUE.
- Look at lines 1253-1272 at the end of reCddTeleBackupSchdlr:
  Every 10ms tick, it checks if NvM_backup_update == TRUE.
  It queries NvM_GetErrorStatus. If the NvM subsystem is ready, it fires NvM_WriteBlock for NvbswcBootSharedBootSharedFBLGeneral and resets the update flag.
  This guarantees safe, non-blocking NVRAM persistence!""")

# ==============================================================================
# SLIDE 17: RUNTIME SEQUENCE DIAGRAM
# ==============================================================================
slide17 = prs.slides.add_slide(blank_layout)
add_header(slide17, "Runtime Sequence Diagram", "9. Runtime Sequence", "End-to-end execution chronology across OS, CDD, CSM, Serial Flash & NvM")
add_footer(slide17, 17, TOTAL_SLIDES)

slide17.shapes.add_picture('diag_sequence.png', Inches(0.8), Inches(1.65), width=Inches(11.733))

set_speaker_notes(slide17,
"""KEY TALKING POINTS FOR SLIDE 17:
- Refer to Figure 8-2-1 from Section 8.2 of the SDD.
- Here is the complete end-to-end interaction sequence:
  1. OS Task fires the 10ms timing event into reCddTeleBackupSchdlr.
  2. CDDTeleBackupMngr issues SF_FULL_ERASE to vMemAccM / Serial Flash and waits for completion.
  3. CDD calls CSM to generate a random 16-byte IV and sets keys valid.
  4. CDD feeds the 8-byte Big-Endian segment descriptor into CSM CMAC (UPDATE).
  5. CDD encrypts 256-byte chunks with AES-128-CBC and updates CMAC.
  6. CDD writes the encrypted page to Serial Flash via SF_PAGE_WRITE.
  7. CDD reads back the page via SF_PAGE_READ and performs byte-by-byte comparison.
  8. Once all segments in a block are written, CSM produces the 16-byte block CMAC, which is stored in Serial Flash.
  9. CDD packages the metadata header, signs it with metadata CMAC, and writes it to flash.
  10. Finally, CDD invokes NvM_WriteBlock to record BACKUP_COMPLT_VALID.""")

# ==============================================================================
# SLIDE 18: FAULT TOLERANCE, RETRY MECHANISM & CYBERSECURITY LOGGING
# ==============================================================================
slide18 = prs.slides.add_slide(blank_layout)
add_header(slide18, "Fault Tolerance & Cybersecurity Event Logging", "10. Error Handling", "3-attempt retry loop, permanent failure recovery, and cybersecurity audit trails")
add_footer(slide18, 18, TOTAL_SLIDES)

c_retry = create_card(slide18, Inches(0.8), Inches(1.65), Inches(5.8), Inches(5.1), C_RED_LIGHT, C_RED_ACCENT, border_width=1.5)
tf_ret = c_retry.text_frame
tf_ret.word_wrap = True
p = tf_ret.paragraphs[0]
p.text = "STATE: BACKUP_RETRY (Line 881)"
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = C_RED_ACCENT
p.space_after = Pt(6)

items_ret = [
    ("Failure Trigger Sources", "Transitions to BACKUP_RETRY from:\n• Serial Flash driver errors (SF_REQUEST_FAIL)\n• CSM crypto errors (E_NOT_OK)\n• Hardware read-back verification byte mismatches!"),
    ("Attempt Counter", "backup_attempts counter increments on each failure entry."),
    ("Attempts <= 3 (Transient Failure)", "Satisfies Requirement 13594046:\n• Loops back to BACKUP_FULL_ERASE to completely wipe Serial Flash and re-execute entire backup pipeline from scratch!"),
    ("Attempts > 3 (Permanent Failure)", "Exhaustion of retries declares backup failure:\n• Sets NVM_Back_up_status = BACKUP_FAILED\n• Sets NvM_backup_update = TRUE to persist failed state\n• Transitions backup_flag = NO_REQUEST.")
]
add_bullet_list(tf_ret, items_ret, font_size=8.5, space_after=4)

c_cyber = create_card(slide18, Inches(6.9), Inches(1.65), Inches(5.6), Inches(5.1), C_BG_CARD, C_BORDER_CARD)
tf_cyb = c_cyber.text_frame
tf_cyb.word_wrap = True
p = tf_cyb.paragraphs[0]
p.text = "CYBERSECURITY EVENT LOGGING (CR#17113464)"
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = C_NAVY_DARK
p.space_after = Pt(6)

items_cyb = [
    ("Regulatory Compliance", "Complies with UNECE R155 & ISO/SAE 21434 automotive cybersecurity audit requirements for software update failures."),
    ("RTE Client/Server Call", "Rte_Call_ppLogCSEvent_LogEvent((uint8)UPDATE_FAILURE, &Update_Failure_ReasonCode[0], 0xFFu, 0xFFu)"),
    ("Reason Codes", "Update_Failure_ReasonCode[2] = {13, 67} (Hex: 0x0D, 0x43) specifically identifying backup flash/crypto failure."),
    ("Next Key Cycle Recovery", "Per Req 13594046: On the next ignition key cycle, reInitCDDTeleBackupMngr detects BACKUP_FAILED and automatically triggers a fresh backup attempt!")
]
add_bullet_list(tf_cyb, items_cyb, font_size=8.5, space_after=4)

set_speaker_notes(slide18,
"""KEY TALKING POINTS FOR SLIDE 18:
- Open code.txt at line 881: case (BACKUP_RETRY).
- Fault tolerance is governed by Requirement 13594046:
  "If the backup is interrupted, the ECU shall immediately retry the operation for three times. If it fails after three attempts, set NVM_Back_up_status to BACKUP_FAILED."
- How it works:
  - Any error (flash failure, crypto error, or verification mismatch) increments backup_attempts.
  - If attempts <= 3: It jumps back to BACKUP_FULL_ERASE. This completely wipes the backup flash area and re-runs the entire pipeline cleanly.
  - If attempts > 3:
    1. Sets NVM_Back_up_status = BACKUP_FAILED.
    2. Calls Rte_Call_ppLogCSEvent_LogEvent with EventType UPDATE_FAILURE (2U) and ReasonCode {13, 67}.
    3. Persists this failure to NvM.
- Auto-recovery on next key cycle:
  Notice what happens in reInitCDDTeleBackupMngr (Line 158):
  If (NVM_Back_up_status == BACKUP_FAILED), it sets BACKUP_IN_PROGRESS upon reboot to try again!""")

# ==============================================================================
# SLIDE 19: DEBUG INSTRUMENTATION & ERROR CODES
# ==============================================================================
slide19 = prs.slides.add_slide(blank_layout)
add_header(slide19, "Debug Instrumentation & Diagnostics Support", "11. Debugging", "Live runtime inspection structures, build switches, and diagnostic error codes")
add_footer(slide19, 19, TOTAL_SLIDES)

c_dbg = create_card(slide19, Inches(0.8), Inches(1.65), Inches(5.8), Inches(5.1), C_BG_CARD, C_BORDER_CARD)
tf_d = c_dbg.text_frame
tf_d.word_wrap = True
p = tf_d.paragraphs[0]
p.text = "DEBUG STRUCTURE: tele_dbg_backup_t"
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = C_NAVY_DARK
p.space_after = Pt(6)

items_dbg = [
    ("Build Switch DBG_TELE_CSU_BACKUP", "When set to STD_ON, enables real-time diagnostic recording without incurring production overhead."),
    ("sm_backup_event_flag", "Tracks the active state of the primary backup state machine (e.g. BACKUP_FULL_ERASE, WRITE_TO_SF)."),
    ("sm_metadata_process_flag", "Tracks the active state of the metadata sub-state machine."),
    ("sf_reference_addr & pf_read_addr", "Records current Serial Flash translated write pointer and Program Flash read address."),
    ("blk_index & seg_index", "Exposes current ODX-F block and segment indices for live debugger inspection.")
]
add_bullet_list(tf_d, items_dbg, font_size=8.5, space_after=4)

c_err = create_card(slide19, Inches(6.9), Inches(1.65), Inches(5.6), Inches(5.1), C_BG_CARD, C_BORDER_CARD)
tf_e = c_err.text_frame
tf_e.word_wrap = True
p = tf_e.paragraphs[0]
p.text = "DIAGNOSTIC ERROR CODE REFERENCE"
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = C_NAVY_DARK
p.space_after = Pt(6)

items_err = [
    ("0x01 / 0x02", "Serial Flash Full Erase request failure (current / previous request error)."),
    ("0x03 / 0x04", "CSM Random IV Generation error / Key Element Set failure."),
    ("0x05 / 0x06", "AES-128 Encryption Start failure / CMAC Start failure."),
    ("0x07 / 0x08", "Segment Start Handle CMAC error / Cyber Update Encrypt error."),
    ("0x0F / 0x10", "WRITE_TO_SF serial flash write transfer failure."),
    ("0x1C", "BACKUP_READ_SF_DATA read command dispatch failure."),
    ("0x1D", "HARDWARE VERIFICATION MISMATCH (Read data != Encrypted data)."),
    ("0x11 / 0x12", "CMAC_WRITE block MAC write failure."),
    ("0x13", "Retry counter exhausted (> 3 attempts) -> BACKUP_FAILED.")
]
add_bullet_list(tf_e, items_err, font_size=8.5, space_after=3)

set_speaker_notes(slide19,
"""KEY TALKING POINTS FOR SLIDE 19:
- Open code.txt and search for tele_dbg_backup.
- The module includes comprehensive debug instrumentation enabled via DBG_TELE_CSU_BACKUP == STD_ON.
- In INCA, CANape, or Lauterbach Trace32, engineers can inspect tele_dbg_backup in real time:
  - You can view the current state of both state machines.
  - You can see the exact PF read address and SF write address.
  - If a backup fails, tele_backup_error_code tells you the exact root cause:
    - 0x01/0x02: Flash erase failure.
    - 0x0F/0x10: Page write failure.
    - 0x1D: Data verification mismatch (data read from flash did not match what was written).
    - 0x13: All 3 retries exhausted.
- This makes bench testing and field issue triage exceptionally fast.""")

# ==============================================================================
# SLIDE 20: REQUIREMENTS TRACEABILITY MATRIX
# ==============================================================================
slide20 = prs.slides.add_slide(blank_layout)
add_header(slide20, "Requirements Traceability Matrix", "12. Verification & Quality", "Direct alignment between Integrity Requirement IDs and implementation code")
add_footer(slide20, 20, TOTAL_SLIDES)

c_rtm = create_card(slide20, Inches(0.8), Inches(1.65), Inches(11.733), Inches(5.1), C_BG_CARD, C_BORDER_CARD)
tf_rtm = c_rtm.text_frame
tf_rtm.word_wrap = True
p = tf_rtm.paragraphs[0]
p.text = "INTEGRITY REQUIREMENT TRACING (Document ID: 9167284)"
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = C_NAVY_DARK
p.space_after = Pt(6)

rtm_items = [
    ("Req 13584655", "Copy calibration from Program Flash, encrypt it, and write to Serial Flash.", "Satisfied by reCddTeleBackupSchdlr (CYBER_UPDATE & WRITE_TO_SF)."),
    ("Req 13584660", "ECM shall start backup whenever new ECM cal/software is flashed.", "Satisfied by reInitCDDTeleBackupMngr & reCddTeleBackupSchdlr."),
    ("Req 13584666", "ECM shall read Program Flash as per ODX-F block/segment structure.", "Satisfied by metadata_extract & PF_ADDR_HANDLE."),
    ("Req 13584663", "ECM shall store backup cals on Serial Flash memory.", "Satisfied by WRITE_TO_SF and SerialFlashGetServ API."),
    ("Req 13738939", "ECM shall calculate CMAC on Metadata and store at end of metadata.", "Satisfied by METADATA_CMAC_FINISH & METADATA_WRITE."),
    ("Req 13594046", "If interrupted, retry 3 times. On 3rd fail, set BACKUP_FAILED; retry on new key cycle.", "Satisfied by BACKUP_RETRY & reInitCDDTeleBackupMngr."),
    ("Req 13738925", "Once complete backup stored, set status to BACKUP_COMPLT_VALID.", "Satisfied by BACKUP_COMPLETE state."),
    ("Req 13738945", "CMAC calculated for each block, considering segment address & length in Big-Endian.", "Satisfied by SEG_START_HANDLE & CMAC_FINISH."),
    ("Req 18134113", "Disable Backup when CSU_Telematics_Feature_Enable is disabled.", "Satisfied by ppCSUFeatureEnbl check in all runnables.")
]
add_bullet_list(tf_rtm, rtm_items, font_size=8, space_after=3)

set_speaker_notes(slide20,
"""KEY TALKING POINTS FOR SLIDE 20:
- Section 6 of the SDD details requirement tracing.
- Every single requirement from Integrity document 9167284 is verified and mapped:
  - Requirement 13584655: Core backup encryption.
  - Requirement 13584660: Automatic trigger upon remote cal download.
  - Requirement 13584666: ODX-F block and segment adherence.
  - Requirement 13594046: 3-attempt retry loop and next key cycle recovery.
  - Requirement 13738925: BACKUP_COMPLT_VALID status update.
  - Requirement 13738945: Big-Endian segment header inclusion in CMAC.
  - Requirement 18134113: CSU Master Feature enable gating.
- This provides full audit readiness for software releases.""")

# ==============================================================================
# SLIDE 21: PRESENTER'S CODE WALKTHROUGH GUIDE
# ==============================================================================
slide21 = prs.slides.add_slide(blank_layout)
add_header(slide21, "Presenter's Code Walkthrough Guide", "13. Code Walkthrough", "Roadmap for explaining CDDTeleBackupMngr.c line-by-line during the live session")
add_footer(slide21, 21, TOTAL_SLIDES)

c_cw1 = create_card(slide21, Inches(0.8), Inches(1.65), Inches(5.8), Inches(5.1), C_BG_CARD, C_BORDER_CARD)
tf_cw1 = c_cw1.text_frame
tf_cw1.word_wrap = True
p = tf_cw1.paragraphs[0]
p.text = "CODE SECTION MAP (CDDTeleBackupMngr.c)"
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = C_NAVY_DARK
p.space_after = Pt(6)

items_cw1 = [
    ("Lines 1 - 137: Includes & Static Globals", "Header inclusions (Rte, Csm, NvM), buffer definitions (Mem_Read_Buff, backup_encrypt_data, CMAC_array), reason codes, and NvM status variables."),
    ("Lines 138 - 248: reInitCDDTeleBackupMngr()", "Boot runnable. Walk through port reads, CSU_feature_enable check, rollback timer arming branch, and NvM_WriteBlock call."),
    ("Lines 249 - 340: reCddTeleBackupSchdlr() Entry", "Scheduler header, local static flags, CSU gate check, NO_REQUEST, and BACKUP_FULL_ERASE."),
    ("Lines 341 - 580: Addressing & Crypto Init", "PF_ADDR_HANDLE, SET_KEYS, ENCRYPT_START, CMAC_START, and SEG_START_HANDLE (point out Big-Endian conversion).")
]
add_bullet_list(tf_cw1, items_cw1, font_size=8.5, space_after=4)

c_cw2 = create_card(slide21, Inches(6.9), Inches(1.65), Inches(5.6), Inches(5.1), C_BG_CARD, C_BORDER_CARD)
tf_cw2 = c_cw2.text_frame
tf_cw2.word_wrap = True
p = tf_cw2.paragraphs[0]
p.text = "CODE SECTION MAP (CONTINUED)"
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = C_NAVY_DARK
p.space_after = Pt(6)

items_cw2 = [
    ("Lines 581 - 825: Chunk Processing & Verify", "CYBER_UPDATE, ENCRYPT_FINISH, WRITE_TO_SF, and BACKUP_READ_SF_DATA (highlight byte-by-byte memcmp verification loop)."),
    ("Lines 826 - 938: Block CMAC & Completion", "CMAC_WRITE, BACKUP_RETRY (show attempt counter & ppLogCSEvent), and BACKUP_COMPLETE."),
    ("Lines 939 - 1250: Metadata State Machine", "switch(backup_metadata_flag), METADATA_ARRAY_HANDLING, and METADATA_WRITE."),
    ("Lines 1251 - 1325: Deferred NvM Commit", "NvM_backup_update polling and NvM_WriteBlock execution."),
    ("Lines 1326 - 1376: reTeleRollBackTimeCheck()", "5-second periodic timer countdown and caTeleRollBackTimer comparison."),
    ("Lines 1377 - 1437: metadata_extract()", "Table traversal, length calculation, and CMAC reference address offset.")
]
add_bullet_list(tf_cw2, items_cw2, font_size=8.5, space_after=3)

set_speaker_notes(slide21,
"""GUIDE FOR PRESENTER DURING LIVE CODE WALKTHROUGH:
Now that we have covered the conceptual architecture and state flows, let's switch over to the actual source file (CDDTeleBackupMngr.c):
1. Start at Line 1: Show the static declarations, especially Mem_Read_Buff, backup_encrypt_data, and Backup_Cipher_IV.
2. Jump to Line 138: Explain reInitCDDTeleBackupMngr. Point out how it reads portover status and arms the rollback timer.
3. Jump to Line 249: Show the 10ms scheduler. Walk through the switch(backup_flag) cases in sequence:
   - Line 299: BACKUP_FULL_ERASE
   - Line 342: PF_ADDR_HANDLE
   - Line 549: SEG_START_HANDLE (show the Big-Endian seg_info array!)
   - Line 581: CYBER_UPDATE
   - Line 740: BACKUP_READ_SF_DATA (show the memcmp verification!)
   - Line 826: CMAC_WRITE
   - Line 881: BACKUP_RETRY and the cybersecurity event logging call.
4. Jump to Line 939: Show the metadata switch statement.
5. Jump to Line 1326: Walk through reTeleRollBackTimeCheck and the 5-second tick logic.
6. Finish at Line 1377: Walk through metadata_extract and how block_cmac_addr_reference is calculated.""")

# ==============================================================================
# SLIDE 22: CONCLUSION, SUMMARY & Q&A
# ==============================================================================
slide22 = prs.slides.add_slide(blank_layout)
add_header(slide22, "Summary & Open Q&A Session", "14. Conclusion", "Key architectural takeaways and open discussion")
add_footer(slide22, 22, TOTAL_SLIDES)

c_sum = create_card(slide22, Inches(0.8), Inches(1.65), Inches(7.5), Inches(5.1), C_BG_CARD, C_BORDER_CARD)
tf_s = c_sum.text_frame
tf_s.word_wrap = True
p = tf_s.paragraphs[0]
p.text = "KEY ARCHITECTURAL TAKEAWAYS"
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = C_NAVY_DARK
p.space_after = Pt(6)

items_sum = [
    ("Autonomous BSW CDD", "Encapsulates the entire calibration backup lifecycle without imposing overhead or blocking application tasks."),
    ("Multi-Layered Security", "Combines AES-128-CBC confidentiality, Big-Endian segment CMAC binding, and dedicated metadata signing."),
    ("Hardware-Level Verification", "Guarantees data integrity by reading back and verifying every single written page from physical flash."),
    ("Robust Fault Tolerance", "Automated 3-attempt retry loop with full chip re-erase, UNECE-compliant cybersecurity event logging, and reboot recovery."),
    ("Clean AUTOSAR Integration", "Seamlessly integrates with RTE, CSM, NvM, and memory drivers while providing full calibration flexibility.")
]
add_bullet_list(tf_s, items_sum, font_size=8.5, space_after=5)

c_qa = create_card(slide22, Inches(8.5), Inches(1.65), Inches(4.0), Inches(5.1), C_TEAL_LIGHT, C_TEAL, border_width=1.5)
tf_q = c_qa.text_frame
tf_q.word_wrap = True
p = tf_q.paragraphs[0]
p.text = "QUESTIONS & DISCUSSION"
p.font.size = Pt(12)
p.font.bold = True
p.font.color.rgb = C_NAVY_DARK
p.space_after = Pt(8)

items_qa = [
    ("Open Discussion Topics", ""),
    ("Timing Constraints", "Impact of 10ms scheduler rate on total flash backup duration."),
    ("Calibration Tuning", "Adjusting caTeleRollBackTimer for specific fleet operating profiles."),
    ("CSM Hardware Acceleration", "Crypto throughput on TC3xx HSM vs Software CSM."),
    ("Diagnostics Integration", "Live debugging via tele_dbg_backup in calibration tools.")
]
add_bullet_list(tf_q, items_qa, font_size=8.5, space_after=4)

set_speaker_notes(slide22,
"""CLOSING & Q&A SESSION:
- Thank you for your time and engagement during this Knowledge Transfer session on CDDTeleBackupMngr.
- To summarize: CDDTeleBackupMngr provides a robust, encrypted, verified rollback vault for remote calibration downloads under Cummins CSAR.
- The presentation slides and reference documents are available in the repository.
- We will now open the floor for any technical questions, timing considerations, or implementation queries.""")

# Save Presentation
output_pptx = "CDDTeleBackupMngr_KT_Presentation.pptx"
prs.save(output_pptx)
print(f"Successfully generated {output_pptx} with {len(prs.slides)} slides!")
