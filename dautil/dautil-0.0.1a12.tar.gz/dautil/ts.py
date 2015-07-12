def groupby_yday(df):
    return df.groupby(lambda d: d.timetuple().tm_yday)

def groupby_month(df):
    return df.groupby(df.index.month)
