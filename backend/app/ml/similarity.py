try:
    import pandas as pd
    from sentence_transformers import SentenceTransformer, util
    SIMILARITY_AVAILABLE = True
except ImportError:
    SIMILARITY_AVAILABLE = False
    print("⚠️ Similarity libraries not available")
    
import logging

logger = logging.getLogger(__name__)


class SimilarityEngine:
    """Semantic similarity engine for finding duplicate campaigns"""
    
    _model = None
    MODEL_NAME = 'all-MiniLM-L6-v2'
    
    @classmethod
    def _load_model(cls):
        """Lazy load sentence transformer model"""
        if cls._model is None:
            try:
                cls._model = SentenceTransformer(cls.MODEL_NAME)
                logger.info(f"✓ Sentence Transformer model '{cls.MODEL_NAME}' loaded")
            except Exception as e:
                logger.error(f"Error loading model: {e}")
                cls._model = None
        return cls._model
    
    @classmethod
    def find_similar(cls, title, description, campaigns_data, top_k=3, threshold=0.3):
        """Find similar campaigns using semantic similarity"""
        if not SIMILARITY_AVAILABLE:
            return {
                'success': False,
                'error': 'Similarity libraries not installed'
            }
            
        try:
            model = cls._load_model()
            
            if model is None:
                return {
                    'success': False,
                    'error': 'Similarity model not loaded'
                }
            
            if not campaigns_data or len(campaigns_data) == 0:
                return {
                    'success': True,
                    'similar_campaigns': []
                }
            
            # Prepare data
            df = pd.DataFrame(campaigns_data)
            df['text'] = df['title'].astype(str) + " " + df['description'].astype(str)
            input_text = title + " " + description
            
            # Encode
            corpus_embeddings = model.encode(df['text'].tolist(), convert_to_tensor=True)
            input_embedding = model.encode(input_text, convert_to_tensor=True)
            
            # Compute similarity
            cos_scores = util.pytorch_cos_sim(input_embedding, corpus_embeddings)[0]
            scores = cos_scores.cpu().tolist()
            
            # Build results
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
            
            # Sort by score and limit
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
