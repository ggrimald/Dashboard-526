import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np
import warnings

warnings.filterwarnings('ignore')

st.set_page_config(layout="wide")
st.title("PROTOCOL : RECHARGE")

url="https://mygame1-cfc60-default-rtdb.firebaseio.com/.json"
response=requests.get(url)
data=response.json()

rows=[]
for session_id,session_data in data.items():
	if not isinstance(session_data,dict):
		continue
	for event_type,event_list in session_data.items():
		if not isinstance(event_list,list):
			continue
		for i,event in enumerate(event_list):
			if not isinstance(event,dict):
				continue
			row={"session_id":session_id,"event_type":event_type,"index":i}
			row.update(event)
			rows.append(row)

df=pd.DataFrame(rows)
df.to_parquet("analytics_clean.parquet",index=False)

energy_df=df[df['event_type']=='PlayerHealthUpdate'].copy()
energy_df['delta']=energy_df['m_NewValue']-energy_df['m_OldValue']
energy_by_source=(energy_df.groupby('m_InstigatorClassName')['delta'].sum().drop('Player_V2',errors='ignore').sort_values())

death_df=df[df['event_type']=='PlayerDeathEvent']
death_counts=death_df['m_InstigatorClassName'].value_counts()

shoot_df=df[df['event_type'].isin(['PlayerHipFireStart','PlayerReloadStart'])].copy()
shoot_df['level_group']=shoot_df['m_LevelName'].replace({'TutorialLevel':'Tutorial','BuildingScene':'Level 1'})
shooting_by_level=(shoot_df.groupby(['level_group','event_type']).size().unstack(fill_value=0).reindex(['Tutorial','Level 1']))
shooting_by_level=shooting_by_level.rename(columns={'PlayerHipFireStart':'Shots','PlayerReloadStart':'Reloads'})

shots=shooting_by_level['Shots'].sum() if 'Shots' in shooting_by_level.columns else 0
reloads=shooting_by_level['Reloads'].sum() if 'Reloads' in shooting_by_level.columns else 0
total_sessions=df['session_id'].nunique() if 'session_id' in df.columns else 'N/A'
total_deaths=len(death_df)
ratio_str=f'{shots/reloads:.1f}×' if reloads>0 else 'N/A'

BG='#ffffff'
BG2='#f5f5f5'
BG3='#eeeeee'
TEXT='#111111'
MUTED='#666666'
ACCENT='#00a572'
RED='#e03030'
PURPLE='#5560dd'
AMBER='#d4860a'
BORDER='#cccccc'

plt.rcParams.update({'figure.facecolor':BG,'axes.facecolor':BG2,'axes.edgecolor':BORDER,'axes.labelcolor':MUTED,'axes.titlecolor':TEXT,'xtick.color':MUTED,'ytick.color':MUTED,'text.color':TEXT,'grid.color':BORDER,'grid.linestyle':'--','grid.linewidth':0.5,'grid.alpha':0.7,'font.family':'DejaVu Sans Mono','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'axes.spines.left':False,'axes.spines.bottom':False})

def card_bg(ax):
	for spine in ax.spines.values():
		spine.set_visible(False)
	ax.set_facecolor(BG2)
	ax.tick_params(colors=MUTED,length=0)
	ax.yaxis.grid(True,linestyle='--',linewidth=0.4,color=BORDER,alpha=0.8)
	ax.set_axisbelow(True)

fig=plt.figure(figsize=(18,21),facecolor=BG)
fig.patch.set_facecolor(BG)
fig.subplots_adjust(left=0.04,right=0.98,top=0.95,bottom=0.03)

gs=gridspec.GridSpec(nrows=5,ncols=3,figure=fig,height_ratios=[0.30,0.60,2.25,2.05,3.35],hspace=0.34,wspace=0.24)

ax_title=fig.add_subplot(gs[0,:])
ax_title.set_facecolor(BG)
ax_title.axis('off')
ax_title.axhline(y=0.98,xmin=0.0,xmax=1.0,color=ACCENT,linewidth=2.5,alpha=0.9)
ax_title.text(0.5,0.50,'PROTOCOL : RECHARGE',transform=ax_title.transAxes,ha='center',va='center',fontsize=28,fontweight='bold',color=TEXT,fontfamily='DejaVu Sans Mono')

kpi_gs=gs[1,:].subgridspec(1,3,wspace=0.18)
kpi_defs=[('TOTAL SESSIONS',str(total_sessions),ACCENT),('TOTAL DEATHS',str(total_deaths),RED),('SHOT / RELOAD',ratio_str,AMBER)]

for i,(label,value,color) in enumerate(kpi_defs):
	ax_k=fig.add_subplot(kpi_gs[0,i])
	ax_k.set_facecolor(BG3)
	ax_k.axis('off')
	ax_k.axhline(y=0.97,xmin=0.04,xmax=0.96,color=color,linewidth=2,alpha=0.9)
	rect=FancyBboxPatch((0.01,0.01),0.98,0.96,boxstyle='round,pad=0.01',linewidth=0.8,edgecolor=BORDER,facecolor=BG3,transform=ax_k.transAxes)
	ax_k.add_patch(rect)
	ax_k.text(0.5,0.72,value,transform=ax_k.transAxes,ha='center',va='center',fontsize=22,fontweight='bold',color=color,fontfamily='DejaVu Sans Mono')
	ax_k.text(0.5,0.25,label,transform=ax_k.transAxes,ha='center',va='center',fontsize=8,color=MUTED,fontfamily='DejaVu Sans Mono')

ax1=fig.add_subplot(gs[2,:])
card_bg(ax1)
bar_colors=[ACCENT if v>=0 else RED for v in energy_by_source.values]
bars=ax1.bar(energy_by_source.index,energy_by_source.values,color=[c+'cc' for c in bar_colors],edgecolor=bar_colors,linewidth=0.8,width=0.55,zorder=3)
ax1.axhline(0,color=BORDER,linewidth=1,zorder=2)

for bar,val in zip(bars,energy_by_source.values):
	va='bottom' if val>=0 else 'top'
	off=15 if val>=0 else -15
	ax1.text(bar.get_x()+bar.get_width()/2,val+off,f'{int(val):+d}',ha='center',va=va,fontsize=9,color=ACCENT if val>=0 else RED,fontfamily='DejaVu Sans Mono',fontweight='bold')

ax1.set_title('M1 - ENERGY CHANGE BY SOURCE',loc='left',fontsize=13,fontweight='bold',color=MUTED,fontfamily='DejaVu Sans Mono',pad=12)
ax1.set_ylabel('Energy',fontsize=9,color=MUTED)
ax1.tick_params(axis='x',labelsize=9,rotation=15)
ax1.margins(x=0.05)
ax1.legend(handles=[mpatches.Patch(color=ACCENT,label='Energy gain'),mpatches.Patch(color=RED,label='Energy loss')],loc='lower right',frameon=False,labelcolor=MUTED,fontsize=9)

mid_gs=gs[3,:].subgridspec(1,2,wspace=0.22)

ax2=fig.add_subplot(mid_gs[0,0])
card_bg(ax2)
death_colors=[RED,AMBER,PURPLE,MUTED]
dc=death_colors[:len(death_counts)]
wedges,texts,autotexts=ax2.pie(death_counts.values,labels=death_counts.index,colors=[c+'dd' for c in dc],autopct='%1.0f%%',pctdistance=0.78,labeldistance=1.05,startangle=140,wedgeprops=dict(width=0.55,edgecolor=BG,linewidth=2))

for t in texts:
	t.set_fontsize(8)
	t.set_color(MUTED)
	t.set_fontfamily('DejaVu Sans Mono')
for t in autotexts:
	t.set_color(TEXT)
	t.set_fontsize(9)
	t.set_fontfamily('DejaVu Sans Mono')

ax2.text(0,0,str(total_deaths),ha='center',va='center',fontsize=20,fontweight='bold',color=TEXT,fontfamily='DejaVu Sans Mono')
ax2.text(0,-0.22,'deaths',ha='center',va='center',fontsize=8,color=MUTED,fontfamily='DejaVu Sans Mono')
ax2.set_title('M2 - PLAYER DEATH CAUSES',loc='left',fontsize=13,fontweight='bold',color=MUTED,fontfamily='DejaVu Sans Mono',pad=12)

ax3=fig.add_subplot(mid_gs[0,1])
card_bg(ax3)
x=np.arange(len(shooting_by_level.index))
width=0.35
shots_vals=shooting_by_level['Shots'].values if 'Shots' in shooting_by_level.columns else np.zeros(len(shooting_by_level))
reloads_vals=shooting_by_level['Reloads'].values if 'Reloads' in shooting_by_level.columns else np.zeros(len(shooting_by_level))

b1=ax3.bar(x-width/2,shots_vals,width=width,color=PURPLE+'cc',edgecolor=PURPLE,linewidth=0.8,label='Shots',zorder=3)
b2=ax3.bar(x+width/2,reloads_vals,width=width,color=AMBER+'cc',edgecolor=AMBER,linewidth=0.8,label='Reloads',zorder=3)

for bar in list(b1)+list(b2):
	val=bar.get_height()
	ax3.text(bar.get_x()+bar.get_width()/2,val+max(shots_vals.max() if len(shots_vals) else 0,reloads_vals.max() if len(reloads_vals) else 0)*0.02,f'{int(val)}',ha='center',va='bottom',fontsize=11,fontweight='bold',color=TEXT,fontfamily='DejaVu Sans Mono')

ax3.set_xticks(x)
ax3.set_xticklabels(shooting_by_level.index,fontsize=9,fontfamily='DejaVu Sans Mono')
ax3.set_title('M3 - SHOOTING ACTIVITY BY LEVEL',loc='left',fontsize=13,fontweight='bold',color=MUTED,fontfamily='DejaVu Sans Mono',pad=12)
ax3.set_ylabel('Count',fontsize=9,color=MUTED)
ax3.legend(loc='upper right',frameon=False,labelcolor=MUTED,fontsize=9)

heat_outer=gs[4,:].subgridspec(2,1,height_ratios=[0.18,0.82],hspace=0.04)

ax4_title=fig.add_subplot(heat_outer[0,0])
ax4_title.axis('off')
ax4_title.set_facecolor(BG)
ax4_title.text(0.5,0.68,'M4 - SPATIAL COMBAT HEATMAPS (DAMAGE VS SHOOTING)',ha='center',va='center',fontsize=14,fontweight='bold',color=MUTED,fontfamily='DejaVu Sans Mono')
ax4_title.text(0.5,0.22,'Blue = Shooting | Red = Damage taken | Purple = Both events',ha='center',va='center',fontsize=10,color=MUTED,fontfamily='DejaVu Sans Mono')

heat_gs=heat_outer[1,0].subgridspec(1,2,wspace=0.22)

ax4a=fig.add_subplot(heat_gs[0,0])
ax4b=fig.add_subplot(heat_gs[0,1])

for ax_h,label,img_path in [(ax4a,'Tutorial','Tutorial-Level.png'),(ax4b,'Level-1','Level-1.png')]:
	ax_h.set_facecolor(BG2)
	ax_h.set_xticks([])
	ax_h.set_yticks([])
	img=plt.imread(img_path)
	ax_h.imshow(img,aspect='auto')
	ax_h.set_title(label,fontsize=11,fontweight='bold',color=MUTED,fontfamily='DejaVu Sans Mono',pad=8)

st.pyplot(fig)