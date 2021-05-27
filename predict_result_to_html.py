import time

import config
from utils.datetime import get_week_day
from utils.psqldb import Psqldb

if __name__ == '__main__':
    # 获取要输出到html的tic
    config.SINGLE_A_STOCK_CODE = ['sh.600036', ]

    # 从 index.html.template 文件中 读取 网页模板
    with open('./template/index.html.template', 'r') as index_page_template:
        text_index_page_template = index_page_template.read()

        all_text_card = ''

        # 从 card_predict_result.template 文件中 读取 结果卡片 模板
        with open('./template/card_predict_result.template', 'r') as result_card_template:
            text_card = result_card_template.read()

            # psql对象
            psql_object = Psqldb(database=config.PSQL_DATABASE, user=config.PSQL_USER,
                                 password=config.PSQL_PASSWORD, host=config.PSQL_HOST, port=config.PSQL_PORT)

            for tic in config.SINGLE_A_STOCK_CODE:
                # 复制一个结果卡片模板，将以下信息 填充到卡片中
                copy_text_card = text_card

                # 获取数据库中最大日期
                sql_cmd = f'SELECT "date" FROM "public"."{tic}" ORDER BY agent, vali_period_value ASC LIMIT 1'
                max_date = psql_object.fetchone(sql_cmd)
                max_date = str(max_date[0])

                # 用此最大日期查询出一批数据
                sql_cmd = f'SELECT "id", "agent", "vali_period_value", "pred_period_name", "action", "hold", "day" ' \
                          f'FROM "public"."{tic}" WHERE "date" = \'{max_date}\' ORDER BY agent, vali_period_value ASC'

                list_result = psql_object.fetchall(sql_cmd)

                text_table_tr_td = ''

                action_list = []
                hold_list = []

                for item_result in list_result:
                    # 替换字符串内容
                    copy_text_card = copy_text_card.replace('<%tic%>', tic)
                    id1, agent1, vali_period_value1, pred_period_name1, action1, hold1, day1 = item_result

                    action_list.append(action1)
                    hold_list.append(hold1)

                    text_table_tr_td += f'<tr><td>{id1}</td><td>{agent1}</td><td>{vali_period_value1}</td>' \
                                        f'<td>{pred_period_name1}</td><td>{action1}</td>' \
                                        f'<td>{hold1}</td><td>{day1}</td></tr>'
                    pass
                pass

                # 日期
                date1 = max_date + ' ' + get_week_day(max_date)
                copy_text_card = copy_text_card.replace('<%date%>', date1)

                # 按 hold 分组，选出数量最多的 hold
                sql_cmd = f'SELECT "hold", COUNT("id") as count1 ' \
                          f'FROM "public"."{tic}" WHERE "date" = \'{max_date}\' GROUP BY "hold"' \
                          f' ORDER BY count1 DESC LIMIT 1'

                max_hold = psql_object.fetchone(sql_cmd)[0]
                copy_text_card = copy_text_card.replace('<%most_hold%>', str(max_hold))

                # 按 action 分组，取数量最多的 action
                sql_cmd = f'SELECT "action", COUNT("id") as count1 ' \
                          f'FROM "public"."{tic}" WHERE "date" = \'{max_date}\' GROUP BY "action"' \
                          f' ORDER BY count1 DESC LIMIT 1'

                max_action = psql_object.fetchone(sql_cmd)[0]
                copy_text_card = copy_text_card.replace('<%most_action%>', str(max_action))

                # 表格
                all_text_card += copy_text_card.replace('<%predict_result_table_tr_td%>', text_table_tr_td)
                all_text_card += '\r\n'
            pass
            psql_object.close()
        pass

        # 将多个 卡片模板 替换到 网页模板
        text_index_page_template = text_index_page_template.replace('<%page_content%>', all_text_card)

        current_time_point = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        text_index_page_template = text_index_page_template.replace('<%page_time_point%>', current_time_point)

        text_index_page_template = text_index_page_template.replace('<%page_title%>', 'A股预测')

        # 写入网页文件
        with open(config.INDEX_HTML_PAGE_PATH, 'w') as file_index:
            file_index.write(text_index_page_template)
            pass
        pass

    pass