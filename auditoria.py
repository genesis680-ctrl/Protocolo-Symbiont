import json
import hashlib
import sys
import os

# --- A SUA CHAVE (NINGUÉM TOCA AQUI) ---
CHAVE_MESTRA = "f31325e573a30a0d3efdc8c3c245d8348eaa5e4858a10e98c0ac933ed9e6ec2a84b3f771eaca75fc7eb2f893cf44ae9a6b3b7c36e29072f1e8e9d08ca2ef9ad4"

def auditar_cadeia():
    print("--- INICIANDO AUDITORIA SYMBIONT ---")
    
    if not os.path.exists("blockchain.json"):
        print("Blockchain não encontrada.")
        return True

    with open("blockchain.json", "r") as f:
        cadeia = json.load(f)

    # Verifica apenas o último bloco (o mais recente)
    ultimo = cadeia[-1]
    
    # REGRA 1: É o Gênese? Se for, passa.
    if ultimo['index'] == 0:
        print("Gênese detectado.")
        return True

    # REGRA 2: Pagou o tributo?
    tributo = ultimo['data'].get('tributo_obrigatorio')
    if tributo != CHAVE_MESTRA:
        print(f"[CRIME] O bloco #{ultimo['index']} não pagou o tributo ao Criador!")
        sys.exit(1) # Trava o sistema e rejeita o bloco
        
    print(f"[SUCESSO] Bloco #{ultimo['index']} validado. Tributo pago.")

if __name__ == "__main__":
    auditar_cadeia()

