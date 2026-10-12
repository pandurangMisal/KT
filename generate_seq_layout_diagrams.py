import matplotlib.pyplot as plt
import matplotlib.patches as patches

plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['figure.dpi'] = 300

def create_sequence_diagram():
    fig, ax = plt.subplots(figsize=(11, 7.5))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    fig.patch.set_facecolor('#FFFFFF')

    ax.text(50, 97, "CDDTeleBackupMngr - End-to-End Runtime Sequence", 
            ha='center', va='center', fontsize=14, fontweight='bold', color='#0B2545')
    ax.text(50, 93.5, "Runtime interaction across RTE Tasks, CDD Scheduler, Crypto Services (CSM), Serial Flash, and NvM", 
            ha='center', va='center', fontsize=8.5, color='#475569')

    # Lifelines
    actors = [
        ("RTE / OS Task\n(10ms / 5s)", 10, '#0B2545'),
        ("CDDTeleBackupMngr\n(Scheduler)", 32, '#00A896'),
        ("CSM\n(Crypto)", 54, '#7C3AED'),
        ("vMemAccM / SF\n(Serial Flash)", 74, '#2563EB'),
        ("NvM\n(Non-Volatile)", 92, '#D97706')
    ]

    for name, x, color in actors:
        # Header box
        ax.add_patch(patches.FancyBboxPatch((x-8, 83), 16, 7, boxstyle="round,pad=0.2", fc=color, ec=color))
        ax.text(x, 86.5, name, ha='center', va='center', fontsize=7.5, fontweight='bold', color='#FFFFFF')
        # Lifeline dashed
        ax.plot([x, x], [5, 83], ls='--', color='#94A3B8', lw=1.2)

    # Sequence Messages
    msgs = [
        (80, 10, 32, "TimingEvent (every 10ms)", '#1E293B', False),
        (74, 32, 74, "SF_FULL_ERASE request (SerialFlashGetServ)", '#2563EB', False),
        (69, 74, 32, "GetSerialFlashState() -> SF_REQUEST_COMPLETE", '#2563EB', True),
        (64, 32, 54, "Csm_RandomGenerate() -> 16-byte IV", '#7C3AED', False),
        (59, 32, 54, "Csm_Encrypt(START) & Csm_MacGenerate(START)", '#7C3AED', False),
        (54, 32, 54, "Csm_MacGenerate(UPDATE) with 8B Seg Header", '#7C3AED', False),
        (49, 32, 54, "Csm_Encrypt(UPDATE) & Csm_MacGenerate(UPDATE) on chunk", '#7C3AED', False),
        (44, 32, 74, "SF_PAGE_WRITE (Encrypted 256B page)", '#2563EB', False),
        (39, 32, 74, "SF_PAGE_READ (Read-back verification)", '#2563EB', False),
        (34, 74, 32, "Verify byte-by-byte (Mem_Read_Buff == backup_encrypt_data)", '#059669', True),
        (29, 32, 54, "Csm_MacGenerate(FINISH) -> 16-byte Block CMAC", '#7C3AED', False),
        (24, 32, 74, "SF_DATA_TRANSFER (Write Block CMAC to ref addr)", '#2563EB', False),
        (19, 32, 54, "Compute Metadata Trailer CMAC", '#7C3AED', False),
        (14, 32, 74, "Write Metadata Structure + CMAC to SF start", '#2563EB', False),
        (9, 32, 92, "NvM_WriteBlock(FBLGeneral) -> BACKUP_COMPLT_VALID", '#D97706', False)
    ]

    for y, x1, x2, text, col, dashed in msgs:
        ls = '--' if dashed else '-'
        ax.annotate("", xy=(x2, y), xytext=(x1, y), 
                    arrowprops=dict(arrowstyle="->", lw=1.3, color=col, ls=ls))
        mid = (x1 + x2) / 2
        va = 'bottom' if y > 50 else 'bottom'
        ax.text(mid, y + 0.8, text, ha='center', va='bottom', fontsize=7, fontweight='bold', color=col,
                bbox=dict(boxstyle="square,pad=0.1", fc='#FFFFFF', ec='none', alpha=0.85))

    plt.tight_layout()
    plt.savefig('diag_sequence.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Generated diag_sequence.png")

def create_data_layout_diagram():
    fig, ax = plt.subplots(figsize=(11, 6.5))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    fig.patch.set_facecolor('#FFFFFF')

    ax.text(50, 96, "Serial Flash Memory Layout & ODX-F CSU Data Structures", 
            ha='center', va='center', fontsize=13, fontweight='bold', color='#0B2545')
    ax.text(50, 92, "Physical and cryptographic organization of the backup calibration data on external serial flash", 
            ha='center', va='center', fontsize=8.5, color='#475569')

    # Top: Serial Flash Partitioning
    ax.add_patch(patches.FancyBboxPatch((4, 68), 92, 20, boxstyle="round,pad=0.4", fc='#F8FAFC', ec='#0B2545', lw=1.5))
    ax.text(8, 83.5, "Serial Flash Physical Layout (512 Mbit / 64 MB Total Space)", fontsize=9.5, fontweight='bold', color='#0B2545')

    # Region 1: Buffer Region
    ax.add_patch(patches.FancyBboxPatch((6, 71), 26, 10, boxstyle="round,pad=0.2", fc='#E0E7FF', ec='#4338CA', lw=1.2))
    ax.text(19, 77.5, "BUFFER REGION\n(0x0200_0000 / 32MB)", ha='center', va='center', fontsize=7.5, fontweight='bold', color='#3730A3')
    ax.text(19, 73, "Staging for Incoming Cal Packages", ha='center', va='center', fontsize=6.8, color='#4338CA')

    # Region 2: Backup Region (Covered by this module)
    ax.add_patch(patches.FancyBboxPatch((35, 71), 59, 10, boxstyle="round,pad=0.2", fc='#FEF3C7', ec='#D97706', lw=1.5))
    ax.text(64.5, 77.5, "BACKUP REGION (0x0300_0000 / 48MB) - Managed by CDDTeleBackupMngr", ha='center', va='center', fontsize=8, fontweight='bold', color='#92400E')
    ax.text(64.5, 73, "Secure encrypted rollback store: Metadata Header + Encrypted Pages + Block CMACs", ha='center', va='center', fontsize=7, color='#B45309')

    # Detailed Backup Region Structure (Lower)
    ax.add_patch(patches.FancyBboxPatch((4, 6), 92, 57, boxstyle="round,pad=0.5", fc='#F1F5F9', ec='#00A896', lw=1.5))
    ax.text(8, 58.5, "Detailed Organization of BACKUP REGION", fontsize=9.5, fontweight='bold', color='#00A896')

    # Component 1: Metadata Structure
    ax.add_patch(patches.FancyBboxPatch((6, 26), 26, 28, boxstyle="round,pad=0.3", fc='#FFFFFF', ec='#00A896', lw=1.5))
    ax.text(19, 49, "CSU Metadata Header\n(SF Start Addr)", ha='center', va='center', fontsize=8.5, fontweight='bold', color='#00A896')
    ax.text(19, 36, "• Fixed Header (0x17 B)\n• Block Info (0x189 B/blk)\n• Segment Records (0xC B/seg)\n• Metadata CMAC (16 B)\n• SF_PAGE_SIZE Padded", 
            ha='center', va='center', fontsize=7.2, color='#1E293B')

    # Component 2: Block Data Pages
    ax.add_patch(patches.FancyBboxPatch((35, 26), 36, 28, boxstyle="round,pad=0.3", fc='#FFFFFF', ec='#2563EB', lw=1.5))
    ax.text(53, 49, "Encrypted Block Data Chunks\n(ODX-F Blocks & Segments)", ha='center', va='center', fontsize=8.5, fontweight='bold', color='#2563EB')
    ax.text(53, 36, "• Page 1: 16B Random IV + Data\n• Pages 2..N: 256B Encrypted\n• Big-Endian [Addr, Len] CMAC\n• Verified by Read-back\n• Repeated per Segment", 
            ha='center', va='center', fontsize=7.2, color='#1E293B')

    # Component 3: Block CMAC
    ax.add_patch(patches.FancyBboxPatch((74, 26), 20, 28, boxstyle="round,pad=0.3", fc='#FFFFFF', ec='#7C3AED', lw=1.5))
    ax.text(84, 49, "Block CMAC Storage\n(Ref Address)", ha='center', va='center', fontsize=8.5, fontweight='bold', color='#7C3AED')
    ax.text(84, 36, "• 16-byte MAC value\n• Covers Seg Descriptors\n  + All chunk data\n• Stored at precomputed\n  block_cmac_addr_ref", 
            ha='center', va='center', fontsize=7.2, color='#1E293B')

    # Bottom Banner: Integrity Flow
    ax.add_patch(patches.FancyBboxPatch((6, 9), 88, 13, boxstyle="round,pad=0.3", fc='#DCFCE7', ec='#16A34A', lw=1.2))
    ax.text(50, 17, "Key Security & Data Integrity Assurance Points:", ha='center', va='center', fontsize=8.5, fontweight='bold', color='#166534')
    ax.text(50, 12, "1. Random IV per session -> 2. AES-128-CBC encryption -> 3. Segment CMAC binding -> 4. Read-back comparison -> 5. Metadata trailer MAC", 
            ha='center', va='center', fontsize=7.5, color='#15803D')

    plt.tight_layout()
    plt.savefig('diag_data_layout.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Generated diag_data_layout.png")

create_sequence_diagram()
create_data_layout_diagram()
