import streamlit as st
import pandas as pd
from typing import List, Tuple
import base64
from io import StringIO
import csv
from difflib import get_close_matches

# Constants
EMAIL_DOMAINS = ['freemail', 'company', 'education']
SEGMENTS = ['micro', 'smb', 'mid-market', 'enterprise']
COUNTRIES = [
    'Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola', 'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan',
    'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bhutan', 'Bolivia',
    'Bosnia and Herzegovina', 'Botswana', 'Brazil', 'Brunei', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cambodia',
    'Cameroon', 'Canada', 'Chad', 'Chile', 'China', 'Colombia', 'Comoros', 'Congo', 'Costa Rica', 'Croatia', 'Cuba',
    'Cyprus', 'Czech Republic', 'Denmark', 'Djibouti', 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador',
    'Equatorial Guinea', 'Eritrea', 'Estonia', 'Ethiopia', 'Fiji', 'Finland', 'France', 'Gabon', 'Gambia', 'Georgia',
    'Germany', 'Ghana', 'Greece', 'Grenada', 'Guatemala', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Honduras',
    'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Israel', 'Italy', 'Jamaica', 'Japan',
    'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', 'Korea, North', 'Korea, South', 'Kuwait', 'Kyrgyzstan', 'Laos',
    'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Madagascar',
    'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Mauritania', 'Mauritius', 'Mexico',
    'Micronesia', 'Moldova', 'Monaco', 'Mongolia', 'Montenegro', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia',
    'Nauru', 'Nepal', 'Netherlands', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Norway', 'Oman', 'Pakistan',
    'Palau', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Qatar',
    'Romania', 'Russia', 'Rwanda', 'Saint Lucia', 'Samoa', 'San Marino', 'Saudi Arabia', 'Senegal', 'Serbia',
    'Seychelles', 'Sierra Leone', 'Singapore', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa',
    'Spain', 'Sri Lanka', 'Sudan', 'Sweden', 'Switzerland', 'Syria', 'Taiwan', 'Tajikistan', 'Tanzania', 'Thailand',
    'Togo', 'Tonga', 'Tunisia', 'Turkey', 'Turkmenistan', 'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates',
    'United Kingdom', 'United States', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Vatican City', 'Venezuela', 'Vietnam',
    'Yemen', 'Zambia', 'Zimbabwe'
]

def handle_multiselect_change(key: str):
    """Handle the change in multiselect values."""
    current_value = st.session_state[f"{key}_select"]
    
    # If "All" is present along with other selections
    if "All" in current_value and len(current_value) > 1:
        # Keep only the most recently added item
        st.session_state[f"{key}_select"] = [item for item in current_value if item != "All"][-1:]

def get_actual_values(selected: List[str], all_options: List[str]) -> List[str]:
    """Convert selection to actual values, handling 'All' case."""
    if not selected:  # If nothing is selected, return all options
        return all_options
    return all_options if "All" in selected else selected

def validate_and_correct_countries(input_countries: List[str]) -> Tuple[List[str], dict]:
    """
    Validate country names and suggest corrections for misspelled ones.
    Returns tuple of (valid_countries, corrections_dict).
    """
    valid_countries = []
    corrections = {}
    
    for country in input_countries:
        country = country.strip().title()
        if country in COUNTRIES:
            valid_countries.append(country)
        else:
            # Find closest matches
            matches = get_close_matches(country, COUNTRIES, n=1, cutoff=0.6)
            if matches:
                corrections[country] = matches[0]
                valid_countries.append(matches[0])
            else:
                corrections[country] = None
    
    return valid_countries, corrections

def generate_combinations(countries: List[str], selected_domains: List[str], selected_segments: List[str]) -> List[str]:
    """Generate combinations based on selected domains, segments, and countries."""
    combined_keys = []
    for country in countries:
        for domain in selected_domains:
            for segment in selected_segments:
                combined_key = f"{domain}-{segment}-{country.lower()}"
                combined_keys.append(combined_key)
    
    return combined_keys

def format_keys_with_commas(keys: List[str]) -> str:
    """Format the combined keys with commas."""
    return ',\n'.join(keys)

def main():
    st.set_page_config(page_title="Segment Combinations Generator", page_icon="🔄")
    
    st.title("🔄 Segment Combinations Generator")
    
    # Create columns for dropdowns
    col1, col2 = st.columns(2)
    
    with col1:
        domains = st.multiselect(
            "Select Email Domains:",
            ["All"] + EMAIL_DOMAINS,
            default=["All"],
            key="domains_select",
            on_change=handle_multiselect_change,
            args=("domains",),
            help="Choose 'All' or select specific domains"
        )
        selected_domains = get_actual_values(domains, EMAIL_DOMAINS)
    
    with col2:
        segments = st.multiselect(
            "Select Segments:",
            ["All"] + SEGMENTS,
            default=["All"],
            key="segments_select",
            on_change=handle_multiselect_change,
            args=("segments",),
            help="Choose 'All' or select specific segments"
        )
        selected_segments = get_actual_values(segments, SEGMENTS)
    
    # Input text area for countries
    countries_input = st.text_area(
        "Enter countries (one per line or separated by commas):",
        height=100,
        help="Example: Belgium, France, Germany\nor\nBelgium\nFrance\nGermany"
    )
    
    if st.button("Generate Combinations"):
        if countries_input and selected_domains and selected_segments:
            # Handle both comma-separated and newline-separated inputs
            input_countries = [
                country.strip() 
                for country in countries_input.replace('\n', ',').split(',')
                if country.strip()
            ]
            
            if input_countries:
                # Validate and correct country names
                valid_countries, corrections = validate_and_correct_countries(input_countries)
                
                # Show corrections if any were made
                if corrections:
                    st.info("📝 Some country names were corrected:")
                    for original, corrected in corrections.items():
                        if corrected:
                            st.write(f"- '{original}' was corrected to '{corrected}'")
                        else:
                            st.error(f"- '{original}' is not a recognized country name")
                
                if valid_countries:
                    # Generate combinations
                    combined_keys = generate_combinations(valid_countries, selected_domains, selected_segments)
                    
                    # Format keys with commas
                    formatted_keys = format_keys_with_commas(combined_keys)
                    
                    # Display formatted keys
                    st.subheader("Generated Combinations:")
                    st.code(formatted_keys)
                    
                    # Statistics
                    st.subheader("📈 Statistics")
                    stats_col1, stats_col2, stats_col3, stats_col4 = st.columns(4)
                    with stats_col1:
                        st.metric("Total Combinations", len(combined_keys))
                    with stats_col2:
                        st.metric("Countries", len(valid_countries))
                    with stats_col3:
                        st.metric("Domains", len(selected_domains))
                    with stats_col4:
                        st.metric("Segments", len(selected_segments))
                    
                    # Download button
                    st.download_button(
                        label="⬇️ Download Text File",
                        data=formatted_keys,
                        file_name="segment_combinations.txt",
                        mime="text/plain"
                    )
                else:
                    st.error("No valid countries found after correction")
            else:
                st.error("Please enter at least one country")
        else:
            st.error("Please ensure you've selected domains, segments, and entered countries")
    
    # Add helpful information at the bottom
    st.markdown("---")
    st.markdown("""
    ### 📝 Notes:
    - Select "All" to include all options, or choose specific items
    - You can select any combination of specific options
    - "All" and specific selections are mutually exclusive
    - All combinations will be in lowercase
    - Each key will be separated by commas
    """)

if __name__ == "__main__":
    main()
