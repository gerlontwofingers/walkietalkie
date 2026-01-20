
# Test script to verify NLTK installation
import nltk

def test_nltk():
    print("Testing NLTK installation...")
    
    # Test tokenization
    try:
        from nltk.tokenize import word_tokenize, sent_tokenize
        text = "This is a test sentence. This is another one!"
        sentences = sent_tokenize(text)
        words = word_tokenize(text)
        print("✓ Tokenization working:")
        print(f"  Sentences: {sentences}")
        print(f"  Words: {words}")
    except Exception as e:
        print(f"✗ Tokenization failed: {e}")
        return False
    
    # Test stopwords
    try:
        from nltk.corpus import stopwords
        stops = set(stopwords.words('english'))
        print(f"✓ Stopwords loaded: {len(stops)} words")
    except Exception as e:
        print(f"✗ Stopwords failed: {e}")
        return False
    
    # Test POS tagging
    try:
        from nltk import pos_tag
        tagged = pos_tag(words)
        print(f"✓ POS tagging working: {tagged}")
    except Exception as e:
        print(f"✗ POS tagging failed: {e}")
        return False
    
    print("🎉 All NLTK tests passed!")
    return True

if __name__ == "__main__":
    test_nltk()
