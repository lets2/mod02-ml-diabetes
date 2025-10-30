
import joblib
import pandas as pd
import os

# Path para a pasta onde  foi salvo o pipeline completo
OUT_DIR = "models_output"
PIPELINE_PATH = os.path.join(OUT_DIR, "full_prediction_pipeline.joblib")

# Carrega o pipeline de previsão
try:
    loaded_pipeline = joblib.load(PIPELINE_PATH)
    print("Prediction pipeline loaded successfully.")
except FileNotFoundError:
    print(f"Error: Pipeline file not found at {PIPELINE_PATH}")
    loaded_pipeline = None

# Lista de features originais
feature_names = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']

def predict_diabetes(data_point):
    """
    Preve se a pessoa é diabética ou não usando a pipeline completa.
    Args:
        data_point (dict): Um dicionário que representa um paciente
        com keys correspondentes aos nomes das features originais.

    Returns:
        int: Diabetes (1 para diabético, 0 para não diabético)
    """
    if loaded_pipeline is None:
        return None

    # Converte os dados de entrada em pandas DataFrame
    # Assegurar a ordem das colunas batem com os dados de treinamentos
    input_df = pd.DataFrame([data_point], columns=feature_names)

    # Fazer previsão
    prediction = loaded_pipeline.predict(input_df)

    # A previsao é um numpy array, returne o primeiro elemento
    return int(prediction[0])

if __name__ == '__main__':
    # Examplo de uso para teste do script diretamente
    # Troque o valor pelos dados de vdd
    sample_data = {
        'Pregnancies': 2.0,
        'Glucose': 100.0, # (mg/dL)
        'BloodPressure': 80.0, # (mm Hg)
        'SkinThickness': 32.0, # (mm)
        'Insulin': 80.0, # (μU/ml)
        'BMI': 32.0, #(kg/m²)
        'DiabetesPedigreeFunction': 0.37, #Prob. de diabetes com base em hist. familiar
        'Age': 29.0 # years
    }

    prediction = predict_diabetes(sample_data)

    if prediction is not None:
        print(f"Sample data: {sample_data}")
        print(f"Predicted diabetes: {prediction}")
    else:
        print("Prediction failed due to pipeline loading error.")
