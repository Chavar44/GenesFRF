
from GENIE3 import GENIE3
from main import *
from sklearn.metrics import mean_squared_error
import numpy as np
from matplotlib import pyplot as plt
import time
import logging

data_path = "TCGA-COAD.htseq_fpkm.tsv"

log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=log_fmt)

logger = logging.getLogger(__name__)
Number_of_Genes=20
# data_path = "/media/sf_Projekt_BIONETS/federated-inference-of-grns/genie3/data.txt"
logger.info('Loading Dataset')
data_path = 'C:/HMDA/Proyecto Random Forest/repository/federated-inference-of-grns/genie3/TCGA-COAD.htseq_fpkm.tsv'
data = import_data(data_path)[:, :Number_of_Genes]

# run GENIE3
logger.info('Run Genie3')
start_genie3 = time.time()
VIM_genie3 = GENIE3(data)
end_genie3 = time.time()

# run federated method
logger.info('Run Federated Approach')
hospital_data = simulate_different_hospitals(data)
start_federated = time.time()
vim_federated = train(hospital_data)
end_federated = time.time()

# save VIM's
logger.info('saving VIM-matrices')
np.savetxt('VIM_genie3.csv', VIM_genie3, delimiter=',')
np.savetxt('VIM_federated.csv', vim_federated, delimiter=',')

logger.info('calculate mse')
mse = mean_squared_error(VIM_genie3, vim_federated)
print("The mse of the two VIM-matrices is: %s" % mse)

logger.info('get linked lists')
edges_genie3 = get_linked_list_federated(VIM_genie3, printing=False)
edges_federated = get_linked_list_federated(vim_federated, printing=False)

logger.info('calculate precision, recall and f1 score')
start_evaluation = time.time()
f1 = [0]
precision = [0]
recall = [0]

num_total = len(edges_federated)
edges_federated = np.delete(np.asarray(edges_federated), obj=2, axis=1).tolist()
edges_genie3 = np.delete(np.asarray(edges_genie3), obj=2, axis=1).tolist()
tp = 0
tn = 0
fp = 0
fn = 0

for i in range(0, num_total):
    if edges_federated[i] == edges_genie3[i]:
        tp += 1
    else:
        if edges_federated[i] in edges_genie3[:i+1]:
            tp += 1
            fn -= 1
        else:
            fp += 1
        if edges_genie3[i] not in edges_federated[:i+1]:
            fn += 1
        else:
            tp += 1
            fp -= 1
    tn = num_total - (tp + fn + fp)
    precision.append(tp / (tp + fp))
    recall.append(tp / (tp + fn))
    if precision[i] + recall[i] != 0:
        f1.append(2 * (precision[i] * recall[i]) / (precision[i] + recall[i]))
    else:
        f1.append(0)
end_evaluation = time.time()
# fig = plt.figure(1)
x = np.arange(0, len(edges_federated)+1)
plt.plot(x, precision, label='precision')
plt.plot(x, recall, label='recall')
plt.plot(x, f1, label='f1')
plt.legend()
plt.xlabel("Number of edges selected")
plt.savefig("precision_recall_f1_scores")
plt.show()

f = open('times.txt', 'w')
f.write("Number of Genes: %d\nTime Genie3 takes: %s\nTime the federated approach takes: %s\nTime evaluation takes: %s" % (
    (Number_of_Genes),(end_genie3 - start_genie3), (end_federated - start_federated),(end_evaluation-start_evaluation)))
f.close()
