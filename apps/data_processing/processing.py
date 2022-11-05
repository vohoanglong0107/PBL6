import argparse
import gzip
import os
import numpy as np


def load_mnist(dataset_dir):
    filename = [
        ["training_images", "train-images-idx3-ubyte.gz"],
        ["test_images", "t10k-images-idx3-ubyte.gz"],
        ["training_labels", "train-labels-idx1-ubyte.gz"],
        ["test_labels", "t10k-labels-idx1-ubyte.gz"]
    ]
    mnist = {}
    for name in filename[:2]:
        with gzip.open(os.path.join(dataset_dir, name[1]), 'rb') as f:
            mnist[name[0]] = np.frombuffer(
                f.read(), np.uint8, offset=16).reshape(-1, 28, 28)
    for name in filename[-2:]:
        with gzip.open(os.path.join(dataset_dir, name[1]), 'rb') as f:
            mnist[name[0]] = np.frombuffer(f.read(), np.uint8, offset=8)
    return mnist


def to_categorical(y, num_classes=None, dtype="float32"):
    y = np.array(y, dtype="int")
    input_shape = y.shape
    if input_shape and input_shape[-1] == 1 and len(input_shape) > 1:
        input_shape = tuple(input_shape[:-1])
    y = y.ravel()
    if not num_classes:
        num_classes = np.max(y) + 1
    n = y.shape[0]
    categorical = np.zeros((n, num_classes), dtype=dtype)
    categorical[np.arange(n), y] = 1
    output_shape = input_shape + (num_classes,)
    categorical = np.reshape(categorical, output_shape)
    return categorical


def transform_mnist(mnist):
    X_train = mnist["training_images"].reshape(-1, 784)
    X_test = mnist["test_images"].reshape(-1, 784)
    X_train = X_train.astype('float32')
    X_test = X_test.astype('float32')
    X_train /= 255
    X_test /= 255
    y_train = to_categorical(mnist["training_labels"])
    y_test = to_categorical(mnist["test_labels"])
    return X_train, X_test, y_train, y_test


def save_mnist(X_train, X_test, y_train, y_test, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    np.savez_compressed(
        os.path.join(output_dir, "mnist.npz"),
        X_train=X_train,
        X_test=X_test,
        y_train=y_train,
        y_test=y_test
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir", type=str, default="/datasets")
    parser.add_argument("--output_dir", type=str, default="/output")
    args = parser.parse_args()
    mnist = load_mnist(args.input_dir)
    X_train, X_test, y_train, y_test = transform_mnist(mnist)
    print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)
    save_mnist(X_train, X_test, y_train, y_test, args.output_dir)
