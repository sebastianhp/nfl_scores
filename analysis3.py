import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator, MultipleLocator, FormatStrFormatter
import matplotlib.patheffects as path_effects
from matplotlib.patches import Ellipse
import matplotlib.gridspec as gridspec

#Here we will do a 2D plot of ratios, not absolutes

snew = np.load('./scores/mat_scores.npy')
inset = True

if inset == False:
	titleadd = ''
	cmax = 25
	c_fac = 1.3
	w_circle = 3
else:
	titleadd = ' Inset'
	cmax = 75
	c_fac = 1.75
	w_circle = 1.75

sz1=len(snew)
sz2=sz1-6
sz=51 #snew is square. whole=len(snew) | inset=51

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
ax.set_title('Symmetric Element Ratios'
				+ titleadd,	fontsize = '32')
fig.text(0.1, 0.01, 'source: www.pro-football-reference.com',
				horizontalalignment='left', 
				verticalalignment='bottom', fontsize=11, 
				transform=fig.transFigure)

#Edit snew matrix
for i in range(sz):
	for j in range(sz):
		rat_sum = snew[i,j] + snew[j,i]
		if rat_sum == 0:
			snew[i,j] = 0
			snew[j,i] = 0
		else:
			snew[i,j] = snew[i,j] / float(rat_sum)
			snew[j,i] = snew[j,i] / float(rat_sum)


plot = ax.pcolor(snew, cmap='Greens')
plot2 = ax.plot([0,sz1],[0,sz1], 'k-', lw=2, alpha=0.5)
plot.set_clim(0,1)

#get center of mass (deleted)

if inset == False:
	ax.axis([0,sz1,0,sz1])
	tick_arr = np.arange(0,cmax+1,5)
	cb = plt.colorbar(plot, ticks = tick_arr)
	cb_arr = [str(int(i)) for i in tick_arr ]
	cb_arr[len(cb_arr)-1] = str(cmax) + '+'
	cb.ax.set_yticklabels(cb_arr)
else:
	ax.axis([0,sz,0,sz])
	'''
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
					fontsize=9, family='sans-serif',
					weight='semibold', color=col )
				text.set_path_effects(
						[ path_effects.Stroke(linewidth=2, 
							foreground='black'),
							path_effects.Normal() ] )
	'''
plt.show()
fig.savefig('./Plots/SymElemInset.png', dpi=100)
