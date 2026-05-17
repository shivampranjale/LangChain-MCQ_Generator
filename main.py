"""
Main entry point for the MCQ Generator application.
"""

from config import get_api_key, get_pdf_path, DEFAULT_TOPIC_DOMAIN
from models import initialize_model
from pdf_processor import read_pdf
from chains import create_summary_chain, create_mcq_chain
from utils import print_header, print_section, save_output
from dotenv import load_dotenv
import os

load_dotenv('/media/shivam/New Volume/Analytics_Vidhya/MCQ_Generator/secrets/.env')
api_key=os.getenv('GOOGLE_API_KEY')

def main():
    """Main function to run the MCQ Generator."""
    print_header("Welcome to MCQ Generator")

    # Step 1: Get API Key
    # print_section("Step 1: API Configuration")
    # api_key = get_api_key()

    # Step 2: Initialize Model
    print_section("Step 2: Initializing Model")
    model = initialize_model(api_key)
    print("✓ Model initialized successfully")

    # Step 3: Get PDF Path and Read Content
    print_section("Step 3: Loading Study Material")
    pdf_path = get_pdf_path()
    study_material = read_pdf(pdf_path)
    print(f"✓ PDF loaded successfully ({len(study_material)} characters)")

    # Step 4: Create Chains
    print_section("Step 4: Creating Processing Chains")
    summary_chain = create_summary_chain(model)
    mcq_chain = create_mcq_chain(model)
    print("✓ Chains created successfully")

    # Step 5: Summarize Content
    print_section("Step 5: Summarizing Content")
    print("Processing study material...")
    content_summary = summary_chain.invoke({'study_material': study_material})
    print("✓ Content summarized successfully")
    print("\nSummary Preview:")
    print("-" * 70)
    print(content_summary[:500] + "..." if len(content_summary) > 500 else content_summary)

    # Step 6: Generate MCQ
    print_section("Step 6: MCQ Generation")
    topic = input(f"Enter a topic from {DEFAULT_TOPIC_DOMAIN} to generate MCQ: ")

    print(f"Generating MCQ for topic: {topic}...")
    mcq_response = mcq_chain.invoke({
        'content_summary': content_summary,
        'topic': topic,
    })

    print("\n" + "=" * 70)
    print("Generated MCQs:")
    print("=" * 70)
    print(mcq_response)

    # Optional: Save outputs
    save_option = input("\nDo you want to save the outputs? (yes/no): ").strip().lower()
    if save_option in ['yes', 'y']:
        from datetime import datetime

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        save_output(content_summary, f"summary_{timestamp}.txt")
        save_output(mcq_response, f"mcq_{topic}_{timestamp}.txt")

    print_header("Thank you for using MCQ Generator!")


if __name__ == "__main__":
    main()
