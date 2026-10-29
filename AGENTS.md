# Architecture
- Keep this deliverable a standalone Streamlit Python app; it runs locally independently of the Lovable preview.
- Keep presentation in styles.py and bilingual copy in i18n.py so users can change appearance without touching inference.
- Load model libraries only on inference requests so the interface remains usable before model installation/download.
- Show CLIP cosine similarity rather than a probability, because retrieval similarity is not calibrated confidence.
