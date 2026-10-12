import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['figure.dpi'] = 300

def create_init_flowchart():
    fig, ax = plt.subplots(figsize=(10, 7.5))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    fig.patch.set_facecolor('#FFFFFF')

    # Title
    ax.text(50, 96, "Initialization Flow: reInitCDDTeleBackupMngr()", 
            ha='center', va='center', fontsize=14, fontweight='bold', color='#0B2545')
    ax.text(50, 92.5, "Executed once at ECU boot after RTE start to restore state & initialize backup triggers", 
            ha='center', va='center', fontsize=9, color='#475569')

    # 1. Start Node
    ax.add_patch(patches.FancyBboxPatch((40, 83), 20, 5.5, boxstyle="round,pad=0.3", fc='#0B2545', ec='#0B2545'))
    ax.text(50, 85.7, "START (ECU Boot)", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#FFFFFF')

    # 2. Read NVM & Port states
    ax.add_patch(patches.FancyBboxPatch((15, 71), 70, 8, boxstyle="round,pad=0.4", fc='#F1F5F9', ec='#64748B', lw=1.2))
    ax.text(50, 75, "Read Port & NVM States via RTE Explicit S/R API:\n• nvrPortOverstatus • ppToolConnectedProg (new_cal_download) • nvrBackupStatus\n• nvrRollBackTimerStatus • ppCSUFeatureEnbl", 
            ha='center', va='center', fontsize=8, color='#0F172A')

    # 3. Decision: CSU_feature_enable == TRUE?
    ax.add_patch(patches.Polygon([[50, 67], [70, 60], [50, 53], [30, 60]], fc='#FEF3C7', ec='#D97706', lw=1.5))
    ax.text(50, 60, "CSU Feature\nEnabled?", ha='center', va='center', fontsize=8.5, fontweight='bold', color='#92400E')

    # No branch -> Disable
    ax.add_patch(patches.FancyBboxPatch((78, 56), 20, 8, boxstyle="round,pad=0.3", fc='#FEE2E2', ec='#DC2626', lw=1.2))
    ax.text(88, 60, "NVM_Back_up_status =\nCSU_FEATURE_DISABLE", ha='center', va='center', fontsize=7.5, fontweight='bold', color='#991B1B')

    # Decision 2: Portover complete & Timer not active?
    ax.add_patch(patches.Polygon([[50, 48], [72, 40], [50, 32], [28, 40]], fc='#E0E7FF', ec='#4338CA', lw=1.5))
    ax.text(50, 40, "Portover Complete &\nTimer Inactive?", ha='center', va='center', fontsize=8, fontweight='bold', color='#3730A3')

    # Yes branch -> Arm Timer
    ax.add_patch(patches.FancyBboxPatch((2, 36), 22, 8, boxstyle="round,pad=0.3", fc='#DCFCE7', ec='#16A34A', lw=1.2))
    ax.text(13, 40, "Arm Rollback Timer:\n• Rollback_timer_status = 1\n• TeleRollBackTimeOut = 0", 
            ha='center', va='center', fontsize=7.5, fontweight='bold', color='#166534')

    # Decision 3: new_cal_download == 1 OR BACKUP_FAILED?
    ax.add_patch(patches.Polygon([[50, 27], [72, 20], [50, 13], [28, 20]], fc='#EDE9FE', ec='#7C3AED', lw=1.5))
    ax.text(50, 20, "New Cal Downloaded OR\nStatus == BACKUP_FAILED?", ha='center', va='center', fontsize=7.5, fontweight='bold', color='#5B21B6')

    # Yes branch -> BACKUP_IN_PROGRESS
    ax.add_patch(patches.FancyBboxPatch((2, 16), 22, 8, boxstyle="round,pad=0.3", fc='#FEF9C3', ec='#CA8A04', lw=1.2))
    ax.text(13, 20, "Trigger Backup:\nNVM_Back_up_status =\nBACKUP_IN_PROGRESS", ha='center', va='center', fontsize=7.5, fontweight='bold', color='#854D0E')

    # 4. Final NvM Write Block
    ax.add_patch(patches.FancyBboxPatch((25, 2), 50, 7, boxstyle="round,pad=0.4", fc='#0B2545', ec='#00A896', lw=1.5))
    ax.text(50, 5.5, "Update NVRAM: Write nvwBackupStatus & Call NvM_WriteBlock()\n(If write fails, set NvM_backup_update = TRUE for retry)", 
            ha='center', va='center', fontsize=8, fontweight='bold', color='#FFFFFF')

    # Arrows
    arr = dict(arrowstyle="->", lw=1.3, color="#334155")
    # Start -> Read
    ax.annotate("", xy=(50, 79), xytext=(50, 83), arrowprops=arr)
    # Read -> Dec 1
    ax.annotate("", xy=(50, 67), xytext=(50, 71), arrowprops=arr)
    # Dec 1 NO -> Disable
    ax.annotate("", xy=(78, 60), xytext=(70, 60), arrowprops=arr)
    ax.text(73, 61.5, "No", fontsize=8, color='#DC2626', fontweight='bold')
    # Dec 1 YES -> Dec 2
    ax.annotate("", xy=(50, 48), xytext=(50, 53), arrowprops=arr)
    ax.text(51.5, 50.5, "Yes", fontsize=8, color='#16A34A', fontweight='bold')
    # Dec 2 YES -> Arm Timer
    ax.annotate("", xy=(24, 40), xytext=(28, 40), arrowprops=arr)
    ax.text(25.5, 41.5, "Yes", fontsize=8, color='#16A34A', fontweight='bold')
    # Dec 2 NO -> Dec 3
    ax.annotate("", xy=(50, 27), xytext=(50, 32), arrowprops=arr)
    ax.text(51.5, 29.5, "No", fontsize=8, color='#DC2626', fontweight='bold')
    # Dec 3 YES -> Trigger Backup
    ax.annotate("", xy=(24, 20), xytext=(28, 20), arrowprops=arr)
    ax.text(25.5, 21.5, "Yes", fontsize=8, color='#16A34A', fontweight='bold')
    # Dec 3 NO -> NvM Write
    ax.annotate("", xy=(50, 9), xytext=(50, 13), arrowprops=arr)
    ax.text(51.5, 11, "No", fontsize=8, color='#64748B')
    # Routes to bottom
    ax.annotate("", xy=(88, 9), xytext=(88, 56), arrowprops=dict(arrowstyle="->", lw=1.2, color="#DC2626", ls=':'))
    ax.annotate("", xy=(13, 9), xytext=(13, 16), arrowprops=dict(arrowstyle="->", lw=1.2, color="#CA8A04", ls=':'))
    ax.annotate("", xy=(13, 24), xytext=(13, 36), arrowprops=dict(arrowstyle="->", lw=1.2, color="#16A34A", ls=':'))

    plt.tight_layout()
    plt.savefig('diag_init_flowchart.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Generated diag_init_flowchart.png")

def create_rollback_flowchart():
    fig, ax = plt.subplots(figsize=(9, 6.8))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    fig.patch.set_facecolor('#FFFFFF')

    # Title
    ax.text(50, 96, "Rollback Timer Management: reTeleRollBackTimeCheck()", 
            ha='center', va='center', fontsize=13, fontweight='bold', color='#0B2545')
    ax.text(50, 92.5, "Triggered on TimingEvent every 5 seconds to manage the automatic backup countdown", 
            ha='center', va='center', fontsize=8.5, color='#475569')

    # 1. Start Node
    ax.add_patch(patches.FancyBboxPatch((35, 83), 30, 6, boxstyle="round,pad=0.3", fc='#0B2545', ec='#0B2545'))
    ax.text(50, 86, "Periodic Event (5s)", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#FFFFFF')

    # 2. Check Rollback Timer Active & CSU Feature Enabled
    ax.add_patch(patches.Polygon([[50, 78], [75, 69], [50, 60], [25, 69]], fc='#FEF3C7', ec='#D97706', lw=1.5))
    ax.text(50, 69, "Rollback_timer_status == TRUE\nAND CSU_feature_enable == TRUE?", 
            ha='center', va='center', fontsize=7.8, fontweight='bold', color='#92400E')

    # False branch
    ax.add_patch(patches.FancyBboxPatch((80, 66), 18, 6, boxstyle="round,pad=0.3", fc='#F1F5F9', ec='#94A3B8', lw=1.2))
    ax.text(89, 69, "NO ACTION\n(Exit Runnable)", ha='center', va='center', fontsize=7.5, color='#475569')

    # Read timeout
    ax.add_patch(patches.FancyBboxPatch((28, 48), 44, 7, boxstyle="round,pad=0.3", fc='#F8FAFC', ec='#64748B', lw=1.2))
    ax.text(50, 51.5, "Read TeleRollBackTimeOut from NVM", ha='center', va='center', fontsize=8.5, color='#0F172A')

    # Decision: Timeout >= caTeleRollBackTimer?
    ax.add_patch(patches.Polygon([[50, 43], [74, 35], [50, 27], [26, 35]], fc='#E0E7FF', ec='#4338CA', lw=1.5))
    ax.text(50, 35, "TeleRollBackTimeOut >=\ncaTeleRollBackTimer?", ha='center', va='center', fontsize=8, fontweight='bold', color='#3730A3')

    # Expired: Yes -> Start Backup
    ax.add_patch(patches.FancyBboxPatch((2, 22), 30, 10, boxstyle="round,pad=0.3", fc='#DCFCE7', ec='#16A34A', lw=1.5))
    ax.text(17, 27, "TIMER EXPIRED:\n• NVM_Back_up_status = BACKUP_IN_PROGRESS\n• Rollback_timer_status = 0 (Deactivate)", 
            ha='center', va='center', fontsize=7.5, fontweight='bold', color='#166534')

    # Not Expired: No -> Increment by 5s
    ax.add_patch(patches.FancyBboxPatch((68, 22), 30, 10, boxstyle="round,pad=0.3", fc='#FEF9C3', ec='#CA8A04', lw=1.5))
    ax.text(83, 27, "TIMER RUNNING:\n• TeleRollBackTimeOut += 5 seconds\n• Wait for next cycle", 
            ha='center', va='center', fontsize=7.5, fontweight='bold', color='#854D0E')

    # Writeback Node
    ax.add_patch(patches.FancyBboxPatch((22, 5), 56, 8, boxstyle="round,pad=0.4", fc='#0B2545', ec='#00A896', lw=1.5))
    ax.text(50, 9, "NVM Persistence:\nWrite nvwTeleRollBackTimeOut & call NvM_WriteBlock()\n(If write fails, set NvM_backup_update = TRUE)", 
            ha='center', va='center', fontsize=8, fontweight='bold', color='#FFFFFF')

    # Arrows
    arr = dict(arrowstyle="->", lw=1.3, color="#334155")
    ax.annotate("", xy=(50, 78), xytext=(50, 83), arrowprops=arr)
    ax.annotate("", xy=(80, 69), xytext=(75, 69), arrowprops=arr)
    ax.text(76, 70.5, "No", fontsize=8, color='#DC2626', fontweight='bold')
    ax.annotate("", xy=(50, 55), xytext=(50, 60), arrowprops=arr)
    ax.text(51.5, 57.5, "Yes", fontsize=8, color='#16A34A', fontweight='bold')
    ax.annotate("", xy=(50, 43), xytext=(50, 48), arrowprops=arr)
    ax.annotate("", xy=(32, 27), xytext=(26, 35), arrowprops=arr)
    ax.text(26, 32, "Yes", fontsize=8, color='#16A34A', fontweight='bold')
    ax.annotate("", xy=(68, 27), xytext=(74, 35), arrowprops=arr)
    ax.text(71, 32, "No", fontsize=8, color='#D97706', fontweight='bold')
    ax.annotate("", xy=(35, 13), xytext=(17, 22), arrowprops=arr)
    ax.annotate("", xy=(65, 13), xytext=(83, 22), arrowprops=arr)

    plt.tight_layout()
    plt.savefig('diag_rollback_flowchart.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Generated diag_rollback_flowchart.png")

def create_state_machine_diagram():
    fig, ax = plt.subplots(figsize=(12, 7.5))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    fig.patch.set_facecolor('#FFFFFF')

    ax.text(50, 97, "reCddTeleBackupSchdlr() - Master State Machine Pipeline", 
            ha='center', va='center', fontsize=14, fontweight='bold', color='#0B2545')
    ax.text(50, 93.5, "2-Tier Architecture: Primary Block/Segment Pipeline (15 States) & Metadata Trailer Pipeline (6 States)", 
            ha='center', va='center', fontsize=9, color='#475569')

    # Primary States Container
    ax.add_patch(patches.FancyBboxPatch((2, 38), 96, 52, boxstyle="round,pad=0.5", fc='#F8FAFC', ec='#0B2545', lw=1.8))
    ax.text(6, 87, "TIER 1: Primary Data State Machine (backup_flag)", fontsize=9.5, fontweight='bold', color='#0B2545')

    # State Boxes for Tier 1
    # Row 1: Erase & Preparation
    t1_states = [
        ("NO_REQUEST\n(Idle)", 5, 75, 12, 8, '#E2E8F0', '#475569'),
        ("BACKUP_FULL_ERASE\n(Erase SF Region)", 20, 75, 16, 8, '#FEE2E2', '#DC2626'),
        ("PF_ADDR_HANDLE\n(Calc next PF Addr)", 39, 75, 16, 8, '#E0E7FF', '#4338CA'),
        ("SET_KEYS\n(Load AES/CMAC Keys)", 58, 75, 16, 8, '#EDE9FE', '#7C3AED'),
        ("ENCRYPT_START\n(Init AES-128)", 77, 75, 14, 8, '#FEF3C7', '#D97706')
    ]

    for name, x, y, w, h, bg, border in t1_states:
        ax.add_patch(patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3", fc=bg, ec=border, lw=1.5))
        ax.text(x + w/2, y + h/2, name, ha='center', va='center', fontsize=7.2, fontweight='bold', color=border)

    # Row 2: Crypto Update & Transfer
    t2_states = [
        ("CMAC_START\n(Init MAC Gen)", 77, 62, 14, 8, '#FEF3C7', '#D97706'),
        ("SEG_START_HANDLE\n(CMAC Seg Descriptor)", 56, 62, 18, 8, '#EDE9FE', '#7C3AED'),
        ("CYBER_UPDATE\n(Encrypt & MAC Data)", 35, 62, 18, 8, '#DCFCE7', '#16A34A'),
        ("ENCRYPT_FINISH\n(Pad / Finalize AES)", 17, 62, 15, 8, '#FEF9C3', '#CA8A04'),
        ("WRITE_TO_SF\n(Write SF 256B Page)", 3, 62, 12, 8, '#E0E7FF', '#4338CA')
    ]

    for name, x, y, w, h, bg, border in t2_states:
        ax.add_patch(patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3", fc=bg, ec=border, lw=1.5))
        ax.text(x + w/2, y + h/2, name, ha='center', va='center', fontsize=7.2, fontweight='bold', color=border)

    # Row 3: Verification & CMAC Storage
    t3_states = [
        ("BACKUP_READ_SF_DATA\n(Read-Back & Verify)", 5, 48, 18, 8, '#CCFBF1', '#0F766E'),
        ("CMAC_FINISH\n(Finalize 16B CMAC)", 26, 48, 16, 8, '#EDE9FE', '#7C3AED'),
        ("CMAC_WRITE\n(Write Block CMAC)", 45, 48, 16, 8, '#DCFCE7', '#16A34A'),
        ("BACKUP_RETRY\n(Retry <= 3 / Failed)", 64, 48, 16, 8, '#FEE2E2', '#DC2626'),
        ("BACKUP_COMPLETE\n(Set NVM Status)", 83, 48, 14, 8, '#DCFCE7', '#15803D')
    ]

    for name, x, y, w, h, bg, border in t3_states:
        ax.add_patch(patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3", fc=bg, ec=border, lw=1.5))
        ax.text(x + w/2, y + h/2, name, ha='center', va='center', fontsize=7.2, fontweight='bold', color=border)

    # Tier 2: Metadata State Machine
    ax.add_patch(patches.FancyBboxPatch((2, 4), 96, 30, boxstyle="round,pad=0.5", fc='#F1F5F9', ec='#00A896', lw=1.8))
    ax.text(6, 30.5, "TIER 2: Metadata Sub-State Machine (backup_metadata_flag)", fontsize=9.5, fontweight='bold', color='#00A896')

    m_states = [
        ("METADATA_NO_REQ\n(Idle)", 4, 12, 14, 13, '#E2E8F0', '#475569'),
        ("METADATA_CMAC_START\n(Init CSM MAC)", 20, 12, 17, 13, '#EDE9FE', '#7C3AED'),
        ("METADATA_ARRAY_HANDLING\n(Extract CSU Table)", 39, 12, 17, 13, '#DCFCE7', '#16A34A'),
        ("METADATA_CMAC_UPDATE\n(Hash Metadata Array)", 58, 12, 17, 13, '#FEF3C7', '#D97706'),
        ("METADATA_CMAC_FINISH\n(Gen Trailer CMAC)", 77, 12, 15, 13, '#EDE9FE', '#7C3AED'),
        ("METADATA_WRITE\n(Write to Serial Flash)", 77, 3, 15, 7, '#CCFBF1', '#0F766E')
    ]

    for name, x, y, w, h, bg, border in m_states:
        ax.add_patch(patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3", fc=bg, ec=border, lw=1.2))
        ax.text(x + w/2, y + h/2, name, ha='center', va='center', fontsize=6.8, fontweight='bold', color=border)

    # Arrows for flow
    arr = dict(arrowstyle="->", lw=1.3, color="#1E293B")
    # T1 Row 1
    ax.annotate("", xy=(20, 79), xytext=(17, 79), arrowprops=arr)
    ax.annotate("", xy=(39, 79), xytext=(36, 79), arrowprops=arr)
    ax.annotate("", xy=(58, 79), xytext=(55, 79), arrowprops=arr)
    ax.annotate("", xy=(77, 79), xytext=(74, 79), arrowprops=arr)
    # T1 Row 1 -> Row 2
    ax.annotate("", xy=(84, 70), xytext=(84, 75), arrowprops=arr)
    # T1 Row 2
    ax.annotate("", xy=(74, 66), xytext=(77, 66), arrowprops=arr)
    ax.annotate("", xy=(53, 66), xytext=(56, 66), arrowprops=arr)
    ax.annotate("", xy=(32, 66), xytext=(35, 66), arrowprops=arr)
    ax.annotate("", xy=(15, 66), xytext=(17, 66), arrowprops=arr)
    # T1 Row 2 -> Row 3
    ax.annotate("", xy=(9, 56), xytext=(9, 62), arrowprops=arr)
    # T1 Row 3
    ax.annotate("", xy=(26, 52), xytext=(23, 52), arrowprops=arr)
    ax.annotate("", xy=(45, 52), xytext=(42, 52), arrowprops=arr)
    # Loop back from verify to PF_ADDR_HANDLE (next page)
    ax.annotate("", xy=(39, 76), xytext=(14, 56), arrowprops=dict(arrowstyle="->", lw=1.2, color="#2563EB", connectionstyle="arc3,rad=-0.3"))
    # CMAC Write to Metadata transition
    ax.annotate("", xy=(28, 25), xytext=(53, 48), arrowprops=dict(arrowstyle="->", lw=1.5, color="#00A896", ls='--', connectionstyle="arc3,rad=-0.2"))
    ax.text(42, 36, "Last Block CMAC Written\n-> Trigger Metadata CMAC", fontsize=7.5, fontweight='bold', color='#00A896')
    # Metadata complete to BACKUP_COMPLETE
    ax.annotate("", xy=(90, 48), xytext=(85, 10), arrowprops=dict(arrowstyle="->", lw=1.5, color="#15803D", ls='--', connectionstyle="arc3,rad=0.3"))

    plt.tight_layout()
    plt.savefig('diag_state_machine.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Generated diag_state_machine.png")

def create_crypto_pipeline_diagram():
    fig, ax = plt.subplots(figsize=(11, 6.2))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    fig.patch.set_facecolor('#FFFFFF')

    ax.text(50, 96, "Cryptographic Pipeline & Verification Flow (AES-128 & CMAC)", 
            ha='center', va='center', fontsize=13, fontweight='bold', color='#0B2545')
    ax.text(50, 92.5, "Confidentiality (AES Encryption), Authenticity (Block CMAC), and Hardware Verification", 
            ha='center', va='center', fontsize=8.5, color='#475569')

    # Step 1: IV Generation & Keys
    ax.add_patch(patches.FancyBboxPatch((3, 62), 21, 26, boxstyle="round,pad=0.4", fc='#EDE9FE', ec='#7C3AED', lw=1.5))
    ax.text(13.5, 84, "STEP 1: Key & IV Init", ha='center', va='center', fontsize=9, fontweight='bold', color='#5B21B6')
    ax.text(13.5, 73, "• Csm_RandomGenerate()\n  generates 16B IV\n• Csm_KeyElementSet()\n  loads key material\n• Csm_KeySetValid()\n  validates AES/CMAC key", 
            ha='center', va='center', fontsize=7.5, color='#4C1D95')

    # Step 2: Segment Header CMAC
    ax.add_patch(patches.FancyBboxPatch((27, 62), 21, 26, boxstyle="round,pad=0.4", fc='#FEF3C7', ec='#D97706', lw=1.5))
    ax.text(37.5, 84, "STEP 2: Segment CMAC", ha='center', va='center', fontsize=9, fontweight='bold', color='#92400E')
    ax.text(37.5, 73, "• ODX-F Segment Header:\n  [Addr: 4B | Size: 4B]\n• Formatted in Big-Endian\n• Fed into CMAC via\n  Csm_MacGenerate(UPDATE)\n  before segment data", 
            ha='center', va='center', fontsize=7.5, color='#78350F')

    # Step 3: Page Encryption & MAC
    ax.add_patch(patches.FancyBboxPatch((51, 62), 21, 26, boxstyle="round,pad=0.4", fc='#DCFCE7', ec='#16A34A', lw=1.5))
    ax.text(61.5, 84, "STEP 3: Chunk Processing", ha='center', va='center', fontsize=9, fontweight='bold', color='#166534')
    ax.text(61.5, 73, "• Plaintext read from PF\n  into Mem_Read_Buff (256B)\n• Csm_Encrypt(UPDATE)\n  AES-128-CBC encryption\n• Csm_MacGenerate(UPDATE)\n  CMAC calculated on plain", 
            ha='center', va='center', fontsize=7.5, color='#14532D')

    # Step 4: Write & Read Verification
    ax.add_patch(patches.FancyBboxPatch((75, 62), 22, 26, boxstyle="round,pad=0.4", fc='#CCFBF1', ec='#0F766E', lw=1.5))
    ax.text(86, 84, "STEP 4: Hardware Verify", ha='center', va='center', fontsize=9, fontweight='bold', color='#115E59')
    ax.text(86, 73, "• SF_PAGE_WRITE:\n  backup_encrypt_data -> SF\n• SF_PAGE_READ:\n  Read back into read buff\n• Byte-by-byte compare:\n  If mismatch -> RETRY!\n  If match -> next page", 
            ha='center', va='center', fontsize=7.5, color='#134E4A')

    # Lower Container: Block CMAC & Finalization
    ax.add_patch(patches.FancyBboxPatch((3, 8), 94, 48, boxstyle="round,pad=0.5", fc='#F8FAFC', ec='#0B2545', lw=1.5))
    ax.text(50, 51, "STEP 5: Block CMAC Generation & Metadata Finalization", ha='center', va='center', fontsize=10, fontweight='bold', color='#0B2545')

    # Sub-boxes
    ax.add_patch(patches.FancyBboxPatch((6, 14), 42, 33, boxstyle="round,pad=0.4", fc='#E0E7FF', ec='#4338CA', lw=1.2))
    ax.text(27, 42, "Block CMAC Storage", ha='center', va='center', fontsize=9, fontweight='bold', color='#3730A3')
    ax.text(27, 28, "• Csm_MacGenerate(FINISH) yields 16-byte CMAC\n• Written to pre-calculated block_cmac_addr_reference\n• Stored in Serial Flash after last segment of block\n• Repeated for all ODX-F blocks in the cal update", 
            ha='center', va='center', fontsize=7.5, color='#312E81')

    ax.add_patch(patches.FancyBboxPatch((52, 14), 42, 33, boxstyle="round,pad=0.4", fc='#FEE2E2', ec='#DC2626', lw=1.2))
    ax.text(73, 42, "CSU Metadata Trailer & Integrity", ha='center', va='center', fontsize=9, fontweight='bold', color='#991B1B')
    ax.text(73, 28, "• Metadata header packed from telematics_csu_table\n• Dedicated metadata CMAC computed via Csm_MacGenerate\n• Metadata array + CMAC written to SF start address\n• On success: NVM_Back_up_status = BACKUP_COMPLT_VALID", 
            ha='center', va='center', fontsize=7.5, color='#7F1D1D')

    # Step arrows
    arr = dict(arrowstyle="->", lw=1.5, color="#1E293B")
    ax.annotate("", xy=(27, 75), xytext=(24, 75), arrowprops=arr)
    ax.annotate("", xy=(51, 75), xytext=(48, 75), arrowprops=arr)
    ax.annotate("", xy=(75, 75), xytext=(72, 75), arrowprops=arr)

    plt.tight_layout()
    plt.savefig('diag_crypto_pipeline.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Generated diag_crypto_pipeline.png")

create_init_flowchart()
create_rollback_flowchart()
create_state_machine_diagram()
create_crypto_pipeline_diagram()
