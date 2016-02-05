#######################
# PATTERN | CHARACTER #
# +-+-+   | A         #
# +-+--   | B         #
# -+--+   | C         #
# +-+-    | D         #
# -+-+    | E         #
# -+--    | F         #
# --+-    | G         #
# +-+     | H         #
# +--     | I         #
# -+-     | J         #
# --+     | K         #
# --      | L         #
# -+      | M         #
# +-      | N         #
# ++      | O         #
# -       | P         #
# +       | Q         #
#######################


cat $1 | sed 's/+-+-+/A/g' | sed 's/+-+--/B/g' | sed 's/-+--+/C/g' | sed 's/+-+-/D/g' | sed 's/-+-+/E/g' | sed 's/-+--/F/g' | sed 's/--+-/G/g' | sed 's/+-+/H/g' | sed 's/+--/I/g' | sed 's/-+-/J/g' | sed 's/--+/K/g' | sed 's/--/L/g' | sed 's/-+/M/g' | sed 's/+-/N/g' | sed 's/++/O/g' | sed 's/-/P/g' | sed 's/+/Q/g' | tr -s "\n"
