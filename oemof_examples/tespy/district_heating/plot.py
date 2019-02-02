from matplotlib import pyplot as plt

T_pp = [70, 80, 90, 100, 110]
T_f = [65.6, 73.1, 80.5, 87.8, 95]
T_amb = [20, 10, 0, -10, -20]
Q = [0.6, 0.8, 1.0, 1.2]
eta = []
eta += [[27.7, 33.1, 38.0, 42.5, 46.7]]
eta += [[22.4, 27.0, 31.2, 35.0, 38.5]]
eta += [[18.9, 23.0, 26.7, 30.0, 33.1]]
eta += [[15.9, 20.1, 23.4, 26.5, 29.3]]
x = T_amb
#y = eta1

colors = ['#00395b', '#74adc1', '#b54036', '#ec6707',
          '#bfbfbf', '#999999', '#010101']

fig, ax = plt.subplots()

for i in range(4):
    plt.plot(x, eta[i], '-x', Color=colors[i],
             label='$\\frac{\dot{Q}}{\dot{Q}_\mathrm{ref}} = $' + str(Q[i]), markersize=7,
             linewidth=2)

ax.set_ylabel('Wärmeverlust in %')
ax.set_xlabel('$T_{amb}$ in °C')
plt.title('Wärmeverluste des Nahwärmenetzes')
plt.legend(loc='upper right')
#ax.set_xlim([-22, 22])
#ax.set_ylim([0, .4])
#plt.yticks(np.arange(0, 7e6, step=1e6), np.arange(0, 7, step=1))
#plt.xticks(np.arange(0, 14e6, step=2e6), np.arange(0, 14, step=2))

plt.show()

fig.savefig('PQ_diagram.svg')