# m h  dom mon dow   command
# */60 * * * * bash ~/workspace/a_share_psql_to_html/cron_psql_to_html.sh

ps -ef|grep predict_summary_to_html.py|grep -v grep|cut -c 9-15|xargs kill -9
cd ~/workspace/a_share_psql_to_html/
source venv/bin/activate
python predict_summary_to_html.py
