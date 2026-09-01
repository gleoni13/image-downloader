# Python Web Utilities

A collection of Python scripts designed for automating bulk media downloads and scraping/converting web documents into PDF format.

## 🚀 Features

* **Batch Image Downloader**: Downloads lists of images via HTTP streaming, optimizing RAM usage and handling network errors gracefully.
* **Scribd Document Scraper**: Extracts documents from Scribd by stripping intrusive UI elements via JavaScript injection, capturing high-resolution screenshots, and reassembling them into a standardized, unified PDF.

## 🛠️ Prerequisites & Dependencies

* **Python**: version 3.8 or higher
* **Google Chrome**: required for Selenium execution

Install all required dependencies by running:

```bash
pip install -r requirements.txt

## 💡 Usage Guide

### 1. Batch Image Downloader (`image_downloader.py`)
1. Open `image_downloader.py` and add your target image links to the `url_immagini` list:
   ```python
   url_immagini = [
       "[https://example.com/image1.jpg](https://example.com/image1.jpg)",
       "[https://example.com/image2.jpg](https://example.com/image2.jpg)"
   ]
