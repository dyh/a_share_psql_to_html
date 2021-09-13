import time

import config
from utils.date_time import get_week_day
from utils.psqldb import Psqldb

if __name__ == '__main__':
    # 从 index.html.template 文件中 读取 网页模板
    with open('./template/index.html.template', 'r') as index_page_template:
        text_index_page_template = index_page_template.read()

        all_text_card = ''

        # 从 card_predict_result.template 文件中 读取 结果卡片 模板
        with open('./template/card_predict_summary.template', 'r') as result_card_template:

            # 交易详情
            text_trade_detail = ''

            text_card = result_card_template.read()

            # psql对象
            psql_object = Psqldb(database=config.PSQL_DATABASE, user=config.PSQL_USER,
                                 password=config.PSQL_PASSWORD, host=config.PSQL_HOST, port=config.PSQL_PORT)

            table_name = 'predict_summary'

            # for tic in config.BATCH_A_STOCK_CODE:
            # 复制一个结果卡片模板，将以下信息 填充到卡片中
            copy_text_card = text_card

            # # 获取数据库中最大hold，最大action，用于计算百分比
            # sql_cmd = f'SELECT abs("hold") FROM "public"."{table_name}" ORDER BY abs("hold") DESC LIMIT 1'
            # max_hold = psql_object.fetchone(sql_cmd)
            # max_hold = max_hold[0]
            #
            # # max_action
            # sql_cmd = f'SELECT abs("action") FROM "public"."{table_name}" ORDER BY abs("action") DESC LIMIT 1'
            # max_action = psql_object.fetchone(sql_cmd)
            # max_action = max_action[0]

            # 获取数据库中最大日期
            sql_cmd = f'SELECT "date" FROM "public"."{table_name}" ORDER BY "date" DESC LIMIT 1'
            max_date = psql_object.fetchone(sql_cmd)
            max_date = str(max_date[0])

            # 用此最大日期查询出一批数据
            sql_cmd = f'SELECT ROW_NUMBER() OVER() as rownum, "tic", "name", "date", "agent", "vali_period_value", ' \
                      f'"pred_period_name", "action", "hold", "day", "episode_return", "max_return", "trade_detail" ' \
                      f' FROM "public"."{table_name}" WHERE "date" = \'{max_date}\' ORDER BY episode_return DESC'

            list_result = psql_object.fetchall(sql_cmd)

            text_table_tr_td = ''

            for item_result in list_result:

                # 替换字符串内容
                # copy_text_card = copy_text_card.replace('<%tic%>', tic)
                # copy_text_card = copy_text_card.replace('<%tic_no_dot%>', tic.replace('.', ''))

                id1, tic1, name1, date1, agent1, vali_period_value1, pred_period_name1, action1, hold1, day1, episode_return1, max_return1, trade_detail1 = item_result

                # <%day%>
                # copy_text_card = copy_text_card.replace('<%day%>', str(day1))

                # # 改为百分比
                # if max_action != 0:
                #     action1 = round(action1 * 100 / max_action, 0)
                #     hold1 = round(hold1 * 100 / max_hold, 0)
                # else:
                #     action1 = 0
                #     hold1 = 0
                # pass

                action1 = round(action1, 0)
                hold1 = round(hold1, 0)

                # agent1
                agent1 = agent1[5:]

                # 回报，百分比
                episode_return1 = round((episode_return1 - 1) * 100, 2)
                max_return1 = round((max_return1 - 1) * 100, 2)

                text_table_tr_td += f'<tr>' \
                                    f'<td>{tic1}</td>' \
                                    f'<td>{name1}</td>' \
                                    f'<td>{action1}</td>' \
                                    f'<td>{hold1}</td>' \
                                    f'<td>{agent1}</td>' \
                                    f'<td>{vali_period_value1}</td>' \
                                    f'<td>{day1}</td>' \
                                    f'<td>{pred_period_name1}</td>' \
                                    f'<td>{episode_return1}%</td>' \
                                    f'<td>{max_return1}%</td>' \
                                    f'</tr>'

                # 交易详情，trade_detail1，保存为独立文件
                text_trade_detail += f'\r\n{"-" * 20} {agent1} {vali_period_value1}天 {"-" * 20}\r\n'
                text_trade_detail += f'{episode_return1}% / {max_return1}% ' \
                                     f' {action1} ' \
                                     f' {hold1} ' \
                                     f' {agent1} ' \
                                     f' {vali_period_value1}天 ' \
                                     f' 第{day1}/{pred_period_name1}天\r\n'

                text_trade_detail += '\r\n交易详情\r\n\r\n'
                text_trade_detail += trade_detail1
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
        date1 = max_date + ' ' + get_week_day(max_date)
        text_index_page_template = text_index_page_template.replace('<%date%>', date1)

        current_time_point = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        text_index_page_template = text_index_page_template.replace('<%page_time_point%>', current_time_point)

        text_index_page_template = text_index_page_template.replace('<%page_title%>', 'A股决策')

        if text_trade_detail is not '':
            # 写入交易详情文件
            detail_file_path = config.INDEX_HTML_PAGE_PATH.replace('index.html', f'trade_detail.txt')

            with open(detail_file_path, 'w') as file_detail:
                file_detail.write(text_trade_detail)
                pass
            pass
            text_trade_detail = ''
        pass

        # 写入网页文件
        with open(config.INDEX_HTML_PAGE_PATH, 'w') as file_index:
            file_index.write(text_index_page_template)
            pass
        pass

    pass
