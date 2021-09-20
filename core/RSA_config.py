from cryptography.hazmat.primitives import serialization

with open('core\\private-key.pem', 'rb') as private_file:
    priavte_key = serialization.load_pem_private_key(
        private_file.read(),
        password=None
    )
    public_key = priavte_key.public_key()

pem = priavte_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

key = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)