def calc_roc(df):
    assert isinstance(df, pd.DataFrame),"Need a pd.DataFrame"
    assert df.columns.size == 2,"Need two columns (x = cumsum_denomi_pct) and (y = cumsum_impact_pct)"

    s = 0 #曲线下面积
    s_temp = 0

    counter = 0 # 计数器
    for row_index,row in df.iterrows():
        if counter == 0:
            s_temp = (0 + row[1]) * (row[0] - 0) * 0.5
        else:
            s_temp = (pre_cumsum_impact_pct + row[1]) * (row[0] - pre_cumsum_denomi_pct) * 0.5

        s = s + s_temp # 累计曲线下面积
        counter = counter + 1 
        
        pre_cumsum_denomi_pct = row[0] # 记录下上一次的值
        pre_cumsum_impact_pct = row[1]

    return s

def calc_var_importance(df):
    assert isinstance(df, pd.DataFrame),"Need a pd.DataFrame"
    assert df.columns.size == 4,"Need four columns (denomi_start,denomi_end,rate_start,rate_end"

    # 总体的rate
    rate_all_start = sum(df.denomi_start * df.rate_start)
    rate_all_end = sum(df.denomi_end * df.rate_end)

    # vector impact_rate,impact_struct,impact_all
    # 每个分量的影响
    impact_rate = (a.rate_end - a.rate_start) * a.denomi_start
    impact_struct = (a.denomi_end - a.denomi_start) * (a.rate_end - rate_all_start)
    impact_all = impact_rate + impact_struct

    
    df['impact_rate'] = impact_rate
    df['impact_struct'] = impact_struct
    df['impact_all'] = impact_all

    # 所有影响分量的加总应该等于总影响
    impart_all_total = sum(df.impact_all)

    # 每个分量上影响的占比占总影响的比例
    df['impact_all_percent'] = df.impact_all / impart_all_total
    df['impact_all_percent_per_denomi'] = df.impact_all_percent / df.denomi_start

    # 按照单位分母对影响度的贡献程度排序
    a_sorted = df.sort_values(by = "impact_all_percent_per_denomi",ascending=False)
    a_sorted['impact_all_percent_cumsum'] = a_sorted['impact_all_percent'].cumsum()
    a_sorted['denomi_start_cumsum'] = a_sorted['denomi_start'].cumsum()

    # plot the Roc pic
    # a_sorted.plot('denomi_start_cumsum','impact_all_percent_cumsum')
    
    return calc_roc(a_sorted[['denomi_start_cumsum','impact_all_percent_cumsum']])

    
            
