import torch.nn as nn
import torchvision.models as models
import os
import numpy as np
import torch
from transform_file import transform
from torch.utils.data import DataLoader
from PIL import Image
import torch.backends.cudnn as cudnn
import torch.optim as optim
from tqdm import tqdm
import sys
import math
from targetmodel import ResNet_ft, VGG_ft, MyDataset, root


if not os.path.exists(root):
    print("No dataset found, please check!")
    sys.exit()

trn_batch=16
val_batch=64
train_data = MyDataset(txt=root+'dataset-trn.txt', transform=transform)
test_data = MyDataset(txt=root+'dataset-val.txt', transform=transform)
test_loader = DataLoader(dataset=test_data, batch_size=val_batch, pin_memory=True)
'''
resnet = models.resnet50(pretrained=False)
net = ResNet_ft(resnet)
'''
vgg = models.vgg16(pretrained=False)
net = VGG_ft(vgg)
best_acc=0
loadfile=torch.load('./checkpoint/vgg16-ckpt0.742412.t7')
net.load_state_dict(loadfile['net'])
best_acc=loadfile['acc']
print("the accuracy of current model: ", best_acc)

if torch.cuda.is_available():
    device = 'cuda'
    net.cuda()
    # speed up slightly
    cudnn.benchmark = True

criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.6, weight_decay=0.003)


def train(epoch, trn_batch):
    print('\nEpoch: %d:' % epoch)
    train_loader = DataLoader(dataset=train_data, batch_size=trn_batch, pin_memory=True, shuffle=True)
    net.train()
    train_loss = 0
    correct = 0
    total = 0
    pbar = tqdm(train_loader)
    for (batch_idx, (inputs, targets)) in enumerate(pbar):
        pbar.set_description("batch " + str(batch_idx) + '/' + str(math.ceil(28037 / trn_batch)))
        inputs, targets = inputs.to(device), targets.to(device)
        optimizer.zero_grad()
        outputs = net(inputs)
        loss = criterion(outputs, targets)
        loss.backward()
        optimizer.step()
        train_loss += loss.item()
        _, predicted = outputs.max(1)
        total += targets.size(0)
        correct += predicted.eq(targets).sum().item()

    print("loss: "+str(round(train_loss/trn_batch,4))+'\t'+str(correct)+'\t'+str(total)+'\t'+str(correct/total))


def test(epoch, val_batch):
    global best_acc
    net.eval()
    test_loss = 0
    correct = 0
    total = 0
    with torch.no_grad():
        pbar = tqdm(test_loader)
        for batch_idx, (inputs, targets) in enumerate(pbar):
            pbar.set_description("batch " + str(batch_idx) + '/' + str(math.ceil(2570 / val_batch)))
            inputs, targets = inputs.to(device), targets.to(device)
            outputs = net(inputs)
            loss = criterion(outputs, targets)
            test_loss += loss.item()
            _, predicted = outputs.max(1)
            total += targets.size(0)
            correct += predicted.eq(targets).sum().item()

        print("loss: "+str(round(test_loss/val_batch,4))+'\t'+str(correct)+'\t'+str(total)+'\t'+str(correct/total))

    acc = correct/total
    if acc > best_acc:
        print('Saving..')
        state = {
            'net': net.state_dict(),
            'acc': acc,
            'epoch': epoch,
        }
        if not os.path.isdir('checkpoint'):
            os.mkdir('checkpoint')
        torch.save(state, './checkpoint/ckpt'+str(round(acc, 6))+'.t7')
        best_acc = acc

def demo(path):
    labels = open('./data/labels.txt', 'r').read().split('\n')
    net.eval()
    img = Image.open(path).convert('RGB')
    img = transform(img)[np.newaxis, :].to(device)
    _,out = net(img).max(1)
    print(labels[out[0]])


test(0, val_batch)
demo('./data/test_im3.png')

for epoch in range(1000000):
    train(epoch, trn_batch)
    test(epoch, val_batch)
    torch.cuda.empty_cache()
