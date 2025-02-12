import streamlit as st
import pandas as pd
from typing import List
import base64
from io import StringIO
import csv

def generate_combinations(countries: List[str]) -> List[str]:
    """Generate all possible combinations of email domains, segments, and countries."""
    EMAIL_DOMAINS = ['freemail', 'company', 'education']
    SEGMENTS = ['micro', 'smb', 'mid-market', 'enterprise']
    
    combined_keys = []
    for country in countries:
        for domain in EMAIL_DOMAINS:
            for segment in SEGMENTS:
                combined_key = f"{domain}-{segment}-{country.lower()}"
                combined_keys.append(combined_key)
    
    return combined_keys

def format_keys_with_commas(keys: List[str]) -> str:
    """Format the combined keys with commas."""
    return ',\n'.join(keys)

def main():
    st.set_page_config(page_title="Segment Combinations Generator", page_icon="🔄")
    
    st.title("🔄 Segment Combinations Generator")
    
    st.write("""
    Generate combinations of email domains, segments, and countries.
    Enter your countries below, separated by commas.
    """)
    
    # Input text area for countries
    countries_input = st.text_area(
        "Enter countries (one per line or separated by commas):",
        height=100,
        help="Example: Belgium, France, Germany\nor\nBelgium\nFrance\nGermany"
    )
    
    if st.button("Generate Combinations"):
        if countries_input:
            # Handle both comma-separated and newline-separated inputs
            countries = [
                country.strip() 
                for country in countries_input.replace('\n', ',').split(',')
                if country.strip()
            ]
            
            if countries:
                # Generate combinations
                combined_keys = generate_combinations(countries)
                
                # Format keys with commas
                formatted_keys = format_keys_with_commas(combined_keys)
                
                # Display formatted keys
                st.subheader("Generated Combinations:")
                st.code(formatted_keys)
                
                # Statistics
                st.subheader("📈 Statistics")
                st.metric("Total Combinations", len(combined_keys))
                
                # Download button
                st.download_button(
                    label="⬇️ Download Text File",
                    data=formatted_keys,
                    file_name="segment_combinations.txt",
                    mime="text/plain"
                )
            else:
                st.error("Please enter at least one country")
        else:
            st.error("Please enter some countries")
    
    # Add helpful information at the bottom
    st.markdown("---")
    st.markdown("""
    ### 📝 Notes:
    - Each country will generate combinations with:
        - Email Domains: freemail, company, education
        - Segments: micro, smb, mid-market, enterprise
    - All combinations will be in lowercase
    - Each key will be separated by commas
    """)

if __name__ == "__main__":
    main()
