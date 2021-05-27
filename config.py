
# current work directory，正在训练使用的目录，cwd: ./AgentPPO/StockTradingEnv-v1_0
# from ctypes import c_char_p
# from multiprocessing import Manager
# manager = Manager()
# CWD = manager.Value(c_char_p, "")

# CWD = './AgentPPO/StockTradingEnv-v1'
CWD = ''

AGENT_NAME = ''

PREDICT_PERIOD = ''

# 单支股票代码List
SINGLE_A_STOCK_CODE = []

# 显示预测信息
IF_SHOW_PREDICT_INFO = True

# 工作日标记，用于加载对应的weights
# weights的vali周期
VALI_DAYS_FLAG = ''

## time_fmt = '%Y-%m-%d'
START_DATE = ""
START_EVAL_DATE = ""
END_DATE = ""
# 要输出的日期
OUTPUT_DATE = ''

DATA_SAVE_DIR = f"datasets"
TRAINED_MODEL_DIR = f"trained_models"
TENSORBOARD_LOG_DIR = f"tensorboard_log"
RESULTS_DIR = f"results"
LOGGER_DIR = f"logger_log"

# batch股票数据库地址
STOCK_DB_PATH = "./" + DATA_SAVE_DIR + '/stock.db'

# ----
# PostgreSQL
PSQL_HOST = "192.168.192.1"
PSQL_PORT = "5432"
PSQL_DATABASE = "a_share"
PSQL_USER = "dyh"
PSQL_PASSWORD = "9898BdlLsdfsHsbgp"
# ----
