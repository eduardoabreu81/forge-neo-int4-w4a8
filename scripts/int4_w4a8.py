# INT4 W4A8 for Forge Neo
# Entry point: Forge Neo imports every scripts/*.py at startup, before any model loads. Any failure leaves Forge Neo
# unchanged and says so in the console.

import sys
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

try:
    import lib_int4_w4a8

    lib_int4_w4a8.register_option()
    lib_int4_w4a8.register_callbacks()
except Exception:
    print("[INT4 W4A8] failed to enable, Forge Neo is unchanged:")
    traceback.print_exc()
