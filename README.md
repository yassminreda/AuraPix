# AuraPix

**AuraPix** is an AI-powered image search and image captioning application built with Python and Streamlit.

## Features

- **Image Search:** Find images using text descriptions.
- **Image Captioning:** Generate descriptions for uploaded images.
- **Arabic and English:** Switch between two interface languages.
- **Light and Dark Modes:** Choose your preferred appearance.
- **Simple Interface:** Easy-to-use design for a smooth experience.

## Technologies

- Python
- Streamlit
- PyTorch
- Hugging Face Transformers
- CLIP for image search
- BLIP for image captioning

## Run Locally

1. Install Python 3.11 or 3.12 (64-bit).
2. Open the project folder in Visual Studio Code.
3. Open the terminal and create a virtual environment:

   ```bash
   python -m venv .venv
   ```

4. Install the required packages:

   **Windows:**
   ```powershell
   .venv\Scripts\python.exe -m pip install -r requirements.txt
   ```

5. Start the application:

   ```powershell
   .venv\Scripts\python.exe -m streamlit run app.py
   ```

## Project Structure

- `app.py` — Main application and interface.
- `models.py` — Loads and runs the AI models.
- `logic.py` — Image search and processing logic.
- `styles.py` — Application styling and themes.
- `i18n.py` — Arabic and English translations.
- `assets/` — Images used in the interface.
- `tests/` — Project tests.

## AI Models

AuraPix uses CLIP for text-based image search and BLIP for image captioning.

The application can be configured to load trained models from private Hugging Face repositories. Keep access tokens and other secrets in Streamlit Secrets or environment variables. **Never upload tokens or private model weights to a public repository.**

Model downloads and inference may require an internet connection and sufficient memory, depending on the configuration.

## Notes

- Image search scores represent cosine similarity, not probabilities.
- The Flickr30K dataset is not included in this repository.
- Performance depends on the models and hardware being used.
