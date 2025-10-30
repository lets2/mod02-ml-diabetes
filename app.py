
from flask import Flask, request, jsonify, redirect
import sys
import os
from flask_swagger_ui import get_swaggerui_blueprint

# Para o google colab exite uma pasta content/
if '/content/' not in sys.path:
    sys.path.append('/content/')

# Importar função de previsão do script
try:
    from predict_script import predict_diabetes
    print("Successfully imported predict_diabetes function.")
except ImportError as e:
    print(f"Error importing predict_diabetes: {e}")
    predict_diabetes = None


app = Flask(__name__)


# Define Swagger UI configuration
SWAGGER_URL = '/swagger'  # URL para acessar Swagger UI
API_URL = '/static/swagger.json' # Nossa Swagger spec é servida daqui

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Diabetes Prediction API"
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Define a especificação do Swagger
SWAGGER_SPEC = {
    "swagger": "2.0",
    "info": {
        "version": "1.0.0",
        "title": "Diabetes Prediction API"
    },
    "paths": {
        "/predict": {
            "post": {
                "summary": "Diabetes Prediction API",
                "consumes": ["application/json"],
                "produces": ["application/json"],
                "parameters": [
                    {
                        "in": "body",
                        "name": "body",
                        "description": "Patient clinical and biometric features",
                        "required": True,
                        "schema": {
                            "type": "object",
                            "properties": {
                                "Pregnancies": { "type": "number", "description": "Número de gestações (contagem)" },
                                "Glucose": { "type": "number", "description": "Concentração plasmática de glicose (mg/dL)" },
                                "BloodPressure": { "type": "number", "description": "Pressão arterial diastólica (mm Hg)" },
                                "SkinThickness": { "type": "number", "description": "Espessura do dobramento cutâneo do tríceps (mm)" },
                                "Insulin": { "type": "number", "description": "Insulina sérica em 2 horas (μU/ml)" },
                                "BMI": { "type": "number", "description": "Índice de massa corporal (kg/m²)" },
                                "DiabetesPedigreeFunction": { "type": "number", "description": "Probabilidade de diabetes com base em histórico familiar (sem unidade)" },
                                "Age": { "type": "number", "description": "Idade do paciente (anos)" }
                            },
                            "example": {
                                'Pregnancies': 2.0,
                                'Glucose': 100.0, # (mg/dL)
                                'BloodPressure': 80.0, # (mm Hg)
                                'SkinThickness': 32.0, # (mm)
                                'Insulin': 80.0, # (μU/ml)
                                'BMI': 32.0, #(kg/m²)
                                'DiabetesPedigreeFunction': 0.37, #Prob. de diabetes com base em hist. familiar
                                'Age': 29.0 # years
                            }
                        }
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Successful prediction",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "prediction": {"type": "integer", "description": "0 for non-diabetic, 1 for diabetic"},
                                "description": {"type": "string", "description": "Human-readable prediction"}
                            }
                        }
                    },
                    "400": {
                        "description": "Invalid input",
                        "example": {
                                'Pregnancies': 2.0,
                                'Glucose': 100.0, # (mg/dL)
                                'BloodPressure': 80.0, # (mm Hg)
                                'SkinThickness': 32.0, # (mm)
                                'Insulin': 80.0, # (μU/ml)
                                'BMI': 32.0, #(kg/m²)
                                'DiabetesPedigreeFunction': 0.37, #Prob. de diabetes com base em hist. familiar
                                'Age': 29.0 # years
                            }
                    },
                    "500": {
                        "description": "Internal server error"
                    }
                }
            }
        }
    }
}

# Route que serve o Swagger JSON spec
@app.route(API_URL)
def swagger_spec():
    return jsonify(SWAGGER_SPEC)


@app.route('/predict', methods=['POST'])
def predict():
    """
    Recebe um JSON payload com as features de uma amostra de água,
    prevê se um paciente é diabético ou nao e retorna o resultado.
    """
    if predict_diabetes is None:
        return jsonify({"error": "Prediction function not loaded."}), 500

    try:
        data = request.get_json(force=True)
        # Assumindo que o JSON de entrada tem keys que bate com os nomes das features
        # ex.: {'Pregnancies': 2.0, 'Glucose': 100.0, ...}

        # Fazer previsão
        prediction = predict_diabetes(data)

        if prediction is not None:
            result = {
                'prediction': prediction,
                'description': 'Pacient is diabetic' if prediction == 1 else 'Pacient is non-diabetic'
            }
            return jsonify(result)
        else:
            return jsonify({"error": "Prediction failed."}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 400


# Redireciona a raiz "/" para a documentação Swagger
@app.route('/')
def redirect_to_swagger():
    return redirect('/swagger', code=302)


if __name__ == '__main__':
    # Execute a aplicação Flask
    app.run(host='0.0.0.0', port=5000)
