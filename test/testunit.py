import unittest
from unittest.mock import patch
from stockPricePredictor import StockPricePredictor

class TestStockPricePredictor(unittest.TestCase):

    @patch("builtins.input", side_effect=["1"])
    def test_preprocess_data(self, mock_input):
        file_path = "datasets/TSLA.csv"
        predictor = StockPricePredictor(file_path)
        predictor.preprocess_data()
        self.assertIsNotNone(predictor.data_scaled)
        self.assertEqual(predictor.data_scaled.shape[1], 1)

    def test_prepare_data(self):
        file_path = "datasets/TSLA.csv"
        predictor = StockPricePredictor(file_path)
        predictor.preprocess_data()
        x_train, y_train, x_test, y_test = predictor.prepare_data()
        self.assertIsNotNone(x_train)
        self.assertIsNotNone(y_train)
        self.assertIsNotNone(x_test)
        self.assertIsNotNone(y_test)
        self.assertEqual(x_train.shape[2], 1)

    def test_build_model(self):
        file_path = "datasets/TSLA.csv"
        predictor = StockPricePredictor(file_path)
        model = predictor.build_model()
        self.assertIsNotNone(model)

    def test_train_model(self):
        file_path = "datasets/TSLA.csv"
        predictor = StockPricePredictor(file_path)
        predictor.preprocess_data()
        x_train, y_train, x_test, y_test = predictor.prepare_data()
        predictor.train_model(x_train, y_train, epochs=1, batch_size=1)

    def test_predict_prices(self):
        file_path = "datasets/TSLA.csv"
        predictor = StockPricePredictor(file_path)
        predictor.preprocess_data()
        x_train, y_train, x_test, y_test = predictor.prepare_data()
        predictor.train_model(x_train, y_train, epochs=1, batch_size=1)
        predicted_price = predictor.predict_prices(x_test)
        self.assertIsNotNone(predicted_price)

    def test_evaluate_model(self):
        file_path = "datasets/TSLA.csv"
        predictor = StockPricePredictor(file_path)
        predictor.preprocess_data()
        x_train, y_train, x_test, y_test = predictor.prepare_data()
        predictor.train_model(x_train, y_train, epochs=1, batch_size=1)
        predicted_price = predictor.predict_prices(x_test)
        real_price = predictor.scaler.inverse_transform(y_test.reshape(-1, 1))
        rmse, mae = predictor.evaluate_model(predicted_price, real_price)
        self.assertIsNotNone(rmse)
        self.assertIsNotNone(mae)

if __name__ == '__main__':
    unittest.main()