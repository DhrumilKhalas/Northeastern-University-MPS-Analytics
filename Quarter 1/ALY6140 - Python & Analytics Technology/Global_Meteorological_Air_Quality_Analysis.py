import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def clean_outliers(df, features):
    """Removes outliers from the given numerical columns using the IQR method."""
    df_clean = df.copy()
    for feature in features:
        Q1 = df_clean[feature].quantile(0.25)
        Q3 = df_clean[feature].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        df_clean = df_clean[(df_clean[feature] >= lower) & (df_clean[feature] <= upper)]
    return df_clean

 
def summarize_feature_distribution(df, features):
    """Generates histograms and boxplots for multiple features."""
    plt.figure(figsize=(20,10))
    for i, feature in enumerate(features, 1):
        plt.subplot(2, 4, i)
        sns.histplot(df[feature], bins=30, kde=True, color='skyblue')
        plt.title(f'Distribution of {feature}')
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(20,10))
    for i, feature in enumerate(features, 1):
        plt.subplot(2, 4, i)
        sns.boxplot(x=df[feature], color='skyblue')
        plt.title(f'Boxplot of {feature}')
    plt.tight_layout()
    plt.show()


def evaluate_classification_model(y_true, y_pred, y_prob=None):
    """Prints and returns key classification metrics."""
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
    results = {
        'Accuracy': accuracy_score(y_true, y_pred),
        'Precision': precision_score(y_true, y_pred),
        'Recall': recall_score(y_true, y_pred),
        'F1 Score': f1_score(y_true, y_pred)
    }
    if y_prob is not None:
        results['ROC AUC'] = roc_auc_score(y_true, y_prob)
    for k, v in results.items():
        print(f"{k}: {v:.3f}")