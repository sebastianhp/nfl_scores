import numpy as np
import matplotlib.pyplot as plt

#make radial distribution function

jawn1 = np.load('./scores/fmt_scores1.npy')
jawn2 = np.load('./scores/fmt_scores2.npy')
cutoffnum = 5

score = np.concatenate((jawn1,jawn2), axis=0).astype(int)
home = score[:,0]
away = score[:,1]
tots = score[:,2]

maxdiff = max(home-away) + 1
harr, aarr = np.zeros(maxdiff), np.zeros(maxdiff)

for i in range(len(home)):
	val = home[i] - away[i]
	if val > 0:
		harr[abs(val)]+=tots[i]
	elif val < 0:
		aarr[abs(val)]+=tots[i]

xarr = np.arange(maxdiff)
yarr = np.zeros(maxdiff)

for i in range(maxdiff):
	if harr[i]==0 and aarr[i]==0:
		yarr[i] = 0
	else:
		yarr[i] = (harr[i]-aarr[i]) / (harr[i]+aarr[i])

funkyvalsx, = np.where( harr+aarr <= cutoffnum)
funkyvalsy = np.array( [yarr[i] for i in funkyvalsx] )

tots2 = harr + aarr
maxtots2 = max(tots2)

sumarr = np.array( [ np.sum(yarr[0:i]) for i in range(len(yarr+1)) ] )
# This is a nice start, but when integrating I think I need 
# to weigh based on the number of games that had a 
# particular score

fig, (ax1) = plt.subplots(nrows=1, ncols=1)
ax1.set_title('Point differential distribution',
		fontsize = '28')

#(home wins - away wins)/total games for a given point differential
yax1 = ax1.get_yaxis()
yax1.set_label_position("right")
ax1.fill_between(xarr, 0, yarr, facecolor='green', lw=0, alpha=0.75)

#total games with a given point differential
ax2 = ax1.twinx()
yax2 = ax2.get_yaxis()
yax2.set_label_position("left")
ax2.plot(xarr, tots2, 'k-', lw=2) 
ax2.set_ylabel('Total games', fontsize='20', color='k')
ax2.tick_params('y', colors='k', labelsize='18', left=True, right=False, labelleft=True, labelright=False)
ax2.set_ylim(-0.05*maxtots2, 1.05*maxtots2)

ax1.set_ylabel('(Home wins - Away wins) / Total games', fontsize='20', color='green')
ax1.set_ylim(-0.05,1.05)
ax1.tick_params('x', labelsize='18')
ax1.tick_params('y', colors='green', labelsize='18', left=False, right=True, labelleft='off', labelright='on')
ax1.set_xlim(0,50)
ax1.set_xlabel('Point Differential', fontsize='20')

fig.text(0.1, 0.01, 'source: www.pro-football-reference.com',
				horizontalalignment='left', 
				verticalalignment='bottom', fontsize=11, 
				transform=fig.transFigure)

plt.show()
