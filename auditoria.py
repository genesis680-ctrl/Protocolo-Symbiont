import json, hashlib, sys, os
from ecdsa import VerifyingKey, SECP256k1

# --- SUA CHAVE MESTRA (Não mude) ---
CHAVE_CRIADOR = "f31325e573a30a0d3efdc8c3c245d8348eaa5e4858a10e98c0ac933ed9e6ec2a84b3f771eaca75fc7eb2f893cf44ae9a6b3b7c36e29072f1e8e9d08ca2ef9ad4"

def auditar_cadeia():
    print("--- 🛡️ PROTOCOLO DE SEGURANÇA 2.0 (ECDSA) ---")
    if not os.path.exists("blockchain.json"): return True
    
    with open("blockchain.json", "r") as f: cadeia = json.load(f)
    ultimo_bloco = cadeia[-1]

    # O Gênese é sagrado e não precisa de assinatura
    if ultimo_bloco['index'] == 0: return True

    # 1. Valida Pagamento de Tributo
    if ultimo_bloco['data'].get('tributo_obrigatorio') != CHAVE_CRIADOR:
        print(f"[CRIME] Tributo não pago ao Criador!")
        sys.exit(1)

    # 2. Valida Assinatura Criptográfica (A Nova Camada)
    try:
        # Recupera a chave pública de quem minerou e a assinatura
        pub_key_hex = ultimo_bloco['data'].get('minerador_pubkey')
        assinatura_hex = ultimo_bloco['data'].get('assinatura')
        
        if not pub_key_hex or not assinatura_hex:
            print("[ERRO] Bloco sem assinatura digital. Rejeitado.")
            sys.exit(1)

        # Reconstrói a "cena do crime" (o que foi assinado)
        # Assinamos: INDEX + PREVIOUS_HASH + NONCE
        payload = f"{ultimo_bloco['index']}{ultimo_bloco['previous_hash']}{ultimo_bloco['nonce']}".encode()
        
        # Verifica matematicamente
        vk = VerifyingKey.from_string(bytes.fromhex(pub_key_hex), curve=SECP256k1)
        if vk.verify(bytes.fromhex(assinatura_hex), payload):
            print(f"[SUCESSO] Assinatura Válida via Curva Elíptica SECP256k1.")
            print(f"[ID] Minerador Autenticado: {pub_key_hex[:15]}...")
        else:
            raise Exception("Assinatura Falsa")

    except Exception as e:
        print(f"[FRAUDE DETECTADA] A assinatura não confere: {e}")
        sys.exit(1)

if __name__ == "__main__":
    auditar_cadeia()

