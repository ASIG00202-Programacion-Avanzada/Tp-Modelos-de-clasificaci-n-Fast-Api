# Bitácora del Proyecto: Predicción de Churn

---

## 1) Dataset y objetivo

- **Dataset:** Información de clientes de telecomunicaciones, incluyendo características de uso (llamadas, minutos, cargos), planes contratados y llamadas al servicio de atención al cliente.
- **Objetivo:** Predecir si un cliente realizará churn (abandono del servicio) basado en sus patrones de uso y características del plan.
- **Motivación:** Identificar clientes con alto riesgo de churn permite tomar acciones preventivas para retenerlos.

---

## 2) Selección de features/target

- **Target:** `Churn` (0 = no churn, 1 = churn)
- **Features originales:**  
  - `Account_Length`, `Area_Code`, `Intl_Plan`, `Vmail_Plan`, `Vmail_Message`, `CustServ_Calls`, `Day_Mins`, `Eve_Mins`, `Night_Mins`, `Intl_Mins`, `Day_Calls`, `Eve_Calls`, `Night_Calls`, `Intl_Calls`, `Day_Charge`, `Eve_Charge`, `Night_Charge`, `Intl_Charge`
- **Transformaciones y feature engineering:**
  - Codificación binaria de planes: `Intl_Plan`, `Vmail_Plan`
  - Derivadas:  
    - `Total_Calls` = suma de todas las llamadas  
    - `Total_Mins` = suma de minutos totales  
    - `Total_Charge` = suma de cargos totales  
    - `High_Usage` = clientes con `Total_Charge` mayor que el promedio  
    - `Many_CustServ_Calls` = clientes con más de 5 llamadas a servicio
- **Columnas finales:**  

`['Account_Length', 'Area_Code', 'Intl_Plan', 'Vmail_Plan', 'Vmail_Message', 'CustServ_Calls',
'Total_Calls', 'Total_Mins', 'Total_Charge', 'High_Usage', 'Many_CustServ_Calls']`


## 3) Modelo y preprocesamiento

- **Modelo:** Decision Tree Classifier (árbol de decisión)  
- **Parámetros ajustados:**  
- `max_depth = 5` → limita la complejidad para evitar overfitting  
- `min_samples_split = 20` → evita divisiones sobre muestras muy pequeñas  
- `min_samples_leaf = 10` → asegura que cada hoja tenga un mínimo de registros  
- **Preprocesamiento:**  
- Transformación de variables categóricas a numéricas
- Generación de features derivadas
- Eliminación de columnas redundantes
- Eliminación de valores nulos

## 4) Métrica principal y resultados

- **Métricas obtenidas en test:**
- Accuracy: 0.931 → proporción total de predicciones correctas
- Precision: 0.762 → de los clientes predichos como churn, 76% realmente churn
- Recall: 0.764 → de los clientes que hicieron churn, 76% fueron detectados. Detectamos 3 de cada 4 clientes.
- F1-score: 0.762 → balance entre precisión y recall
- **Interpretación:**  
- La métrica principal depende del objetivo de negocio. Para retención, generalmente **recall** es clave: no perder clientes que realmente van a churn.
- La precisión también es importante para no gastar recursos en clientes que no van a churn.
- Nuestro modelo muestra un buen balance entre precisión y recall.



## 5) Decisiones de contrato (payload, validaciones, respuestas)

- **Payload de entrada (`ChurnInput`):**
```json
{
  "Account_Length": 150,
  "Area_Code": 415,
  "Intl_Plan": 1,
  "Vmail_Plan": 0,
  "Vmail_Message": 50,
  "CustServ_Calls": 3,
  "Total_Calls": 500,
  "Total_Mins": 1200,
  "Total_Charge": 250,
  "High_Usage": 1,
  "Many_CustServ_Calls": 0
}```


Validaciones:

Rangos para cada campo
Tipos numéricos
Campos obligatorios

```json response
{
  "predicted_churn": 1,
  "probability_churn": 0.78,
  "warnings": ["CustServ_Calls fuera de rango típico"]
}
```


## 6) Observabilidad y pruebas

- Middleware de latencia: añade header X-Process-Time-ms a cada respuesta
- Logger estructurado: registro de cada request con ruta, método, status y tiempo de procesamiento
- Pruebas realizadas:
- Casos válidos: 3 (diferentes perfiles de clientes)
- Casos inválidos: 3 (campo faltante, tipo incorrecto, campo extra)
- Verificación de probabilidades y predicciones
- Endpoint adicional: /export_predictions
- Genera un Excel con los datos originales, las features derivadas y las predicciones + probabilidades



## 7) Lecciones aprendidas

- La selección de features derivadas (Total_Calls, Total_Charge, High_Usage) mejoró el desempeño del modelo sin agregar complejidad innecesaria.
- Ajustar min_samples_split y min_samples_leaf permite balancear overfitting y precisión.
- Es crítico definir claramente el payload y validaciones para APIs de ML, evitando errores por desorden de columnas o tipos de datos.
- Medir tanto precision como recall ayuda a decidir umbrales de acción para negocio.
- Registrar métricas de latencia y warnings incrementa la confiabilidad y explicabilidad de la API.
- La documentación clara y el pipeline reproducible facilitan la entrega y el entendimiento por terceros.
