import numpy as np


class NaiveBayes:
    
    def fit(self, X, y):
        n_samples, n_features = X.shape 
        self._classes = np.unique(y)
        n_classes = len(self._classes)
        
        # Init mean, variance, prior probabilities
        self._mean = np.zeros((n_classes, n_features), dtype=np.float64)
        self._var = np.zeros((n_classes, n_features), dtype=np.float64)
        self._priors = np.zeros(n_classes, dtype=np.float64)
        
        for cls in self._classes:
            X_cls = X[y == cls]
            self._mean[cls,:] = X_cls.mean(axis=0)
            self._var[cls,:] = X_cls.var(axis=0 )
            self._priors[cls] = X_cls.shape[0] / float(n_samples)
    
    def predict(self, X):
        y_predicted = [self._predict(x) for x in X]
        return y_predicted
    
    def _predict(self, x):
        posteriors = []
        
        for idx, cls in enumerate(self._classes):
            prior = np.log(self._priors[idx])
            class_conditional = np.sum(np.log(self._pdf(idx, x)))
            posterior = prior + class_conditional
            posteriors.append(posterior)
            
        return self._classes[np.argmax(posteriors)]
                  
    def _pdf(self, class_idx, x):
        mean = self._mean[class_idx]
        var = self._var[class_idx]
        numerator = np.exp(- (x - mean)**2 / (2 * var)) 
        denominator = np.sqrt(2 * np.pi * var)
        return numerator / denominator