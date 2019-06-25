
Import torch
import torchvision
import torchvision.transforms as transforms import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import copy
############################################ # 1. Loading and normalizing CIFAR-10 ############################################
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
transform_train = transforms.Compose([
transforms.RandomCrop(32, padding=4), transforms.RandomHorizontalFlip(),
transforms.ToTensor(),
transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)),
])
transform_test = transforms.Compose([
transforms.ToTensor(),
transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)),
])
trainset = torchvision.datasets.CIFAR10(root='./data', train=True, download=True, transform=transform_train)
trainloader = torch.utils.data.DataLoader(trainset, batch_size=128, shuffle=True, num_workers=8)
testset = torchvision.datasets.CIFAR10(root='./data', train=False, download=True, transform=transform_test)
testloader = torch.utils.data.DataLoader(testset, batch_size=128, shuffle=False, num_workers=8)
############################################ # 2. Define a Convolutional Neural Network
############################################
## vgg 사용
## filter크기에 맞추어 padding 값 1
learning_rate = 0.1
class Net(nn.Module):
def __init__(self, architechture):
super(Net, self).__init__()
self.features = self._make_layers(architechture) self.classifier = nn.Linear(4096, 10)
def forward(self, x):
out = self.features(x)
out = out.view(out.size(0), -1) out = self.classifier(out) return out
def _make_layers(self, cfg): layers = []
in_channels = 3 for x in cfg:
if x == 'M':
layers += [nn.MaxPool2d(kernel_size=2, stride=2)]
else:
layers += [nn.Conv2d(in_channels, x, kernel_size=3, padding=1),
nn.BatchNorm2d(x),
nn.ReLU(inplace=True)] in_channels = x
layers += [nn.AvgPool2d(kernel_size=1, stride=1)] return nn.Sequential(*layers)
net = Net([64, 'M', 128, 'M', 256, 256, 'M']).to(device)
############################################ # 3. Define a Loss function and optimizer ############################################
criterion = nn.CrossEntropyLoss().cuda()
optimizer = optim.SGD(net.parameters(), lr=learning_rate, momentum=0.9)

############################################ # 4. Train the network ############################################
## hyperparameter의 최적 값을 구할때 범위를 지정하고 log scale만큼 변화를 주어 learning rate 값 바꾸었다.
def train():
best_acc = 0
for epoch in range(150):
if epoch < 40:
lr = learning_rate* 0.2
elif epoch < 90 :
lr = learning_rate* 0.1
else:
lr = learning_rate * 0.1
for param_group in optimizer.param_groups: param_group['lr'] = lr
running_loss = 0.0
for i, data in enumerate(trainloader):
images, labels = data
images, labels = images.to(device), labels.to(device) optimizer.zero_grad()
outputs = net(images)
loss = criterion(outputs, labels)
loss.backward()
optimizer.step()
# print statistics
running_loss += loss.item()
if i % 100 == 99: # print every 2000 mini-batches
print('[{}, {}] loss: {:.4f}'.format(epoch + 1, i + 1, running_loss / 2000)) running_loss = 0.0
# save the best model test_acc = test()
if test_acc > best_acc:
best_acc = test_acc
best_model = copy.deepcopy(net)
torch.save(best_model.state_dict(), 'JY_best_model.pt') print('Finished Training')
 ############################################

# 5. Test the network on the test data ############################################
def test(): correct = 0
total = 0
accuracy = 0
with torch.no_grad():
for data in testloader:
images, labels = data
images, labels = images.to(device), labels.to(device) outputs = net(images)
_, predicted = torch.max(outputs.data, 1)
total += labels.size(0)
correct += (predicted == labels).sum().item() accuracy = 100 * correct / total
print('Accuracy on test images: {:.2f}%'.format(accuracy)) print()
return accuracy
if __name__ == '__main__': train()