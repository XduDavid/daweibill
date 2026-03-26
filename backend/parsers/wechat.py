"""
微信账单解析器
"""
import pandas as pd
import logging

logger = logging.getLogger(__name__)


def parse_wechat_csv(filepath):
    """
    解析微信 CSV 账单文件

    Args:
        filepath: CSV 文件路径

    Returns:
        pandas.DataFrame: 解析后的数据框

    Raises:
        Exception: 解析失败时抛出异常
    """
    try:
        # 微信 CSV 处理逻辑
        with open(filepath, encoding='utf-8-sig') as f:
            lines = f.readlines()
            header_row = None
            for i, line in enumerate(lines):
                if '交易时间' in line and '交易类型' in line:
                    header_row = i
                    break

        if header_row is None:
            raise ValueError("无法找到微信账单表头行")

        df = pd.read_csv(filepath, encoding='utf-8-sig', skiprows=header_row)

        # 映射列名
        df = df.rename(columns={
            '交易类型': '交易分类',
            '商品': '商品说明',
            '金额(元)': '金额',
            '当前状态': '交易状态',
            '支付方式': '收/付款方式'
        })

        # 清理金额列 (移除 '¥')
        df['金额'] = df['金额'].astype(str).str.replace('¥', '').str.replace(',', '').astype(float)

        # 处理时间
        df['交易时间'] = pd.to_datetime(df['交易时间'])
        df['月份'] = df['交易时间'].dt.strftime('%Y-%m')
        df['日期'] = df['交易时间'].dt.strftime('%Y-%m-%d')

        # 标记退款
        df['是否退款'] = df['交易状态'].astype(str).str.contains('退款|关闭|撤销', case=False, na=False)
        df.loc[df['是否退款'], '金额'] = -df.loc[df['是否退款'], '金额'].abs()

        # 确保必要列
        if '交易对方' not in df.columns:
            df['交易对方'] = '未知'
        if '收/支' not in df.columns:
            df['收/支'] = '/'
        if '商品说明' not in df.columns:
            df['商品说明'] = ''

        df['来源'] = '微信'

        logger.info(f"成功解析微信 CSV 账单: {len(df)} 条记录")

        return df

    except Exception as e:
        logger.error(f"解析微信 CSV 失败: {str(e)}")
        raise


def parse_wechat_xlsx(filepath):
    """
    解析微信 XLSX 账单文件

    Args:
        filepath: XLSX 文件路径

    Returns:
        pandas.DataFrame: 解析后的数据框

    Raises:
        Exception: 解析失败时抛出异常
    """
    try:
        # 先读取所有行查找表头位置（自适应支持不同版本微信导出格式）
        all_df = pd.read_excel(filepath, header=None, engine='openpyxl')
        header_row = None

        # 在前30行中查找包含关键列名的表头行
        for i in range(min(30, len(all_df))):
            row_str = str(all_df.iloc[i])
            if '交易时间' in row_str and ('金额' in row_str):
                header_row = i
                break

        if header_row is None:
            raise ValueError("不是有效的微信账单文件，无法找到表头")

        # 使用正确的表头行读取数据
        df = pd.read_excel(filepath, header=header_row, engine='openpyxl')

        # 检查是否是有效的微信账单（检查关键列，支持多种列名变种）
        if '交易时间' not in df.columns:
            raise ValueError("不是有效的微信账单文件，缺少'交易时间'列")

        # 处理金额列名的不同变体
        amount_col = None
        if '金额(元)' in df.columns:
            amount_col = '金额(元)'
        elif '金额' in df.columns:
            amount_col = '金额'

        if amount_col is None:
            raise ValueError("不是有效的微信账单文件，缺少金额列")

        # 映射列名以匹配支付宝格式
        rename_map = {
            '交易类型': '交易分类',
            '商品': '商品说明',
            '当前状态': '交易状态',
            '支付方式': '收/付款方式'
        }
        # 金额列可能有不同名称
        rename_map[amount_col] = '金额'
        df = df.rename(columns=rename_map)

        # 清理金额列 (移除 '¥' 和 ',')
        df['金额'] = df['金额'].astype(str).str.replace('¥', '').str.replace(',', '').astype(float)

        # 处理时间
        df['交易时间'] = pd.to_datetime(df['交易时间'])
        df['月份'] = df['交易时间'].dt.strftime('%Y-%m')
        df['日期'] = df['交易时间'].dt.strftime('%Y-%m-%d')

        # 标记退款
        df['是否退款'] = df['交易状态'].astype(str).str.contains('退款|关闭|撤销', case=False, na=False)
        df.loc[df['是否退款'], '金额'] = -df.loc[df['是否退款'], '金额'].abs()

        # 确保所有必要列都存在
        if '交易对方' not in df.columns:
            df['交易对方'] = '未知'
        if '收/支' not in df.columns:
            df['收/支'] = '/'
        if '商品说明' not in df.columns:
            df['商品说明'] = ''

        # 添加来源标识
        df['来源'] = '微信'

        logger.info(f"成功解析微信 XLSX 账单: {len(df)} 条记录")

        return df

    except Exception as e:
        logger.error(f"解析微信 XLSX 失败: {str(e)}")
        raise
