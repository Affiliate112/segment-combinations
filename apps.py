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
    
    combinations = []
    for country in countries:
        for domain in EMAIL_DOMAINS:
            for segment in SEGMENTS:
                combination = f"{domain}-{segment}-{country.lower()}"
                combinations.append([domain, segment, country.lower(), combination])
    
    return combinations

def get_csv_download_link(df):
    """Generate a link to download the dataframe as CSV."""
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'data:file/csv;base64,{b64}'
    return href

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
                combinations = generate_combinations(countries)
                df = pd.DataFrame(
                    combinations,
                    columns=['Email_Domain', 'Segment', 'Country', 'Combined_Key']
                )
                
                # Display preview
                st.subheader("📊 Preview")
                st.dataframe(df.head())
                
                # Statistics
                st.subheader("📈 Statistics")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Total Combinations", len(combinations))
                with col2:
                    st.metric("Countries Processed", len(countries))
                
                # Download button
                csv = df.to_csv(index=False)
                st.download_button(
                    label="⬇️ Download CSV",
                    data=csv,
                    file_name="segment_combinations.csv",
                    mime="text/csv"
                )
                
                # Display example usage
                st.subheader("🔍 Sample Combinations")
                st.code('\n'.join([combo[3] for combo in combinations[:5]]))
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
    - The CSV file contains both individual components and combined keys
    """)

if __name__ == "__main__":
    main()