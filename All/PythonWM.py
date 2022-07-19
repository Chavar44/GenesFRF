from main import *
import config
from sklearn.metrics import mean_squared_error
import numpy as np
from matplotlib import pyplot as plt
import time
import logging
import subprocess
import os

log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=log_fmt)
logger = logging.getLogger(__name__)


logger.info('Loading Dataset')
data, gene_names, transcription_factors = import_data(config.data_path, config.path_transcription_factors)
#data = data[:, :80]


# run federated method
logger.info('Run Federated Approach')
hospital_data = simulate_different_hospitals(data)

start_federated = time.time()
vim_federated = train(hospital_data, gene_names=gene_names, regulators=transcription_factors)
end_federated = time.time()
# save VIM federated
logger.info('saving VIM-matrix from federated approach')
np.savetxt('VIM_federated.csv', vim_federated, delimiter=',')


#da

logger.info('get linked lists')
edges_federated = get_linked_list_federated(vim_federated, printing=False)


f = open('times.txt', 'w')
f.write("Time the federated approach takes: %s\n" % (
       (end_federated - start_federated)))
f.close()
