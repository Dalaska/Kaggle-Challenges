#https://pytorch.org/tutorials/beginner/blitz/tensor_tutorial.html#sphx-glr-beginner-blitz-tensor-tutorial-py
# 60 min bliz

from __future__ import print_function
from __future__ import print_function
import torch

##1
x = torch.empty(5,3)
x = torch.rand(5, 3)
x = torch.tensor([5.5, 3])
x = torch.zeros(5, 3, dtype=torch.long)

# operation
y = torch.rand(5, 3)
print(x + y)
x = torch.randn(4, 4)
y = x.view(16)
b = y.numpy()

# cuda
if torch.cuda.is_available():
    device = torch.device("cuda")          # a CUDA device object
    y = torch.ones_like(x, device=device)  # directly create a tensor on GPU
    x = x.to(device)                       # or just use strings ``.to("cuda")``
    z = x + y
    print(z)
    print(z.to("cpu", torch.double))

##2 auto grad, automatic differentation
x = torch.ones(2, 2, requires_grad=True)
y = x + 2
print(y)
print(y.grad_fn)
z = y * y * 3
out = z.mean()
print(z, out)


print('la fin')