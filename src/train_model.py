import pandas as pd
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_validate
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline
import joblib
import os

MODEL_PATH = "models/trainModel.pkl"
os.makedirs("models", exist_ok=True)

class TrainModel():

    # ------------------------------
    # Funciones
    # ------------------------------

    def load_data(self, path="source_data/Churn.xlsx"):
        """Cargar dataset"""
        df = pd.read_excel(path)
        return df

    def explore_data(self, df):
        """Explorar dataset."""
        print("Primeras filas:\n", df.head())
        print("\nInformación del dataset:\n", df.describe())
        print("\nDistribución de la variable objetivo 'Churn':\n", df['Churn'].value_counts(normalize=True))

    def preprocess_data(self, df):
        # Transformación
        df['Intl_Plan'] = df['Intl_Plan'].map({'yes': 1, 'no': 0})
        df['Vmail_Plan'] = df['Vmail_Plan'].map({'yes': 1, 'no': 0})
        df['Churn'] = df['Churn'].map({'True.': 1, 'False.': 0})

        # Nuevas variables derivadas
        df['Total_Calls'] = df['Day_Calls'] + df['Eve_Calls'] + df['Night_Calls'] + df['Intl_Calls']
        df['Total_Mins'] = df['Day_Mins'] + df['Eve_Mins'] + df['Night_Mins'] + df['Intl_Mins']
        df['Total_Charge'] = df['Day_Charge'] + df['Eve_Charge'] + df['Night_Charge'] + df['Intl_Charge']
        df['High_Usage'] = (df['Total_Charge'] > df['Total_Charge'].mean()).astype(int)
        df['Many_CustServ_Calls'] = (df['CustServ_Calls'] > 5).astype(int)

        df = df.drop(columns=['Phone', 'State','Day_Calls', 'Eve_Calls', 'Night_Calls','Intl_Calls',   
                            'Day_Mins', 'Eve_Mins', 'Night_Mins','Intl_Mins', 
                            'Day_Charge', 'Eve_Charge','Night_Charge', 'Intl_Charge'])
        # Eliminar nulos
        df = df.dropna()

        X = df.drop('Churn', axis=1)
        y = df['Churn']

        return X, y


    def split_data(self, X, y, test_size=0.3, random_state=42):
        """Dividir dataset en train/test."""
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state, stratify=y)
        return X_train, X_test, y_train, y_test

    def create_model_pipeline(self, max_depth=5, min_samples_leaf=10, min_samples_split=20):
        """Crear pipeline árbol de decisión."""
        pipeline = Pipeline(steps=[
            ('smote', SMOTE(random_state=42)),
            ('clf', DecisionTreeClassifier(max_depth=max_depth, min_samples_leaf=min_samples_leaf,min_samples_split=min_samples_split, random_state=42))
        ])
        return pipeline

    def train_model(self, pipeline, X_train, y_train):
        """Entrenar modelo de árbol de decisión."""
        pipeline.fit(X_train, y_train)
        return pipeline

    def evaluate_model(self, model, X_test, y_test):
        """Evaluar modelo en test y mostrar métricas."""
        y_pred = model.predict(X_test)
        print("\n📊 Reporte de Clasificación en Test:\n")
        print(classification_report(y_test, y_pred))
        return y_pred

    def cross_validate_model(self, model, X_train, y_train):
        """Cross-validation 5 folds en train."""
        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
        scoring = ['accuracy', 'precision', 'recall', 'f1']
        cv_results = cross_validate(model, X_train, y_train, cv=cv, scoring=scoring)
        print("\n📊 Resultados de cross-validation (promedio en 5 folds):")
        for metric in scoring:
            print(f"{metric}: {cv_results['test_' + metric].mean():.3f}")

    def create_model_visualization(self, model, X, y_test, y_pred):
        """Visualización del árbol y matriz de confusión."""
        plt.figure(figsize=(20, 8))
        plot_tree(
            model.named_steps['clf'],
            feature_names=X.columns,
            class_names=["Churn", "No Churn"],
            filled=True,
            rounded=True,
            fontsize=10
        )
        plt.title("Árbol de Decisión - Churn")
        plt.show()

        # Matriz de confusión
        cm = confusion_matrix(y_test, y_pred)
        disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["Churn", "No Churn"])
        disp.plot(cmap='Blues')
        plt.title("Matriz de Confusión - Árbol de Decisión")
        plt.show()

    def save_model(self, model, columns, path=MODEL_PATH):
        """Guardar modelo + columnas usadas."""
        joblib.dump({
            "model": model,
            "columns": columns
        }, path)
        print(f"\n✅ Modelo guardado en {path}")

    # ------------------------------
    # Pipeline principal
    # ------------------------------

    def main(self):
        df = self.load_data()
        self.explore_data(df)
        X, y = self.preprocess_data(df)
        X_train, X_test, y_train, y_test = self.split_data(X, y)
        
        pipeline = self.create_model_pipeline()
        model = self.train_model(pipeline, X_train, y_train)
        
        y_pred = self.evaluate_model(model, X_test, y_test)
        self.cross_validate_model(model, X_train, y_train)
        
        self.create_model_visualization(model, X, y_test, y_pred)
        self.save_model(model, X.columns.tolist())

# ------------------------------
# Ejecutar
# ------------------------------

if __name__ == "__main__":
    trainer = TrainModel()
    trainer.main()
