import pandas as pd
import nltk,os
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

# Step 1: Data Preprocessing
nltk.download('stopwords')
nltk.download('punkt')
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    # Remove special characters and symbols
    text = ''.join([c for c in text if c.isalnum() or c.isspace()])
    # Convert to lowercase
    text = text.lower()
    # Tokenize text
    tokens = word_tokenize(text)
    # Remove stopwords
    tokens = [token for token in tokens if token not in stop_words]
    return ' '.join(tokens)

# Step 2: Feature Extraction
def extract_features(text_data):
    vectorizer = CountVectorizer()
    features = vectorizer.fit_transform(text_data)
    return features, vectorizer

# Step 3: Clustering
def perform_clustering(features, num_clusters):
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    cluster_labels = kmeans.fit_predict(features)
    return cluster_labels

# Step 4: Visualization and Evaluation
def visualize_clusters(features, cluster_labels):
    # Reduce dimensionality for visualization
    pca = PCA(n_components=2)
    reduced_features = pca.fit_transform(features.toarray())

    # Plotting the clusters
    plt.scatter(reduced_features[:, 0], reduced_features[:, 1], c=cluster_labels, cmap='viridis')
    plt.xlabel('PC1')
    plt.ylabel('PC2')
    plt.title('Cluster Visualization')
    plt.show()

    # Evaluate clustering using silhouette score
    silhouette_avg = silhouette_score(features, cluster_labels)
    print(f"Silhouette Score: {silhouette_avg}")

# Step 5: Aggregation
def aggregate_clusters(data, cluster_labels):
    data['Cluster'] = cluster_labels
    # Display a representative article from each cluster
    aggregated_data = data.groupby('Cluster').first()
    return aggregated_data

if __name__ == '__main__':

    # Load the sample data into a Pandas DataFrame
    file_path = os.path.join(os.getcwd(), "Headlines_dataset.csv")
    data = pd.read_csv(file_path)

    # Step 1: Data Preprocessing
    data['Title'] = data['Title'].apply(preprocess_text)
    data['Description'] = data['Description'].apply(preprocess_text)

    # Step 2: Feature Extraction
    text_data = data['Title'] + ' ' + data['Description']
    features, vectorizer = extract_features(text_data)

    # Step 3: Clustering
    num_clusters = 3 # You can set the desired number of clusters
    cluster_labels = perform_clustering(features, num_clusters)

    # Step 4: Visualization and Evaluation
    visualize_clusters(features, cluster_labels)

    # Step 5: Aggregation
    aggregated_data = aggregate_clusters(data, cluster_labels)
    print(aggregated_data)