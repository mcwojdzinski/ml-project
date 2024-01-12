from programUtils import LibraryChecker as LC
#if LC().check_all_libraries() == False:quit(0)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn import metrics
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout






class StockPricePredictor:
    def __init__(self, file_path):
        self.dataset = pd.read_csv(file_path)
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.window = 70
        self.model = self.build_model()

    def preprocess_data(self):
        trainset = self.dataset.iloc[:, 3:4].values
        self.data_scaled = self.scaler.fit_transform(trainset)

    def prepare_data(self):
        x_train, y_train = [], []
        x_test, y_test = [], []

        for i in range(self.window, len(self.data_scaled)):
            x_train.append(self.data_scaled[i - self.window:i, 0])
            y_train.append(self.data_scaled[i, 0])

        for i in range(len(self.data_scaled) - self.window, len(self.data_scaled)):
            x_test.append(self.data_scaled[i - self.window:i, 0])
            y_test.append(self.data_scaled[i, 0])

        x_train, y_train = np.array(x_train), np.array(y_train)
        x_test, y_test = np.array(x_test), np.array(y_test)

        x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
        x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

        return x_train, y_train, x_test, y_test

    def build_model(self):
        regressor = Sequential()
        regressor.add(LSTM(units=50, return_sequences=True, input_shape=(self.window, 1)))
        regressor.add(Dropout(0.2))
        regressor.add(LSTM(units=50, return_sequences=True))
        regressor.add(Dropout(0.2))
        regressor.add(LSTM(units=50, return_sequences=True))
        regressor.add(Dropout(0.2))
        regressor.add(LSTM(units=50))
        regressor.add(Dropout(0.2))
        regressor.add(Dense(units=1))
        regressor.compile(optimizer='adam', loss='mean_squared_error')
        return regressor

    def train_model(self, x_train, y_train, epochs=30, batch_size=32):
        self.model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size)

    def predict_prices(self, x_test):
        predicted_price = self.model.predict(x_test)
        return self.scaler.inverse_transform(predicted_price)

    def evaluate_model(self, predicted_price, real_price):
        rmse = metrics.mean_squared_error(predicted_price, real_price, squared=False)
        mae = metrics.mean_absolute_error(predicted_price, real_price)
        return rmse, mae

    def plot_prices(self, real_price, predicted_price):
        plt.plot(real_price, color='orange', label='Real Price')
        plt.plot(predicted_price, color='green', label='Predicted Price')
        plt.title('Stock Price Prediction')
        plt.xlabel('Time')
        plt.ylabel('Stock Price')
        plt.legend()
        plt.show()
