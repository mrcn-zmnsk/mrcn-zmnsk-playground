# Notes from the FastAI course

This project is built along taking the [FastAI Course](https://course.fast.ai/). Based on prior experience, using websearch may be problematic on Kaggle, Colab and similar.

## Chapters

### 1.6 Decision Trees and Random Forests
[Jupyter](1.6/trees.ipynb)

1. Practicing fundamentals of Decision Trees - OneR classifier
1. Building Trees and Forrests - trivial with sklearn

Take-aways:
- Neat built-in feature for `feature importanc`e to reduce the feature space in analysis
- Random Forests are hard to mess up, cheap to train, and eat training data before cleaning. Great start to analysis of tabular data.

![Small decision tree](../docs/fastai-course/1.6%20Small%20decision%20tree.png)

![Small decision tree](../docs/fastai-course/1.6%20Feature%20importance%20in%20Random%20Forest.png)

### 1.5 Advancing linear to Neural Net, to deep Neural Net
[Jupyter](1.5/titanic.ipynb)

#### Data preparation and feature engineering

1. Download Titanic dataset from kaggle competition
1. Load dataframe and analyze with `isNa()`, `describe()`, `info()`
1. isNa analysis: replacing Nas with `mode()` -> data interpolation
1. Long-tailed `Fare` attribute analysis with `hist()` -> `logp1` to reduce distribution
1. Categorical attributes (e.g. boarded in) are exploded to binary variables using `get_dummies()`
1. Project only resulting columns, force as float, and normalize by dividing with max value per column

Results is a pytorch rank-2 tensor representing the input data.

#### Preparing 3 models: linear, NN and Deep-NN

The model can be thought of as an interface implementation of:
 - init_coefficients()  -> returns grad-enabled represntation of model variables
 - calc_predictions(coefficients, training input)  -> applies coefficients on training input, producing an **actual** result
 - calc_loss(coefficients, training input, expected results) -> calculates predictions and measures distance to **expected** result. We're using MAE (mean abs error)
 - update_coefficients(coefficients, learning_rate)  ->  apply gradients on coefficients in propotion to LR
 - (optional) show_coefficients -> in linear we can still track what's going on, later it's getting tough

##### Linear
Linear model implements the above as producing a vector of coeffs, and simply multiplies the input data through it. It wraps the result in Sigmoid - clamps output between (0, 1).

![Linear](../docs/fastai-course/1.5%20linear.png)

##### NN
NN-model adds in a layer in between input coefficients and output. There are 2 matrix multiplications. First is wrapped in ReLU (zero the negative values), second wrapped in Sigmoid

![Linear](../docs/fastai-course/1.5%20NN.png)

##### Deep-NN
Deep-NN-model has 2 layers in between. All but last layer is ReLU-ed, last layer is Sigmoid-ed.

![Linear](../docs/fastai-course/1.5%20Deep%20NN.png)

#### Take-aways

- There are inconsistencies in course material that led me to 2 fails in training models. **Make sure to zero the gradients**, and **normalize the numeric data, removing bias from data**.
- In this tabular data problem, the Deep NN achieved the best fit, the linear was a close 2nd, and I had the most challenges fiddling with the single-layer NN.
- With some fiddling of parameters of this vanilla model I achieved loss of 0.19, and accuracy of 83%. Kaggle submission had 77% accuracy, placing me on the 27th percentile of the competition.

### 1.3 Neural Networks from Scratch - Stochastic Gradient Descent
[Jupyter](1.3/SGD.ipynb)

1. Went through building a linear model from scratch, using pure PyTorch tensors and operations. The model was fitting a quadratic function on generated data.
1. Built a 95% accurate model differentiating between 3s and 7s from MNIST dataset.
1. Coded raw PyTorch, then wrapped in fastai Learners, one with Linear model, one with simple neural network (1 hidden layer of 30 neurons with ReLU).

![Quadratic function during fitting](../docs/fastai-course/1.3.png)

### 1.2 Deploying
[Jupyter](1.2/dogs_cats.ipynb)

1. Using Python's pickle serialization to export/load models - simplistic. PKL isn't interoperable with other programming languages, and serialized objects will fail to deserialize on changed code.
1. Using Gradio to create dead-simple UX for the loaded model and running predict() function.
1. Useful helper functions in the fastai library for viewing examples with largest loss function, and for cleaning dataset according to loss-function. Unusual technique to make dirty training on uncleaned data, and use the draft model to find dirty data.


![Gradio UX with dog-cat classifier](../docs/fastai-course/1.2.png)

### 1.1 Getting started - training visual classifier
[Jupyter](1.1/is-it-a-bird-creating-a-model-from-your-own-data.ipynb)

1. Installed CUDA-enabled PyTorch to use laptop GPU - https://pytorch.org/get-started/locally/
1. Issues with DuckDuckGo Search for images. Permanent 429s. Replaced with GoogleSearchAPI Custom Search opened in the Agents project. 100 searches per day for free.
1. Categorizing between forks and knifes. The model does well despite bogus images within training data.

![Fork-knife model testing](../docs/fastai-course/1.1.png)