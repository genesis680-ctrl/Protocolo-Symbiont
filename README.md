# Protocolo-Symbiont
#   Symbiont Protocol
> **Decentralized Consensus via Parasitic Infrastructure and Proof of Publication (PoP).**

Symbiont is a distributed architecture experiment that implements a functional, serverless blockchain by utilizing GitHub as a persistence layer and GitHub Actions as a deterministic validation oracle.

---

##   System Architecture

Unlike traditional blockchains that rely on expensive, always-online P2P nodes, Symbiont operates as a benign "parasite" within existing CI/CD infrastructure.

1.  **Immutable Ledger:** Git's commit history functions as the block chain.
2.  **Consensus (Proof of Merge):** Validation is not performed by voting nodes, but through algorithmic auditing executed via GitHub Actions.
3.  **Proof of Work (PoW):** Mining occurs client-side (Python) to prevent spam, requiring a SHA-256 hash with dynamic difficulty.

##  The Cycle

1.  **Mining (Client-Side):** The `miner.py` script downloads the current ledger state (`blockchain.json`), calculates the next valid hash, and updates the file locally.
2.  **Propagation (Pull Request):** The miner submits a PR with the new block.
3.  **Auditing (Server-Side):** The `validador.yml` Workflow is triggered automatically. It runs the audit script to verify:
    * Hash Integrity (PoW).
    * Correct Chaining (Previous Hash).
    * Protocol Fee Signature.
4.  **Finalization (Merge):** If the Action returns "Success" (Green), the block is accepted and merged into the main branch, becoming the official truth.

##   How to Mine (Join the Network)

You only need Python installed. No heavy dependencies required.

1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/genesis680-ctrl/Protocolo-Symbiont](https://github.com/genesis680-ctrl/Protocolo-Symbiont)
   cd Protocolo-Symbiont
