
from genie3 import GENIE3
from main import *
from sklearn.metrics import *
import numpy as np
from matplotlib import pyplot as plt
import time


def calculate_confusion_matrix(edges_genie3, edges_federated, num_total):
    tp = 0
    tn = 0
    fp = 0
    fn = 0

    edges_federated = np.delete(np.asarray(edges_federated), obj=2, axis=1).tolist()
    edges_genie3 = np.delete(np.asarray(edges_genie3), obj=2, axis=1).tolist()
    for i in range(len(edges_federated)):
        if edges_federated[i] in edges_genie3:
            tp += 1
        else:
            fp += 1
        if edges_genie3[i] not in edges_federated:
            fn += 1
    fn = num_total - (tp + fn + fp)
    return tp, fp, fn, tn


data_path = "TCGA-COAD.htseq_fpkm.tsv"
data = import_data(data_path)

# run GENIE3
start_genie3 = time.time()
VIM_genie3 = GENIE3(data)
end_genie3 = time.time()

# run federated method
number_patients = data.shape[0]
number_genes = data.shape[1]
hospital_data = simulate_different_hospitals(data)
start_federated = time.time()
vim_federated = train(hospital_data, number_genes, number_patients)
end_federated = time.time()
# save VIM's
np.savetxt('VIM_genie3.csv', VIM_genie3, delimiter=',')
np.savetxt('VIM_federated.csv', vim_federated, delimiter=',')

mse = mean_squared_error(VIM_genie3, vim_federated)
print("The mse of the two VIM-matrices is: %s" % mse)

edges_genie3 = get_linked_list_federated(VIM_genie3)
edges_federated = get_linked_list_federated(vim_federated)

start_evaluation = time.time()
f1 = [0]
precision = [0]
recall = [0]
for i in range(1, len(edges_federated)):
    tp, fp, fn, tn = calculate_confusion_matrix(edges_genie3[:i], edges_federated[:i], len(edges_federated))
    precision.append(tp / (tp + fp))
    recall.append(tp / (tp + fn))
    if precision[i] + recall[i] != 0:
        f1.append(2 * (precision[i] * recall[i]) / (precision[i] + recall[i]))
    else:
        f1.append(0)
end_evaluation = time.time()

print("Evaluation complete, waiting on plot....")

# fig = plt.figure(1)
x = np.arange(0, len(edges_federated))
plt.plot(x, precision, label='precision')
plt.plot(x, recall, label='recall')
plt.plot(x, f1, label='f1')
plt.legend()
plt.xlabel("Number of edges selected")
plt.savefig("precision_recall_f1_scores")
plt.show()

f = open('times.txt', 'w')
f.write("Number of Genes: %s\nNumber of Samples: %s\nTime Genie3 takes: %s\nTime the federated approach takes: %s \nTime Evaluation takes: %s " % (
    (config.Genes_size), (config.Sample_size), (end_genie3 - start_genie3), (end_federated - start_federated), (end_evaluation - start_evaluation)))
f.close()
