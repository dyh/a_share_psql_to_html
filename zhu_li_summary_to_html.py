import time

import config
from utils.date_time import get_week_day
from utils.psqldb import Psqldb

if __name__ == '__main__':
    # 从 index.html.template 文件中 读取 网页模板
    with open('./template/zhu_li.html.template', 'r', encoding='utf-8') as index_page_template:
        text_index_page_template = index_page_template.read()

        all_text_card = ''

        # 从 card_predict_result.template 文件中 读取 结果卡片 模板
        with open('./template/card_zhu_li_summary.template', 'r', encoding='utf-8') as result_card_template:

            text_card = result_card_template.read()

            # psql对象
            psql_object = Psqldb(database=config.PSQL_DATABASE, user=config.PSQL_USER,
                                 password=config.PSQL_PASSWORD, host=config.PSQL_HOST, port=config.PSQL_PORT)

            table_name = 'zhu_li_summary'

            # for tic in config.BATCH_A_STOCK_CODE:
            # 复制一个结果卡片模板，将以下信息 填充到卡片中
            copy_text_card = text_card

            # # 获取数据库中最大日期
            # sql_cmd = f'SELECT "date" FROM "public"."{table_name}" ORDER BY "date" DESC LIMIT 1'
            # max_date = psql_object.fetchone(sql_cmd)
            # max_date = str(max_date[0])

            # 用此最大日期查询出一批数据
            sql_cmd = f'SELECT ROW_NUMBER() OVER() as rownum, "tic", "name", "industry", "date", "jin_chang", ' \
                      f'"xi_pan", "chu_huo", "wu_kong_pan", "kai_shi_kong_pan", "you_zhuang_kong_pan", ' \
                      f'"day200", "day100", "day50", "days_avg", "volume", "amount", "turn", "pct_chg" ' \
                      f' FROM "public"."{table_name}" ORDER BY jin_chang DESC'

            list_result = psql_object.fetchall(sql_cmd)

            text_table_tr_td = ''

            for item_result in list_result:

                _, tic, name, industry, date, jin_chang, xi_pan, chu_huo, wu_kong_pan, kai_shi_kong_pan, you_zhuang_kong_pan, day200, day100, day50, days_avg, volume, amount, turn, pct_chg = item_result

                jin_chang = round(jin_chang, 2)
                xi_pan = round(xi_pan, 2)
                chu_huo = round(chu_huo, 2)
                wu_kong_pan = round(wu_kong_pan, 2)
                kai_shi_kong_pan = round(kai_shi_kong_pan, 2)
                you_zhuang_kong_pan = round(you_zhuang_kong_pan, 2)

                day200 = round(day200, 2)
                day100 = round(day100, 2)
                day50 = round(day50, 2)
                days_avg = round(days_avg, 2)

                volume = round(volume, 0)
                amount = round(amount, 0)

                turn = round(turn, 2)
                pct_chg = round(pct_chg, 2)

                text_table_tr_td += f'<tr>' \
                                    f'<td>{tic}</td>' \
                                    f'<td>{name}</td>' \
                                    f'<td>{industry}</td>' \
                                    f'<td>{date}</td>' \
                                    f'<td>{jin_chang}</td>' \
                                    f'<td>{xi_pan}</td>' \
                                    f'<td>{chu_huo}</td>' \
                                    f'<td>{wu_kong_pan}</td>' \
                                    f'<td>{kai_shi_kong_pan}</td>' \
                                    f'<td>{you_zhuang_kong_pan}</td>' \
                                    f'<td>{day200}</td>' \
                                    f'<td>{day100}</td>' \
                                    f'<td>{day50}</td>' \
                                    f'<td>{days_avg}</td>' \
                                    f'<td>{volume}</td>' \
                                    f'<td>{amount}</td>' \
                                    f'<td>{turn}%</td>' \
                                    f'<td>{pct_chg}%</td>' \
                                    f'</tr>'

                pass
            pass

            # 表格
            all_text_card += copy_text_card.replace('<%predict_result_table_tr_td%>', text_table_tr_td)
            all_text_card += '\r\n'

            pass
            psql_object.close()
        pass

        # 将多个 卡片模板 替换到 网页模板
        text_index_page_template = text_index_page_template.replace('<%page_content%>', all_text_card)

        # 日期
        # date1 = max_date + ' ' + get_week_day(max_date)
        text_index_page_template = text_index_page_template.replace('<%date%>', '')

        current_time_point = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        text_index_page_template = text_index_page_template.replace('<%page_time_point%>', current_time_point)

        text_index_page_template = text_index_page_template.replace('<%page_title%>', '主力控盘')

        # 写入网页文件
        with open(config.INDEX_HTML_PAGE_PATH, 'w', encoding='utf-8') as file_index:
            file_index.write(text_index_page_template)
            pass
        pass

    pass
