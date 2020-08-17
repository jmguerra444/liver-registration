# # %%
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import medfilt

def reject_outliers(data, m = 4):
    return data[abs(data - np.mean(data)) < m * np.std(data)]

def log_reader(path):

    with open(path) as f:
        f = f.readlines()

    report = ""
    trainLoss = np.array([float(l[5:]) for l in f if l[:3] == "[L]"])
    validLoss = np.array([float(l[5:]) for l in f if l[:3] == "[V]"])
    summary = [(l[5:]) for l in f if l[:3] == "[E]"]

    d1_loss = np.array([float(l[6:]) for l in f if l[:4] == "[D1]"])
    d2_loss = np.array([float(l[6:]) for l in f if l[:4] == "[D2]"])
    info = np.array([l for l in f if l[0] != "["])
    
    # validLoss, d1_loss, d2_loss = reject_outliers(validLoss), reject_outliers(d1_loss), reject_outliers(d2_loss)
    # trainLoss = medfilt(trainLoss, 5)
    validLoss = medfilt(validLoss, 5)
    d1_loss = medfilt(d1_loss, 5)
    d1_loss = medfilt(d1_loss, 5)
    d2_loss = medfilt(d2_loss, 5)


    tr = [float(x[22:28]) for x in summary]
    vl = [float(x[46:52]) for x in summary]
    plt.plot(trainLoss, label = "Training")
    plt.plot(validLoss, label = "Validation")
    plt.ylabel('Loss')
    # Set the y axis label of the current axis.
    plt.xlabel('Training epochs')
    # Set a title of the current axes.
    plt.legend()
    plt.show()

    epochs = list(range(0, len(summary)))
    fig = plt.figure()
    fig.suptitle(info[0])
    
    ax_tr = plt.subplot(2, 2, 1)
    ax_tr.plot(trainLoss)
    ax_tr.title.set_text("Training")
    ax_tr.get_xaxis().set_ticks([])
    ax_tr.set_xlabel("Epoch")
    ax_tr.set_ylabel("Dice Loss")
    ax_tr.set_ylim(0, 0.7)

    ax_vl = plt.subplot(2, 2, 2)
    ax_vl.plot(validLoss)
    ax_vl.title.set_text("Validation")
    ax_vl.get_xaxis().set_ticks([])
    ax_vl.set_xlabel("Epoch")
    ax_vl.set_ylabel("Dice Loss")
    ax_vl.set_ylim(0, 0.1)
    
    ax_d1 = plt.subplot(2, 2, 3)
    ax_d1.plot(d1_loss)
    ax_d1.title.set_text("Bacground")
    ax_d1.get_xaxis().set_ticks([])
    ax_d1.set_xlabel("Epoch")
    ax_d1.set_ylabel("Dice Loss")
    ax_d1.set_ylim(0.95, 1)
    
    ax_d2 = plt.subplot(2, 2, 4)
    ax_d2.plot(d2_loss)
    ax_d2.title.set_text("Liver")
    ax_d2.get_xaxis().set_ticks([])
    ax_d2.set_xlabel("Epoch")
    ax_d2.set_ylabel("Dice Loss")
    ax_d2.set_ylim(0.85, 1)
    
    plt.show()
    return trainLoss, validLoss, summary, report
