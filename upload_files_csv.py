#!/usr/bin/env python3
"""
Spotify Pipeline Automation Script
"""

import boto3
import time
import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Configuration
REGION = 'us-east-1'
RAW_BUCKET = 'spotify-pipeline-aya-v2-raw'


# Clients AWS
s3_client = boto3.client('s3', region_name=REGION)


print("="*60)
print("SPOTIFY PIPELINE UPLOAD - START")
print("="*60)


print("\n ÉTAPE 1: Uploading CSV files to S3...")

def upload_csv_files(csv_directory='./data'):
    """Upload tous les fichiers CSV dans le bucket raw"""
    csv_files = glob.glob(os.path.join(csv_directory, '*.csv'))
    
    if not csv_files:
        print(f"  Aucun fichier CSV trouvé dans {csv_directory}")
        print("   Place tes fichiers CSV dans le dossier './data/'")
        return False
    
    for csv_file in csv_files:
        filename = os.path.basename(csv_file)
        s3_key = f'daily/{filename}'
        
        try:
            s3_client.upload_file(
                csv_file,
                RAW_BUCKET,
                s3_key
            )
            print(f"    Uploaded: {filename}")
        except Exception as e:
            print(f"    Error uploading {filename}: {e}")
            return False
    
    print(f"\n {len(csv_files)} fichiers CSV uploadés avec succès!")
    return True
