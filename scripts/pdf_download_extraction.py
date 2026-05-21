import pandas as pd
import requests
import os
import time
import glob
import fitz  # PyMuPDF

def download_pdfs_from_csv(csv_path, doi_column, output_dir, email):
    """
    Reads a CSV of DOIs and downloads the corresponding Open Access PDFs.
    """
    df = pd.read_csv(csv_path)
    
    # Drop any empty rows and get unique DOIs
    dois = df[doi_column].dropna().unique()

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print(f"Found {len(dois)} unique DOIs. Starting download...")

    for doi in dois:
        doi_clean = str(doi).strip()
        # Unpaywall API endpoint
        url = f"https://api.unpaywall.org/v2/{doi_clean}?email={email}"
        
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                oa_location = data.get('best_oa_location', {})
                
                if oa_location and oa_location.get('url_for_pdf'):
                    pdf_url = oa_location['url_for_pdf']
                    
                    # Download the actual PDF file
                    pdf_response = requests.get(pdf_url, stream=True)
                    if pdf_response.status_code == 200:
                        # Replace slashes in DOI to create a valid filename
                        safe_doi = doi_clean.replace('/', '_')
                        file_path = os.path.join(output_dir, f"{safe_doi}.pdf")
                        
                        with open(file_path, 'wb') as f:
                            for chunk in pdf_response.iter_content(chunk_size=8192):
                                f.write(chunk)
                        print(f"Success: Downloaded {doi_clean}")
                    else:
                        print(f"Failed: Could not fetch PDF file for {doi_clean} (HTTP {pdf_response.status_code})")
                else:
                    print(f"Failed: No direct Open Access PDF link found for {doi_clean}")
            else:
                print(f"Failed: Unpaywall API error for {doi_clean} (HTTP {response.status_code})")

            # Polite rate limiting for the API
            time.sleep(1)
            
        except Exception as e:
            print(f"Error processing {doi_clean}: {e}")

def convert_pdfs_to_text(pdf_dir, text_dir):
    """
    Converts a directory of PDF files into machine-readable text files.
    """
    if not os.path.exists(text_dir):
        os.makedirs(text_dir)

    pdf_files = glob.glob(os.path.join(pdf_dir, '*.pdf'))
    print(f"\nFound {len(pdf_files)} PDFs to convert. Starting extraction...")

    for pdf_path in pdf_files:
        base_name = os.path.basename(pdf_path).replace('.pdf', '.txt')
        txt_path = os.path.join(text_dir, base_name)

        try:
            # Open the PDF using PyMuPDF
            doc = fitz.open(pdf_path)
            text_content = []
            
            # Iterate through pages and extract text
            for page in doc:
                text_content.append(page.get_text())
                
            full_text = "\n".join(text_content)

            # Write the extracted text to a new file
            with open(txt_path, 'w', encoding='utf-8') as f:
                f.write(full_text)

            print(f"Converted: {os.path.basename(pdf_path)}")
            doc.close()
            
        except Exception as e:
            print(f"Error converting {pdf_path}: {e}")

if __name__ == "__main__":
    # Configuration Variables
    CSV_FILENAME = "Scoping Review Sheet - citations_reviewed.csv"
    DOI_COLUMN_NAME = "DOI"
    PDF_OUTPUT_DIRECTORY = "downloaded_pdfs"
    TEXT_OUTPUT_DIRECTORY = "extracted_text"
    USER_EMAIL = "bmb646@nau.edu"  # Update if wanted

    # Step 1: Download the PDFs
    download_pdfs_from_csv(
        csv_path=CSV_FILENAME,
        doi_column=DOI_COLUMN_NAME,
        output_dir=PDF_OUTPUT_DIRECTORY,
        email=USER_EMAIL
    )

    # Step 2: Convert downloaded PDFs to text
    convert_pdfs_to_text(
        pdf_dir=PDF_OUTPUT_DIRECTORY,
        text_dir=TEXT_OUTPUT_DIRECTORY
    )