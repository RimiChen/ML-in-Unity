import torch
import torch.nn as nn
import torch.nn.functional as F
import sklearn.datasets
import matplotlib.pyplot as plt

# System check
if torch.cuda.is_available():
    print("System Check: GPU accessible.")
else:
    print("System Check: Fail on installing Pytorch GPU version")



# Import and Dataset
x, y = sklearn.datasets.make_moons(200, noise = 0.25, random_state = 1)
# print(x)
# print(y)
# x = x.unsqueeze(1)
# y = y.unsqueeze(1)
x = torch.tensor(x)
y = torch.tensor(y)

y = y.view(y.shape[0], 1)  # reshape y

print("x.shape = ", x.shape)
print("y.shape = ", y.shape)

plt.scatter(x[:,0], x[:,1], c = y)
plt.show()


# Create and train model
class Neural_Net(nn.Module):
    def __init__(self):
        
        super().__init__() # instantiate our nn.Module
        self.fc1 = nn.Linear(2, 10)
        self.fc2 = nn.Linear(10, 1)


    def forward(self, x):
        x = F.tanh(self.fc1(x))
        x = F.sigmoid(self.fc2(x))

        return x

model = Neural_Net()
cost_func = nn.BCELoss()
optimizer = torch.optim.Adam(model.parameters(), lr = 0.05)
epochs = 10000


for i in range(epochs):
    output = model(x.float())
    loss = cost_func(output, y.float())

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if (i% 1000 == 0):
        print(loss)


# Export the model to onnx
torch.onnx.export(model,                              # model being run
                  x[0].float(),                       # model dummy input (or a tuple for multiple inputs)
                  "make_moons.onnx",                  # where to save the model (can be a file or file-like object)
                  export_params=True,                 # store the trained parameter weights inside the model file
                  opset_version=9,                    # the ONNX version to export the model to
                  do_constant_folding=True,           # whether to execute constant folding for optimization
                  input_names = ['x'],                # the model's input names
                  output_names = ['y']                # the model's output names
                  )