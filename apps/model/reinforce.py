import argparse
import os

import mlflow
import numpy as np
from keras import backend as K
from keras.layers import Dense, Dropout, Input
from keras.models import Model
from keras.optimizers import RMSprop


def REINFORCE(y_true, y_pred):
    correct = K.argmax(y_true, axis=1)
    guess = K.argmax(y_pred, axis=1)
    reward = K.equal(correct, guess)
    baseline = K.mean(reward)
    reward = K.cast(reward, baseline.dtype)
    adv = reward - baseline
    logit = K.log(K.max(y_pred, axis=1))

    return -adv * logit


def create_model():
    X = Input(shape=(784,), name="X")

    l1 = Dense(512, activation="relu")(X)
    l2 = Dropout(0.2)(l1)
    l3 = Dense(512, activation="relu")(l2)
    l4 = Dropout(0.2)(l3)
    out = Dense(10, activation="softmax", name="out")(l4)

    model = Model(inputs=[X], outputs=[out])
    model.compile(loss=REINFORCE, optimizer=RMSprop(), metrics=["accuracy"])
    return model


def load_data(dataset_dir):
    return np.load(os.path.join(dataset_dir, "mnist.npz"), allow_pickle=True)


def preprocess_data(data):
    X_train = data["X_train"]
    X_test = data["X_test"]
    y_train = data["y_train"]
    y_test = data["y_test"]
    return X_train, X_test, y_train, y_test


def train(
    model, X, y, epochs=10, batch_size=32, verbose=1, validation_split=0.1, shuffle=True
):
    model.fit(
        X,
        y,
        batch_size=batch_size,
        epochs=epochs,
        verbose=verbose,
        validation_split=validation_split,
        shuffle=shuffle,
    )


def evaluate(model, X, y):
    return model.evaluate(X, y)


def predict(model, X):
    return model.predict(X)


def main(args):
    data = load_data(args.dataset_dir)
    X_train, X_test, y_train, y_test = preprocess_data(data)
    model = create_model()
    mlflow.set_tracking_uri(args.tracking_uri)
    mlflow.set_experiment("mnist")
    mlflow.tensorflow.autolog()
    train(
        model,
        X_train,
        y_train,
        epochs=args.epochs,
        batch_size=args.batch_size,
        verbose=args.verbose,
        validation_split=args.validation_split,
        shuffle=args.shuffle,
    )
    evaluate(model, X_test, y_test)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dataset_dir",
        type=str,
        default="/datasets",
        help="Directory containing the dataset",
    )
    parser.add_argument("--tracking_uri", type=str, help="MLFlow tracking URI")
    parser.add_argument("--epochs", type=int, default=10)
    parser.add_argument("--batch_size", type=int, default=32)
    parser.add_argument("--verbose", type=int, default=1)
    parser.add_argument("--validation_split", type=float, default=0.1)
    parser.add_argument("--shuffle", type=bool, default=True)
    args = parser.parse_args()

    main(args)
