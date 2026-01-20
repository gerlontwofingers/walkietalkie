import nltk
import ssl
import os
import subprocess
import sys

def attempt_nltk_download():
    """
    Attempts to download the required NLTK data using multiple strategies.
    """
    packages = ['punkt', 'stopwords', 'wordnet', 'omw-1.4', 'averaged_perceptron_tagger']
    
    print("Attempting to download NLTK data...")
    
    # Strategy 1: Try direct download first
    print("\n1. Trying standard download...")
    try:
        for package in packages:
            nltk.download(package)
        print("✓ Download successful using standard method.")
        return
    except Exception as e:
        print(f"✗ Standard download failed: {e}")
    
    # Strategy 2: Try with unverified SSL context
    print("\n2. Trying with unverified SSL context...")
    try:
        # Create an unverified SSL context
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        # Apply the unverified context
        ssl._create_default_https_context = ssl._create_unverified_context
        
        for package in packages:
            nltk.download(package)
        print("✓ Download successful using unverified SSL context.")
        return
    except Exception as e:
        print(f"✗ Unverified context download failed: {e}")
    
    # Strategy 3: Provide instructions for system-level fixes
    print("\n3. Please try a system-level fix:")
    if sys.platform == "darwin":  # macOS
        print("   → On macOS, run this command in your terminal:")
        python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
        print(f'   bash "/Applications/Python {python_version}/Install Certificates.command"')
    else:
        print("   → Install the 'certifi' package and set an environment variable:")
        print("     pip install certifi")
        print("     Then, find the path to 'cacert.pem' by running in Python:")
        print("     import certifi; print(certifi.where())")
        print("     Set this environment variable in your shell:")
        print("     export SSL_CERT_FILE=/path/to/cacert.pem")

if __name__ == "__main__":
    attempt_nltk_download()
