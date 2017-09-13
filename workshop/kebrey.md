### Explore the effects for different K in K Nearest Neighbor classification.

![Screenshots](https://github.com/Nikhila-B/FSS17_Group_L/blob/master/workshop/kebrey_changingk.png)

### Explain how we should choose K.

If K is smaller, the model is more sensitive to noise. However, that might be good for situations where you have a small cluster near a big cluster, because otherwise records that belong in the small cluster would be 'eaten' by the big cluster. So, it depends on the shapes and sizes of the cluster you have, and the goals you have for your model. 

I think of the political map example we looked at in class last week. There could have actually been an strongly rebuplican area in the middle of the democratic area, but a too-large k would hide it.


### Explore different kernels of Support Vector Machine.

#### linear  
Predicted: [1 2 1 0 0 0 2 1 2 0]  
Actual:    [1 1 1 0 0 0 2 1 2 0]  

#### rbf
Predicted: [1 2 1 0 0 0 2 1 2 0]
Actual:    [1 1 1 0 0 0 2 1 2 0]

#### sigmoid
Predicted: [2 2 2 2 2 2 2 2 2 2]
Actual:    [1 1 1 0 0 0 2 1 2 0]

The different kernels gave very different performance. The sigmoid kernel resulted in terrible predictions.

### Explian how we should choose the kernel.

As I understand it, the kernel determines the shape of the curve that splits the clusters. So, depending on the shapes of the cluster, the proper kernel to use can be very important. In some cases, simply looking at the data might make sense. However, I assume with high dimensional data that might not tell you much.

One example is a cluster inside another cluster. A linear kernel would not make sense here, because there is no way a plane can split the data properly. The rbf kernel would work better here.
