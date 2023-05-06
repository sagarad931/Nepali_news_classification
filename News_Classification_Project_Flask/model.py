import numpy as np
from scipy.sparse import csr_matrix
from sklearn.feature_extraction.text import CountVectorizer

class Multinomial:
    def __init__(self, alpha=1.0):
        self.alpha = alpha
        self.vectorizer = None
        
    
    def fit(self, X, y):
        # Convert text to word count matrix
        X_sparse = X
        
        # Get unique class labels and their counts
        self.classes, class_counts = np.unique(y, return_counts=True)
        n_classes = len(self.classes)
        
        # Calculate class prior probabilities
        self.class_prior = class_counts / np.sum(class_counts)
        
        # Calculate count of each feature per class and add smoothing
        feature_count = np.zeros((n_classes, X_sparse.shape[1]))
        for i in range(n_classes):
            Xi = X_sparse[y == self.classes[i]]
            feature_count[i, :] = np.array(Xi.sum(axis=0)).flatten() + self.alpha
        
        # Calculate count of each class
        class_count = feature_count.sum(axis=1)
        
        # Calculate log probability of each feature for each class
        self.feature_log_prob = (np.log(feature_count) - np.log(class_count.reshape(-1, 1)))
        
        return self
    
    def _log_prob(self, X):
        # Calculate log probability of each class for each sample
        return X @ self.feature_log_prob.T + np.log(self.class_prior)
    
    def predict(self, X):
        X_sparse = X
        
        # Calculate log probability of each class for each sample
        log_prob = self._log_prob(X_sparse)
        
        # Find class with highest log probability for each sample
        y_pred = np.argmax(log_prob, axis=1)
        
        # Map class index to label
        return self.classes[y_pred]
    
    def score(self, X, y):
        y_pred = self.predict(X)
        return np.mean(y_pred == y)  