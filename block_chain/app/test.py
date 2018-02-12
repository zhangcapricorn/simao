import time
import textwrap
from util import draw_detail
from util import draw_list
from util import select_from_db
from util import cut_out_word

if __name__ == "__main__":
    sql = "select date, title, summary from block_chain where id in (%s)" % ('1, 2, 100, 1111, 2111')
    result = [[i[0], i[1].strip(), i[2].strip()]for i in select_from_db(sql)]
    time_stmp = int(time.time())
    draw_list(result, time_stmp)
    for i in range(0, len(result)):
        draw_detail(result[i], i, time_stmp)

