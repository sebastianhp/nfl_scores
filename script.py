import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator, MultipleLocator, FormatStrFormatter
import matplotlib.patheffects as path_effects
from matplotlib.patches import Ellipse
import matplotlib.gridspec as gridspec

snew = np.load('./scores/mat_scores.npy')
inset = False

if inset == False:
	titleadd = ''
	cmax = 20
	c_fac = 1.3
	w_circle = 3
else:
	titleadd = ' Inset'
	cmax = 75
	c_fac = 1.75
	w_circle = 1.75

sz1=len(snew)
sz2=sz1-6
sz=46 #snew is square. whole=len(snew) | inset=51

xml = FixedLocator(np.arange(0,71,5)+0.5)
yml = FixedLocator(np.arange(0,71,5)+0.5)
xmil = MultipleLocator(1)
ymil = MultipleLocator(1)
xf = FormatStrFormatter('%d')
yf = FormatStrFormatter('%d')

fig = plt.figure()
ax = fig.add_subplot(111)
ax.xaxis.set_major_locator(xml)
ax.yaxis.set_major_locator(yml)
ax.xaxis.set_minor_locator(xmil)
ax.yaxis.set_minor_locator(ymil)
ax.yaxis.set_major_formatter(xf)
ax.xaxis.set_major_formatter(yf)
ax.tick_params(which = 'major', direction = 'out', 
				width = 1.5, length = 5,
				top = 'off', right = 'off',
                                labelsize = '18')
ax.tick_params(which = 'minor', direction = 'out', 
				top = 'off', right = 'off')
ax.grid(True, 'minor', linestyle='-', color='0.5')
ax.set_aspect('auto')
ax.set_xlabel('Away Team Points', fontsize='24')
ax.set_ylabel('Home Team Points', fontsize='24')
ax.set_title('Pro Football Point Distribution (1920-2017 minus SB)'
				+ titleadd,	fontsize = '32')
fig.text(0.1, 0.01, 'source: www.pro-football-reference.com',
				horizontalalignment='left', 
				verticalalignment='bottom', fontsize=11, 
				transform=fig.transFigure)
plot = ax.pcolor(snew, cmap='PuBuGn')
plot2 = ax.plot([0,sz1],[0,sz1], 'k-', lw=2, alpha=0.5)
plot.set_clim(0,cmax)

#get center of mass
sum_mass = 0
sum_wmass = np.zeros(2)
for i in range(sz1):
	for j in range(sz1):
		mass = snew[i,j]
		sum_mass += mass
		sum_wmass += mass*np.array([i,j])

com_coords = sum_wmass / float(sum_mass)
com_circle = Ellipse(tuple(com_coords[::-1]), 
		w_circle, c_fac*w_circle,
		lw=2, fc=(1,0,0,0.25), ec=(1,0,0,0.5) )
ax.add_artist(com_circle)

ccmag = np.sqrt(com_coords[1]**2 + com_coords[0]**2)
ptdiff = ccmag*np.sin(np.arccos((com_coords[1] + com_coords[0])/(ccmag*np.sqrt(2))))
ptdiffstr = 'Home team advantage\n(distance between\nweighted average\nand diagonal): ' + str(int(ptdiff)) + ' points'

if inset == False:
	ax.axis([0,sz1,0,sz1])
	tick_arr = np.arange(0,cmax+1,5)
	cb = plt.colorbar(plot, ticks = tick_arr)
	cb_arr = [str(int(i)) for i in tick_arr ]
	cb_arr[len(cb_arr)-1] = str(cmax) + '+'
	cb.ax.set_yticklabels(cb_arr)
        fmtstr = '{0:.1f}'
        annotstr = 'weighted average\n(' + fmtstr.format(com_coords[1]) + ' , ' + fmtstr.format(com_coords[0]) + ')'
        ax.annotate(annotstr, fontsize='28', color='red',
                xy=(com_coords[1]+0.25, com_coords[0]+0.25), xytext=(32, 50),
                arrowprops=dict(width=5, 
                facecolor='red', lw=0, alpha=0.5) )
        ax.text(50, 35, ptdiffstr, fontsize='24')
else:
	ax.axis([0,sz,0,sz])
	for i in range(sz):
		for j in range(sz):
			txt_val = int(snew[j,i])
			col='white'
			#if txt_val >= int(cmax*0.95):
			#	col = 'white'
			#else:
			#	col = str(txt_val/float(cmax*0.95))
			if txt_val != 0:
				text = ax.text( i + 0.5, j + 0.4, str(txt_val), 
					horizontalalignment='center', 
					verticalalignment='center', 
					fontsize=12, family='sans-serif',
					weight='semibold', color=col )
				text.set_path_effects(
						[ path_effects.Stroke(linewidth=2, 
							foreground='black'),
							path_effects.Normal() ] )

plt.show()
fig.savefig('./Plots/2D.png', dpi=100)	
