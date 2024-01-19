
from stockPricePredictor import StockPricePredictor
from programUtils import welcome_user as WU

selected_asset = WU()

file_path = f"../datasets/{selected_asset}.csv"

predictor = StockPricePredictor(file_path)

predictor.preprocess_data()

x_train, y_train, x_test, y_test = predictor.prepare_data()
x_train, y_train, x_test, y_test

predictor.train_model(x_train, y_train)

predicted_price = predictor.predict_prices(x_test)
predicted_price

real_price = predictor.scaler.inverse_transform(y_test.reshape(-1, 1))
real_price

predictor.plot_prices(real_price, predicted_price)

rmse, mae = predictor.evaluate_model(predicted_price, real_price)

print(f'RMSE: {rmse}')
print(f'MAE: {mae}')


