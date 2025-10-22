from enum import Enum


class MessageType(Enum):
    CONNECT = 0b000
    SET_TEMPO = 0b001
    START = 0b010
    STOP = 0b011
    ALERT = 0b100


class ConductorID(Enum):
    CONDUCTOR_1 = 0b00
    CONDUCTOR_2 = 0b01
    CONDUCTOR_3 = 0b10
    CONDUCTOR_4 = 0b11


class TargetGroupID(Enum):
    ALL = 0
    WOODWINDS = 1
    PERCUSSION = 2
    BRASS = 3
    STRINGS = 4
    CHOIR = 5
    SOLOIST = 6
    OTHER = 7


def build_message():
    """Ask user for details and build exactly 3 bytes (packet)."""
    print("\nAvailable message types:")
    for t in MessageType:
        print(f" - {t.name}")

    msg_name = input("Enter message type: ").strip().upper()
    try:
        msg_type = MessageType[msg_name]
    except KeyError:
        raise ValueError("Invalid message type")

    print("\nConductor IDs:")
    for c in ConductorID:
        print(f" - {c.name} ({c.value})")

    conductor_value = int(input("Enter conductor ID (0–3): "))
    conductor = ConductorID(conductor_value)

    print("\nTarget Group IDs:")
    for g in TargetGroupID:
        print(f" - {g.name} ({g.value})")

    target_value = int(input("Enter target group ID (0–7): "))
    target = TargetGroupID(target_value)

    # --- Build first byte (3 bits + 2 bits + 3 bits)
    first_byte = (msg_type.value << 5) | (conductor.value << 3) | target.value

    # --- Determine next two bytes ---
    second_byte = 0
    third_byte = 0

    if msg_type == MessageType.SET_TEMPO:
        tempo = float(input("Enter tempo (BPM): "))
        tempo_int = int(tempo)  # integer BPM (not ×100)
        second_byte = (tempo_int >> 8) & 0xFF
        third_byte = tempo_int & 0xFF

    elif msg_type == MessageType.START:
        time_ms = int(input("Enter time (ms since last minute): "))
        second_byte = (time_ms >> 8) & 0xFF
        third_byte = time_ms & 0xFF

    packet = bytes([first_byte, second_byte, third_byte])

    # --- Show formatted output ---
    print("\n→ Packet:")
    print(f"{first_byte:08b} {second_byte:08b} {third_byte:08b}")
    print(f"Raw bytes: {packet}")

    return packet


# --- Example usage ---
if __name__ == "__main__":
    build_message()