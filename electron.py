import torch

class Electron(torch.nn.Module):

    def __init__(self):
        super(Electron, self).__init__()
        self.activation = torch.nn.ReLU()
        self.linear1 = torch.nn.Linear(7, 30)
        self.linear2 = torch.nn.Linear(30, 20)
        self.linear3 = torch.nn.Linear(20, 2)

    def forward(self, x):
        x = self.linear1(x)
        x = self.activation(x)
        x = self.linear2(x)
        x = self.activation(x)
        x = self.linear3(x)
        return x