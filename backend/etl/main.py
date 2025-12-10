"""ETL orchestration script."""
import argparse
import sys
from typing import List
import os
import sys

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from backend.config import Config
from backend.etl.extract import DataExtractor
from backend.etl.transform import SentimentTransformer
from backend.etl.load import DataLoader


def run_etl(keywords: List[str] = None, verbose: bool = True):
    """Run the complete ETL pipeline.
    
    Args:
        keywords: List of keywords to process. Defaults to Config.KEYWORDS.
        verbose: Print progress messages.
    """
    if verbose:
        print("=" * 50)
        print("Tech Trend Sentiment Analyst - ETL Pipeline")
        print("=" * 50)
    
    # Validate configuration
    if not Config.validate():
        missing = Config.get_missing_config()
        print(f"ERROR: Missing required configuration: {', '.join(missing)}")
        print("Please check your .env file.")
        sys.exit(1)
    
    keywords = keywords or Config.KEYWORDS
    
    if verbose:
        print(f"\nProcessing keywords: {', '.join(keywords)}")
        print("\n[1/3] Extracting data...")
    
    # Extract phase
    extractor = DataExtractor()
    extracted_data = extractor.extract_all(keywords)
    
    if verbose:
        print(f"Extracted {len(extracted_data)} records")
        print("\n[2/3] Transforming data with AI...")
    
    # Transform phase
    transformer = SentimentTransformer()
    transformed_data = transformer.transform_batch(extracted_data)
    
    if verbose:
        print(f"Transformed {len(transformed_data)} records")
        print("\n[3/3] Loading data into database...")
    
    # Load phase
    loader = DataLoader()
    stats = loader.load_batch(transformed_data)
    
    if verbose:
        print("\n" + "=" * 50)
        print("ETL Pipeline Complete!")
        print("=" * 50)
        print(f"Loaded: {stats['loaded']} new records")
        print(f"Duplicates: {stats['duplicates']} records")
        print(f"Errors: {stats['errors']} records")
        print("=" * 50)
    
    return stats


def main():
    """Main entry point for ETL script."""
    parser = argparse.ArgumentParser(description="Run ETL pipeline for sentiment analysis")
    parser.add_argument(
        "--keywords",
        type=str,
        help="Comma-separated list of keywords to process"
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress output messages"
    )
    
    args = parser.parse_args()
    
    keywords = None
    if args.keywords:
        keywords = [k.strip() for k in args.keywords.split(",")]
    
    run_etl(keywords=keywords, verbose=not args.quiet)


if __name__ == "__main__":
    main()

