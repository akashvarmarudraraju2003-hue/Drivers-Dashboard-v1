"""Reads the driver report xlsx and writes site/data.json + site/index.html."""
import sys, os, json, shutil, datetime as dt
import pandas as pd
src = sys.argv[1] if len(sys.argv) > 1 else 'driver_report.xlsx'
MASK = os.environ.get('MASK_IDS', '1') == '1'   # 1 = show only last 4 digits of driver ID
d = pd.read_excel(src)
d['duty_date'] = pd.to_datetime(d.duty_date).dt.normalize()
end = d.duty_date.max()
rows = []
for uid, g in d.groupby('user_id'):
    w = g[g.duty_date > end - pd.Timedelta(days=7)]; m = g[g.duty_date > end - pd.Timedelta(days=30)]
    ident = '…' + str(uid)[-4:] if MASK else str(uid)[-10:]
    rows.append([ident, g.fname.iloc[0], round(g.balance.sum()), round(w.balance.sum()), round(m.balance.sum()),
                 (end - g.duty_date.max()).days, round(g.cashCollected.sum() + g.qr_amount.sum()), len(g)])
piv = d.pivot_table(index='duty_date', columns='user_id', values='balance', aggfunc='sum').fillna(0).cumsum()
days = pd.date_range(d.duty_date.min(), end)
piv = piv.reindex(days).ffill().fillna(0)
owed = piv.clip(upper=0).sum(axis=1) * -1
trend = [[x.strftime('%Y-%m-%d'), round(a)] for x, a in zip(days, owed)][7:]
data = dict(end=end.strftime('%Y-%m-%d'), updated=dt.datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC'), rows=rows, trend=trend)
os.makedirs('site', exist_ok=True)
json.dump(data, open('site/data.json', 'w'), separators=(',', ':'))
shutil.copy('web/index.html', 'site/index.html')
print('drivers', len(rows), 'as of', data['end'])
