   # Task-01 Terminal Voyage
   
   Level 1 - Loguetown Reef
   Command: chmod +x sector_C/devil_fruit_3.txt
   Then: ./eat.sh sector_C/devil_fruit_3.txt
   Flag: ONE_PIECE{GITO_GITO_NO_AWAKENING}
   
   Learnings: cd, ls, chmod, running shell scripts

  ## Level 2: Whiskey Peak - commit 0c60b00
**Commands:**
git checkout 0c60b00
ls -la GrandLine/Whiskey_Peak/
cat .baroque_dial

## Level 3: Little Garden - commit a802662
**Commands:**
git checkout a802662
find GrandLine/Little_Garden -type f | wc -l

**Found:** BAROQUE_DIAL flag + PONEGLYPH_FRAGMENT_I
Fragment I: `KjY2MjF4bW0lkZyQyNyBsIS0vbTAtJTcnL`
**Note:** Direct base64 decode gave *6621xmoe garbage - indicates XOR protection

## Level 4: Water 7 - commit f0e51c0
**Commands:**

git checkout f0e51c0
ls GrandLine/Water_7/
file puffing_tom_blueprints
tar -xvf puffing_tom_blueprints
unzip step1_blueprints.zip
cat blueprints_extracted/secret_link.txt
cat hull_design/frame_specs.dat

**Found:** Fragment II: `SwnbzptDiM3JSpvFiMuJ28PJzAlJ28VIzA=`
DECOY_DATA_01 was fake lead.

## Level 5: Enies Lobby - commit d4e7bf5 (FINAL VAULT)
**Commands:**
git checkout d4e7bf5
cat GrandLine/Enies_Lobby/.cp9_secure_vault/poneglyph.py

**File showed:** `base64.b64decode(input) ^ 0x42`
**Final decode:**
```python
import base64
f1="KjY2MjF4bW0lkZyQyNyBsIS0vbTAtJTcnL"
f2="SwnbzptDiM3JSpvFiMuJ28PJzAlJ28VIzA="
full=f1+f2
print(bytes(b ^ 0x42 for b in base64.b64decode(full)).decode())





