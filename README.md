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

```

## 💡 Usage Guide

### 1. Batch Image Downloader (`image_downloader.py`)
1. Open `image_downloader.py` and add your target image links to the `url_immagini` list:
   ```python
   url_immagini = [
       "[https://example.com/image1.jpg](https://example.com/image1.jpg)",
       "[https://example.com/image2.jpg](https://example.com/image2.jpg)"
   ]

   ```

 ### 2. Scribd to PDF Converter (`scribd_to_pdf.py`)
1. Open `scribd_to_pdf.py` and set the url variable to your target Scribd document:
   ```python
   url = "[https://example.com/document](https://example.com/document)"

   ```
2. Run the script:
   ```python
   python scribd_to_pdf.py

   ```
3. An automated Chrome window will open with a standardized high resolution (`1400x2000`).
4. Dismiss any cookie banners manually or log into your Scribd account if required.
5. Return to your terminal and press **ENTER** to initiate the extraction process.
6. The script will automatically:
   * Inject JavaScript to hide UI headers, sticky elements, and ads.
   * Scroll page-by-page with dynamic pauses to allow text lazy-loading.
   * Capture clean screenshots of each page element.
   * Standardize all image dimensions using Lanczos resampling.
   * Merge images into a single output PDF (`Brancalonia_X1_Pugno_Luppoli.pdf`) and clean up temporary `.png` files.
