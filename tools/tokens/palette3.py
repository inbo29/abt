from color import *
H=238
P = {
 'dark': {
  'bg':(0.205,0.012,H),'surface':(0.235,0.013,H),'surface-raised':(0.27,0.014,H),'surface-hover':(0.258,0.014,H),
  'surface-sunken':(0.19,0.011,H),'surface-selected':(0.30,0.016,H),'line':(0.325,0.014,H),'line-strong':(0.585,0.015,H),
  'ink':(0.945,0.006,H),'ink-muted':(0.765,0.015,H),'ink-faint':(0.58,0.014,H),
  'action':(0.945,0.006,H),'action-hover':(0.86,0.008,H),'on-action':(0.205,0.012,H),
  'progress':(0.765,0.105,262),'progress-soft':(0.32,0.06,262),'on-progress':(0.20,0.035,262),
  'positive':(0.80,0.12,172),'positive-soft':(0.315,0.05,172),
  'attention':(0.85,0.13,80),'attention-soft':(0.33,0.055,75),
  'critical':(0.70,0.17,24),'critical-soft':(0.30,0.07,22),'on-critical':(0.18,0.04,24),
  'chart-actual':(0.80,0.012,H),
 },
 'light': {
  'bg':(0.966,0.004,H),'surface':(1,0,0),'surface-raised':(1,0,0),'surface-hover':(0.975,0.005,H),
  'surface-sunken':(0.979,0.004,H),'surface-selected':(0.94,0.008,H),'line':(0.905,0.007,H),'line-strong':(0.615,0.014,H),
  'ink':(0.215,0.014,H),'ink-muted':(0.485,0.018,H),'ink-faint':(0.71,0.01,H),
  'action':(0.215,0.014,H),'action-hover':(0.33,0.016,H),'on-action':(1,0,0),
  'progress':(0.50,0.15,262),'progress-soft':(0.95,0.025,262),'on-progress':(1,0,0),
  'positive':(0.50,0.10,172),'positive-soft':(0.955,0.035,172),
  'attention':(0.52,0.13,75),'attention-soft':(0.965,0.058,88),
  'critical':(0.42,0.165,22),'critical-soft':(0.955,0.03,20),'on-critical':(1,0,0),
  'chart-actual':(0.42,0.014,H),
 }}
HEX = {t:{k:oklch_to_hex(*v) for k,v in d.items()} for t,d in P.items()}
def check(verbose=False):
  pairs = [
   ('ink',['bg','surface','surface-raised','surface-hover','surface-sunken','surface-selected','progress-soft','positive-soft','attention-soft','critical-soft'],4.5),
   ('ink-muted',['bg','surface','surface-raised','surface-hover','surface-sunken','surface-selected'],4.5),
   ('progress',['bg','surface','surface-raised','surface-hover','surface-sunken','progress-soft'],4.5),
   ('positive',['bg','surface','surface-raised','surface-hover','surface-sunken','positive-soft'],4.5),
   ('attention',['bg','surface','surface-raised','surface-hover','surface-sunken','attention-soft'],4.5),
   ('critical',['bg','surface','surface-raised','surface-hover','surface-sunken','critical-soft'],4.5),
   ('on-action',['action','action-hover'],4.5),
   ('on-progress',['progress'],4.5),
   ('on-critical',['critical'],4.5),
   ('line-strong',['surface','surface-sunken','surface-raised','bg','surface-selected'],3.0),
   ('chart-actual',['surface','bg'],3.0),
   ('action',['surface','bg'],3.0),
   ('attention',['surface'],3.0),('critical',['surface'],3.0),('positive',['surface'],3.0),('progress',['surface'],3.0),
  ]
  bad=0; rows=[]
  for t in HEX:
    h=HEX[t]
    for fg,bgs,need in pairs:
      for b in bgs:
        r=cr(h[fg],h[b]); rows.append((t,fg,b,r,need))
        if r<need: bad+=1; print(f"FAIL {t}: {fg} on {b} {r:.2f} < {need}")
  if verbose:
    for t,fg,b,r,need in rows: print(f"{t:5s} {fg:13s} on {b:16s} {r:5.2f} (need {need})")
  return bad
if __name__=='__main__':
  import json, sys
  print(json.dumps(HEX, indent=1))
  print('fails:', check('-v' in sys.argv))
