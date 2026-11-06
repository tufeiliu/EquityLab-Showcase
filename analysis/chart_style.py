"""Shared chart palette, so each strategy keeps one colour in every figure.

Colours come from the ggsci NEJM palette for R (New England Journal of Medicine style),
with a neutral grey for T-bills, on a white background. Line charts also use dashes to
help separate series, and bar charts rely on direct labels.
"""
import matplotlib as mpl

SURFACE='#ffffff'
INK='#1b2430'
INK_2='#566274'
GRID='#e8ecf1'
AXIS='#aab3c0'

STATE_SPACE='#0072B5'
KALMAN='#BC3C29'
SPY='#20854E'
SPY_TBILL='#6F99AD'   # tint of SPY: same family, secondary emphasis
CONTROL='#E18727'
CONTROL_2='#FFDC91'   # tint of the control, for a second representation
TBILL='#B3B3B3'
MPT_MEAN='#7876B1'
MPT_SHRINK='#FFDC91'
MPT_MATCHED='#EE4C97'
MPT_LIGHT='#7876B1'

POSITIVE='#0072B5'
NEGATIVE='#BC3C29'

def apply():
    mpl.rcParams.update({
        'figure.facecolor':SURFACE,'axes.facecolor':SURFACE,'savefig.facecolor':SURFACE,
        'text.color':INK,'axes.labelcolor':INK_2,'axes.titlecolor':INK,
        'xtick.color':INK_2,'ytick.color':INK_2,'axes.edgecolor':AXIS,
        'axes.spines.top':False,'axes.spines.right':False,'axes.linewidth':.8,
        'xtick.major.size':0,'ytick.major.size':0,
        'grid.color':GRID,'grid.linewidth':.8,'grid.alpha':1,
        'axes.titlesize':10.5,'axes.titleweight':'bold','axes.labelsize':9.5,
        'xtick.labelsize':8.5,'ytick.labelsize':8.5,'legend.fontsize':8.5,
        'figure.titlesize':14,'figure.titleweight':'bold',
    })
