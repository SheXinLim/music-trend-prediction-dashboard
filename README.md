# AI-Powered A&R Music Trends Dashboard

This project showcases an end-to-end pipeline from data collection and feature engineering to model training and dashboard deployment. With robust performance metrics and clear insights from feature importance, the model effectively distinguishes viral tracks from non-viral ones, offering valuable support for A&R decision-making in the music industry.

## Conclusions & Strategic Insights
Overall, I’ve shown that artist popularity and release timing are pivotal in predicting song virality. My model’s high performance and the dashboard’s interactive charts provide a powerful tool for A&R teams to identify and track emerging trends.

## Tech Stack
- **Data Processing & Storage:** Python, Pandas, NumPy, SQL, PostgreSQL
- **Machine Learning/AI Libraries:** scikit-learn, LightGBM, XGBoost, and Optuna for hyperparameter tuning
- **Visualization & Dashboard:** Plotly, Dash (or Streamlit for a web app)

## Key Insights
### 1. Artist Popularity Dominates
My feature importance plot shows that artist_popularity is by far the strongest predictor of whether a track goes viral. This indicates that well-known artists heavily influence a song’s chance of becoming a hit.

### 2. Release Timing Matters
release_month and days_since_release also contribute significantly to virality predictions, suggesting seasonality (certain months may boost a track’s visibility) and that recent releases can be more likely to surge in popularity.

### 3. High Model Performance
My LightGBM model achieves high accuracy (around 97%), along with strong precision, recall, and F1-scores. This means it both catches most viral songs (high recall) and rarely misclassifies non-viral tracks as viral (high precision).

### 4. Actionable Dashboard Visualizations
The bar chart comparing track popularity by artist highlights which artists are currently driving hits, helping A&R teams quickly spot rising stars or confirm which established artists continue to perform well.
 
### 5. Robust, Not Overfitting
Cross-validation (around 95.9% accuracy) confirms that the model generalizes well to unseen data, reducing the risk of overfitting.


## **1. Problem Definition**
   - **Objective**: Predict song virality based on features like artist popularity, release date, and audio features.
   - **Relevance**: This is a real-world problem in the music industry, where predicting viral songs can help A&R (Artists and Repertoire) teams make data-driven decisions.

---

## **2. Data Collection and Preprocessing**
   - **Data Source**: Used **Spotify API** to collect data on artists, tracks, and audio features.
   - **Data Cleaning**: Handled missing or inconsistent data (e.g., fixing `release_date` formats).
   - **Feature Engineering**: Created meaningful features like `days_since_release` and `release_year` to improve model performance.

---

## **3. Model Development**
   - **Algorithm**: **LightGBM**
   - **Hyperparameter Tuning**:  **Optuna** is used to fine-tune the model's hyperparameters
   - **Evaluation Metrics**: Evaluated the model using **accuracy, precision, recall, F1-score, and AUC-ROC**, which are appropriate for a binary classification problem.

---

## **4. Model Performance**
   - **Accuracy**: **97.4%** on the test set and **95.9%** in cross-validation, which is excellent.
   - **Precision (85%)**: When the model predicts a song as viral, it’s correct 85% of the time.
   - **Recall (96%)**: The model captures 96% of the actual viral songs, meaning it misses very few.
   - **F1-Score (0.90)**: Balances precision and recall, indicating strong overall performance.
   - **AUC-ROC (0.96)**: The model has a 96% chance of correctly distinguishing between viral and non-viral songs, which is outstanding.

---

## **5. Robustness and Generalization**
   - **Cross-Validation**: The high cross-validation accuracy (**95.9%**) confirms that the model generalizes well to unseen data and is not overfitting.
   - **Baseline Comparison**: The baseline accuracy (**86.98%**) is significantly lower than your model's accuracy, showing that your model adds real value.

---

## **6. Feature Importance**
   - Analyzed feature importance to understand which features (e.g., `artist_popularity`, `days_since_release`) are driving the predictions. This is critical for interpretability and actionable insights.

---

## **7. Dashboard 
   - **Dashboard**: Used **Plotly/Dash** to create an interactive dashboard for visualizing trends, predicted hits, and genre popularity shifts.



