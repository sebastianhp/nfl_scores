import numpy as np
import matplotlib.pyplot as plt

jawn1 = np.load('./scores/fmt_scores1.npy')
# 0-0 works now. jawn1[86,2] = 73 #0-0 doesn't work, so manually entered. need to check that this still works
jawn2 = np.load('./scores/fmt_scores2.npy')

score = np.concatenate((jawn1,jawn2), axis=0).astype(int)
home = score[:,0]
away = score[:,1]
max_home = np.amax(home)
max_away = np.amax(away)

snew = np.zeros([max_home, max_away]) #will be a proper x vs y array
                                    #try plotting with plt.matshow()
                                    #something like that..

for i in range(max_home):
    for j in range(max_away):
            temp0 = np.where(home == i )[0]
            temp1 = np.where(away == j )[0]
            index = np.intersect1d(temp0,temp1)
            if index.size == 0:
                snew[i,j] = 0
            else:
                snew[i,j] = score[index[0], 2]

np.save('./scores/mat_scores.npy', snew)

plt.matshow(snew, clim=(0,50))
plt.grid(b=True, which='both', axis='both')
plt.colorbar()
plt.show()
