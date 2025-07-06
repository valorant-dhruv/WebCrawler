import json
import re
from typing import List, Dict, Any

def preprocess_job_data(file_path: str, field_priority: List[str]) -> List[str]:
    """
    Preprocesses job data from JSON file for vector embedding.
    
    Args:
        file_path (str): Path to the JSON file containing job data
        field_priority (List[str], optional): Order of fields by importance for embedding.
                                            Options: 'job_description', 'technology_stack', 'company_location'
                                            Default: ['job_description', 'technology_stack', 'company_location']
                                            
    Returns:
        List[str]: List of preprocessed text documents, one per job listing
    """
    
    # Default priority order (semantic importance)
    if field_priority is None:
        field_priority = ['job_description', 'technology_stack', 'company_location']
    
    # Validate field_priority
    valid_fields = {'job_description', 'technology_stack', 'company_location'}
    if not all(field in valid_fields for field in field_priority):
        raise ValueError(f"Invalid field in priority list. Valid fields: {valid_fields}")
    
    print(f"Using field priority order: {field_priority}")
    print("(Earlier fields get higher weight in embedding)")
    
    
    def clean_text(text: str) -> str:
        if not text or text.strip() == "":
            return ""
        
        # Remove URLs (they add noise to embeddings)
        text = re.sub(r'https?://[^\s]+', '', text)
        
        # Remove email addresses (also noise for job matching)
        text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '', text)
        
        # Remove excessive whitespace and newlines
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep alphanumeric and basic punctuation
        text = re.sub(r'[^\w\s\-\.,/()]', '', text)
        
        # Strip leading/trailing whitespace
        text = text.strip()
        
        return text
    
    def create_document(job: Dict[str, Any]) -> str:
        """
        Create a single text document from job fields using configurable ordering.
        """
        # Map field names to job dictionary keys
        field_mapping = {
            'job_description': 'job_description',
            'technology_stack': 'technology_stack', 
            'company_location': 'company_name_and_location'
        }
        
        # Extract and clean fields based on priority order
        cleaned_parts = []
        for field in field_priority:
            raw_text = job.get(field_mapping[field], '') or ''
            cleaned_text = clean_text(raw_text)
            if cleaned_text:  # Only add non-empty fields
                cleaned_parts.append(cleaned_text)
        
        # Join all parts with spaces
        document = ' '.join(cleaned_parts)
        return document
    
    # Load JSON data
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            jobs_data = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Could not find file: {file_path}")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON format in file: {file_path}")
    
    # Filter out jobs with errors
    valid_jobs = [job for job in jobs_data if not job.get('error', False)]
    
    # Process each job into a document
    documents = []
    for i, job in enumerate(valid_jobs):
        document = create_document(job)
        
        # Skip empty documents
        if document:
            documents.append(document)
        else:
            print(f"Warning: Job {i} resulted in empty document, skipping")
    
    print(f"Preprocessed {len(documents)} job listings from {len(jobs_data)} total entries")
    return documents

# Example usage with different priorities
if __name__ == "__main__":
    # Default priority (job content first)
    print("=== DEFAULT PRIORITY ===")
    docs_default = preprocess_job_data('../jobs.json', ['job_description','technology_stack','company_location'])
    print(f"Sample: {docs_default[0]}...")
    
    # Location-first priority (for location-sensitive searches)
    print("\n=== LOCATION-FIRST PRIORITY ===")
    docs_location_first = preprocess_job_data('../jobs.json', 
                                            ['company_location', 'job_description', 'technology_stack'])
    print(f"Sample: {docs_location_first[0]}...")
    
    # Tech-first priority (for skill-based matching)
    print("\n=== TECH-FIRST PRIORITY ===")
    docs_tech_first = preprocess_job_data('../jobs.json',
                                        ['technology_stack', 'job_description', 'company_location'])
    print(f"Sample: {docs_tech_first[0]}...")
    
    # Compare how the same job looks with different priorities
    print(f"\nProcessed {len(docs_default)} documents with each priority configuration")