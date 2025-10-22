from enum import Enum

# --- Enums ---

class MessageType(Enum):
    CONNECT = 0b000
    SET_TEMPO = 0b001
    START = 0b010
    STOP = 0b011
    ALERT = 0b100

class ConductorID(Enum):
    C1 = 0b00  # now 1
    C2 = 0b01  # now 2
    C3 = 0b10  # now 3
    C4 = 0b11  # now 4

class TargetGroupID(Enum):
    ALL = 0b000
    WOODWINDS = 0b001
    PERCUSSION = 0b010
    BRASS = 0b011
    STRINGS = 0b100
    OTHER1 = 0b101
    OTHER2 = 0b110
    OTHER3 = 0b111


# --- Decrypt function ---

def decrypt_message(packet_bits: str):
    parts = packet_bits.strip().split()
    if len(parts) != 3:
        raise ValueError("Input must contain exactly 3 bytes separated by spaces.")

    packet = bytes(int(b, 2) for b in parts)

    first_byte = packet[0]
    msg_type_bits = (first_byte >> 5) & 0b111
    conductor_bits = (first_byte >> 3) & 0b11
    target_bits = first_byte & 0b111

    msg_type = MessageType(msg_type_bits)
    conductor = ConductorID(conductor_bits)
    target = TargetGroupID(target_bits)

    extra_value = (packet[1] << 8) | packet[2]

    tempo = None
    time_ms = None

    if msg_type == MessageType.SET_TEMPO:
        tempo = extra_value
    elif msg_type == MessageType.START:
        time_ms = extra_value

    # Human-readable printout
    print("\n==============================")
    print("PACKET DECRYPTION SUMMARY")
    print("==============================")
    print(f"Input Bits: {packet_bits}")
    print("------------------------------")
    print(f"Message Type: {msg_type.name:<10} → {msg_type.value:03b}")
    print(f"Conductor ID: {conductor.name:<10} → {conductor.value:02b}")
    print(f"Target Group ID: {target.name:<10} → {target.value:03b}")

    if tempo is not None:
        print(f"Tempo: {tempo} BPM → {packet[1]:08b} {packet[2]:08b}")
    elif time_ms is not None:
        print(f"Time: {time_ms} ms → {packet[1]:08b} {packet[2]:08b}")
    else:
        print("Tempo/Time: N/A → 00000000 00000000")

    print("------------------------------")
    print(f"→ Packet: {packet[0]:08b} {packet[1]:08b} {packet[2]:08b}")
    print("==============================\n")


# --- User Input ---

if __name__ == "__main__":
    packet_bits = input("Enter 3 bytes (e.g. 00101001 00000011 00100000): ")
    decrypt_message(packet_bits)
