import hashlib, json, time, os
# Se der erro aqui, rode: pip install ecdsa
from ecdsa import SigningKey, SECP256k1

CHAVE_CRIADOR = "f31325e573a30a0d3efdc8c3c245d8348eaa5e4858a10e98c0ac933ed9e6ec2a84b3f771eaca75fc7eb2f893cf44ae9a6b3b7c36e29072f1e8e9d08ca2ef9ad4"

def carregar_carteira():
    # Cria uma chave privada se não existir
    if not os.path.exists("wallet.pem"):
        sk = SigningKey.generate(curve=SECP256k1)
        with open("wallet.pem", "wb") as f: f.write(sk.to_pem())
        print("[*] NOVA CARTEIRA CRIADA: Guarde 'wallet.pem' com sua vida!")
    else:
        with open("wallet.pem", "rb") as f: sk = SigningKey.from_pem(f.read())
    return sk

def minerar():
    print("--- ⛏️ SYMBIONT MINER v2 (SECURE) ---")
    
    # 1. Carrega Identidade
    sk = carregar_carteira()
    minha_pub_key = sk.verifying_key.to_string().hex()
    print(f"[*] Identidade: {minha_pub_key[:15]}...")

    # 2. Carrega Blockchain
    try:
        with open("blockchain.json", "r") as f: cadeia = json.load(f)
    except:
        print("[X] Erro: blockchain.json não encontrado.")
        return

    ultimo = cadeia[-1]
    novo_index = ultimo['index'] + 1
    print(f"[*] Minerando Bloco #{novo_index}...")

    nonce = 0
    start = time.time()

    while True:
        # A Prova de Trabalho
        # Payload simples para minerar rápido, mas assinar o resultado
        dados_temp = str(novo_index) + ultimo['hash'] + str(nonce)
        hash_calc = hashlib.sha256(dados_temp.encode()).hexdigest()
        
        if hash_calc.startswith("0000"): # Dificuldade
            print(f"\n[$$$] BLOCO ENCONTRADO! Hash: {hash_calc}")
            
            # 3. ASSINATURA DIGITAL (O Selo de Autenticidade)
            payload_assinar = f"{novo_index}{ultimo['hash']}{nonce}".encode()
            assinatura = sk.sign(payload_assinar).hex()
            
            novo_bloco = {
                "index": novo_index,
                "timestamp": time.time(),
                "data": {
                    "minerador": "Dev_Secure",
                    "tributo_obrigatorio": CHAVE_CRIADOR,
                    "minerador_pubkey": minha_pub_key,
                    "assinatura": assinatura
                },
                "previous_hash": ultimo['hash'],
                "nonce": nonce
            }
            
            cadeia.append(novo_bloco)
            with open("blockchain.json", "w") as f: json.dump(cadeia, f, indent=2)
            print("[!] Cofre atualizado e assinado criptograficamente.")
            break
        nonce += 1

if __name__ == "__main__":
    minerar()
