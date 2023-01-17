import base64


def to_id(id: int, prefix: str) -> str:
    """Return Base64 string with a prefix"""
    encoded = base64.b64encode(
        bytes(f"{prefix}:{id}", "utf-8")
    )

    return encoded.decode("utf-8")


def from_id(id: str) -> int:
    """Return decoded id from the Base64 string"""
    decoded = base64.b64decode(id)

    decoded_id = decoded.decode("utf-8").split(":").pop()

    return int(decoded_id)
