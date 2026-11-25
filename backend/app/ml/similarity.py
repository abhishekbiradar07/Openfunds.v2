try:
    import pandas as pd
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    SIMILARITY_AVAILABLE = True
except ImportError:
    SIMILARITY_AVAILABLE = False
    print("⚠️ Similarity libraries not available")

import logging

logger = logging.getLogger(__name__)


class SimilarityEngine:
    """TF-IDF cosine similarity engine for finding duplicate campaigns"""

    @classmethod
    def find_similar(cls, title, description, campaigns_data, top_k=3, threshold=0.3):
        """Find similar campaigns using TF-IDF cosine similarity"""
        if not SIMILARITY_AVAILABLE:
            return {
                'success': False,
                'error': 'Similarity libraries not installed'
            }

        try:
            if not campaigns_data or len(campaigns_data) == 0:
                return {
                    'success': True,
                    'similar_campaigns': [],
                    'count': 0
                }

            df = pd.DataFrame(campaigns_data)
            df['text'] = df['title'].astype(str) + " " + df['description'].astype(str)
            input_text = title + " " + description

            corpus = df['text'].tolist()
            all_texts = [input_text] + corpus

            vectorizer = TfidfVectorizer(stop_words='english', min_df=1)
            tfidf_matrix = vectorizer.fit_transform(all_texts)

            # Compare input (index 0) against all corpus entries
            scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])[0]

            results = []
            for idx, score in enumerate(scores):
                if score > threshold:
                    row = df.iloc[idx]
                    results.append({
                        'id': int(row['id']) if 'id' in row else None,
                        'title': row['title'],
                        'description': row['description'],
                        'score': float(score),
                        'match_percentage': round(float(score) * 100, 2)
                    })

            results = sorted(results, key=lambda x: x['score'], reverse=True)[:top_k]

            return {
                'success': True,
                'similar_campaigns': results,
                'count': len(results)
            }

        except Exception as e:
            logger.error(f"Error in similarity search: {e}")
            return {
                'success': False,
                'error': f"Similarity search error: {str(e)}"
            }
