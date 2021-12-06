

import pandas as pd

conditions = ['active1_st', 'active2_end']

for cond in conditions:

    for s in range(102):
        data = pd.read_csv(r'/home/vera/MNE/MEM_regression/MEM_old_right_baseline/table_for_mem_{0}/{0}_{1}.csv'.format(cond, s))
        stim = data['stimulus'].to_list()
        limbs = []
        for i in stim:
            if i == 1:
                limb = 'l_hand'
                limbs.append(limb)
            elif i == 9:
                    limb = 'r_hand'
                    limbs.append(limb)

            elif i == 8320:
                    limb = 'r_foot'
                    limbs.append(limb)

            else:
                    limb = 'l_foot'
                    limbs.append(limb)

        data['limbs'] = limbs

        data.to_csv('/home/vera/MNE/MEM_regression/MEM_old_right_baseline/table_for_mem_{0}/{0}_{1}.csv'.format(cond, s))
