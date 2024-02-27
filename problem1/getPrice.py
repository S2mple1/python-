import sys
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep


def get_currency_name(code_dict, currency_code):
    """根据货币代号查询中文名"""
    return code_dict.get(currency_code, '')


def get_date(date):
    """处理日期，将其格式化为YYYY-MM-DD"""
    return date[:4] + '-' + date[4:6] + '-' + date[6:]


def get_code_dict():
    """打开code.txt，把每一行的标准代码和中文名存入字典，方便查询"""
    with open('code.txt', 'r', encoding='utf8') as f:
        lines = f.readlines()
        code_dict = {code: name for code, name in (line.split() for line in lines)}
    return code_dict


def write_to_file(table, rows):
    """将所有表格结果写入文件"""

    with open('result.txt', 'w', encoding='utf8') as f:

        """获取并写入表头"""
        headers = table.find_elements(By.TAG_NAME, "th")
        for header in headers:
            f.write(header.text + '\t')
        f.write('\n')

        """获取并写入表格数据"""
        for row in rows:
            for col in row.find_elements(By.TAG_NAME, "td"):
                f.write(col.text + '\t\t')
            f.write('\n')


def get_sell_price(driver, date, currency_name):
    """从网站获取 现汇卖出价"""

    driver.get("https://www.boc.cn/sourcedb/whpj/")

    """"等待页面加载完成，定位class为"invest_t"的元素"""
    invest = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "invest_t")))

    """在日期输入框中输入起始时间和结束时间"""
    invest.find_element(By.ID, "erectDate").send_keys(date)
    invest.find_element(By.ID, "nothing").send_keys(date)

    """在牌价选择下拉框中选择货币名称"""
    select = Select(driver.find_element(By.ID, "pjname"))
    select.select_by_value(currency_name)

    """点击查询按钮"""
    btn = invest.find_element(By.CLASS_NAME, "search_btn")
    btn.click()

    """跳转到查询结果窗口"""
    driver.switch_to.window(driver.window_handles[-1])

    """等待1秒，让新页面加载完成"""
    sleep(1)

    """找到class为"boc_main.publish"的元素"""
    cls = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.CLASS_NAME, "boc_main.publish")))

    """获取表格元素"""
    table = cls.find_element(By.TAG_NAME, "table")

    """获取表格中的行"""
    rows = table.find_elements(By.TAG_NAME, "tr")

    """将所有表格结果写入文件"""
    write_to_file(table, rows)

    """获取表格中的列"""
    cols = rows[1].find_elements(By.TAG_NAME, "td")

    """获取现汇卖出价"""
    sell_price = cols[3].text
    return sell_price


def main():
    """获取命令行参数"""
    date, currency_code = sys.argv[1], sys.argv[2]

    """格式化日期为YYYY-MM-DD"""
    date = get_date(date)

    """构建标准代码和中文名的字典"""
    code_dict = get_code_dict()

    """根据代码查询中文名"""
    currency_name = get_currency_name(code_dict, currency_code)

    if not currency_name:
        print('货币代码不存在')
        return

    """启动Chrome浏览器"""
    driver = webdriver.Chrome()

    try:
        """获取现汇卖出价"""
        sell_price = get_sell_price(driver, date, currency_name)
        print(sell_price)

    except TimeoutException:
        print('查询超时')

    finally:
        """关闭Chrome浏览器"""
        driver.quit()


if __name__ == "__main__":
    main()
