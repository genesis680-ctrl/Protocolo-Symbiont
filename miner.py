import hashlib, json, time

# --- SYMBIONT MINER (GITHUB EDITION) ---
# Esta ferramenta lê o cofre, minera e salva o resultado.
CHAVE_CRIADOR = "f31325e573a30a0d3efdc8c3c245d8348eaa5e4858a10e98c0ac933ed9e6ec2a84b3f771eaca75fc7eb2f893cf44ae9a6b3b7c36e29072f1e8e9d08ca2ef9ad4"

def minerar():
    print("--- INICIANDO MINERADOR SYMBIONT ---")
    
    # 1. Abre o Cofre
    try:
        with open("blockchain.json", "r") as f:
            cadeia = json.load(f)
    except FileNotFoundError:
        print("Erro: blockchain.json não encontrado.")
        return

    ultimo = cadeia[-1]
    novo_index = ultimo['index'] + 1
    print(f"[*] Último Bloco: #{ultimo['index']}")
    print(f"[*] Minerando Bloco #{novo_index} para o Criador...")

    # 2. Prepara a Picareta
    nonce = 0
    start = time.time()
    dados = {
        "minerador": "Dev_Anonimo", 
        "tributo_obrigatorio": CHAVE_CRIADOR
    }

    # 3. Minera (Proof of Work)
    while True:
        novo_bloco = {
            "index": novo_index,
            "timestamp": time.time(),
            "data": dados,
            "previous_hash": ultimo['hash'],
            "nonce": nonce
        }
        
        # Calcula o Hash
        bloco_string = json.dumps(novo_bloco, sort_keys=True).encode()
        hash_calc = hashlib.sha256(bloco_string).hexdigest()
        
        if hash_calc.startswith("0000"): # Dificuldade
            tempo = time.time() - start
            print(f"\n[$$$] SUCESSO EM {tempo:.2f}s!")
            print(f"Hash Encontrado: {hash_calc}")
            
            # 4. Guarda no Cofre
            cadeia.append(novo_bloco)
            with open("blockchain.json", "w") as f:
                json.dump(cadeia, f, indent=2)
                
            print("\n[!] Cofre atualizado com sucesso.")
            print("[!] AGORA: Faça o Commit e mande o Pull Request!")
            break
            
        nonce += 1

if __name__ == "__main__":
    minerar()
