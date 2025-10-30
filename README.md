
# PROJETO DE MACHINE LEARNING - DIABETES

## 🌍 Contexto e Motivação

A **diabetes** é uma das maiores ameaças à saúde pública global: é crônica, progressiva e responsável por grande parte dos custos hospitalares, perda de produtividade e redução da qualidade de vida. Detectá-la cedo transforma cuidados clínicos, reduz complicações evitáveis e otimiza alocação de recursos em saúde, por isso modelos preditivos bem calibrados podem funcionar como ferramentas de triagem que ampliam o alcance de equipes médicas e programas preventivos.

Este projeto tem como objetivo construir um serviço de inferência que preveja **a presença de diabetes (classe 1)** a partir de features clínicos e demográficas, unindo técnicas de pré-processamento, balanceamento e aprendizado de máquina para entregar previsões confiáveis, interpretáveis e acionáveis. Ao transformar dados em alertas clínicos, o sistema pode priorizar pacientes para exames adicionais, orientar intervenções precoces e reduzir custos e danos associados a diagnósticos tardios.

**Benefícios esperados:**

- **Detecção precoce:** aumentar a sensibilidade para identificar casos reais.

- **Eficiência clínica:** priorização de pacientes de alto risco para testes confirmatórios.

- **Redução de custos:** evitar hospitalizações e complicações caras por diagnóstico tardio.

- **Transparência:** fornecer explicações e importâncias de variáveis para suporte clínico.

---

## 📊 Base de Dados

O conjunto de dados utilizado está disponível no Kaggle:

[**Diabetes Dataset from Kaggle** - Ayushman Yashaswi](https://www.kaggle.com/datasets/ayushmanyashaswi/diabetes-dataset-from-kaggle)

Para realizar o **download localmente**, execute o comando abaixo:

```bash
#!/bin/bash
curl -L -o ~/Downloads/diabetes-dataset-from-kaggle.zip\
  https://www.kaggle.com/api/v1/datasets/download/ayushmanyashaswi/diabetes-dataset-from-kaggle
```

Sobre as colunas, apresenta-se o significado e a unidade a seguir:

- **Pregnancies:** Número de gestações.
- **Glucose:** Concentração plasmática de glicose (mg/dL).
- **BloodPressure:** Pressão arterial diastólica (mm Hg).
- **SkinThickness:** Espessura do dobramento cutâneo do tríceps (mm).
- **Insulin:** Insulina sérica em 2 horas (μU/ml).
- **BMI:** Índice de massa corporal (kg/m²).
- **DiabetesPedigreeFunction:** Probabilidade de diabetes com base em histórico familiar.
- **Age:** Idade do paciente (anos).
- **Outcome:** Variável alvo (0: Não diabético, 1: Diabético).

---

## 🧩 Estrutura do Projeto

```bash
./
├── app.py
├── Dockerfile
├── notebook.ipynb
├── predict_script.py
├── requirements.txt
└── models_output/
    └── *.joblib  (modelos treinados)
```

---

## ⚙️ Instalação e Execução

A partir da raiz do projeto, inicie o notebook jupyter:

```bash
jupyter notebook
```

Na aba que se abre no navegador, acesse o notebook e execute todas as células. Espere a conclusão do treinamento.

Instale as dependências necessárias:

```bash
pip install -r requirements.txt
```

Execute a aplicação localmente:

```bash
python app.py
```

A aplicação estará disponível em:

- [http://localhost:5000](http://localhost:5000)
- [http://127.0.0.1:5000](http://127.0.0.1:5000)

Requisições à raiz redirecionam automaticamente para a **documentação Swagger**:

- [http://localhost:5000/swagger](http://localhost:5000/swagger)

---

## 🧪 Testando a API

Considere um paciente com essas informações:

```python
    person =  {
        'Pregnancies': 2.0, # Quant. de gestações
        'Glucose': 100.0, # (mg/dL) - Concentração plasmática de glicose 
        'BloodPressure': 80.0, # (mm Hg) - Pressão arterial 
        'SkinThickness': 32.0, # (mm) - Espessura do dobramento cutâneo do tríceps 
        'Insulin': 80.0, # (μU/ml) - Insulina sérica em 2 horas
        'BMI': 32.0, # (kg/m²) - Índice de massa corporal
        'DiabetesPedigreeFunction': 0.37, # Prob. de diabetes com base em hist. familiar
        'Age': 29.0 # anos
    }
```

Você pode realizar requisições via terminal com **cURL**:

```bash
curl -X 'POST' \
  'http://127.0.0.1:5000/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "Age": 29,
  "BMI": 32,
  "BloodPressure": 80,
  "DiabetesPedigreeFunction": 0.37,
  "Glucose": 100,
  "Insulin": 80,
  "Pregnancies": 2,
  "SkinThickness": 32
}'
```

Também é possível testar diretamente pela interface Swagger, clicando em **Try it out**, alterando os valores conforme desejado e pressionando **Execute**.  
A resposta será semelhante a:

```bash
{
  "description": "Pacient is non-diabetic",
  "prediction": 0
}
```

---

## 🐳 Execução com Docker

### Criar a imagem

```bash
docker build -t flask-diabetes-app .
```

### Executar o container

```bash
docker run -d -p 5000:5000 --name flask-diabetes-container flask-diabetes-app
```

A aplicação estará disponível em:

- [http://localhost:5000](http://localhost:5000)
- [http://127.0.0.1:5000](http://127.0.0.1:5000)

Requisições à raiz redirecionam automaticamente para a **documentação Swagger**:

- [http://localhost:5000/swagger](http://localhost:5000/swagger)

### Visualizar logs

```bash
docker logs -f flask-diabetes-container
```

### Encerrar e remover container e imagem

```bash
docker stop flask-diabetes-container
docker rm flask-diabetes-container
docker rmi flask-diabetes-app
```

---

Projeto desenvolvido para estudos em **Machine Learning aplicado à identificação de pacientes diabéticos**.
