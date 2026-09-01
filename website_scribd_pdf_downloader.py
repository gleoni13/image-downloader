import os
import time
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# 1. Browser configuration.
options = webdriver.ChromeOptions()
# Set a fixed resolution, usually wide and very tall. That forces Scribd to load images in high quality and reduces awkward scaling issues.
options.add_argument("--window-size=1400,2000") 

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Target URL (Replace with your target Scribd document URL)
url = "https://example.com/document"
driver.get(url)

print("Browser started.")
# Make sure to manually close the initial cookie banner and log in if required to access the full document.
input("Dismiss any cookie banners or complete login if required. Press ENTER in the terminal once the document is ready to be scrolled...")

# 2. Radical UI cleanup via JavaScript
print("Cleaning up UI elements...")
driver.execute_script("""
    // 1. Find and hide all 'fixed' or 'sticky' screen elements (headers, social buttons, chat, banners)
    document.querySelectorAll('*').forEach(el => {
        let style = window.getComputedStyle(el);
        if (style.position === 'fixed' || style.position === 'sticky') {
            el.style.display = 'none';
        }
    });
    
    // 2. Hide specific Scribd selectors that act as overlays or distractions
    let intrusiveSelectors = '.header_wrapper, .doc_info, .page_tools, .document_actions, .between_page_module, .related_docs, .doc_bottom_metadata';
    document.querySelectorAll(intrusiveSelectors).forEach(el => el.style.display = 'none');
""")

# 3. Page identification
pages = driver.find_elements(By.CSS_SELECTOR, "div[data-page-number]")
if not pages:
    pages = driver.find_elements(By.CLASS_NAME, "outer_page")

print(f"Found {len(pages)} pages to process.")
page_images = []

# 4. Capture loop
for index, page in enumerate(pages):
    page_number = index + 1
    
    # Scroll page into exact center alignment
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", page)
    time.sleep(3.5)  # Generous pause to allow text to load (Lazy Loading)
    
    image_name = f"temp_page_{page_number}.png"
    # Capture screenshot exclusively from the target page container
    page.screenshot(image_name)
    page_images.append(image_name)
    
    print(f"Captured page {page_number}/{len(pages)}")

# 5. PDF generation with standardized dimensions
if page_images:
    print("Generating PDF (Standardizing image dimensions)...")
    
    converted_pages = []
    
    # Open the first image and use it as the benchmark size for width and height
    first_image = Image.open(page_images[0]).convert('RGB')
    base_width, base_height = first_image.size
    converted_pages.append(first_image)
    
    # Process all remaining images
    for img_path in page_images[1:]:
        img = Image.open(img_path).convert('RGB')
        
        # If dimensions differ even by a single pixel, resize to match the base page
        if img.size != (base_width, base_height):
            img = img.resize((base_width, base_height), Image.Resampling.LANCZOS)
            
        converted_pages.append(img)
        
    pdf_filename = "example.pdf"
    
    # Merge and save to PDF
    converted_pages[0].save(
        pdf_filename, 
        save_all=True, 
        append_images=converted_pages[1:]
    )
    print(f"Success! File saved as: {pdf_filename}")
    
    # Clean up temporary screenshot files
    for img in page_images:
        if os.path.exists(img):
            os.remove(img)
    print("Temporary screenshot files cleaned up.")
else:
    print("Error: Could not capture any pages.")

driver.quit()
