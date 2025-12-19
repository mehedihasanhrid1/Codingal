import tensorflow as tf
import matplotlib.pyplot as plt

(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

x_train = x_train.reshape(-1, 28*28) / 255.0
x_test = x_test.reshape(-1, 28*28) / 255.0

W1 = tf.Variable(tf.random.normal([784, 128]))
b1 = tf.Variable(tf.zeros([128]))
W2 = tf.Variable(tf.random.normal([128, 10]))
b2 = tf.Variable(tf.zeros([10]))

def model(x):
    h = tf.nn.relu(tf.matmul(x, W1) + b1)
    return tf.matmul(h, W2) + b2

optimizer = tf.optimizers.Adam()

for epoch in range(5):
    with tf.GradientTape() as tape:
        logits = model(x_train)
        loss = tf.reduce_mean(
            tf.nn.sparse_softmax_cross_entropy_with_logits(
                labels=y_train, logits=logits
            )
        )
    grads = tape.gradient(loss, [W1, b1, W2, b2])
    optimizer.apply_gradients(zip(grads, [W1, b1, W2, b2]))

logits_test = model(x_test)
predictions = tf.argmax(logits_test, axis=1)
accuracy = tf.reduce_mean(tf.cast(predictions == y_test, tf.float32))
print("Test accuracy:", accuracy.numpy())

plt.imshow(x_test[0].reshape(28, 28), cmap="gray")
plt.title(f"Predicted: {predictions[0].numpy()}")
plt.show()
