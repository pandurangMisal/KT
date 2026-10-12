import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Configure matplotlib style
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10
plt.rcParams['figure.dpi'] = 300

def create_csar_arch_diagram():
    fig, ax = plt.subplots(figsize=(10, 6.2))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Background
    fig.patch.set_facecolor('#FFFFFF')

    # Title
    ax.text(50, 96, "CDDTeleBackupMngr - CSAR System Architecture & Boundaries", 
            ha='center', va='center', fontsize=14, fontweight='bold', color='#0B2545')

    # Layers
    # Application Layer
    ax.add_patch(patches.FancyBboxPatch((5, 80), 90, 11, boxstyle="round,pad=0.5", fc='#EBF3FA', ec='#134074', lw=1.5))
    ax.text(50, 85.5, "Application Layer / SWCs (Telematics Processing, Cal Download, Diagnostics)", 
            ha='center', va='center', fontsize=10, fontweight='bold', color='#134074')

    # RTE Layer
    ax.add_patch(patches.FancyBboxPatch((5, 68), 90, 8, boxstyle="round,pad=0.3", fc='#FEF3C7', ec='#D97706', lw=1.5))
    ax.text(50, 72, "AUTOSAR Run Time Environment (RTE) - S/R Ports, C/S Ports & Timing Events (10ms, 5s)", 
            ha='center', va='center', fontsize=9.5, fontweight='bold', color='#92400E')

    # BSW Layer Outer Container
    ax.add_patch(patches.FancyBboxPatch((5, 18), 90, 46, boxstyle="round,pad=0.5", fc='#F8FAFC', ec='#64748B', lw=1.5, ls='--'))
    ax.text(12, 61, "BSW Layer (Basic Software)", fontsize=9, fontweight='bold', color='#475569')

    # Complex Device Driver (CDDTeleBackupMngr) - Highlighted
    ax.add_patch(patches.FancyBboxPatch((32, 38), 36, 19, boxstyle="round,pad=0.6", fc='#0B2545', ec='#00A896', lw=2.5))
    ax.text(50, 51, "CDDTeleBackupMngr", ha='center', va='center', fontsize=12, fontweight='bold', color='#FFFFFF')
    ax.text(50, 45, "• reInitCDDTeleBackupMngr (Init)\n• reTeleRollBackTimeCheck (5s)\n• reCddTeleBackupSchdlr (10ms)\n• metadata_extract()", 
            ha='center', va='center', fontsize=8, color='#E2E8F0')

    # CSM Module
    ax.add_patch(patches.FancyBboxPatch((8, 38), 20, 19, boxstyle="round,pad=0.5", fc='#E6FFFA', ec='#00A896', lw=1.5))
    ax.text(18, 50, "CSM\n(Crypto)", ha='center', va='center', fontsize=10, fontweight='bold', color='#065F46')
    ax.text(18, 42, "• AES-128-CBC\n• CMAC Gen\n• Key Management\n• Random IV", 
            ha='center', va='center', fontsize=7.5, color='#047857')

    # NvM Module
    ax.add_patch(patches.FancyBboxPatch((72, 38), 20, 19, boxstyle="round,pad=0.5", fc='#EDE9FE', ec='#7C3AED', lw=1.5))
    ax.text(82, 50, "NvM\n(Non-Volatile)", ha='center', va='center', fontsize=10, fontweight='bold', color='#5B21B6')
    ax.text(82, 42, "• Backup Status\n• Rollback Timer\n• Portover Status\n• FBL General Blk", 
            ha='center', va='center', fontsize=7.5, color='#6D28D9')

    # Memory Access / SPI Driver
    ax.add_patch(patches.FancyBboxPatch((32, 21), 36, 12, boxstyle="round,pad=0.4", fc='#E0E7FF', ec='#4338CA', lw=1.5))
    ax.text(50, 28.5, "vMemAccM / SPI Driver", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#3730A3')
    ax.text(50, 24, "SerialFlashGetServ() / GetSerialFlashState()", ha='center', va='center', fontsize=7.5, color='#4338CA')

    # Physical Hardware Layer
    # Program Flash
    ax.add_patch(patches.FancyBboxPatch((8, 3), 36, 11, boxstyle="round,pad=0.5", fc='#F1F5F9', ec='#334155', lw=1.8))
    ax.text(26, 9.5, "Onboard Program Flash (PF)", ha='center', va='center', fontsize=9, fontweight='bold', color='#0F172A')
    ax.text(26, 5.5, "AURIX TC3xx Microcontroller (Plain Data Source)", ha='center', va='center', fontsize=7.5, color='#475569')

    # Serial Flash
    ax.add_patch(patches.FancyBboxPatch((56, 3), 36, 11, boxstyle="round,pad=0.5", fc='#FEE2E2', ec='#DC2626', lw=1.8))
    ax.text(74, 9.5, "External Serial Flash (SF)", ha='center', va='center', fontsize=9, fontweight='bold', color='#991B1B')
    ax.text(74, 5.5, "Cypress S25FL512S / Micron 25QL512 (Secure Backup)", ha='center', va='center', fontsize=7.5, color='#B91C1C')

    # Connectors / Arrows
    arrow_props = dict(arrowstyle="->", lw=1.5, color="#1E293B")
    d_arrow_props = dict(arrowstyle="<->", lw=1.5, color="#00A896")

    # RTE <-> CDD
    ax.annotate("", xy=(50, 57), xytext=(50, 68), arrowprops=d_arrow_props)
    # CDD <-> CSM
    ax.annotate("", xy=(32, 47.5), xytext=(28, 47.5), arrowprops=d_arrow_props)
    # CDD <-> NvM
    ax.annotate("", xy=(68, 47.5), xytext=(72, 47.5), arrowprops=d_arrow_props)
    # CDD -> vMemAccM
    ax.annotate("", xy=(50, 33), xytext=(50, 38), arrowprops=arrow_props)
    # vMemAccM -> Serial Flash
    ax.annotate("", xy=(74, 14), xytext=(58, 21), arrowprops=arrow_props)
    # CDD reads Program Flash directly
    ax.annotate("", xy=(26, 14), xytext=(40, 38), arrowprops=dict(arrowstyle="<-", lw=1.5, color="#2563EB", ls='--'))

    plt.tight_layout()
    plt.savefig('diag_csar_architecture.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Generated diag_csar_architecture.png")

create_csar_arch_diagram()
