# Traffic

### Experimentation process

The first thing I did was to download the `gtsrb-small` dataset to help me write the `load_data` function. When this was working I moved on to use the larger dataset.

I began by copying the Sequential model used in the lectures for the digit recognition example. This gave a very poor accuracy and the model didn't really learn at all.

Next I experimented with adding more convolutional and pooling layers. Adding an extra 1 of each made a significant improvement but adding a third of each had the opposite effect.

I then added another hidden layer and dropout layer. The didn't perform well so I removed the second dropout layer and the accuracy improved again. I tried a third hidden layer but, again the performance got worse.

The final thing I tried was changing the activation algorithm from `relu` to `sigmoid` for the convolution layers. The again caused a small improvement in accuracy. I ended up with a training accuracy of 0.9533, loss of 0.1459 and a testing accuracy of 0.9715, loss of 0.1019.