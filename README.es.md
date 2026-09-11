# Telecom Customer Churn Prediction

Proyecto de machine learning de extremo a extremo para predecir la probabilidad de abandono de un cliente de telecomunicaciones (churn) a partir de datos históricos de cuenta, suscripción y uso.

---

## 1. Descripción del proyecto

El proyecto cubre todo el ciclo de vida de un modelo de machine learning: análisis exploratorio de datos (EDA), preprocesamiento, entrenamiento y comparación de cinco algoritmos de clasificación, y una aplicación web desarrollada con Streamlit para realizar predicciones de churn en tiempo real y contenerizada con Docker.

**Dataset:** `internet_service_churn.csv` — 72.274 registros de clientes con variables relacionadas con suscripciones, contratos y uso de servicios, y una variable objetivo binaria `churn`.

---

## 2. Estructura del repositorio

```text
telecom-churn-prediction/

├── data/                    # Datasets sin procesar y procesados

├── notebooks/

│   └── 01_eda.ipynb          # EDA + preprocesamiento (combinados intencionadamente; ver las notas más abajo)

│   └── 02_model_training.ipynb  # Entrenamiento, ajuste, evaluación y comparación de modelos

├── functions/                # Funciones reutilizables

├── models/                   # Artefactos de modelos guardados (.pkl, .keras) y scaler ajustado

├── history_nn/               # Historial de entrenamiento (curvas de loss/accuracy) de la red neuronal

├── pages/                    # Pantallas de la aplicación multipágina de Streamlit

├── streamlit_app.py          # Punto de entrada de la aplicación Streamlit

├── requirements.txt

├── Dockerfile                # (ver la Sección 5)

├── .gitignore

└── LICENSE
```

**Nota:** El análisis exploratorio y el preprocesamiento se combinan intencionadamente en un único notebook, ya que cada decisión de preprocesamiento (tratamiento de valores faltantes, ingeniería de características) se tomó como resultado directo del análisis realizado previamente. La justificación de cada decisión está documentada junto con el propio análisis.

---

## 3. Análisis de datos y preprocesamiento

**Principales hallazgos del EDA:**

* Se detectaron valores faltantes en `remaining_contract` (~30 % de las filas). Estos valores no se distribuyen de forma aleatoria: los clientes sin este dato presentan una tasa de churn del 91,4 %, frente al 40,1 % de los clientes con información activa sobre el contrato. En lugar de realizar una imputación simple, se crearon dos nuevas características: `has_contract_info` (indica si existe información sobre el contrato) y `has_active_contract` (indica si el contrato está actualmente activo).

* Del mismo modo, los valores faltantes en `download_avg`/`upload_avg` estaban relacionados con clientes registrados recientemente (0 % de churn). Esta situación se gestionó mediante la creación de la variable indicadora `has_usage_data`.

* La característica `dual_subscriber` se eliminó después de que el análisis de correlación revelara una correlación casi perfecta (99,99 %) con `is_movie_package_subscriber`.

* La característica `id` se eliminó, ya que su correlación con churn (-0,45) resultó ser un artefacto relacionado con el orden de registro de los clientes y no un predictor real.

* Se aplicó la estandarización (`StandardScaler`) de manera uniforme a todas las características antes del entrenamiento de los modelos, incluidos los modelos basados en árboles, para los que no es estrictamente necesaria. Esto permite mantener un único pipeline de preprocesamiento coherente.

---

## 4. Modelos y parámetros

Se entrenaron y compararon cinco modelos de clasificación, cada uno ajustado mediante `GridSearchCV` con validación cruzada:

| Modelo                 | Parámetros principales                                                                                                              |
| ---------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| Logistic Regression    | `C=7.5`, `penalty='l2'`                                                                                                             |
| Decision Tree          | `criterion='entropy'`, `max_depth=9`, `min_samples_leaf=3`                                                                          |
| Random Forest          | `criterion='entropy'`, `max_features=None`, `min_samples_leaf=4`                                                                    |
| SVM                    | `kernel='rbf'`, `C=90`, `gamma='scale'`, `probability=True`                                                                         |
| Neural Network (Keras) | Capas Dense con activación ReLU, salida sigmoid, regularización Dropout, optimizador Adam, función de pérdida `binary_crossentropy` |

---

## 5. Resultados y métricas

La evaluación se realizó utilizando Accuracy, Precision, Recall y F1-score (promedio macro y también por separado para cada clase).

| Métrica (macro avg) | Logistic Regression | Decision Tree | Random Forest |    SVM | Neural Network |
| ------------------- | ------------------: | ------------: | ------------: | -----: | -------------: |
| Accuracy            |              0.9236 |        0.9393 |    **0.9435** | 0.9322 |         0.9360 |
| Precision           |              0.9219 |        0.9377 |    **0.9423** | 0.9306 |         0.9347 |
| Recall              |              0.9256 |        0.9401 |    **0.9437** | 0.9331 |         0.9362 |
| F1-score            |              0.9231 |        0.9387 |    **0.9430** | 0.9316 |         0.9354 |

**Conclusión:** **Random Forest** fue seleccionado como modelo final. Presenta de forma consistente los mejores resultados o resultados muy cercanos al segundo puesto en prácticamente todas las métricas para ambas clases, además de ofrecer un entrenamiento rápido y una implementación sencilla.

Logistic Regression sigue siendo una alternativa sólida cuando la interpretabilidad tiene prioridad.

La diferencia de accuracy entre todos los modelos no supera el 2 %, lo que indica que las características diseñadas contienen una señal predictiva fuerte y, en gran medida, linealmente separable.

---

## 6. Integración e interfaz

La aplicación web está desarrollada con Streamlit (`streamlit_app.py`) y utiliza navegación multipágina mediante `pages/`.

Los usuarios pueden cargar un archivo CSV que contenga datos de clientes con las mismas características utilizadas durante el entrenamiento. La aplicación aplica automáticamente el mismo preprocesamiento (tratamiento de valores faltantes, creación de `has_contract_info`/`has_active_contract`) y la estandarización mediante el `scaler.pkl` guardado.

A continuación, genera una predicción de churn ("High/Low churn probability") y un porcentaje de probabilidad para cada cliente.

**Columnas de entrada requeridas:**

`is_tv_subscriber`, `is_movie_package_subscriber`, `subscription_age`, `bill_avg`, `remaining_contract`, `service_failure_count`, `download_avg`, `upload_avg`, `download_over_limit`

---

## 7. Instalación y uso

### Configuración local

```bash
git clone https://github.com/MaksimDar/telecom-churn-prediction.git

cd telecom-churn-prediction

conda create -n churn-prediction python=3.10

conda activate churn-prediction

pip install -r requirements.txt

streamlit run streamlit_app.py
```

La aplicación estará disponible en:

```text
http://localhost:8501
```

### Containerización / Docker

El proyecto está contenerizado para garantizar un entorno de ejecución reproducible.

```bash
# Construir la imagen / Build the image

docker build -t telecom-churn-app .

# Ejecutar el contenedor / Run the container

docker run --name telecom-churn-app -p 80:8501 -d telecom-churn-app
```

El contenedor escucha internamente en el puerto `8501`, que se asigna al puerto `80` del equipo anfitrión.

Después de iniciar correctamente el contenedor, la aplicación estará disponible en:

```text
http://localhost
```

Para detener el contenedor:

```bash
docker stop telecom-churn-app

docker rm telecom-churn-app
```

---

## 8. Ejemplo de uso

1. Abre la aplicación en `http://localhost` (si se ejecuta mediante Docker) o en `http://localhost:8501` (si se ejecuta localmente sin Docker).

2. Selecciona el idioma de la interfaz (ucraniano / inglés) en la barra lateral.

3. Accede a la página **"Customer Churn Risk Assessment"**.

4. Carga un archivo CSV que contenga datos de clientes con las siguientes columnas:

   `is_tv_subscriber`, `is_movie_package_subscriber`, `subscription_age`, `bill_avg`, `remaining_contract`, `service_failure_count`, `download_avg`, `upload_avg`, `download_over_limit`

5. La aplicación aplica automáticamente el preprocesamiento (tratamiento de valores faltantes, creación de `has_contract_info`/`has_active_contract` y estandarización) y genera para cada cliente una predicción ("High/Low churn probability") junto con un porcentaje de probabilidad.

**Ejemplo de fila de entrada:**

| is_tv_subscriber | is_movie_package_subscriber | subscription_age | bill_avg | remaining_contract | service_failure_count | download_avg | upload_avg | download_over_limit |
| ---------------- | --------------------------- | ---------------: | -------: | ------------------ | --------------------: | -----------: | ---------: | ------------------: |
| 1                | 0                           |              0.5 |       18 |                    |                     0 |         12.4 |        2.1 |                   0 |

**Ejemplo de salida:**

> **Resultado:** High churn probability

> **Probabilidad:** 87.42 %

---

## 9. Tecnologías utilizadas

Python 3.10 · pandas · numpy · scikit-learn · TensorFlow / Keras · Streamlit · matplotlib · seaborn · joblib · Docker

---

## 10. Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo `LICENSE` para obtener más información.

---

## 11. Autor

**Maksym Dovhusha**

Desarrollado como parte de un proyecto académico del curso de Data Science & Machine Learning.
