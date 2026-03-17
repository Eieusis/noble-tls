"""
Custom TLS profiles that override the Go library's built-in profiles.

These profiles bypass the compiled Go binary's pre-built browser profiles to fix
fingerprinting discrepancies (e.g., the bogdanfinn/utls ECH GREASE implementation
incorrectly adds extension 0xCA34 which real Chrome does not send).

Profile data is derived from real Chrome ClientHello captures.
"""

# Chrome 146 custom profile — matches a real Chrome 146 ClientHello (FP1)
# without the spurious 0xCA34 (ECH GREASE outer extensions) that
# bogdanfinn's utls fork incorrectly adds.
#
# JA4 fingerprint: t13d1516h2
# Extensions (sorted, hex): 0005,000a,000b,000d,0012,0017,001b,0023,002b,002d,0033,44cd,fe0d,ff01
CHROME_146_PROFILE = {
    "ja3_string": (
        "771,"
        "4865-4866-4867-49195-49199-49196-49200-52393-52392-49171-49172-156-157-47-53,"
        "65281-0-45-23-18-17613-11-51-43-13-65037-10-27-5-35-16,"
        "4588-29-23-24,"
        "0"
    ),
    "h2_settings": {
        "HEADER_TABLE_SIZE": 65536,
        "ENABLE_PUSH": 0,
        "MAX_CONCURRENT_STREAMS": 1000,
        "INITIAL_WINDOW_SIZE": 6291456,
        "MAX_HEADER_LIST_SIZE": 262144,
    },
    "h2_settings_order": [
        "HEADER_TABLE_SIZE",
        "ENABLE_PUSH",
        "MAX_CONCURRENT_STREAMS",
        "INITIAL_WINDOW_SIZE",
        "MAX_HEADER_LIST_SIZE",
    ],
    "supported_signature_algorithms": [
        "ECDSAWithP256AndSHA256",
        "PSSWithSHA256",
        "PKCS1WithSHA256",
        "ECDSAWithP384AndSHA384",
        "PSSWithSHA384",
        "PKCS1WithSHA384",
        "PSSWithSHA512",
        "PKCS1WithSHA512",
    ],
    "supported_versions": ["GREASE", "1.3", "1.2"],
    "key_share_curves": ["GREASE", "X25519MLKEM768", "X25519"],
    "cert_compression_algo": "brotli",
    "alps_protocols": ["h2"],
    "pseudo_header_order": [":method", ":authority", ":scheme", ":path"],
    "connection_flow": 15663105,
}

# Maps Go library client identifier strings to custom profiles.
# When a session is created with a client whose identifier is in this dict,
# the custom profile is used instead of the Go library's built-in profile.
CUSTOM_PROFILES = {
    "chrome_146_real": CHROME_146_PROFILE,
}
