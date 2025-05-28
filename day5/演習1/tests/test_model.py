"""
モデルのテスト処理を実装するモジュール

このモジュールでは以下のテストを実装します：
1. モデルの推論精度の検証
2. 推論時間の測定
3. 過去バージョンのモデルとの性能比較
"""

import os
import time
import pickle
import mlflow
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from day5.演習1.main import prepare_data, train_and_evaluate

def test_model_accuracy():
    """モデルの推論精度を検証するテスト"""
    # テストデータの準備
    X_train, X_test, y_train, y_test = prepare_data(test_size=0.2, random_state=42)
    
    # モデルの学習
    model, _ = train_and_evaluate(X_train, X_test, y_train, y_test)
    
    # 推論
    predictions = model.predict(X_test)
    
    # 各種メトリクスの計算
    accuracy = accuracy_score(y_test, predictions)
    precision = precision_score(y_test, predictions)
    recall = recall_score(y_test, predictions)
    f1 = f1_score(y_test, predictions)
    
    # 閾値の設定（例：accuracy > 0.75）
    assert accuracy > 0.75, f"精度が閾値を下回っています: {accuracy}"
    assert precision > 0.7, f"適合率が閾値を下回っています: {precision}"
    assert recall > 0.69, f"再現率が閾値を下回っています: {recall}"
    assert f1 > 0.7, f"F1スコアが閾値を下回っています: {f1}"

def test_inference_time():
    """推論時間を測定するテスト"""
    # テストデータの準備
    X_train, X_test, y_train, y_test = prepare_data(test_size=0.2, random_state=42)
    
    # モデルの学習
    model, _ = train_and_evaluate(X_train, X_test, y_train, y_test)
    
    # 推論時間の測定
    start_time = time.time()
    _ = model.predict(X_test)
    inference_time = time.time() - start_time
    
    # 推論時間の閾値（例：1秒未満）
    assert inference_time < 1.0, f"推論時間が閾値を超えています: {inference_time}秒"

def test_model_comparison():
    """過去バージョンのモデルとの性能比較テスト"""
    # 現在のモデルの学習
    X_train, X_test, y_train, y_test = prepare_data(test_size=0.2, random_state=42)
    current_model, current_accuracy = train_and_evaluate(X_train, X_test, y_train, y_test)
    
    # 過去のモデルの読み込み（存在する場合）
    model_path = os.path.join("models", "titanic_model.pkl")
    if os.path.exists(model_path):
        with open(model_path, "rb") as f:
            previous_model = pickle.load(f)
        
        # 過去モデルの性能評価
        previous_predictions = previous_model.predict(X_test)
        previous_accuracy = accuracy_score(y_test, previous_predictions)
        
        # 性能劣化のチェック（例：5%以内の許容範囲）
        performance_degradation = previous_accuracy - current_accuracy
        assert performance_degradation <= 0.05, f"性能が5%以上劣化しています: {performance_degradation}"

def test_mlflow_integration():
    """MLflowとの統合テスト"""
    # テストデータの準備
    X_train, X_test, y_train, y_test = prepare_data(test_size=0.2, random_state=42)
    
    # モデルの学習とMLflowへの記録
    model, accuracy = train_and_evaluate(X_train, X_test, y_train, y_test)
    
    # MLflowの実行を確認
    with mlflow.start_run() as run:
        mlflow.log_metric("test_accuracy", accuracy)
        # 実行が開始されたことを確認
        assert run.info.status in ["RUNNING", "FINISHED"], "MLflowの実行が開始されていません" 
