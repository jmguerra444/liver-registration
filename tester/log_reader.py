# # %%
import matplotlib.pyplot as plt 

def log_reader(path):
    with open(path) as f:
        f = f.readlines()

    report = ""
    trainLoss = [float(l[5:]) for l in f if l[:3] == "[L]"]
    validLoss = [float(l[5:]) for l in f if l[:3] == "[V]"]
    summary = [(l[5:]) for l in f if l[:3] == "[E]"]

    d1_loss = [float(l[6:]) for l in f if l[:4] == "[D1]"]
    d2_loss = [float(l[6:]) for l in f if l[:4] == "[D2]"]
    d3_loss = [float(l[6:]) for l in f if l[:4] == "[D3]"]
    info = [l for l in f if l[0] != "["]
    
    fig = plt.figure()
    fig.suptitle(info[0])
    
    ax_tr = plt.subplot(2, 2, 1)
    ax_tr.plot(trainLoss)
    ax_tr.title.set_text("Train Loss")
    
    ax_vl = plt.subplot(2, 2, 3)
    ax_vl.plot(validLoss)
    ax_vl.title.set_text("Validation Loss")
    
    ax_d1 = plt.subplot(3, 2, 2)
    ax_d1.plot(d1_loss)
    ax_d1.title.set_text("Background dice")
    
    ax_d2 = plt.subplot(3, 2, 4)
    ax_d2.plot(d2_loss)
    ax_d2.title.set_text("Liver dice")
    
    ax_d3 = plt.subplot(3, 2, 6)
    ax_d3.plot(d3_loss)
    ax_d3.title.set_text("Lesion dice")
    
    plt.show()
    return trainLoss, validLoss, summary, report


# path = "C:/Master thesis/master/simple-2d-unet/logs/12162115.log"
# readLoss(path)
