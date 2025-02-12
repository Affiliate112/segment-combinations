import streamlit as st
import pandas as pd
from typing import List
import base64
from io import StringIO
import csv

# Constants
EMAIL_DOMAINS = ['freemail', 'company', 'education']
SEGMENTS = ['micro', 'smb', 'mid-market', 'enterprise']

def handle_multiselect_change(key: str):
    """Handle the change in multiselect values."""
    current_value = st.session_state[f"{key}_select"]
    previous_value = st.session_state[f"{key}_previous"]
    
    # If "All" was just selected
    if "All" in current_value and "All" not in previous_value:
        st.session_state[f"{key}_select"] = ["All"]
    # If switching from "All" to specific selections
    elif "All" not in current_value and "All" in previous_value:
        # Keep only the new specific selections
        st.session_state[f"{key}_select"] = [x for x in current_value if x != "All"]
    # If trying to add "All" to specific selections
    elif "All" in current_value and len(current_value) > 1:
        # Keep only "All"
        st.session_state[f"{key}_select"] = ["All"]
        
    # Update previous value
    st.session_state[f"{key}_previous"] = st.session_state[f"{key}_select"]

def initialize_session_state():
    """Initialize session state variables if they don't exist."""
    if 'domains_select' not in st.session_state:
        st.session_state.domains_select = ["All"]
    if 'domains_previous' not in st.session_state:
        st.session_state.domains_previous = ["All"]
    if 'segments_select' not in st.session_state:
        st.session_state.segments_select = ["All"]
    if 'segments_previous' not in st.session_state:
        st.session_state.segments_previous = ["All"]

def get_actual_values(selected: List[str], all_options: List[str]) -> List[str]:
    """Convert selection to actual values, handling 'All' case."""
    if not selected:  # If nothing is selected, return all options
        return all_options
    return all_options if "All" in selected else selected

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
    
    # Initialize session state
    initialize_session_state()
    
    # Create columns for dropdowns
    col1, col2 = st.columns(2)
    
    with col1:
        domains = st.multiselect(
            "Select Email Domains:",
            ["All"] + EMAIL_DOMAINS,
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
            countries = [
                country.strip() 
                for country in countries_input.replace('\n', ',').split(',')
                if country.strip()
            ]
            
            if countries:
                # Generate combinations
                combined_keys = generate_combinations(countries, selected_domains, selected_segments)
                
                # Format keys with commas
                formatted_keys = format_keys_with_commas(combined_keys)
                
                # Display formatted keys
                st.subheader("Generated Combinations:")
                st.code(formatted_keys)
                
                # Statistics
                st.subheader("📈 Statistics")
                stats_col1, stats_col2, stats_col3 = st.columns(3)
                with stats_col1:
                    st.metric("Total Combinations", len(combined_keys))
                with stats_col2:
                    st.metric("Domains Selected", len(selected_domains))
                with stats_col3:
                    st.metric("Segments Selected", len(selected_segments))
                
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
