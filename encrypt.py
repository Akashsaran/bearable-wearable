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


# --- Encryption Function ---

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


# --- Main (User Input) ---

if __name__ == "__main__":
    """Ask user for details and build exactly 3 bytes (packet)."""

    print("\nAvailable message types:")
    for t in MessageType:
        print(f" - {t.name} ({t.value:03b})")

    msg_name = input("Enter message type: ").strip().upper()
    try:
        msg_type = MessageType[msg_name]
    except KeyError:
        raise ValueError("Invalid message type")

    print("\nConductor IDs:")
    for c in ConductorID:
        print(f" - {c.name} ({c.value})")

    conductor_value = int(input("Enter conductor ID (1–4): "))
    try:
        conductor = ConductorID(conductor_value)
    except ValueError:
        raise ValueError("Invalid conductor ID")

    print("\nTarget Group IDs:")
    for g in TargetGroupID:
        print(f" - {g.name} ({g.value})")

    target_value = int(input("Enter target group ID (0–7): "))
    try:
        target = TargetGroupID(target_value)
    except ValueError:
        raise ValueError("Invalid target group ID")

    tempo = None
    time_ms = None
    if msg_type == MessageType.SET_TEMPO:
        tempo = int(input("Enter Tempo (BPM): "))
    elif msg_type == MessageType.START:
        time_ms = int(input("Enter Time (ms): "))

    encrypt_message(msg_type, conductor, target, tempo, time_ms)
