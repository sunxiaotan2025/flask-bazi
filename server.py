from flask import Flask, request, jsonify
from flask_cors import CORS  # 允许前端访问 API
import datetime
from lunarcalendar import Converter, Solar


app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})  # 允许所有域访问 API

TIANGAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
DIZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

def calculate_bazi(year, month, day, hour):
    """ 计算八字四柱（年柱、月柱、日柱、时柱） """
    year_gan = TIANGAN[(year - 4) % 10]
    year_zhi = DIZHI[(year - 4) % 12]

    solar_date = Solar(year, month, day)
    lunar_date = Converter.Solar2Lunar(solar_date)
    lunar_month = lunar_date.month
    gan_starts = [2, 4, 6, 8, 0]
    month_gan = TIANGAN[(gan_starts[TIANGAN.index(year_gan) // 2] + lunar_month - 1) % 10]
    month_zhi = DIZHI[(lunar_month + 1) % 12]

    base_date = datetime.date(1900, 1, 31)
    current_date = datetime.date(year, month, day)
    delta_days = (current_date - base_date).days
    day_gan = TIANGAN[(delta_days + 10) % 10]
    day_zhi = DIZHI[(delta_days + 12) % 12]

    hour_index = int((hour + 1) / 2) % 12
    hour_gan = TIANGAN[(TIANGAN.index(day_gan) % 5 * 2 + hour_index) % 10]
    hour_zhi = DIZHI[hour_index]

    return {
        "年柱": f"{year_gan}{year_zhi}",
        "月柱": f"{month_gan}{month_zhi}",
        "日柱": f"{day_gan}{day_zhi}",
        "时柱": f"{hour_gan}{hour_zhi}"
    }

@app.route('/api/bazi', methods=['GET'])
def get_bazi():
    """ API：获取八字计算结果 """
    year = int(request.args.get("year"))
    month = int(request.args.get("month"))
    day = int(request.args.get("day"))
    hour = int(request.args.get("hour"))

    bazi_result = calculate_bazi(year, month, day, hour)

    return jsonify(bazi_result), 200, {"Content-Type": "application/json; charset=utf-8"}

if __name__ == '__main__':
import os  # 添加这一行

port = int(os.environ.get("PORT", 5000))  # 让 Flask 使用 Render 服务器分配的端口
app.run(host="0.0.0.0", port=port, debug=True)