__VERSION__ = '0.10'

# PORT = 50054
#
# DATABASE = "wasureji.db"

'''
wasureji.json
{
    "host" : "192.168.0.xx",    # or null
    "port" : 50054,
    "database" : "wasureji.db",
    "directory" : "c:\\document\\yyyyyyyy",
    "excel_file" : "wasureji.xlsx",
    "excel_sheet" : "wasureji"
}
'''


PING     = "ping"

KILL     = "kill"
SQL      = "sql :"
COMMIT   = "commit"
ROLLBACK = "rollback"

ASK_FILE = "file?"
INS_FILE = "file>"
REP_FILE = "file$"
DEL_FILE = "file<"

ASK_DOC  = "doc ?"
ASK_CUST = "cust?"
ASK_SECT = "sect?"

ASK_IN   = "in  ?"
INS_IN   = "in  >"
REP_IN   = "in  $"
DEL_IN   = "in  <"

ASK_OUT  = "out ?"
INS_OUT  = "out >"
REP_OUT  = "out $"
DEL_OUT  = "out <"  # ファイル指定　~~項目　全指定~~

ASK_IN_ORIGIN = "ino ?"
ASK_IN_BY     = "inb ?"
ASK_OUT_DELIV = "outd?"
ASK_OUT_BY    = "outb?"

ASK_HISTORY   = "hist?"