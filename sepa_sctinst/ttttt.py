from sepa_sctinst.sct_inst_interbank import SCTInst
from sepa_sctinst.sct_inst_c2b import SCTInstC2B

c2b_message = SCTInstC2B.random(nb_txs=4)
interbank_message = SCTInst.random()