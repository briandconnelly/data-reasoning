import csv,datetime as dt,collections
D='/var/folders/4_/s6fbcjyn4b13xdxkd3lv0kw00000gn/T/arm-s15-pre-a2im8ufd/data/s15-assist-rollout/'
P=lambda s:dt.datetime.strptime(s,'%Y-%m-%dT%H:%M:%SZ')
inc=list(csv.DictReader(open(D+'incidents.csv')))
act={r['incident_id']:r for r in csv.DictReader(open(D+'activity.csv'))}
stf=list(csv.DictReader(open(D+'staffing.csv')))
for r in inc:
    r['opened']=P(r['opened_at']);a=act.get(r['incident_id'])
    r['closed']=P(a['closed_at']) if a and a['closed_at'] else None
    r['ttc']=(r['closed']-r['opened']).total_seconds()/3600 if r['closed'] else None
    r['rm']=float(a['responder_minutes']) if a and a['responder_minutes'] else None
    r['ho']=int(a['handoffs']) if a and a['handoffs'] else None
    r['ro']=int(a['reopened_within_72h']) if a and a['reopened_within_72h'] else None
    r['has']=a is not None
