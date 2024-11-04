"""Constants used with SahamatiNet APIs."""

from utils import data_utils

# Provided by sahamatinet after onboarding
HOST = "https://api.sandbox.sahamati.org.in"
MEMBER_ID = "cuspmoney-fiu-buildaathon-24"
USER_NAME = "hetul@infocusp.com"
PASSWORD = ""

# Data fetch config
MAX_TRIALS = 3
DELAY_FOR_RETRY = 1

# Load private key used for generating detached jws
RSA_PRIVATE_KEY_JWK = data_utils.load_json_from_disk(
    "data/key-pairs/rsa_private_key_for_sahamati_api_signature.json"
)

# SahamatiNet simulator configs
SIMULATE_FI_FETCH = True  # Mocks FI/fetch response
MOCK_AA_SIMULATOR = "CUSPMONEY-AA-SIMULATOR"  # AA entity used for simulation

# Both key pairs are generated using sahamati rahasya's "/ecc/v1/generateKey"
# endpoint to simulate data encryption and decryption.
AA_SIMULATOR_ECC_KEY_PAIR = data_utils.load_json_from_disk(
    "data/key-pairs/simulator_ecc_key_pair.json"
)  # Simulator data is already encrypted using private key of this key pair

FIU_ECC_KEY_PAIR = data_utils.load_json_from_disk(
    "data/key-pairs/fiu_ecc_key_pair.json"
)  # FIU should decrypt the simulated response using this key pair.

# Nonces generated using `utils.sahamati.sahamati_rahasya_utils`.
AA_SIMULATOR_NONCE = AA_SIMULATOR_ECC_KEY_PAIR["Nonce"]
FIU_NONCE = FIU_ECC_KEY_PAIR["Nonce"]
