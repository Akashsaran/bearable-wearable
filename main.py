from enum import Enum

# --- Enums ---

class MessageType(Enum):
    DIRECT_PAIRING = 0b000
    GROUP_PAIRING = 0b001
    SET_TEMPO = 0b010
    START = 0b011
    STOP = 0b100
    ALERT = 0b101

class ConductorID(Enum):
    C1 = 0b00
    C2 = 0b01
    C3 = 0b10
    C4 = 0b11

class TargetGroupID(Enum):
    ALL = 0b000
    WOODWINDS = 0b001
    PERCUSSION = 0b010
    BRASS = 0b011
    STRINGS = 0b100
    OTHER1 = 0b101
    OTHER2 = 0b110
    OTHER3 = 0b111

def encrypt_message(msg_type: MessageType, conductor: ConductorID,
                    target: TargetGroupID, tempo: int = None, time_ms: int = None):
    """Build exactly 3 bytes (packet) based on inputs."""

    # Build first byte: 3 bits (msg) + 2 bits (conductor) + 3 bits (target)
    first_byte = (msg_type.value << 5) | (conductor.value << 3) | target.value

    # Build next two bytes depending on message type
    if msg_type == MessageType.SET_TEMPO:
        value = tempo or 0
    elif msg_type == MessageType.START:
        value = time_ms or 0
    else:
        value = 0

    second_byte = (value >> 8) & 0xFF
    third_byte = value & 0xFF
    packet = bytes([first_byte, second_byte, third_byte])

    # --- Display result ---
    print("\n==============================")
    print("PACKET ENCRYPTION SUMMARY")
    print("==============================")
    print(f"Message Type: {msg_type.name:<13} → {msg_type.value:03b}")
    print(f"Conductor ID: {conductor.name:<10} → {conductor.value:02b}")
    print(f"Target Group ID: {target.name:<10} → {target.value:03b}")

    if msg_type == MessageType.SET_TEMPO:
        print(f"Tempo: {value} BPM → {second_byte:08b} {third_byte:08b}")
    elif msg_type == MessageType.START:
        print(f"Time: {value} ms → {second_byte:08b} {third_byte:08b}")
    else:
        print("Tempo/Time: N/A → 00000000 00000000")

    print("------------------------------")
    print(f"→ Packet: {first_byte:08b} {second_byte:08b} {third_byte:08b}")
    print(f"→ Raw Bytes: {packet}")
    print("==============================\n")

    return packet

def decrypt_message(packet_bytes: bytes):
    """Take 3 bytes and decode them into readable values."""
    if len(packet_bytes) != 3:
        raise ValueError("Packet must be exactly 3 bytes.")

    first, second, third = packet_bytes

    # Extract fields
    msg_val = (first >> 5) & 0b111
    conductor_val = (first >> 3) & 0b11
    target_val = first & 0b111
    value = (second << 8) | third

    # Convert to Enums
    msg_type = MessageType(msg_val) if msg_val in [t.value for t in MessageType] else None
    conductor = ConductorID(conductor_val) if conductor_val in [c.value for c in ConductorID] else None
    target = TargetGroupID(target_val) if target_val in [g.value for g in TargetGroupID] else None

    # --- Display ---
    print("\n==============================")
    print("PACKET DECRYPTION SUMMARY")
    print("==============================")
    print(f"Raw Input Bytes: {first:08b} {second:08b} {third:08b}")
    print("------------------------------")

    if msg_type:
        print(f"Message Type: {msg_type.name:<13} ({msg_val:03b})")
    else:
        print(f"Message Type: Unknown ({msg_val:03b})")

    if conductor:
        print(f"Conductor ID: {conductor.name:<10} ({conductor_val:02b})")
    else:
        print(f"Conductor ID: Unknown ({conductor_val:02b})")

    if target:
        print(f"Target Group ID: {target.name:<10} ({target_val:03b})")
    else:
        print(f"Target Group ID: Unknown ({target_val:03b})")

    # Decode tempo/time depending on message type
    if msg_type == MessageType.SET_TEMPO:
        print(f"Tempo: {value} BPM")
    elif msg_type == MessageType.START:
        print(f"Time: {value} ms")
    else:
        print("Tempo/Time: N/A")

    print("==============================\n")

    ## Tempo
    ## typeOfConnection (Direct - Will NOT Propogate vs Group - Will Propogate)
    ## Conductor ID
    ## VibrationIntensity (If Metronome then Low Value, If Alert then High Value)
    ## LEDColor (Either Group ID, Connection, Status Indicator)
    ## LagCompensation (Current Time - Sent Time) mod 60
