from datetime import datetime

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.ticker import MaxNLocator
import matplotlib.dates as mdates

import data.transfer
import akshare as ak

def akshare_test(bondCode):
    stock_value_em_df = ak.stock_value_em(symbol=bondCode)
    print(stock_value_em_df)

def grid_moni(bondCode):
    original_data = data.transfer.getAllDayDataOfSpecificETF(bondCode)
    # 日期
    dates = original_data.iloc[:, 2]
    # 开盘价
    open_prices = original_data.iloc[:, 3]
    # 收盘价
    close_prices = original_data.iloc[:, 4]
    # 最高价
    high_prices = original_data.iloc[:, 5]
    # 最低价
    low_prices = original_data.iloc[:, 6]
    datas = {
        'dates': dates,
        'Open': open_prices,
        'Low': low_prices,
        'High': high_prices,
        'Close': close_prices
    }
    prices = pd.DataFrame(datas)
    return None


def grid_moni_1(bondCode, initial_share=20000, initial_price=None, grid_ratio=0.01, trade_share=100):
    """
    网格交易策略模拟

    参数:
    bondCode: ETF代码
    initial_share: 初始持仓份额D
    initial_price: 初始价格Z，如果为None则使用第一天开盘价
    grid_ratio: 网格比例，默认2%
    trade_share: 每次交易份额Y

    返回:
    交易记录DataFrame和最终收益
    """
    original_data = data.transfer.getAllDayDataOfSpecificETF(bondCode)

    # 构建价格DataFrame
    prices = pd.DataFrame({
        'Date': original_data.iloc[:, 2],
        'Open': original_data.iloc[:, 3],
        'Low': original_data.iloc[:, 6],
        'High': original_data.iloc[:, 5],
        'Close': original_data.iloc[:, 4]
    })

    # 初始化变量
    if initial_price is None:
        initial_price = prices['Open'].iloc[0]

    trades = []  # 记录交易
    current_shares = initial_share
    reference_price = initial_price

    # 遍历每一天的价格变动
    for _, row in prices.iterrows():
        daily_prices = []

        # 按照开盘、最低、最高、收盘价的顺序构建价格序列
        if row['Open'] != row['Low']:
            daily_prices.append(('Open', row['Open']))
        if row['Low'] != row['Open'] and row['Low'] != row['High']:
            daily_prices.append(('Low', row['Low']))
        if row['High'] != row['Open'] and row['High'] != row['Close']:
            daily_prices.append(('High', row['High']))
        if row['Close'] != row['High']:
            daily_prices.append(('Close', row['Close']))

        # 对每个价格点进行判断
        for price_type, price in daily_prices:
            # 检查上涨网格 - 卖出
            while price >= reference_price * (1 + grid_ratio):
                if current_shares >= trade_share:  # 确保有足够的份额卖出
                    new_price = reference_price * (1 + grid_ratio)
                    trades.append({
                        'Date': row['Date'],
                        'Price': new_price,
                        'Type': 'Sell',
                        'Shares': trade_share,
                        'Price_Type': price_type
                    })
                    current_shares -= trade_share
                    reference_price = new_price
                else:
                    break  # 如果没有足够份额卖出，退出循环

            # 检查下跌网格 - 买入
            while price <= reference_price * (1 - grid_ratio):
                if current_shares + trade_share <= initial_share * 10:  # 检查是否超过持仓上限
                    new_price = reference_price * (1 - grid_ratio)
                    trades.append({
                        'Date': row['Date'],
                        'Price': new_price,
                        'Type': 'Buy',
                        'Shares': trade_share,
                        'Price_Type': price_type
                    })
                    current_shares += trade_share
                    reference_price = new_price
                else:
                    break  # 如果达到持仓上限，退出循环

    # 计算收益
    trades_df = pd.DataFrame(trades)
    if len(trades) > 0:
        profit = 0
        for _, trade in trades_df.iterrows():
            if trade['Type'] == 'Sell':
                profit += trade['Shares'] * trade['Price']
            else:
                profit -= trade['Shares'] * trade['Price']

        # 加上最终持仓的市值
        final_price = prices['Close'].iloc[-1]
        profit += (current_shares - initial_share) * final_price
    else:
        profit = 0

    # 调用绘图函数时获取收益率信息
    fig, final_return, final_profit = plot_price_and_cost(prices, trades_df, initial_share, initial_price)

    # 打印交易统计信息
    print("\n====== 交易统计 ======")
    print(f"总交易次数: {len(trades_df)}")
    if len(trades_df) > 0:
        buy_trades = trades_df[trades_df['Type'] == 'Buy']
        sell_trades = trades_df[trades_df['Type'] == 'Sell']
        print(f"买入次数: {len(buy_trades)}")
        print(f"卖出次数: {len(sell_trades)}")
        print(f"初始持仓: {initial_share}份")
        print(f"当前持仓: {current_shares}份")
        print(f"初始价格: {initial_price:.4f}")
        print(f"最终价格: {prices['Close'].iloc[-1]:.4f}")
        print(f"总收益: {final_profit:.2f}")
        print(f"总收益率: {final_return:.2f}%")

        if len(buy_trades) > 0:
            avg_buy_price = buy_trades['Price'].mean()
            print(f"平均买入价: {avg_buy_price:.4f}")
        if len(sell_trades) > 0:
            avg_sell_price = sell_trades['Price'].mean()
            print(f"平均卖出价: {avg_sell_price:.4f}")
    plt.show()

    return trades_df, profit


def plot_price_and_cost(prices, trades_df, initial_share, initial_price):
    prices['Date'] = pd.to_datetime(prices['Date'])
    if len(trades_df) > 0:
        trades_df['Date'] = pd.to_datetime(trades_df['Date'])

    # 设置中文字体
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    fig, ax1 = plt.subplots(figsize=(12, 6))

    # 初始化数据
    daily_cost = []
    daily_returns = []
    daily_profit = []
    daily_shares = []  # 记录每日持仓数量

    current_shares = initial_share
    current_cost = initial_share * initial_price
    cumulative_profit = 0

    # 对每一天进行计算
    for idx, row in prices.iterrows():
        # 处理当天的交易
        if len(trades_df) > 0:
            day_trades = trades_df[trades_df['Date'] == row['Date']]

            for _, trade in day_trades.iterrows():
                if trade['Type'] == 'Buy':
                    current_cost += trade['Shares'] * trade['Price']
                    current_shares += trade['Shares']
                else:  # Sell
                    avg_cost = current_cost / current_shares
                    sell_profit = trade['Shares'] * (trade['Price'] - avg_cost)
                    cumulative_profit += sell_profit

                    # 更新成本和持仓
                    remaining_ratio = (current_shares - trade['Shares']) / current_shares
                    current_cost = current_cost * remaining_ratio
                    current_shares -= trade['Shares']

        # 记录当天的各项数据
        daily_shares.append(current_shares)

        # 计算当天的平均成本
        if current_shares > 0:
            avg_cost = current_cost / current_shares
        else:
            avg_cost = 0
        daily_cost.append(avg_cost)

        # 计算当天的收益率
        market_value = current_shares * row['Close']
        floating_profit = market_value - current_cost
        total_profit = floating_profit + cumulative_profit
        initial_value = initial_share * initial_price
        returns_pct = (total_profit / initial_value) * 100

        daily_returns.append(returns_pct)
        daily_profit.append(total_profit)

    # 绘制图表
    ax1.plot(prices['Date'], prices['Close'], label='ETF价格', color='blue', alpha=0.8)
    ax1.plot(prices['Date'], daily_cost, label='平均持仓成本', color='green', alpha=0.8)

    # 设置x轴格式
    ax1.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

    ax1.set_xlabel('时间')
    ax1.set_ylabel('价格')
    ax1.grid(True, linestyle='--', alpha=0.3)

    # 创建次坐标轴并绘制收益率
    ax2 = ax1.twinx()
    ax2.plot(prices['Date'], daily_returns, label='收益率', color='red', linestyle='--', alpha=0.8)
    ax2.set_ylabel('收益率(%)')

    # 添加图例
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='best')

    plt.title('网格交易策略模拟结果')
    fig.autofmt_xdate()
    plt.tight_layout()

    return fig, daily_returns[-1], daily_profit[-1]

def grid_trading_strategy(dates, prices, sell_threshold, buy_threshold, buy_share, sell_share, bond_code):
    # 初始化变量
    total_profit = 0
    shares = 0
    # current_base_price = base_price
    current_base_price = prices['Open'][0]
    sell_out_count = 0

    # 新建一个DataFrame来记录每天结束时持有的份额
    daily_shares = pd.DataFrame(index=dates, columns=['Shares'])

    # 遍历每日股票价格
    for index, row in prices.iterrows():
        # 按顺序处理价格变化
        daily_prices = [row['Open'], row['Low'], row['High'], row['Close']]

        for price in daily_prices:
            # 先处理卖出逻辑
            if price > current_base_price * (1 + sell_threshold):
                # 计算卖出倍数
                sell_multiple = int((price / current_base_price - 1) / sell_threshold)
                if sell_multiple > 0:
                    # 卖出
                    sell_price = price
                    profit = (sell_price - current_base_price) * sell_share * sell_multiple
                    total_profit += profit
                    shares -= sell_share * sell_multiple
                    current_base_price = sell_price  # 更新基准价
                    sell_out_count+=sell_multiple
                    break  # 卖出后跳出当前价格循环

            # 然后处理买入逻辑
            elif price < current_base_price * (1 - buy_threshold):
                # 计算买入倍数
                buy_multiple = int((current_base_price / price - 1) / buy_threshold)
                if buy_multiple > 0:
                    # 买入
                    buy_price = price
                    shares += buy_share * buy_multiple
                    current_base_price = buy_price  # 更新基准价
                    break  # 买入后跳出当前价格循环

        # 记录每天结束时持有的份额
        daily_shares.at[dates[index], 'Shares'] = shares

    # 计算年化收益率
    start_date = datetime.strptime(dates.iloc[0], '%Y-%m-%d')
    end_date = datetime.strptime(dates.iloc[-1], '%Y-%m-%d')
    days = (end_date - start_date).days
    years = days / 365.0
    initial_investment = buy_share * current_base_price
    final_value = (shares * prices['Close'].iloc[-1]) + total_profit
    annualized_return = ((final_value / initial_investment) ** (1 / years) - 1) * 100

    print(bond_code, sell_out_count, 'sell out percentage', f"{sell_out_count / len(prices['Open']):.2f}")
    print(f"年化收益率: {annualized_return:.2f}%")

    print(bond_code, sell_out_count,'sell out percentage', f"{sell_out_count / len(prices['Open']):.2f}")
    # 绘制折线图
    plt.figure(figsize=(10, 5))
    plt.plot(dates, prices['Close'], marker='o', label='价格变化')
    plt.xlabel('日期')
    plt.ylabel('价格')
    plt.title(f'价格变化')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.gca().xaxis.set_major_locator(MaxNLocator(nbins=10))
    plt.legend()
    plt.tight_layout()
    plt.show()

    # 绘制每天结束时持有的份额
    plt.figure(figsize=(10, 5))
    plt.plot(daily_shares.index, daily_shares['Shares'], marker='o', label='持有份额')
    plt.xlabel('日期')
    plt.ylabel('持有份额')
    plt.title(f'{bond_code} 每天结束时持有的份额')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.gca().xaxis.set_major_locator(MaxNLocator(nbins=10))
    plt.legend()
    plt.tight_layout()
    plt.show()
    return total_profit


def average_move_category(bondCode):
    original_data = data.transfer.getAllDayDataOfSpecificETF(bondCode)

    # 构建价格DataFrame
    prices = pd.DataFrame({
        'Date': original_data.iloc[:, 2],
        'Open': original_data.iloc[:, 3],
        'Low': original_data.iloc[:, 6],
        'High': original_data.iloc[:, 5],
        'Close': original_data.iloc[:, 4]
    })
    calculate_multiple_parameters(prices)

def calculate_multiple_parameters(prices, ma_windows=[10, 20, 30], std_devs=[1.5, 2, 2.5], initial_capital=1000000):
    """
    计算不同参数组合下的均值回归策略收益率

    参数:
    prices: DataFrame, 价格数据
    ma_windows: list, 移动平均窗口期列表
    std_devs: list, 标准差倍数列表
    initial_capital: float, 初始资金

    返回:
    DataFrame: 不同参数组合下的年化收益率和夏普比率
    """

    results = []

    for window in ma_windows:
        for std_dev in std_devs:
            # 复制价格数据
            df = prices.copy()
            df['Date'] = pd.to_datetime(df['Date'])
            df = df.sort_values('Date').reset_index(drop=True)

            # 计算移动平均和标准差
            df['MA'] = df['Close'].rolling(window=window).mean()
            df['STD'] = df['Close'].rolling(window=window).std()
            df['Upper'] = df['MA'] + std_dev * df['STD']
            df['Lower'] = df['MA'] - std_dev * df['STD']

            # 初始化变量
            position = 0
            cash = initial_capital
            trades = []
            daily_returns = []
            prev_value = initial_capital

            # 遍历价格数据
            for i in range(window, len(df)):
                current_price = df.iloc[i]['Close']
                current_date = df.iloc[i]['Date']

                # 计算当前总资产价值
                current_value = cash + position * current_price
                daily_return = (current_value - prev_value) / prev_value
                daily_returns.append(daily_return)
                prev_value = current_value

                # 计算可买入数量
                max_shares = (cash // (current_price * 100)) * 100

                # 交易逻辑
                if current_price < df.iloc[i]['Lower'] and position == 0 and max_shares > 0:
                    shares_to_buy = min(max_shares, 1000)
                    position = shares_to_buy
                    cash -= shares_to_buy * current_price
                    trades.append({
                        'Date': current_date,
                        'Type': 'Buy',
                        'Price': current_price,
                        'Shares': shares_to_buy,
                        'Cash': cash
                    })

                elif current_price > df.iloc[i]['Upper'] and position > 0:
                    cash += position * current_price
                    trades.append({
                        'Date': current_date,
                        'Type': 'Sell',
                        'Price': current_price,
                        'Shares': position,
                        'Cash': cash
                    })
                    position = 0

            # 强制平仓
            if position > 0:
                final_price = df.iloc[-1]['Close']
                cash += position * final_price
                trades.append({
                    'Date': df.iloc[-1]['Date'],
                    'Type': 'Sell',
                    'Price': final_price,
                    'Shares': position,
                    'Cash': cash
                })

            # 计算收益指标
            total_days = (df.iloc[-1]['Date'] - df.iloc[window]['Date']).days
            total_return = (cash - initial_capital) / initial_capital
            annual_return = (1 + total_return) ** (365 / total_days) - 1

            # 计算夏普比率
            daily_returns = np.array(daily_returns)
            annual_volatility = np.std(daily_returns) * np.sqrt(252)
            risk_free_rate = 0.03  # 假设无风险利率为3%
            sharpe_ratio = (annual_return - risk_free_rate) / annual_volatility if annual_volatility != 0 else 0

            # 计算最大回撤
            cumulative_returns = np.cumprod(1 + daily_returns)
            running_max = np.maximum.accumulate(cumulative_returns)
            drawdowns = (running_max - cumulative_returns) / running_max
            max_drawdown = np.max(drawdowns) * 100

            # 统计交易次数
            trade_count = len(trades)

            results.append({
                'MA_Window': window,
                'STD_Dev': std_dev,
                'Annual_Return(%)': annual_return * 100,
                'Sharpe_Ratio': sharpe_ratio,
                'Max_Drawdown(%)': max_drawdown,
                'Trade_Count': trade_count
            })

    # 创建结果DataFrame
    results_df = pd.DataFrame(results)
    results_df = results_df.sort_values('Annual_Return(%)', ascending=False)
    return results_df

# 使用示例:
# ma_windows = [10, 15, 20, 25, 30]
# std_devs = [1.5, 2.0, 2.5, 3.0]
# results = calculate_multiple_parameters(prices, ma_windows, std_devs)
# print(results)