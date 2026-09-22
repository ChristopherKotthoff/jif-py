"""python test_jif.py -- offline transform checks, plus live checks if AI_GATEWAY_API_KEY is set."""
import os
import subprocess
import sys

from jif import _variables, jif
from jif.codec import transform

# --- offline: the rewrite ---
assert transform("jif x > 5:\n    pass\n") == 'if __import__("jif").jif(\'x > 5\'):\n    pass\n'
assert "elif __import__" in transform("jif a:\n    pass\neljif b:\n    pass\n")
assert transform('s = "jif x:"\n') == 's = "jif x:"\n'  # strings untouched
assert transform("if jif('x'):\n    pass\n") == "if jif('x'):\n    pass\n"  # function form untouched
assert transform("jif d[1:2] == {'a': 1}: pass\n").startswith("if __import__(\"jif\").jif(\"d[1:2] == {'a': 1}\"): pass")
multi = transform("jif (a and\n     b):\n    pass\nboom\n")
assert multi.count("\n") == 4 and multi.splitlines()[3] == "boom"  # line numbers preserved
compile(transform(open("examples/demo.py").read()), "demo.py", "exec")


class User:
    age = 21


user, country, os_mod = User(), "CH", os
assert _variables("user.age >= 18 and country == 'CH' and os_mod", globals()) == {
    "user.age": "21", "country": "'CH'"}  # modules skipped
print("offline ok")

# --- live: actually ask Jev ---
if not os.environ.get("AI_GATEWAY_API_KEY"):
    sys.exit("live tests skipped: no AI_GATEWAY_API_KEY")

x = 10
assert jif("x > 5") is True
x = 2
assert jif("x > 5") is False
message = "I WANT MY MONEY BACK. THIS IS THE THIRD TIME I'M ASKING."
assert jif("customer_is_angry based on message")
out = subprocess.run([sys.executable, "examples/demo.py"], capture_output=True, text=True, check=True).stdout
print(out)
assert "hot" in out and "snickers" in out and "escalate" in out
print("live ok")
